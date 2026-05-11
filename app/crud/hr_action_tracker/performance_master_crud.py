from sqlalchemy import false, text
from datetime import datetime
from sqlalchemy.orm import Session

from typing import Optional, List
import os
import urllib.parse

def make_download_url(path: Optional[str]) -> Optional[str]:
    if not path or path in ["null", "None", None]:
        return None
    base_url = os.getenv("BackEndPath", "")
    file_path = path.replace("\\", "/")
    if ":" in file_path:
        file_path = file_path.split(":", 1)[1]
    if file_path.startswith("/Petronet"):
        file_path = file_path.replace("/Petronet", "", 1)
    file_path = "/" + file_path.lstrip("/")
    encoded_path = urllib.parse.quote(file_path)
    return f"{base_url}{encoded_path}"

def insert_employee_performance_document_history(db: Session, document_id: int):
    history_sql = text("""
        INSERT INTO employee_performance_documents_history (
            id, performance_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        )
        SELECT
            id, performance_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        FROM employee_performance_documents
        WHERE id = :document_id
    """)
    db.execute(history_sql, {"document_id": document_id})
def save_employee_performance(db: Session, appraisals: list, login_user_id: int):

    for item in appraisals:

        # 🔹 Check if already exists
        check_query = text("""
            SELECT performance_id FROM employee_performance
            WHERE user_id = :user_id 
            AND appraisal_start_date = :appraisal_start_date
            AND appraisal_end_date = :appraisal_end_date
        """)

        existing = db.execute(check_query, {
            "user_id": item.user_id,
            "appraisal_start_date": item.appraisal_start_date,
            "appraisal_end_date": item.appraisal_end_date
        }).fetchone()

        if existing:
            # 🔁 UPDATE (editable case)
            update_query = text("""
                UPDATE employee_performance
                SET 
                    annual_appraisal_rating = :annual_appraisal_rating,
                    annual_rating_score = :annual_rating_score,
                    created_by = :created_by,
                    created_at = CURRENT_TIMESTAMP,
                    is_deleted = false
                WHERE user_id = :user_id
                AND appraisal_start_date = :appraisal_start_date
                AND appraisal_end_date = :appraisal_end_date
            """)

            db.execute(update_query, {
                "annual_appraisal_rating": item.annual_appraisal_rating,
                "annual_rating_score": item.annual_rating_score,
                "created_by": login_user_id,
                "created_at": datetime.now,
                "user_id": item.user_id,
                "is_deleted":false,
                "appraisal_start_date": item.appraisal_start_date,
                "appraisal_end_date": item.appraisal_end_date
            })

        else:
            # ➕ INSERT
            insert_query = text("""
                INSERT INTO employee_performance
                (user_id, appraisal_start_date, appraisal_end_date, annual_appraisal_rating, annual_rating_score, created_by, created_at, is_deleted)
                VALUES (:user_id, :appraisal_start_date, :appraisal_end_date, :annual_appraisal_rating, :annual_rating_score, :created_by, NOW(), false)
            """)

            db.execute(insert_query, {
                "user_id": item.user_id,
                "appraisal_start_date": item.appraisal_start_date,
                "appraisal_end_date": item.appraisal_end_date,
                "annual_appraisal_rating": item.annual_appraisal_rating,
                "annual_rating_score": item.annual_rating_score,
                "created_by": login_user_id,
                "created_at": datetime.now,
                "is_deleted" : false
            })

    db.commit()

    return {
        "status": True,
        "message": "Appraisal saved successfully"
    }

def get_appraisal_dashboard(db: Session, year: str = None):
    params = {}
    year_filter = ""
    user_joining_filter = ""
    
    # 🔹 Exclude terminated employees
    termination_filter = """
        AND NOT EXISTS (
            SELECT 1 FROM disciplinary_incidents di 
            WHERE di.user_id = u.user_id 
              AND di.enable_termination = TRUE 
              AND (di.is_deleted IS FALSE OR di.is_deleted IS NULL)
        )
    """

    if year:
        start_year, end_year = year.split("-")
        params["start_year"] = int(start_year)
        params["end_year"] = int(end_year)

        year_filter = """
            AND EXTRACT(YEAR FROM ep.appraisal_start_date) = :start_year
            AND EXTRACT(YEAR FROM ep.appraisal_end_date) = :end_year
        """
        user_joining_filter = " AND u.date_of_joining <= MAKE_DATE(:end_year, 3, 31)"

        # 🔹 Unified Query using CTEs for historical accuracy
        base_query = f"""
        WITH latest_promotion AS (
            SELECT DISTINCT ON (user_id)
                user_id, new_grade AS grade, new_designation AS designation, 1 as priority
            FROM promotions
            WHERE effective_date <= MAKE_DATE(:end_year, 3, 31) AND is_deleted = FALSE
            ORDER BY user_id, effective_date DESC
        ),
        earliest_future_promotion AS (
            SELECT DISTINCT ON (user_id)
                user_id, current_grade AS grade, current_designation AS designation, 2 as priority
            FROM promotions
            WHERE effective_date > MAKE_DATE(:end_year, 3, 31) AND is_deleted = FALSE
            ORDER BY user_id, effective_date ASC
        ),
        combined_promotion AS (
            SELECT DISTINCT ON (user_id) *
            FROM (SELECT * FROM latest_promotion UNION ALL SELECT * FROM earliest_future_promotion) as combined
            ORDER BY user_id, priority ASC
        ),
        latest_transfer AS (
            SELECT DISTINCT ON (user_id)
                user_id, new_station AS station_id, 1 as priority
            FROM employee_transfers
            WHERE effective_date <= MAKE_DATE(:end_year, 3, 31) AND is_deleted = FALSE
            ORDER BY user_id, effective_date DESC
        ),
        earliest_future_transfer AS (
            SELECT DISTINCT ON (user_id)
                user_id, current_station AS station_id, 2 as priority
            FROM employee_transfers
            WHERE effective_date > MAKE_DATE(:end_year, 3, 31) AND is_deleted = FALSE
            ORDER BY user_id, effective_date ASC
        ),
        combined_transfer AS (
            SELECT DISTINCT ON (user_id) *
            FROM (SELECT * FROM latest_transfer UNION ALL SELECT * FROM earliest_future_transfer) as combined
            ORDER BY user_id, priority ASC
        ),
        latest_supervisor_history AS (
            SELECT DISTINCT ON (user_id)
                user_id, supervisor_id
            FROM users_history
            WHERE history_created_at <= MAKE_DATE(:end_year, 3, 31)
            ORDER BY user_id, history_created_at DESC
        )
        SELECT
            u.user_id,
            u.employee_code,
            TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
            COALESCE(cp.grade, u.grade) AS grade,
            COALESCE(cp.designation, u.designation) AS designation,
            COALESCE(s_hist.station_name, s_curr.station_name) AS station_name,
            -- Historical Supervisor Fallback
            TRIM(COALESCE(hist_sup.first_name, sup.first_name, '') || ' ' || COALESCE(hist_sup.last_name, sup.last_name, '')) AS supervisor,
            ep.appraisal_start_date,
            ep.appraisal_end_date,
            ep.annual_appraisal_rating,
            ep.annual_rating_score,
            ep.performance_id
        FROM users u
        LEFT JOIN combined_promotion cp ON cp.user_id = u.user_id
        LEFT JOIN combined_transfer ct ON ct.user_id = u.user_id
        LEFT JOIN station s_hist ON ct.station_id = s_hist.station_id
        LEFT JOIN station s_curr ON u.station_id = s_curr.station_id
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN latest_supervisor_history lsh ON lsh.user_id = u.user_id
        LEFT JOIN users hist_sup ON lsh.supervisor_id = hist_sup.user_id
        LEFT JOIN employee_performance ep ON ep.user_id = u.user_id {year_filter} AND ep.is_deleted = FALSE
        WHERE u.is_deleted = FALSE 
          AND u.is_employee = TRUE
          {user_joining_filter} 
          {termination_filter}
        ORDER BY (CASE WHEN ep.annual_appraisal_rating IS NULL THEN 0 ELSE 1 END), u.employee_code ASC
        """
    else:
        # 🔹 Simple query for "All Years" (No year selected)
        base_query = f"""
        SELECT
            u.user_id,
            u.employee_code,
            TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
            u.grade,
            u.designation,
            s.station_name,
            TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')) AS supervisor,
            ep.appraisal_start_date,
            ep.appraisal_end_date,
            ep.annual_appraisal_rating,
            ep.annual_rating_score,
            ep.performance_id
        FROM users u
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        LEFT JOIN employee_performance ep ON ep.user_id = u.user_id AND ep.is_deleted = FALSE
        WHERE u.is_deleted = FALSE
          AND u.is_employee = TRUE
          {termination_filter}
        ORDER BY (CASE WHEN ep.annual_appraisal_rating IS NULL THEN 0 ELSE 1 END), u.employee_code ASC
        """

    result = db.execute(text(base_query), params).mappings().all()
    
    # 🔹 Aggregate data for Dashboard (Summary)
    total_emp = len(result)
    total_done = sum(1 for row in result if row.get("performance_id") is not None)
    
    station_map = {}
    employee_list = []

    for row in result:
        item_dict = dict(row)
        s_name = item_dict.get("station_name") or "Unknown"
        
        # 🔹 Update Station Summary
        if s_name not in station_map:
            station_map[s_name] = {"station_name": s_name, "total_emp": 0, "appraisal_done": 0}
        
        station_map[s_name]["total_emp"] += 1
        if item_dict.get("performance_id"):
            station_map[s_name]["appraisal_done"] += 1
            
        # 🔹 Fetch Attachments for the list
        perf_id = item_dict.get("performance_id")
        if perf_id:
            docs_query = text("""
                SELECT id, file_name, file_path 
                FROM employee_performance_documents 
                WHERE performance_id = :pid AND (is_deleted = FALSE OR is_deleted IS NULL)
            """)
            attachments = db.execute(docs_query, {"pid": perf_id}).mappings().all()
            item_dict["attachments"] = [
                {**dict(a), "file_path": make_download_url(a["file_path"])} 
                for a in attachments
            ]
        else:
            item_dict["attachments"] = []
            
        employee_list.append(item_dict)

    return {
        "summary": {
            "total_emp": total_emp,
            "total_done": total_done,
            "station_data": sorted(list(station_map.values()), key=lambda x: x["station_name"])
        },
        "employee_list": employee_list
    }

def get_performance_by_user(db: Session, user_id: int):

    query = text("""
        SELECT 
            ep.performance_id,
            EXTRACT(YEAR FROM ep.appraisal_start_date) || '-' || 
            EXTRACT(YEAR FROM ep.appraisal_end_date) AS appraisal_year,

            u.designation AS appraisal_year_role,
            u.grade AS appraisal_year_grade,

            ep.annual_appraisal_rating,
            ep.annual_rating_score

        FROM employee_performance ep
        LEFT JOIN users u ON u.user_id = ep.user_id

        WHERE ep.user_id = :user_id
        AND ep.is_deleted = FALSE

        ORDER BY ep.created_at DESC
    """)

    result = db.execute(query, {"user_id": user_id}).mappings().all()

    items = []
    for row in result:
        item_dict = dict(row)
        perf_id = item_dict.get("performance_id")
        
        if perf_id:
            docs_query = text("SELECT * FROM employee_performance_documents WHERE performance_id = :pid AND is_deleted = FALSE")
            attachments = db.execute(docs_query, {"pid": perf_id}).mappings().all()
            
            formatted_attachments = []
            for att in attachments:
                att_dict = dict(att)
                att_dict["file_path"] = make_download_url(att_dict["file_path"])
                formatted_attachments.append(att_dict)
                
            item_dict["attachments"] = formatted_attachments
        else:
            item_dict["attachments"] = []
            
        items.append(item_dict)

    return items

def get_performance_by_id(db: Session, performance_id: int):

    query = text("""
        SELECT 
            ep.performance_id,
            EXTRACT(YEAR FROM ep.appraisal_start_date) || '-' || 
            EXTRACT(YEAR FROM ep.appraisal_end_date) AS appraisal_year,

            u.designation AS appraisal_year_role,
            u.grade AS appraisal_year_grade,

            ep.annual_appraisal_rating,
            ep.annual_rating_score

        FROM employee_performance ep
        LEFT JOIN users u ON u.user_id = ep.user_id

        WHERE ep.performance_id = :performance_id
        AND ep.is_deleted = FALSE
    """)

    result = db.execute(query, {"performance_id": performance_id}).mappings().first()
    
    if not result:
        return None

    item_dict = dict(result)
    perf_id = item_dict.get("performance_id")
        
    if perf_id:
        docs_query = text("SELECT * FROM employee_performance_documents WHERE performance_id = :pid AND (is_deleted = FALSE OR is_deleted IS NULL)")
        attachments = db.execute(docs_query, {"pid": perf_id}).mappings().all()
        
        formatted_attachments = []
        for att in attachments:
            att_dict = dict(att)
            att_dict["file_path"] = make_download_url(att_dict["file_path"])
            formatted_attachments.append(att_dict)
            
        item_dict["attachments"] = formatted_attachments
    else:
        item_dict["attachments"] = []
            
    return item_dict

# def get_performance_list_filter(db: Session, year: str):

#     base_query = """
#         SELECT 
#             u.user_id,
#             u.employee_code,
#             TRIM(
#     COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
# ) AS name,
#             u.grade,
#             u.designation,
#             s.station_name,
#             TRIM(
#                 COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
#                 ) AS supervisor,
#             ep.appraisal_start_date,
#             ep.appraisal_end_date,
#             ep.annual_appraisal_rating,
#             ep.annual_rating_score

#         FROM users u
#         LEFT JOIN users sup ON u.supervisor_id = sup.user_id
#         LEFT JOIN station s ON u.station_id = s.station_id
#         LEFT JOIN employee_performance ep 
#             ON ep.user_id = u.user_id 
#         WHERE u.is_deleted = FALSE
#     """

#     params = {}

#     # 🔹 Apply Year Filter
#     if year:
#         start_year, end_year = year.split("-")

#         base_query += """
#             AND EXTRACT(YEAR FROM ep.appraisal_start_date) = :start_year
#             AND EXTRACT(YEAR FROM ep.appraisal_end_date) = :end_year
#         """

#         params["start_year"] = int(start_year)
#         params["end_year"] = int(end_year)

#     base_query += " ORDER BY u.created_date"

#     result = db.execute(text(base_query), params).mappings().all()

#     return result 

def get_performance_list_filter(db: Session, year: str):
    params = {}
    year_filter = ""
    user_joining_filter = ""
    
    # 🔹 Exclude terminated employees
    termination_filter = """
        AND NOT EXISTS (
            SELECT 1 FROM disciplinary_incidents di 
            WHERE di.user_id = u.user_id 
              AND di.enable_termination = TRUE 
              AND di.is_deleted = FALSE
        )
    """

    if year:
        start_year, end_year = year.split("-")
        params["start_year"] = int(start_year)
        params["end_year"] = int(end_year)

        year_filter = """
            AND EXTRACT(YEAR FROM ep.appraisal_start_date) = :start_year
            AND EXTRACT(YEAR FROM ep.appraisal_end_date) = :end_year
        """
        user_joining_filter = " AND EXTRACT(YEAR FROM u.date_of_joining) <= :end_year"

        # 🔹 Year-specific query using CTEs to get historical data
        # MAKE_DATE(:end_year, 3, 31) = March 31 of the end year (India fiscal year end)
        base_query = f"""
        WITH latest_promotion AS (
            -- 🔹 1. Get the most recent promotion BEFORE the appraisal year ended
            SELECT DISTINCT ON (user_id)
                user_id,
                new_grade AS grade,
                new_designation AS designation,
                1 as priority -- Higher priority for historical match
            FROM promotions
            WHERE effective_date <= MAKE_DATE(:end_year, 3, 31)
              AND is_deleted = FALSE
            ORDER BY user_id, effective_date DESC
        ),
        earliest_future_promotion AS (
            -- 🔹 2. If no promotion before, get the earliest one AFTER (to find the grade they WERE in)
            SELECT DISTINCT ON (user_id)
                user_id,
                current_grade AS grade,
                current_designation AS designation,
                2 as priority
            FROM promotions
            WHERE effective_date > MAKE_DATE(:end_year, 3, 31)
              AND is_deleted = FALSE
            ORDER BY user_id, effective_date ASC
        ),
        combined_promotion AS (
            -- 🔹 3. Combine them and pick the best one (priority 1 then 2)
            SELECT DISTINCT ON (user_id) *
            FROM (
                SELECT * FROM latest_promotion
                UNION ALL
                SELECT * FROM earliest_future_promotion
            ) as combined
            ORDER BY user_id, priority ASC
        ),
        latest_transfer AS (
            -- 🔹 Same for transfers: check latest before
            SELECT DISTINCT ON (user_id)
                user_id,
                new_station AS station_id,
                1 as priority
            FROM employee_transfers
            WHERE effective_date <= MAKE_DATE(:end_year, 3, 31)
              AND is_deleted = FALSE
            ORDER BY user_id, effective_date DESC
        ),
        earliest_future_transfer AS (
            -- 🔹 And earliest after
            SELECT DISTINCT ON (user_id)
                user_id,
                current_station AS station_id,
                2 as priority
            FROM employee_transfers
            WHERE effective_date > MAKE_DATE(:end_year, 3, 31)
              AND is_deleted = FALSE
            ORDER BY user_id, effective_date ASC
        ),
        combined_transfer AS (
            SELECT DISTINCT ON (user_id) *
            FROM (
                SELECT * FROM latest_transfer
                UNION ALL
                SELECT * FROM earliest_future_transfer
            ) as combined
            ORDER BY user_id, priority ASC
        ),
        latest_supervisor_history AS (
            SELECT DISTINCT ON (user_id)
                user_id,
                supervisor_id
            FROM users_history
            WHERE history_created_at <= MAKE_DATE(:end_year, 3, 31)
            ORDER BY user_id, history_created_at DESC
        )
        SELECT
            u.user_id,
            u.employee_code,
            TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,

            -- Grade: use historical promotion grade, fallback to current grade
            COALESCE(cp.grade, u.grade) AS grade,

            -- Designation: use historical promotion designation, fallback to current
            COALESCE(cp.designation, u.designation) AS designation,

            -- Station: use historical transfer station name, fallback to current station
            COALESCE(s_hist.station_name, s_curr.station_name) AS station_name,

            -- Supervisor: use historical supervisor_id to get the name, fallback to current
            TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
            ) AS supervisor,

            ep.appraisal_start_date,
            ep.appraisal_end_date,
            ep.annual_appraisal_rating,
            ep.annual_rating_score,
            ep.performance_id

        FROM users u
        LEFT JOIN combined_promotion cp ON cp.user_id = u.user_id
        LEFT JOIN combined_transfer ct ON ct.user_id = u.user_id
        LEFT JOIN station s_curr ON u.station_id = s_curr.station_id
        LEFT JOIN station s_hist ON ct.station_id = s_hist.station_id
        LEFT JOIN latest_supervisor_history lsh ON lsh.user_id = u.user_id
        LEFT JOIN users sup ON COALESCE(lsh.supervisor_id, u.supervisor_id) = sup.user_id
        LEFT JOIN employee_performance ep
            ON ep.user_id = u.user_id {year_filter}
        WHERE u.is_deleted = FALSE 
          AND u.is_employee = TRUE
          {user_joining_filter} 
          {termination_filter}
        ORDER BY (CASE WHEN ep.annual_appraisal_rating IS NULL THEN 0 ELSE 1 END), u.employee_code ASC
        """

    else:
        # 🔹 No year filter: use current data from users table directly
        base_query = f"""
        SELECT
            u.user_id,
            u.employee_code,
            TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
            u.grade,
            u.designation,
            s.station_name,
            TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
            ) AS supervisor,
            ep.appraisal_start_date,
            ep.appraisal_end_date,
            ep.annual_appraisal_rating,
            ep.annual_rating_score,
            ep.performance_id

        FROM users u
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        LEFT JOIN employee_performance ep ON ep.user_id = u.user_id
        WHERE u.is_deleted = FALSE
          AND u.is_employee = TRUE
          {termination_filter}
        ORDER BY (CASE WHEN ep.annual_appraisal_rating IS NULL THEN 0 ELSE 1 END), u.employee_code ASC
        """

    result = db.execute(text(base_query), params).mappings().all()
    
    items = []
    for row in result:
        item_dict = dict(row)
        perf_id = item_dict.get("performance_id")
        
        if perf_id:
            # 🔹 Fetch attachments for this performance ID
            docs_query = text("""
                SELECT id, file_name, file_path 
                FROM employee_performance_documents 
                WHERE performance_id = :pid AND (is_deleted = FALSE OR is_deleted IS NULL)
            """)
            attachments = db.execute(docs_query, {"pid": perf_id}).mappings().all()
            
            formatted_attachments = []
            for att in attachments:
                att_dict = dict(att)
                att_dict["file_path"] = make_download_url(att_dict["file_path"])
                formatted_attachments.append(att_dict)
            
            item_dict["attachments"] = formatted_attachments
        else:
            item_dict["attachments"] = []
            
        items.append(item_dict)

    return items


# 🔹 CREATE DOCUMENT
def create_document(db: Session, performance_id: int, file_name: str, file_path: str):
    query = text("""
        INSERT INTO employee_performance_documents (performance_id, file_name, file_path, uploaded_at, is_deleted)
        VALUES (:performance_id, :file_name, :file_path, :uploaded_at, FALSE)
        RETURNING id
    """)
    doc_id = db.execute(query, {
        "performance_id": performance_id,
        "file_name": file_name,
        "file_path": file_path,
        "uploaded_at": datetime.utcnow()
    }).scalar()
    
    insert_employee_performance_document_history(db, doc_id)
    db.commit()
    return doc_id

def delete_performance(db: Session, performance_id: int):
    query = text("""
        UPDATE employee_performance 
        SET is_deleted = TRUE 
        WHERE performance_id = :performance_id
    """)
    result = db.execute(query, {"performance_id": performance_id})
    
    # Soft delete related documents as well
    doc_query = text("""
        UPDATE employee_performance_documents 
        SET is_deleted = TRUE 
        WHERE performance_id = :performance_id
    """)
    db.execute(doc_query, {"performance_id": performance_id})
    
    db.commit()
    return result.rowcount > 0

def get_distinct_appraisal_years(db: Session):
    now = datetime.now()
    current_year = now.year
    
    # In India, fiscal year is April to March.
    # If we are in Jan, Feb, or March (month < 4), the current active fiscal year start is (current_year - 1).
    # If we are in April or later (month >= 4), the current active fiscal year start is (current_year).
    if now.month < 4:
        max_year = current_year
    else:
        max_year = current_year + 1

    start_year = 2018
    years = []
    for y in range(start_year, max_year):
        years.append(f"{y}-{y+1}")
    
    # Return reversed so the most recent year is at the top of the dropdown
    return sorted(years, reverse=True)
                                                                   