from datetime import date, timedelta
import json
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.crud.employees_info.user_finance_crud import make_download_url
from app.database import SessionLocal


# ---------------------------------------------------------
# Helper: Convert raw leave record into downloadable URLs
# ---------------------------------------------------------

def fix_document_paths(record):
    """Convert document_path into downloadable URL."""
    if not record:
        return record

    if "leave_header" in record:
        header = record["leave_header"]

        # SINGLE DOCUMENT FILE
        doc = header.get("document_path")
        if doc:
            header["document_path"] = make_download_url(doc)

    return record


# ---------------------------------------------------------
# Helper: Handle SQL result (string JSON or parsed JSON)
# ---------------------------------------------------------

def process_result(raw_json):
    """
    Handles BOTH:
    - JSON strings from PostgreSQL
    - Already-parsed Python dict/list returned by FastAPI/SQLAlchemy
    """

    if raw_json is None:
        return None

    # CASE 1: Already a list/dict -> process directly
    if isinstance(raw_json, list):
        return [fix_document_paths(item) for item in raw_json]

    if isinstance(raw_json, dict):
        return fix_document_paths(raw_json)

    # CASE 2: JSON string -> parse it
    try:
        data = json.loads(raw_json)
    except Exception:
        return raw_json  # Not JSON, return as-is

    if isinstance(data, list):
        return [fix_document_paths(item) for item in data]

    if isinstance(data, dict):
        return fix_document_paths(data)

    return data


# ---------------------------------------------------------
# CRUD FUNCTIONS
# ---------------------------------------------------------

def crud_my_leaves(db: Session, user_id: int):
    sql = text("SELECT get_leave_list('MY', :uid, NULL) AS data")
    raw = db.execute(sql, {"uid": user_id}).scalar()
    return process_result(raw)


# def crud_subordinate_leaves(db: Session, supervisor_id: int):
#     sql = text("""
#         SELECT *
#         FROM hr_leave_application
#         WHERE supervisor_id = :supervisor_id
#         ORDER BY created_at DESC NULLS LAST
#     """)
#     result = db.execute(sql, {"supervisor_id": supervisor_id}).mappings().all()
#     return result

# def crud_subordinate_leaves(db: Session, supervisor_id: int):
#     sql = text("""
#         SELECT 
#             hl.*,
#             u.employee_code
#         FROM hr_leave_application hl
#         LEFT JOIN users u ON u.user_id = hl.user_id
#         WHERE hl.supervisor_id = :supervisor_id
#         ORDER BY hl.created_at DESC NULLS LAST
#     """)
#     result = db.execute(sql, {"supervisor_id": supervisor_id}).mappings().all()
#     return result


def crud_subordinate_leaves(db: Session, supervisor_id: int):
    sql = text("""
        SELECT 
            hl.*,
            u.employee_code
        FROM hr_leave_application hl
        LEFT JOIN users u ON u.user_id = hl.user_id
        WHERE hl.supervisor_id = :supervisor_id
        ORDER BY 
            CASE 
                WHEN LOWER(hl.status) = 'pending' THEN 0
                ELSE 1
            END,
            hl.created_at DESC NULLS LAST
    """)
    
    result = db.execute(sql, {"supervisor_id": supervisor_id}).mappings().all()
    return result











# def crud_all_leaves(db: Session):
#     sql = text("SELECT get_leave_list('ALL', NULL, NULL) AS data")
#     raw = db.execute(sql).scalar()
#     return process_result(raw)
def crud_all_leaves(db: Session):
    sql = text("SELECT get_leave_list('ALL', NULL, NULL) AS data")
    raw = db.execute(sql).scalar()
    result = process_result(raw)
    
    if not result:
        return result
    
    # Extract all unique user_ids from the result
    user_ids = list({item["leave_header"]["user_id"] for item in result})
    
    # Fetch employee_codes for all those user_ids in one query
    users_sql = text("""
        SELECT user_id, employee_code 
        FROM users 
        WHERE user_id = ANY(:user_ids)
    """)
    users = db.execute(users_sql, {"user_ids": user_ids}).mappings().all()
    
    # Build a lookup dict {user_id: employee_code}
    employee_code_map = {u["user_id"]: u["employee_code"] for u in users}
    
    # Inject employee_code into each leave_header
    for item in result:
        user_id = item["leave_header"]["user_id"]
        item["leave_header"]["employee_code"] = employee_code_map.get(user_id)
    
    return result

def crud_leave_by_id(db: Session, leave_id: int):
    sql = text("SELECT get_leave_list('ONE', NULL, :lid) AS data")
    raw = db.execute(sql, {"lid": leave_id}).scalar()
    return process_result(raw)


