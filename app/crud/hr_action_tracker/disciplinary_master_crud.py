from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.hr_action_tracker.disciplinary_master_schema import DisciplinaryIncidentCreate
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

def insert_disciplinary_incident_document_history(db: Session, document_id: int):
    history_sql = text("""
        INSERT INTO disciplinary_incident_documents_history (
            id, disciplinary_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        )
        SELECT
            id, disciplinary_id, file_name, file_path, uploaded_at, acknowledgement, is_deleted
        FROM disciplinary_incident_documents
        WHERE id = :document_id
    """)
    db.execute(history_sql, {"document_id": document_id}) 
def create_incident(db: Session, incident_in: DisciplinaryIncidentCreate):
    sql = text("""
        INSERT INTO disciplinary_incidents (
            user_id, incident_date, severity, incident_details, investigation_finding,
            measures_taken, enable_suspension, enable_termination, suspension_effective_from,
            suspension_effective_to, termination_effective_from, outcome, created_at,
            created_by, acknowledgement, is_deleted
        ) VALUES (
            :user_id, :incident_date, :severity, :incident_details, :investigation_finding,
            :measures_taken, :enable_suspension, :enable_termination, :suspension_effective_from,
            :suspension_effective_to, :termination_effective_from, :outcome, NOW(),
            :created_by, false, FALSE
        ) RETURNING disciplinary_id, created_at
    """)
   
    result = db.execute(sql, {
        "user_id": incident_in.user_id,
        "incident_date": incident_in.incident_date,
        "severity": incident_in.severity,
        "incident_details": incident_in.incident_details,
        "investigation_finding": incident_in.investigation_finding,
        "measures_taken": incident_in.measures_taken,
        "enable_suspension": incident_in.enable_suspension,
        "enable_termination": incident_in.enable_termination,
        "suspension_effective_from": incident_in.suspension_effective_from,
        "suspension_effective_to": incident_in.suspension_effective_to,
        "termination_effective_from": incident_in.termination_effective_from,
        "outcome": incident_in.outcome,
        "created_by": incident_in.created_by
        
    })
   
    row = result.fetchone()
    db.commit()
   
    incident_id = row[0]
    created_at = row[1]
 
    # Insert into history
    history_sql = text("""
        INSERT INTO disciplinary_incidents_history (
            disciplinary_id, user_id, incident_date, severity, incident_details, investigation_finding,
            measures_taken, enable_suspension, enable_termination, suspension_effective_from,
            suspension_effective_to, termination_effective_from, outcome, acknowledgement,
            is_deleted, created_at, created_by
        ) VALUES (
            :disciplinary_id, :user_id, :incident_date, :severity, :incident_details, :investigation_finding,
            :measures_taken, :enable_suspension, :enable_termination, :suspension_effective_from,
            :suspension_effective_to, :termination_effective_from, :outcome, false,
            FALSE, :created_at, :created_by
        )
    """)
   
    db.execute(history_sql, {
        "disciplinary_id": incident_id,
        "user_id": incident_in.user_id,
        "incident_date": incident_in.incident_date,
        "severity": incident_in.severity,
        "incident_details": incident_in.incident_details,
        "investigation_finding": incident_in.investigation_finding,
        "measures_taken": incident_in.measures_taken,
        "enable_suspension": incident_in.enable_suspension,
        "enable_termination": incident_in.enable_termination,
        "suspension_effective_from": incident_in.suspension_effective_from,
        "suspension_effective_to": incident_in.suspension_effective_to,
        "termination_effective_from": incident_in.termination_effective_from,
        "outcome": incident_in.outcome,
        "created_at": created_at,
        "created_by": incident_in.created_by
    })
    db.commit()
 
    return {"disciplinary_id": incident_id, "created_at": created_at}
 
def get_all_incidents(db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[dict], int]:
    sql = text("""
        SELECT * FROM disciplinary_incidents
        WHERE is_deleted = FALSE OR is_deleted IS NULL
        ORDER BY created_at DESC
    """)
    result = db.execute(sql)
    rows = result.fetchall()
   
    items = []
    for row in rows:
        incident_dict = dict(row._mapping)
        docs_query = text("SELECT * FROM disciplinary_incident_documents WHERE disciplinary_id = :did AND is_deleted = FALSE")
        attachments = db.execute(docs_query, {"did": incident_dict["disciplinary_id"]}).mappings().all()
       
        formatted_attachments = []
        for att in attachments:
            att_dict = dict(att)
            att_dict["file_path"] = make_download_url(att_dict["file_path"])
            formatted_attachments.append(att_dict)
           
        incident_dict["attachments"] = formatted_attachments
        items.append(incident_dict)
       
    return items, len(items)
 
def get_incident_by_id(db: Session, incident_id: int) -> Optional[dict]:
    # sql = text("SELECT * FROM disciplinary_incidents WHERE disciplinary_id = :id ORDER BY created_at DESC")
    sql = text("SELECT * FROM disciplinary_incidents WHERE disciplinary_id = :id AND (is_deleted = FALSE OR is_deleted IS NULL)")

    result = db.execute(sql, {"id": incident_id})
    row = result.fetchone()
    # return dict(row._mapping) if row else None
    if not row:
        return None
    
    incident_dict = dict(row._mapping)
    # docs_query = text("SELECT * FROM disciplinary_incident_documents WHERE disciplinary_id = :did AND is_deleted = FALSE")
    docs_query = text("SELECT * FROM disciplinary_incident_documents WHERE disciplinary_id = :did AND (is_deleted = FALSE OR is_deleted IS NULL)")

    attachments = db.execute(docs_query, {"did": incident_dict["disciplinary_id"]}).mappings().all()
    
    formatted_attachments = []
    for att in attachments:
        att_dict = dict(att)
        att_dict["file_path"] = make_download_url(att_dict["file_path"])
        formatted_attachments.append(att_dict)
    
    incident_dict["attachments"] = formatted_attachments
    return incident_dict
 
def delete_incident(db: Session, incident_id: int) -> bool:
    # Get current data for history
    current = get_incident_by_id(db, incident_id)
    if not current:
        return False
   
    # Soft delete (Consistent with user preference for history tracking modules)
    sql = text("UPDATE disciplinary_incidents SET is_deleted = TRUE WHERE disciplinary_id = :id")
    db.execute(sql, {"id": incident_id})
   
    # Update history
    history_sql = text("""
        INSERT INTO disciplinary_incidents_history (
            disciplinary_id, user_id, incident_date, severity, incident_details, investigation_finding,
            measures_taken, enable_suspension, enable_termination, suspension_effective_from,
            suspension_effective_to, termination_effective_from, outcome, acknowledgement,
            is_deleted, created_at, created_by
        ) VALUES (
            :disciplinary_id, :user_id, :incident_date, :severity, :incident_details, :investigation_finding,
            :measures_taken, :enable_suspension, :enable_termination, :suspension_effective_from,
            :suspension_effective_to, :termination_effective_from, :outcome, :acknowledgement,
            TRUE, NOW(), :created_by
        )
    """)
   
    db.execute(history_sql, {
        "disciplinary_id": incident_id,
        "user_id": current["user_id"],
        "incident_date": current["incident_date"],
        "severity": current["severity"],
        "incident_details": current["incident_details"],
        "investigation_finding": current["investigation_finding"],
        "measures_taken": current["measures_taken"],
        "enable_suspension": current["enable_suspension"],
        "enable_termination": current["enable_termination"],
        "suspension_effective_from": current["suspension_effective_from"],
        "suspension_effective_to": current["suspension_effective_to"],
        "termination_effective_from": current["termination_effective_from"],
        "outcome": current["outcome"],
        "acknowledgement": current["acknowledgement"],
        "created_by": current["created_by"]
    })
   
    db.commit()
    return True

def get_by_user_disciplinary_incident(db: Session, user_id: int):
    query = text("""
        SELECT
            d.disciplinary_id,
            d.user_id,
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
            d.severity,
            d.incident_details,
            d.incident_date,
            d.measures_taken,
            d.investigation_finding,
            d.enable_suspension,
            d.enable_termination,
            d.suspension_effective_from,
            d.suspension_effective_to,
            d.termination_effective_from,
            d.outcome,
            CASE 
                WHEN d.acknowledgement = TRUE THEN 'Yes'
                ELSE 'No'
            END AS acknowledgement,

            d.created_at,
            d.comments

        FROM disciplinary_incidents d
        JOIN users u ON d.user_id = u.user_id

        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id

        WHERE d.user_id = :user_id
        AND d.is_deleted = FALSE

        ORDER BY d.created_at DESC
    """)

    result = db.execute(query, {"user_id": user_id}).mappings().all()
    # return result
    items = []
    for row in result:
        item_dict = dict(row)
        docs_query = text("SELECT * FROM disciplinary_incident_documents WHERE disciplinary_id = :did AND is_deleted = FALSE")
        attachments = db.execute(docs_query, {"did": item_dict["disciplinary_id"]}).mappings().all()
        
        formatted_attachments = []
        for att in attachments:
            att_dict = dict(att)
            att_dict["file_path"] = make_download_url(att_dict["file_path"])
            formatted_attachments.append(att_dict)
            
        item_dict["attachments"] = formatted_attachments
        items.append(item_dict)
        
    return items


def acknowledge_hr_disciplinary(db: Session, disciplinary_id: int, user_id: int, payload: dict):

    # 🔹 Step 1: Check record exists
    check_query = text("""
        SELECT disciplinary_id, user_id, acknowledgement
        FROM disciplinary_incidents
        WHERE disciplinary_id = :disciplinary_id
        AND is_deleted = FALSE
    """)

    record = db.execute(check_query, {"disciplinary_id": disciplinary_id}).mappings().first()

    if not record:
        return {"status": False, "message": "Action not found"}

    # 🔹 Step 3: Update only allowed fields
    update_query = text("""
        UPDATE disciplinary_incidents
        SET 
            comments = :comments,           
            acknowledgement = :acknowledgement
        WHERE  user_id = :user_id and disciplinary_id = :disciplinary_id 
    """)
 
    db.execute(update_query, {
        "acknowledgement": payload.get("acknowledgement", True),
        "comments": payload.get("comments"),
        "user_id": user_id,
        "disciplinary_id": disciplinary_id
    })

    db.commit()

    return {"status": True, "message": "Acknowledged successfully"}


def get_employee_activity_disciplinary(db: Session, request, user_id: int):
 
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
            d.disciplinary_id AS id,
            d.user_id,
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
 
            d.created_at,
            d.created_by
 
        FROM disciplinary_incidents d
        LEFT JOIN users u ON d.user_id = u.user_id
        LEFT JOIN users sup ON u.supervisor_id = sup.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
 
        WHERE d.is_deleted = FALSE
    """
 
    params = {"user_id": user_id}
    today = datetime.utcnow()
 
    # 🔹 Always filter by creator (strict visibility for the creator's dashboard)
    # base_query += " AND d.created_by = :user_id"
     # 🔹 Apply Visibility Filters
    if is_hr:
        # HR sees actions they personally created
        # HR sees actions they personally created (Work History)
        base_query += " AND d.created_by = :user_id"
    else:
       
        # Dynamic Hierarchy: Show actions for anyone who reports to this user_id
        base_query += " AND u.supervisor_id = :user_id"
 
 
    # 🔹 Step 4: Date Filters (using incident_date)
 
    if request.filter_type:
        filter_val = request.filter_type.lower().strip().replace(" ", "_")
 
        if filter_val == "today":
            base_query += " AND DATE(d.incident_date) = CURRENT_DATE"
 
        elif filter_val in ["week", "last_7_days"]:
            base_query += " AND d.incident_date >= :date"
            params["date"] = today - timedelta(days=7)
 
        elif filter_val == "days_15":
            base_query += " AND d.incident_date >= :date"
            params["date"] = today - timedelta(days=15)
 
        elif filter_val in ["month_1", "last_1_month"]:
            base_query += " AND d.incident_date >= :date"
            params["date"] = today - timedelta(days=30)
 
        elif filter_val in ["month_3", "last_3_months"]:
            base_query += " AND d.incident_date >= :date"
            params["date"] = today - timedelta(days=90)
 
        elif filter_val in ["month_6", "half_yearly"]:
            base_query += " AND d.incident_date >= :date"
            params["date"] = today - timedelta(days=180)
 
        elif filter_val == "last_1_year":
            base_query += " AND d.incident_date >= :date_365"
            params["date_365"] = today - timedelta(days=365)
 
        elif filter_val == "quarterly":
            base_query += " AND d.incident_date >= date_trunc('quarter', CURRENT_DATE)"
 
        elif filter_val == "custom_range" and request.from_date and request.to_date:
            try:
                from_date_str = str(request.from_date).split('T')[0].split(' ')[0]
                to_date_str = str(request.to_date).split('T')[0].split(' ')[0]
                base_query += " AND d.incident_date BETWEEN :from_date AND :to_date"
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
 
            quarter_conditions.append(f"(d.incident_date BETWEEN :start{i} AND :end{i})")
            params[f"start{i}"] = start
            params[f"end{i}"] = end
 
        if quarter_conditions:
            base_query += " AND (" + " OR ".join(quarter_conditions) + ")"
 
    # 🔹 Step 6: Order
    base_query += " ORDER BY d.incident_date DESC"
 
    # 🔹 Step 7: Execute
    result = db.execute(text(base_query), params).mappings().all()
 
    return result
# 🔹 CREATE DOCUMENT
def create_document(db: Session, disciplinary_id: int, file_name: str, file_path: str):
    query = text("""
        INSERT INTO disciplinary_incident_documents (disciplinary_id, file_name, file_path, uploaded_at, is_deleted)
        VALUES (:disciplinary_id, :file_name, :file_path, :uploaded_at, FALSE)
        RETURNING id
    """)
    doc_id = db.execute(query, {
        "disciplinary_id": disciplinary_id,
        "file_name": file_name,
        "file_path": file_path,
        "uploaded_at": datetime.utcnow()
    }).scalar()
    
    insert_disciplinary_incident_document_history(db, doc_id)
    db.commit()
    return doc_id