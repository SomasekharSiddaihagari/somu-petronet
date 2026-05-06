from sqlalchemy import text
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.schemas.hr_action_tracker.promotion_master_schema import PromotionCreate
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

def insert_promotion_document_history(db: Session, document_id: int):
    history_sql = text("""
        INSERT INTO promotion_documents_history (
            id, promotion_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        )
        SELECT
            id, promotion_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        FROM promotion_documents
        WHERE id = :document_id
    """)
    db.execute(history_sql, {"document_id": document_id})

# 🔹 CREATE
def create_promotion(db: Session, data: PromotionCreate):
    payload = data.model_dump()
    query = text("""
        INSERT INTO promotions
        (user_id, current_grade, new_grade, current_designation, new_designation,
         effective_date, remarks, created_by, created_at, acknowledgement, is_deleted)
        VALUES
        (:user_id, :current_grade, :new_grade, :current_designation, :new_designation,
         :effective_date, :remarks, :created_by,NOW(), false, false)
        RETURNING id
    """)

    result = db.execute(query, payload)
    id = result.scalar()
    insert_promotions_history(db, id)

    user = db.execute(text("SELECT grade, designation FROM users WHERE user_id = :user_id"), {"user_id": payload["user_id"]}).mappings().first()
    if user:
        current_grade = user["grade"]
        current_desig = user["designation"]
        new_grade = payload.get("new_grade")
        new_desig = payload.get("new_designation")
        effective_date = payload.get("effective_date")

        should_update = False
        
        if (new_grade and new_grade != current_grade) or (new_desig and new_desig != current_desig):
            if effective_date:
                try:
                    if isinstance(effective_date, str):
                        date_str = str(effective_date).replace("T", " ").split(" ")[0]
                        if len(date_str.split("-")[0]) == 4:
                            eff_date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                        else:
                            eff_date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
                    elif isinstance(effective_date, datetime):
                        eff_date_obj = effective_date.date()
                    else:
                        eff_date_obj = effective_date 
                        
                    if eff_date_obj <= datetime.utcnow().date():
                        should_update = True
                except Exception as e:
                    print(f"Error parsing date in promotions: {e}")
                    should_update = True
            else:
                should_update = True

        if should_update:
            to_update_grade = new_grade if new_grade and new_grade != current_grade else current_grade
            to_update_desig = new_desig if new_desig and new_desig != current_desig else current_desig

            db.execute(text("""
                UPDATE users
                SET grade = :grade, designation = :designation
                WHERE user_id = :user_id
            """), {
                "grade": to_update_grade,
                "designation": to_update_desig,
                "user_id": payload["user_id"]
            })

    db.commit()
    return id

def insert_promotions_history(db: Session, id: int):
    history_sql = text(""" 
                    INSERT INTO promotions_history (
                       id,
                       user_id, 
                       current_grade, 
                       new_grade, 
                       current_designation, 
                       new_designation,
                        effective_date, 
                        remarks, 
                       created_at, 
                       created_by
                    )
                    SELECT
                       id,
                       user_id, 
                       current_grade, 
                       new_grade, 
                       current_designation, 
                       new_designation,
                       effective_date, 
                       remarks, 
                       created_at, 
                       created_by
                    FROM promotions
                    WHERE id = :id
                       """)
    db.execute(history_sql, {"id": id})

# 🔹 GET BY ID
def get_promotion_based_promotionid(db, id: int):
    query = text("""
        SELECT * FROM promotions WHERE id = :id order by created_at desc
    """)
    row = db.execute(query, {"id": id}).mappings().first()
    if not row:
        return None
    
    promotion_dict = dict(row)
    # docs_query = text("SELECT * FROM promotion_documents WHERE promotion_id = :pid AND is_deleted = FALSE")
    docs_query = text("SELECT * FROM promotion_documents WHERE promotion_id = :pid AND (is_deleted = FALSE OR is_deleted IS NULL)")

    attachments = db.execute(docs_query, {"pid": row["id"]}).mappings().all()
    
    formatted_attachments = []
    for att in attachments:
        att_dict = dict(att)
        att_dict["file_path"] = make_download_url(att_dict["file_path"])
        formatted_attachments.append(att_dict)
    
    promotion_dict["attachments"] = formatted_attachments
    return promotion_dict

def get_by_user_promotions(db: Session, user_id: int):
    query = text("""
        SELECT
            p.id,
            p.user_id,
            u.employee_code,
            TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
            u.contact_phone,

            s.station_name,

            p.current_designation,
            p.current_grade,
            p.new_designation,
            p.new_grade,
            p.effective_date,

            CASE 
                WHEN p.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,

            p.created_at,
            p.comments,
            p.remarks

        FROM promotions p
        JOIN users u ON p.user_id = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id

        WHERE p.user_id = :user_id
        AND p.is_deleted = FALSE

        ORDER BY p.created_at DESC
    """)

    result = db.execute(query, {"user_id": user_id}).mappings().all()
    items = []
    for row in result:
        item_dict = dict(row)
        # docs_query = text("SELECT * FROM promotion_documents WHERE promotion_id = :pid AND is_deleted = FALSE")
        docs_query = text("SELECT * FROM promotion_documents WHERE promotion_id = :pid AND (is_deleted = FALSE OR is_deleted IS NULL)")

        attachments = db.execute(docs_query, {"pid": item_dict["id"]}).mappings().all()
        
        formatted_attachments = []
        for att in attachments:
            att_dict = dict(att)
            att_dict["file_path"] = make_download_url(att_dict["file_path"])
            formatted_attachments.append(att_dict)
            
        item_dict["attachments"] = formatted_attachments
        items.append(item_dict)
        
    return items

# 🔹 GET ALL
def get_all_promotions(db):
    query = text("""
        SELECT * FROM promotions ORDER BY id DESC
    """)
    result = db.execute(query).fetchall()
    return result

def get_grade_designation(db, user_id: int):
    query = text("""
             SELECT
            u.user_id,
            u.employee_code,
            TRIM(
                COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
            ) AS name,
            u.email,

            -- 🔥 Promotion fallback
            COALESCE(p.new_designation, u.designation) AS designation,
            COALESCE(p.new_grade, u.grade) AS grade,

            u.employment_type,

            -- 🔥 Latest transfer station
            COALESCE(t.new_station, u.station_id) AS station_id,

            -- 🔥 Correct station name
            s.station_name

        FROM users u

        -- 🔥 Latest Promotion
        LEFT JOIN (
            SELECT DISTINCT ON (user_id)
                user_id,
                new_designation,
                new_grade
            FROM promotions
            ORDER BY user_id DESC, id desc
        ) p ON u.user_id = p.user_id

        -- 🔥 Latest Transfer (IMPORTANT FIX)
        LEFT JOIN (
            SELECT DISTINCT ON (user_id)
                user_id,
                new_station
            FROM employee_transfers
            ORDER BY user_id DESC, id DESC
        ) t ON u.user_id = t.user_id

        -- 🔥 Join using FINAL station_id
        LEFT JOIN station s 
            ON s.station_id = COALESCE(t.new_station, u.station_id)

        WHERE u.is_deleted = FALSE 
        AND u.user_id = :user_id
    """)
    result = db.execute(query, {"user_id": user_id}).fetchone()
    return result

def delete_promotion(db: Session, id: int):
    query = text("""
        UPDATE promotions
        SET
            is_deleted = TRUE
            WHERE id = :id
    """)

    db.execute(query, {
        "id": id
    })
    db.commit()
    return True

def get_all_promotions_hr(db: Session, user_id: int):

    # 🔹 Step 1: Get ALL roles
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)

    roles = db.execute(role_query, {"user_id": user_id}).scalars().all()

    is_hr = any(r.lower() == "hr" for r in roles)

    # 🔹 Step 2: Base Query (Added Supervisor + Full Name)
    base_query = """
        SELECT
            u.user_id,
            u.employee_code,
            TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
            u.contact_phone,
            s.station_name,
            u.designation as current_designation,
            u.grade as current_grade,
            p.new_designation,
            p.new_grade,
            p.effective_date,

            CASE 
                WHEN p.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,

            TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ) AS supervisor_name,

            p.created_at

        FROM users u
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        LEFT JOIN promotions p ON p.user_id = u.user_id
        WHERE u.is_deleted = FALSE and u.is_employee = true
    """

    # 🔹 Step 3: Role Condition
    if is_hr:
        query = text(base_query + " ORDER BY p.created_at DESC NULLS LAST")
        params = {}
    else:
        query = text(base_query + """
            AND u.supervisor_id = :user_id
            ORDER BY p.created_at DESC NULLS LAST
        """)
        params = {"user_id": user_id}

    # 🔹 Step 4: Execute
    result = db.execute(query, params).mappings().all()

    return result

def get_all_performance_hr(db: Session, user_id: int):

    # 🔹 Step 1: Get ALL roles
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)

    roles = db.execute(role_query, {"user_id": user_id}).scalars().all()

    is_hr = any(r.lower() == "hr" for r in roles)

    # 🔹 Step 2: Base Query (Added Supervisor + Full Name)

    base_query = """
    SELECT
        u.user_id,
        u.employee_code,
        TRIM(
            COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
        ) AS name,
        u.contact_phone,
        s.station_name,
        u.designation,
        u.grade,
 
        TRIM(
            COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
        ) AS supervisor_name,
 
        ep.appraisal_start_date,
        ep.appraisal_end_date,
        ep.annual_appraisal_rating,
        ep.annual_rating_score,
        ep.created_by,
        ep.created_at,
        ep.performance_id
 
    FROM users u
    LEFT JOIN users sup ON u.supervisor_id = sup.user_id
    LEFT JOIN station s ON u.station_id = s.station_id
 
    LEFT JOIN employee_performance ep
        ON ep.user_id = u.user_id
        AND ep.is_deleted = FALSE
 
    WHERE u.is_deleted = FALSE
    AND u.is_employee = true
 
    -- 🔥 exclude terminated employees
    AND NOT EXISTS (
        SELECT 1
        FROM disciplinary_incidents d
        WHERE d.user_id = u.user_id
        AND d.enable_termination = TRUE
        AND d.is_deleted = FALSE
    )
"""

    # 🔹 Step 3: Role Condition
    if is_hr:
        query = text(base_query + " ORDER BY ep.created_at DESC")
        params = {}
    
    # 🔹 Step 4: Execute
    result = db.execute(query, params).mappings().all()
    
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

def get_all_actions_hr(db: Session, user_id: int):

    # 🔹 Step 1: Get ALL roles
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)

    roles = db.execute(role_query, {"user_id": user_id}).scalars().all()

    is_hr = any(r.lower() == "hr" for r in roles)

    # 🔹 Step 2: Base Query
    base_query = """
        SELECT
            u.user_id,
            u.employee_code,
            TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
            u.contact_phone,
            s.station_name,

            u.designation,
            u.grade,

            TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ) AS supervisor_name,

            CASE 
                WHEN a.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,

            a.created_at AS hr_action_date,
            a.action_type AS hr_action_type
        FROM users u
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        LEFT JOIN hr_action a ON a.user_id = u.user_id
        WHERE u.is_deleted = FALSE and u.is_employee = true
    """

    # 🔹 Step 3: Role Condition
    if is_hr:
        query = text(base_query + " ORDER BY a.created_at DESC NULLS LAST")
        params = {}
    else:
        query = text(base_query + """
            AND u.supervisor_id = :user_id
            ORDER BY a.created_at DESC NULLS LAST
        """)
        params = {"user_id": user_id}

    # 🔹 Step 4: Execute
    result = db.execute(query, params).mappings().all()

    return result

def get_all_emp_transfer_hr(db: Session, user_id: int):

    # 🔹 Step 1: Get ALL roles
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)

    roles = db.execute(role_query, {"user_id": user_id}).scalars().all()
    is_hr = any(r.lower() == "hr" for r in roles)

    # 🔹 Step 2: Base Query
    base_query = """
                SELECT
                u.user_id,
                u.employee_code,
                TRIM(
                    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
                ) AS name,
                u.contact_phone AS mobile_no,

                -- 🔥 Previous station
                s_prev.station_name AS previous_station,

                u.designation AS previous_designation,
                u.grade AS previous_grade,

                -- 🔥 New station
                et.new_station AS new_station_id,
                s_new.station_name AS new_station,

                TRIM(
                    COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ) AS supervisor_name,

                CASE 
                    WHEN et.acknowledgement = TRUE THEN 'Yes'
                    ELSE 'No'
                END AS acknowledgement,

                et.effective_date,
                et.created_at,
                et.office_order_number,
                et.actual_joining_date

            FROM users u
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN employee_transfers et ON et.user_id = u.user_id
            LEFT JOIN station s_prev ON et.current_station = s_prev.station_id
            LEFT JOIN station s_new ON et.new_station = s_new.station_id

            WHERE u.is_deleted = FALSE and u.is_employee = true
        """

    # 🔹 Step 3: Role Condition
    if is_hr:
        query = text(base_query + " ORDER BY et.created_at DESC NULLS LAST")
        params = {}
    else:
        query = text(base_query + """
            AND u.supervisor_id = :user_id
            ORDER BY et.created_at DESC NULLS LAST
        """)
        params = {"user_id": user_id}

    # 🔹 Step 4: Execute
    result = db.execute(query, params).mappings().all()

    return result

def get_all_emp_disciplinary_hr(db: Session, user_id: int):

    # 🔹 Step 1: Get roles
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)

    roles = db.execute(role_query, {"user_id": user_id}).scalars().all()
    is_hr = any(r.lower() == "hr" for r in roles)

    # 🔹 Step 2: Base Query
    base_query = """
        SELECT
            u.user_id,
            u.employee_code,
            TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
            u.contact_phone AS mobile_no,

            s.station_name,
            u.designation,
            u.grade,

            TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ) AS supervisor_name,

            d.incident_date AS issue_date,
            d.severity,

            CASE 
                WHEN d.enable_suspension = TRUE THEN 'Yes'
                ELSE 'No'
            END AS suspension,

            d.suspension_effective_from,
            d.suspension_effective_to,

            CASE 
                WHEN d.enable_termination = TRUE THEN 'Yes'
                ELSE 'No'
            END AS termination,

            d.termination_effective_from,

            CASE 
                WHEN d.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,

            d.created_at

        FROM users u
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        LEFT JOIN disciplinary_incidents d 
            ON d.user_id = u.user_id 
            AND d.is_deleted = FALSE

        WHERE u.is_deleted = FALSE and u.is_employee = true
    """

    # 🔹 Step 3: Role condition
    if is_hr:
        query = text(base_query + " ORDER BY d.created_at DESC NULLS LAST")
        params = {}
    else:
        query = text(base_query + """
            AND u.supervisor_id = :user_id
            ORDER BY d.created_at DESC NULLS LAST
        """)
        params = {"user_id": user_id}

    # 🔹 Step 4: Execute
    result = db.execute(query, params).mappings().all()

    return result

def get_all_emp_hr(db: Session, user_id: int):

    # 🔹 Step 1: Get Role
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)

    roles = db.execute(role_query, {"user_id": user_id}).scalars().all()

    is_hr = any(r.lower() == "hr" for r in roles)

    # 🔹 Step 2: Base Query (UNION of all actions)
    base_query = """
    
    SELECT 
        u.user_id,
        u.employee_code,
        TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
        u.contact_phone AS mobile_no,
        s.station_name,
        u.designation,
        u.grade,
        TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ) AS supervisor,
        u.employment_type,
        a.action_date,
        a.created_at AS issue_date,
        a.action_type AS type
    FROM users u
    LEFT JOIN users sup ON u.supervisor_id = sup.user_id
    LEFT JOIN station s ON u.station_id = s.station_id
    LEFT JOIN hr_action a ON a.user_id = u.user_id
    WHERE u.is_deleted = FALSE AND u.is_employee = TRUE

    UNION 

    SELECT 
        u.user_id,
        u.employee_code,
        TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
        u.contact_phone,
        s.station_name,
        u.designation,
        u.grade,
        TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ),
        u.employment_type,
        
        d.incident_date,
        d.created_at,
        'Disciplinary'
    FROM users u
    LEFT JOIN users sup ON u.supervisor_id = sup.user_id
    LEFT JOIN station s ON u.station_id = s.station_id
    JOIN disciplinary_incidents d ON d.user_id = u.user_id
    WHERE u.is_deleted = FALSE AND u.is_employee = TRUE

    UNION

    SELECT 
        u.user_id,
        u.employee_code,
        TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
        u.contact_phone,
        s.station_name,
        p.new_designation,
        p.new_grade,
        TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ),
        u.employment_type,
        p.effective_date,
        p.created_at,
        'Promotion'
    FROM users u
    LEFT JOIN users sup ON u.supervisor_id = sup.user_id
    LEFT JOIN station s ON u.station_id = s.station_id
    JOIN promotions p ON p.user_id = u.user_id
    WHERE u.is_deleted = FALSE AND u.is_employee = TRUE

    UNION

    SELECT 
        u.user_id,
        u.employee_code,
        TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
        u.contact_phone,
        s.station_name,
        u.designation,
        u.grade,
        TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ),
        u.employment_type,
        t.effective_date,
        t.created_at,
        'Transfer'
    FROM users u
    LEFT JOIN users sup ON u.supervisor_id = sup.user_id
    LEFT JOIN station s ON u.station_id = s.station_id
    JOIN employee_transfers t ON t.user_id = u.user_id
    WHERE u.is_deleted = FALSE AND u.is_employee = TRUE

    """

    # 🔹 Step 3: Apply Role Filter
    if is_hr:
        query = text(base_query + " ORDER BY issue_date DESC NULLS LAST")
        params = {}
    else:
        query = text("""
            SELECT * FROM (
        """ + base_query + """
            ) AS combined
            WHERE user_id IN (
                SELECT user_id FROM users WHERE supervisor_id = :user_id
            )
            ORDER BY issue_date DESC NULLS LAST
        """)
        params = {"user_id": user_id}

    # 🔹 Step 4: Execute
    result = db.execute(query, params).mappings().all()

    return result

def acknowledge_hr_promotion(db: Session, id: int, user_id: int, payload: dict):

    # 🔹 Step 1: Check record exists
    check_query = text("""
        SELECT id, user_id, acknowledgement
        FROM promotions
        WHERE id = :id
        AND is_deleted = FALSE
    """)

    record = db.execute(check_query, {"id": id}).mappings().first()

    if not record:
        return {"status": False, "message": "Action not found"}

    # 🔹 Step 3: Update only allowed fields
    update_query = text("""
        UPDATE promotions
        SET 
            comments = :comments,           
            acknowledgement = :acknowledgement
        WHERE  user_id = :user_id and id = :id 
    """)
 
    db.execute(update_query, {
        "acknowledgement": payload.get("acknowledgement", True),
        "comments": payload.get("comments"),
        "user_id": user_id,
        "id": id
    })

    db.commit()

    return {"status": True, "message": "Acknowledged successfully"}

def get_employee_activity(db: Session, request,user_id: int):
 
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)
 
    roles = db.execute(role_query, {"user_id": user_id}).scalars().all()
 
    is_hr = any(r.lower() == "hr" for r in roles)
   
    base_query = """
        SELECT * FROM (
            -- 1. HR Actions
            SELECT
                a.id,
                a.user_id,
                u.employee_code,
                TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
                u.contact_phone AS mobile_no,
                s.station_name,
                u.designation,
                u.grade,
                TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')) AS supervisor,
                u.employment_type,
                a.created_at AS issue_date,
                a.action_type AS type,
                u.station_id,
                a.created_by,
                u.supervisor_id
            FROM hr_action a
            LEFT JOIN users u ON a.user_id = u.user_id
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN station s ON u.station_id = s.station_id
            WHERE a.is_deleted = FALSE
 
            UNION ALL
 
            -- 2. Disciplinary
            SELECT
                d.disciplinary_id AS id,
                d.user_id,
                u.employee_code,
                TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
                u.contact_phone,
                s.station_name,
                u.designation,
                u.grade,
                TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')),
                u.employment_type,
                d.incident_date,
                'Disciplinary',
                u.station_id,
                d.created_by,
                u.supervisor_id
            FROM disciplinary_incidents d
            LEFT JOIN users u ON d.user_id = u.user_id
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN station s ON u.station_id = s.station_id
            WHERE d.is_deleted = FALSE
 
            UNION ALL
 
            -- 3. Promotions
            SELECT
                p.id,
                p.user_id,
                u.employee_code,
                TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
                u.contact_phone,
                s.station_name,
                p.new_designation,
                p.new_grade,
                TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')),
                u.employment_type,
                p.effective_date,
                'Promotion',
                u.station_id,
                p.created_by,
                u.supervisor_id
            FROM promotions p
            LEFT JOIN users u ON p.user_id = u.user_id
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN station s ON u.station_id = s.station_id
            WHERE p.is_deleted = FALSE
 
            UNION ALL
 
            -- 4. Transfers
            SELECT
                t.id,
                t.user_id,
                u.employee_code,
                TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
                u.contact_phone,
                s.station_name,
                u.designation,
                u.grade,
                TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')),
                u.employment_type,
                t.effective_date,
                'Transfer',
                u.station_id,
                t.created_by,
                u.supervisor_id
            FROM employee_transfers t
            LEFT JOIN users u ON t.user_id = u.user_id
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN station s ON u.station_id = s.station_id
            WHERE t.is_deleted = FALSE
        ) AS combined
        WHERE 1=1
    """
 
    params = {"user_id": user_id}
    today = datetime.utcnow()

     # 🔹 Apply Visibility Filters
    if is_hr:
        base_query += " AND created_by = :user_id"
    else:
       
        # Dynamic Hierarchy: Show actions for anyone who reports to this user_id
        base_query += " AND supervisor_id = :user_id"
 
    # 🔹 No Station/Employee filters required as per new requirement
 
    # 🔹 3. Date Range Filters
    if request.filter_type:
        filter_val = request.filter_type.lower().strip().replace(" ", "_")
 
        if filter_val == "today":
            base_query += " AND DATE(issue_date) = CURRENT_DATE"
 
        elif filter_val in ["last_7_days", "week"]:
            base_query += " AND issue_date >= :date_7"
            params["date_7"] = today - timedelta(days=7)
 
        elif filter_val == "days_15":
            base_query += " AND issue_date >= :date_15"
            params["date_15"] = today - timedelta(days=15)
 
        elif filter_val in ["last_1_month", "month_1"]:
            base_query += " AND issue_date >= :date_30"
            params["date_30"] = today - timedelta(days=30)
 
        elif filter_val in ["last_3_months", "month_3"]:
            base_query += " AND issue_date >= :date_90"
            params["date_90"] = today - timedelta(days=90)
 
        elif filter_val in ["month_6", "half_yearly"]:
            base_query += " AND issue_date >= :date_m6"
            params["date_m6"] = today - timedelta(days=180)
 
        elif filter_val == "last_1_year":
            base_query += " AND issue_date >= :date_365"
            params["date_365"] = today - timedelta(days=365)
 
        elif filter_val == "quarterly":
            base_query += " AND issue_date >= date_trunc('quarter', CURRENT_DATE)"
 
        elif filter_val == "custom_range" and request.from_date and request.to_date:
            try:
                from_date_str = str(request.from_date).split('T')[0].split(' ')[0]
                to_date_str = str(request.to_date).split('T')[0].split(' ')[0]
               
                base_query += " AND issue_date BETWEEN :from_date AND :to_date"
                params["from_date"] = f"{from_date_str} 00:00:00"
                params["to_date"] = f"{to_date_str} 23:59:59"
            except Exception:
                pass
 
 
    # 🔹 5. Strict Visibility Check (Mandatory for all per requirement)
    # base_query += " AND created_by = :viewer_id"
    # params["viewer_id"] = user_id
 
    base_query += " ORDER BY issue_date DESC NULLS LAST"
 
    result = db.execute(text(base_query), params).mappings().all()
 
    return result
# 🔹 CREATE DOCUMENT
def create_document(db: Session, promotion_id: int, file_name: str, file_path: str):
    query = text("""
        INSERT INTO promotion_documents (promotion_id, file_name, file_path, uploaded_at, is_deleted)
        VALUES (:promotion_id, :file_name, :file_path, :uploaded_at, FALSE)
        RETURNING id
    """)
    doc_id = db.execute(query, {
        "promotion_id": promotion_id,
        "file_name": file_name,
        "file_path": file_path,
        "uploaded_at": datetime.utcnow()
    }).scalar()
    
    insert_promotion_document_history(db, doc_id)
    db.commit()
    return doc_id
def get_employee_activity_promotion(db: Session, request, user_id: int):
 
    # 🔹 Step 1: Get roles
    role_query = text("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = :user_id
    """)
 
    roles = db.execute(role_query, {"user_id": user_id}).scalars().all()
    is_hr = any(r.lower() == "hr" for r in roles)
 
    # 🔹 Step 2: Base Query
    base_query = """
        SELECT
            p.id,
            p.user_id,
            u.employee_code,
            TRIM(
                COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
            ) AS name,
            u.contact_phone,
            s.station_name,
 
            p.current_designation,
            p.current_grade,
            p.new_designation,
            p.new_grade,
 
            p.effective_date,
 
            CASE
                WHEN p.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,
 
            TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ) AS supervisor_name,
 
            p.created_at,
            p.created_by
 
        FROM promotions p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
 
        WHERE p.is_deleted = FALSE
    """
 
    params = {"user_id": user_id}
    today = datetime.utcnow()
 
    # 🔹 Always filter by creator (strict visibility for the creator's dashboard)
    # base_query += " AND p.created_by = :user_id"
     # 🔹 Apply Visibility Filters
    if is_hr:
        # HR sees actions they personally created
        # HR sees actions they personally created (Work History)
        base_query += " AND p.created_by = :user_id"
    else:
       
        # Dynamic Hierarchy: Show actions for anyone who reports to this user_id
        base_query += " AND u.supervisor_id = :user_id"
 
    # 🔹 Step 4: Date Filters (use effective_date)
    if request.filter_type:
        filter_val = request.filter_type.lower().strip().replace(" ", "_")
 
        if filter_val == "today":
            base_query += " AND DATE(p.effective_date) = CURRENT_DATE"
 
        elif filter_val in ["week", "last_7_days"]:
            base_query += " AND p.effective_date >= :date_7"
            params["date_7"] = today - timedelta(days=7)
 
        elif filter_val == "days_15":
            base_query += " AND p.effective_date >= :date_15"
            params["date_15"] = today - timedelta(days=15)
 
        elif filter_val in ["month_1", "last_1_month"]:
            base_query += " AND p.effective_date >= :date_30"
            params["date_30"] = today - timedelta(days=30)
 
        elif filter_val in ["month_3", "last_3_months"]:
            base_query += " AND p.effective_date >= :date_90"
            params["date_90"] = today - timedelta(days=90)
 
        elif filter_val in ["month_6", "half_yearly"]:
            base_query += " AND p.effective_date >= :date_180"
            params["date_180"] = today - timedelta(days=180)
 
        elif filter_val in ["last_1_year"]:
            base_query += " AND p.effective_date >= :date_365"
            params["date_365"] = today - timedelta(days=365)
 
        # elif filter_val == "quarterly":
        #     base_query += " AND p.effective_date >= date_trunc('quarter', CURRENT_DATE)"
 
        elif filter_val == "custom_range" and request.from_date and request.to_date:
            try:
                from_date_str = str(request.from_date).split('T')[0].split(' ')[0]
                to_date_str = str(request.to_date).split('T')[0].split(' ')[0]
               
                base_query += " AND p.effective_date BETWEEN :from_date AND :to_date"
                params["from_date"] = f"{from_date_str} 00:00:00"
                params["to_date"] = f"{to_date_str} 23:59:59"
            except Exception:
                pass
 
 
    # 🔹 Step 5: Quarter Filter
 
    # if request.quarters:
    #     quarter_conditions = []
 
    #     for i, q in enumerate(request.quarters):
 
    #         if not q or "-" not in q:
    #             continue
 
    #         try:
    #             quarter, year = q.split("-")
    #             year = int(year)
    #         except:
    #             continue
 
    #         if quarter == "Q1":
    #             start, end = f"{year}-01-01", f"{year}-03-31"
    #         elif quarter == "Q2":
    #             start, end = f"{year}-04-01", f"{year}-06-30"
    #         elif quarter == "Q3":
    #             start, end = f"{year}-07-01", f"{year}-09-30"
    #         elif quarter == "Q4":
    #             start, end = f"{year}-10-01", f"{year}-12-31"
    #         else:
    #             continue
 
    #         quarter_conditions.append(f"(p.effective_date BETWEEN :start{i} AND :end{i})")
    #         params[f"start{i}"] = start
    #         params[f"end{i}"] = end
 
    #     if quarter_conditions:
    #         base_query += " AND (" + " OR ".join(quarter_conditions) + ")"
 
    # 🔹 Step 6: Order
    base_query += " ORDER BY p.effective_date DESC NULLS LAST"
 
    # 🔹 Step 7: Execute
    result = db.execute(text(base_query), params).mappings().all()
 
    return result