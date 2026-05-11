from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from datetime import datetime, timedelta,date
import os
import urllib.parse
 
from app.schemas.hr_action_tracker.emp_transfer_master_schema import EmployeeTransferCreate, EmployeeTransferUpdate
 
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
 
def insert_transfer_history(db: Session, transfer_id: int):
    history_sql = text("""
        INSERT INTO employee_transfers_history (
            id, user_id, current_station, new_station, effective_date,
            remarks, acknowledgement, is_deleted, created_at, created_by, office_order_number
        )
        SELECT
            id, user_id, current_station, new_station, effective_date,
            remarks, acknowledgement, is_deleted, created_at, created_by, office_order_number
        FROM employee_transfers
        WHERE id = :transfer_id
    """)
    db.execute(history_sql, {"transfer_id": transfer_id})
 
def insert_transfer_document_history(db: Session, document_id: int):
    history_sql = text("""
        INSERT INTO transfer_documents_history (
            id, transfer_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        )
        SELECT
            id, transfer_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        FROM transfer_documents
        WHERE id = :document_id
    """)
    db.execute(history_sql, {"document_id": document_id})
 
# 🔹 CREATE
def create_transfer(db: Session, transfer_in: EmployeeTransferCreate):
    payload = transfer_in.model_dump()
    query = text("""
        INSERT INTO employee_transfers (user_id, current_station, new_station, effective_date, remarks, created_at, created_by,acknowledgement, is_deleted, office_order_number)
        VALUES (:user_id, :current_station, :new_station, :effective_date, :remarks, :created_at, :created_by,false, FALSE, :office_order_number)
        RETURNING id
    """)
    payload["created_at"] = datetime.utcnow()
   
    result = db.execute(query, payload)
    transfer_id = result.scalar()
    insert_transfer_history(db, transfer_id)

    user = db.execute(text("SELECT station_id FROM users WHERE user_id = :user_id"), {"user_id": payload["user_id"]}).mappings().first()
    if user:
        current_station = user["station_id"]
        new_station = payload.get("new_station")
        effective_date = payload.get("effective_date")

        should_update = False
        if new_station and new_station != current_station:
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
                    print(f"Error parsing date in transfer: {e}")
                    should_update = True
            else:
                should_update = True

        if should_update:
            db.execute(text("""
                UPDATE users
                SET station_id = :new_station
                WHERE user_id = :user_id
            """), {
                "new_station": new_station,
                "user_id": payload["user_id"]
            })

    db.commit()
    return get_transfer_by_id(db, transfer_id)
 
# 🔹 GET BY ID
def get_transfer_by_id(db: Session, transfer_id: int):
    query = text("""
                    SELECT 
                et.id,
                et.user_id,

                et.current_station,
                cs.station_name AS current_station_name,

                et.new_station,
                ns.station_name AS new_station_name,

                et.effective_date,
                et.remarks,
                et.created_at,
                et.created_by,
                 CASE 
                WHEN et.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,
                 et.is_deleted,
                 et.comments,
                 et.office_order_number,
                 et.actual_joining_date
            FROM employee_transfers et

            LEFT JOIN station cs ON cs.station_id = et.current_station
            LEFT JOIN station ns ON ns.station_id = et.new_station

            WHERE et.id = :transfer_id
            order by et.created_at desc
    """)
    row = db.execute(query, {"transfer_id": transfer_id}).mappings().first()
    if not row:
        return None
       
    transfer_dict = dict(row)
    # docs_query = text("SELECT * FROM transfer_documents WHERE transfer_id = :tid AND is_deleted = FALSE")
    docs_query = text("SELECT * FROM transfer_documents WHERE transfer_id = :tid AND (is_deleted = FALSE OR is_deleted IS NULL)")

    attachments = db.execute(docs_query, {"tid": row["id"]}).mappings().all()
   
    formatted_attachments = []
    for att in attachments:
        att_dict = dict(att)
        att_dict["file_path"] = make_download_url(att_dict["file_path"])
        formatted_attachments.append(att_dict)
   
    transfer_dict["attachments"] = formatted_attachments
    return transfer_dict
 
# 🔹 GET ALL
def get_all_transfers(db: Session):
    query = text("""
        SELECT 
                et.id,
                et.user_id,

                et.current_station,
                cs.station_name AS current_station_name,

                et.new_station,
                ns.station_name AS new_station_name,

                et.effective_date,
                et.remarks,
                et.created_at,
                et.created_by,
                 CASE 
                WHEN et.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,
                 et.is_deleted,
                 et.comments,
                 et.office_order_number,
                 et.actual_joining_date
            FROM employee_transfers et

            LEFT JOIN station cs ON cs.station_id = et.current_station
            LEFT JOIN station ns ON ns.station_id = et.new_station 
        WHERE et.is_deleted = FALSE ORDER BY et.created_at DESC
    """)
    rows = db.execute(query).mappings().all()
   
    items = []
    for row in rows:
        transfer_dict = dict(row)
        # docs_query = text("SELECT * FROM transfer_documents WHERE transfer_id = :tid AND is_deleted = FALSE")
        docs_query = text("SELECT * FROM transfer_documents WHERE transfer_id = :tid AND (is_deleted = FALSE OR is_deleted IS NULL)")

        attachments = db.execute(docs_query, {"tid": row["id"]}).mappings().all()
       
        formatted_attachments = []
        for att in attachments:
            att_dict = dict(att)
            att_dict["file_path"] = make_download_url(att_dict["file_path"])
            formatted_attachments.append(att_dict)
           
        transfer_dict["attachments"] = formatted_attachments
        items.append(transfer_dict)
   
    total = db.execute(text("SELECT COUNT(*) FROM employee_transfers WHERE is_deleted = FALSE")).scalar()
    return items, total
 
# 🔹 DELETE
def delete_transfer(db: Session, transfer_id: int):
    query = text("""
        UPDATE employee_transfers
        SET is_deleted = TRUE
        WHERE id = :id
    """)
    result = db.execute(query, {"id": transfer_id})
    db.commit()
    return result.rowcount > 0
 
# 🔹 CREATE DOCUMENT
def create_document(db: Session, transfer_id: int, file_name: str, file_path: str):
    query = text("""
        INSERT INTO transfer_documents (transfer_id, file_name, file_path, uploaded_at, is_deleted)
        VALUES (:transfer_id, :file_name, :file_path, :uploaded_at, FALSE)
        RETURNING id
    """)
    doc_id = db.execute(query, {
        "transfer_id": transfer_id,
        "file_name": file_name,
        "file_path": file_path,
        "uploaded_at": datetime.utcnow()
    }).scalar()
   
    insert_transfer_document_history(db, doc_id)
    db.commit()
    return doc_id

def get_by_user_transfers(db: Session, user_id: int):
    query = text("""
        SELECT
            et.id,
            et.user_id,
            u.employee_code,
            TRIM(
    COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
) AS name,
            u.contact_phone AS mobile_no,
            s1.station_name AS previous_station,
            u.designation AS previous_designation,
            u.grade AS previous_grade,
            -- New details
            s2.station_name AS new_station,
            et.effective_date,
            et.remarks,
            CASE 
                WHEN et.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,

            et.created_at,
            et.comments,
            et.office_order_number,
            et.actual_joining_date

        FROM employee_transfers et
        JOIN users u ON et.user_id = u.user_id

        LEFT JOIN station s1 ON et.current_station = s1.station_id
        LEFT JOIN station s2 ON et.new_station = s2.station_id

        WHERE et.user_id = :user_id
        AND et.is_deleted = FALSE
        ORDER BY et.created_at DESC
    """)

    rows = db.execute(query, {"user_id": user_id}).mappings().all()
    items = []
    for row in rows:
        action_dict = dict(row)
        docs_query = text("SELECT * FROM transfer_documents WHERE transfer_id = :aid AND is_deleted = FALSE")
        attachments = db.execute(docs_query, {"aid": row["id"]}).mappings().all()
       
        formatted_attachments = []
        for att in attachments:
            att_dict = dict(att)
            att_dict["file_path"] = make_download_url(att_dict["file_path"])
            formatted_attachments.append(att_dict)
           
        action_dict["attachments"] = formatted_attachments
        items.append(action_dict)
    return items
    

def acknowledge_hr_transfer(db: Session, id: int, user_id: int, payload: dict):

    # 🔹 Step 1: Check if record exists and belongs to this user
    check_query = text("""
        SELECT id, user_id, acknowledgement
        FROM employee_transfers
        WHERE id = :id
        AND is_deleted = FALSE
    """)

    record = db.execute(check_query, {"id": id}).mappings().first()

    if not record:
        return {"status": False, "message": "Transfer record not found"}
    
    if record["user_id"] != user_id:
        return {
            "status": False, 
            "message": f"User ID mismatch. This transfer belongs to user {record['user_id']}, but you provided {user_id}."
        }

    # 🔹 Step 3: Update the record
    update_query = text("""
        UPDATE employee_transfers
        SET 
            comments = :comments,           
            acknowledgement = :acknowledgement,
            actual_joining_date = :actual_joining_date
        WHERE id = :id 
    """)
 
    result = db.execute(update_query, {
        "acknowledgement": payload.get("acknowledgement", True),
        "comments": payload.get("comments"),
        "actual_joining_date": payload.get("actual_joining_date"),
        "id": id
    })

    db.commit()

    if result.rowcount == 0:
        return {"status": False, "message": "Update failed. No rows were changed."}

    return {"status": True, "message": "Acknowledged successfully"}

def get_employee_activity_transfer(db: Session, request, user_id: int ):
 
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
            et.id,
            et.user_id,
            u.employee_code,
            TRIM(
                COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')
            ) AS name,
            u.contact_phone AS mobile_no,
 
            s.station_name AS previous_station,
            u.designation AS previous_designation,
            u.grade AS previous_grade,
 
            et.new_station AS new_station_id,
            ns.station_name AS new_station,
 
            TRIM(
                COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')
                ) AS supervisor_name,
 
            CASE
                WHEN et.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,
 
            et.effective_date,
            et.created_at,
            et.created_by,
            et.office_order_number,
            et.actual_joining_date
        FROM employee_transfers et
        LEFT JOIN users u ON et.user_id = u.user_id
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        LEFT JOIN station ns ON ns.station_id = et.new_station
 
        WHERE et.is_deleted = FALSE
    """
 
    params = {"user_id": user_id}
    today = datetime.utcnow()
 
    # 🔹 Always filter by creator (strict visibility for the creator's dashboard)
    # base_query += " AND et.created_by = :user_id"
     # 🔹 Apply Visibility Filters
    if is_hr:
        # HR sees actions they personally created
        # HR sees actions they personally created (Work History)
        base_query += " AND et.created_by = :user_id"
    else:
       
        # Dynamic Hierarchy: Show actions for anyone who reports to this user_id
        base_query += " AND u.supervisor_id = :user_id"
 
    # 🔹 Step 4: Date Filters (use effective_date)
 
    if request.filter_type:
        filter_val = request.filter_type.lower().strip().replace(" ", "_")
 
        if filter_val == "today":
            base_query += " AND DATE(et.effective_date) = CURRENT_DATE"
 
        elif filter_val in ["week", "last_7_days"]:
            base_query += " AND et.effective_date >= :date"
            params["date"] = today - timedelta(days=7)
 
        elif filter_val == "days_15":
            base_query += " AND et.effective_date >= :date"
            params["date"] = today - timedelta(days=15)
 
        elif filter_val in ["month_1", "last_1_month"]:
            base_query += " AND et.effective_date >= :date"
            params["date"] = today - timedelta(days=30)
 
        elif filter_val in ["month_3", "last_3_months"]:
            base_query += " AND et.effective_date >= :date"
            params["date"] = today - timedelta(days=90)
 
        elif filter_val in ["month_6", "half_yearly"]:
            base_query += " AND et.effective_date >= :date"
            params["date"] = today - timedelta(days=180)
 
        elif filter_val == "last_1_year":
            base_query += " AND et.effective_date >= :date_365"
            params["date_365"] = today - timedelta(days=365)
 
        elif filter_val == "quarterly":
            base_query += " AND et.effective_date >= date_trunc('quarter', CURRENT_DATE)"
 
        elif filter_val == "custom_range" and request.from_date and request.to_date:
            try:
                from_date_str = str(request.from_date).split('T')[0].split(' ')[0]
                to_date_str = str(request.to_date).split('T')[0].split(' ')[0]
               
                base_query += " AND et.effective_date BETWEEN :from_date AND :to_date"
                params["from_date"] = f"{from_date_str} 00:00:00"
                params["to_date"] = f"{to_date_str} 23:59:59"
            except Exception:
                pass
 
    # 🔹 Step 5: Quarter Filter
 
    if getattr(request, 'quarters', None):
        quarter_conditions = []
 
        for i, q in enumerate(getattr(request, 'quarters', [])):
 
            if not q or "-" not in q:
                continue
 
            try:
                quarter, year = q.split("-")
                year = int(year)
            except:
                continue
 
            if quarter == "Q1":
                start, end = f"{year}-01-01", f"{year}-03-31"
            elif quarter == "Q2":
                start, end = f"{year}-04-01", f"{year}-06-30"
            elif quarter == "Q3":
                start, end = f"{year}-07-01", f"{year}-09-30"
            elif quarter == "Q4":
                start, end = f"{year}-10-01", f"{year}-12-31"
            else:
                continue
 
            quarter_conditions.append(f"(et.effective_date BETWEEN :start{i} AND :end{i})")
            params[f"start{i}"] = start
            params[f"end{i}"] = end
 
        if quarter_conditions:
            base_query += " AND (" + " OR ".join(quarter_conditions) + ")"
 
    # 🔹 Step 6: Order
    base_query += " ORDER BY et.effective_date DESC"
 
    # 🔹 Step 7: Execute
    result = db.execute(text(base_query), params).mappings().all()
 
    return result