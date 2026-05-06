from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from datetime import datetime, timedelta
import os
import urllib.parse
 
# from app.routers.UserAuthR2 import make_download_url

from app.schemas.hr_action_tracker.action_master_schema import HRActionCreate, HRActionUpdate
 
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
 
def insert_hr_action_history(db: Session, action_id: int):
    history_sql = text("""
        INSERT INTO hr_action_history (
            id, user_id, action_type, action_date, justification,
            acknowledgement, created_at, created_by, is_deleted
        )
        SELECT
            id, user_id, action_type, action_date, justification,
            acknowledgement, created_at, created_by, is_deleted
        FROM hr_action
        WHERE id = :action_id
    """)
    db.execute(history_sql, {"action_id": action_id})
 
def insert_hr_action_document_history(db: Session, document_id: int):
    history_sql = text("""
        INSERT INTO hr_action_documents_history (
            id, hr_action_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        )
        SELECT
            id, hr_action_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        FROM hr_action_documents
        WHERE id = :document_id
    """)
    db.execute(history_sql, {"document_id": document_id})
 
# 🔹 CREATE
def create_action(db: Session, action_in: HRActionCreate):
    payload = action_in.model_dump()
    query = text("""
        INSERT INTO hr_action (user_id, action_type, action_date, justification, created_at, created_by,acknowledgement, is_deleted)
        VALUES (:user_id, :action_type, :action_date, :justification, :created_at, :created_by, FALSE, false)
        RETURNING id
    """)
    payload["created_at"] = datetime.utcnow()
   
    result = db.execute(query, payload)
    action_id = result.scalar()
    insert_hr_action_history(db, action_id)
    db.commit()
    return get_action_by_id(db, action_id)
 
# 🔹 GET BY ID
def get_action_by_id(db: Session, action_id: int):
    query = text("""
        SELECT * FROM hr_action WHERE id = :action_id ORDER BY created_at DESC
    """)
    row = db.execute(query, {"action_id": action_id}).mappings().first()
    if not row:
        return None
       
    action_dict = dict(row)
    docs_query = text("SELECT * FROM hr_action_documents WHERE hr_action_id = :aid AND is_deleted = FALSE")
    attachments = db.execute(docs_query, {"aid": row["id"]}).mappings().all()
   
    formatted_attachments = []
    for att in attachments:
        att_dict = dict(att)
        att_dict["file_path"] = make_download_url(att_dict["file_path"])
        formatted_attachments.append(att_dict)
   
    action_dict["attachments"] = formatted_attachments
    return action_dict
 
# 🔹 GET ALL
def get_all_actions(db: Session):
    query = text("""
        SELECT * FROM hr_action WHERE is_deleted = FALSE ORDER BY created_at DESC
    """)
    rows = db.execute(query).mappings().all()
   
    items = []
    for row in rows:
        action_dict = dict(row)
        docs_query = text("SELECT * FROM hr_action_documents WHERE hr_action_id = :aid AND is_deleted = FALSE")
        attachments = db.execute(docs_query, {"aid": row["id"]}).mappings().all()
       
        formatted_attachments = []
        for att in attachments:
            att_dict = dict(att)
            att_dict["file_path"] = make_download_url(att_dict["file_path"])
            formatted_attachments.append(att_dict)
           
        action_dict["attachments"] = formatted_attachments
        items.append(action_dict)
   
    total = db.execute(text("SELECT COUNT(*) FROM hr_action WHERE is_deleted = FALSE")).scalar()
    return items, total
 
# 🔹 GET ACTIONS BY USER
def get_actions_by_user(db: Session, user_id: int):
    query = text("""
        SELECT * FROM hr_action WHERE user_id = :user_id AND is_deleted = FALSE ORDER BY created_at DESC
    """)
    rows = db.execute(query, {"user_id": user_id}).mappings().all()
   
    items = []
    for row in rows:
        action_dict = dict(row)
        docs_query = text("SELECT * FROM hr_action_documents WHERE hr_action_id = :aid AND is_deleted = FALSE")
        attachments = db.execute(docs_query, {"aid": row["id"]}).mappings().all()
       
        formatted_attachments = []
        for att in attachments:
            att_dict = dict(att)
            att_dict["file_path"] = make_download_url(att_dict["file_path"])
            formatted_attachments.append(att_dict)
           
        action_dict["attachments"] = formatted_attachments
        items.append(action_dict)
    return items
 
# 🔹 DELETE
def delete_action(db: Session, action_id: int):
    query = text("""
        UPDATE hr_action
        SET is_deleted = TRUE
        WHERE id = :id
    """)
    result = db.execute(query, {"id": action_id})
    db.commit()
    return result.rowcount > 0
 
# 🔹 UPDATE
def update_action(db: Session, action_id: int, action_in: HRActionUpdate, updated_by: int):
    pass
 
# 🔹 CREATE DOCUMENT
def create_document(db: Session, hr_action_id: int, file_name: str, file_path: str):
    query = text("""
        INSERT INTO hr_action_documents (hr_action_id, file_name, file_path, uploaded_at, is_deleted)
        VALUES (:hr_action_id, :file_name, :file_path, :uploaded_at, FALSE)
        RETURNING id
    """)
    doc_id = db.execute(query, {
        "hr_action_id": hr_action_id,
        "file_name": file_name,
        "file_path": file_path,
        "uploaded_at": datetime.utcnow()
    }).scalar()
   
    insert_hr_action_document_history(db, doc_id)
    db.commit()
    return doc_id

def acknowledge_hr_action(db: Session, id: int, user_id: int, payload: dict):

    # 🔹 Step 1: Check record exists
    check_query = text("""
        SELECT id,user_id, acknowledgement
        FROM hr_action
        WHERE id = :id
        AND is_deleted = FALSE
    """)

    record = db.execute(check_query, {"id": id}).mappings().first()

    if not record:
        return {"status": False, "message": "Action not found"}

    # 🔹 Step 3: Update only allowed fields
    update_query = text("""
        UPDATE hr_action
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

# get_employee_activity_actions

def get_employee_activity_actions(db: Session, request, user_id: int):
 
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
            a.id,
            a.user_id,
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
 
            a.action_date AS issue_date,
            a.action_type,
            a.justification,
 
            CASE
                WHEN a.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,
 
            a.created_at,
            a.created_by
 
        FROM hr_action a
        LEFT JOIN users u ON a.user_id = u.user_id
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
 
        WHERE a.is_deleted = FALSE
    """
 
    params = {"user_id": user_id}
    today = datetime.utcnow()
 
    if is_hr:
        # HR sees ALL actions company-wide (No filters added)
        pass
    else:
        # Dynamic Hierarchy: Show actions for anyone who reports to this user_id
        base_query += " AND u.supervisor_id = :user_id"
 
    # 🔹 Step 4: Date Filters
    if request.filter_type:
        filter_val = request.filter_type.lower().strip()
       
        # We will filter on action_date (Issue Date) because that makes sense for the user view.
        if filter_val == "today":
            base_query += " AND DATE(a.action_date) = CURRENT_DATE"
 
        elif filter_val in ["last 7 days", "last_7_days", "week"]:
            base_query += " AND a.action_date >= :date_7"
            params["date_7"] = today - timedelta(days=7)
 
        elif filter_val == "days_15":
            base_query += " AND a.action_date >= :date_15"
            params["date_15"] = today - timedelta(days=15)
 
        elif filter_val in ["last 1 month", "last_1_month", "month_1"]:
            base_query += " AND a.action_date >= :date_30"
            params["date_30"] = today - timedelta(days=30)
 
        elif filter_val in ["last 3 months", "last_3_months", "month_3"]:
            base_query += " AND a.action_date >= :date_90"
            params["date_90"] = today - timedelta(days=90)
 
        elif filter_val == "month_6":
            base_query += " AND a.action_date >= :date_180"
            params["date_180"] = today - timedelta(days=180)
 
        elif filter_val in ["last 1 year", "last_1_year"]:
            base_query += " AND a.action_date >= :date_365"
            params["date_365"] = today - timedelta(days=365)
 
        elif filter_val in ["custom range", "custom_range"] and request.from_date and request.to_date:
            try:
                # Need to handle DD-MM-YYYY or DD/MM/YYYY to YYYY-MM-DD
                fd_raw = str(request.from_date).split('T')[0].split(' ')[0]
                td_raw = str(request.to_date).split('T')[0].split(' ')[0]
               
                # Check if format is DD-MM-YYYY
                if "-" in fd_raw and len(fd_raw.split("-")[0]) <= 2:
                    parts = fd_raw.split("-")
                    fd_raw = f"{parts[2]}-{parts[1]}-{parts[0]}"
               
                if "-" in td_raw and len(td_raw.split("-")[0]) <= 2:
                    parts = td_raw.split("-")
                    td_raw = f"{parts[2]}-{parts[1]}-{parts[0]}"
               
                base_query += " AND a.action_date BETWEEN :from_date AND :to_date"
                params["from_date"] = f"{fd_raw} 00:00:00"
                params["to_date"] = f"{td_raw} 23:59:59"
            except Exception as e:
                print("Date parse error:", e)
 
    # 🔹 Step 6: Order
    base_query += " ORDER BY a.created_at DESC"
 
    # 🔹 Step 7: Execute
    result = db.execute(text(base_query), params).mappings().all()
 
    return result
 
    # 🔹 Always filter by creator (strict visibility for the creator's dashboard)
    #base_query += " AND a.created_by = :user_id"
    # 🔹 Apply Visibility Filters
    # if is_hr:
    #     # HR sees actions they personally created
    #     # HR sees actions they personally created (Work History)
    #     base_query += " AND a.created_by = :user_id"
    # else:
       
    #     # Dynamic Hierarchy: Show actions for anyone who reports to this user_id
    #     base_query += " AND u.supervisor_id = :user_id"

 
    # # 🔹 Step 4: Date Filters
 
    # if request.filter_type:
    #     filter_val = request.filter_type.lower().strip()
 
    #     if filter_val == "today":
    #         base_query += " AND DATE(a.created_at) = CURRENT_DATE"
 
    #     elif filter_val in ["last 7 days", "last_7_days", "week"]:
    #         base_query += " AND a.created_at >= :date_7"
    #         params["date_7"] = today - timedelta(days=7)
 
    #     elif filter_val == "days_15":
    #         base_query += " AND a.created_at >= :date_15"
    #         params["date_15"] = today - timedelta(days=15)
 
    #     elif filter_val in ["last 1 month", "last_1_month", "month_1"]:
    #         base_query += " AND a.created_at >= :date_30"
    #         params["date_30"] = today - timedelta(days=30)
 
    #     elif filter_val in ["last 3 months", "last_3_months", "month_3"]:
    #         base_query += " AND a.created_at >= :date_90"
    #         params["date_90"] = today - timedelta(days=90)
 
    #     elif filter_val == "month_6":
    #         base_query += " AND a.created_at >= :date_180"
    #         params["date_180"] = today - timedelta(days=180)
 
    #     elif filter_val in ["last 1 year", "last_1_year"]:
    #         base_query += " AND a.created_at >= :date_365"
    #         params["date_365"] = today - timedelta(days=365)
 
    #     # elif filter_val == "quarterly":
    #     #     base_query += " AND a.created_at >= date_trunc('quarter', CURRENT_DATE)"
 
    #     # elif filter_val == "half_yearly":
    #     #     base_query += " AND a.created_at >= CURRENT_DATE - INTERVAL '6 months'"
 
    #     elif filter_val in ["custom range", "custom_range"] and request.from_date and request.to_date:
    #         try:
    #             from_date_str = str(request.from_date).split('T')[0].split(' ')[0]
    #             to_date_str = str(request.to_date).split('T')[0].split(' ')[0]
               
    #             base_query += " AND a.created_at BETWEEN :from_date AND :to_date"
    #             params["from_date"] = f"{from_date_str} 00:00:00"
    #             params["to_date"] = f"{to_date_str} 23:59:59"
    #         except Exception:
    #             pass
 
    # # 🔹 Step 6: Order
    # base_query += " ORDER BY a.created_at DESC"
 
    # # 🔹 Step 7: Execute
    # result = db.execute(text(base_query), params).mappings().all()
 
    # return result
    