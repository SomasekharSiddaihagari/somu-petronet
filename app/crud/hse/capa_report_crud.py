from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.hse.capa_report_schema import CapaReportCreate, CapaReportUpdate


# -------------------------------------------------
# CREATE CAPA REPORT
# -------------------------------------------------
def create_capa_report(db: Session, data: CapaReportCreate):
    payload = data.dict()
    
    # Remove "string" placeholder values from Swagger
    payload = {k: (None if isinstance(v, str) and v == "string" else v) for k, v in payload.items()}

    # Auto-fetch reference_no from incident_report table if not provided
    ref_no = payload.get("report_no")
    # Check if empty, None, or literal "string" (Swagger default)
    if not ref_no or (isinstance(ref_no, str) and ref_no.strip() in ["", "string"]):
        # Fetch reference number from incident_report table using incident_id
        if payload.get("incident_id"):
            ref_sql = text("""
                SELECT incident_no_during_year FROM incident_report 
                WHERE incident_id = :incident_id
            """)
            ref_result = db.execute(ref_sql, {"incident_id": payload["incident_id"]}).fetchone()
            if ref_result and ref_result[0]:
                payload["report_no"] = ref_result[0]
            else:
                payload["report_no"] = None
        else:
            payload["report_no"] = None

    sql = text("""
        INSERT INTO capa_report (
            incident_id, format_no, revision_date, report_no,
            department, start_date, team_or_capa_study, planned_completion_date, reference_no,
            problem_description,
            correction_action, correction_target_date, correction_actual_date,
            root_cause_analysis,
            corrective_action, corrective_target_date, corrective_actual_date,
            preventive_action, preventive_target_date, preventive_actual_date,
            evidence_file_name, evidence_file_path, evidence_file_type,
            hse_head_id,prepared_by_name, prepared_by_designation,
            approved_by_name, approved_by_designation,
            remarks, status, created_at
        )
        VALUES (
            :incident_id, :format_no, :revision_date, :report_no,
            :department, :start_date, :team_or_capa_study, :planned_completion_date, :reference_no,
            :problem_description,
            :correction_action, :correction_target_date, :correction_actual_date,
            :root_cause_analysis,
            :corrective_action, :corrective_target_date, :corrective_actual_date,
            :preventive_action, :preventive_target_date, :preventive_actual_date,
            :evidence_file_name, :evidence_file_path, :evidence_file_type,
            :hse_head_id,:prepared_by_name, :prepared_by_designation,
            :approved_by_name, :approved_by_designation,
            :remarks, :status, NOW()
        )
        RETURNING capa_report_id
    """)

    result = db.execute(sql, payload)
    capa_report_id = result.scalar()

    insert_capa_report_history(db, capa_report_id)

    db.commit()

    return {
        "capa_report_id": capa_report_id,
        "message": "CAPA report created successfully"
    }


# -------------------------------------------------
# INSERT HISTORY SNAPSHOT
# -------------------------------------------------
def insert_capa_report_history(db: Session, capa_report_id: int):
    history_sql = text("""
        INSERT INTO capa_report_history (
            capa_report_id, incident_id, format_no, revision_date, report_no,
            department, start_date, team_or_capa_study, planned_completion_date, reference_no,
            problem_description,
            correction_action, correction_target_date, correction_actual_date,
            root_cause_analysis,
            corrective_action, corrective_target_date, corrective_actual_date,
            preventive_action, preventive_target_date, preventive_actual_date,
            evidence_file_name, evidence_file_path, evidence_file_type,
            hse_head_id,prepared_by_name, prepared_by_designation,
            approved_by_name, approved_by_designation,
            remarks, status, created_at, updated_at
        )
        SELECT
            capa_report_id, incident_id, format_no, revision_date, report_no,
            department, start_date, team_or_capa_study, planned_completion_date, reference_no,
            problem_description,
            correction_action, correction_target_date, correction_actual_date,
            root_cause_analysis,
            corrective_action, corrective_target_date, corrective_actual_date,
            preventive_action, preventive_target_date, preventive_actual_date,
            evidence_file_name, evidence_file_path, evidence_file_type, 
            hse_head_id,prepared_by_name, prepared_by_designation,
            approved_by_name, approved_by_designation,
            remarks, status, created_at, NOW()
        FROM capa_report
        WHERE capa_report_id = :capa_report_id
    """)

    db.execute(history_sql, {"capa_report_id": capa_report_id})


# -------------------------------------------------
# UPDATE
# -------------------------------------------------
def update_capa_report(db: Session, capa_report_id: int, data: CapaReportUpdate):
    payload = data.dict(exclude_unset=True)

    # Filter out "string" placeholders
    payload = {
        k: (None if isinstance(v, str) and v == "string" else v) 
        for k, v in payload.items()
    }
    # Filter out None values (since we just set "string" to None)
    payload = {k: v for k, v in payload.items() if v is not None}

    if not payload:
        return {"message": "No fields to update"}

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    sql = text(f"""
        UPDATE capa_report
        SET {set_clause}, updated_at = NOW()
        WHERE capa_report_id = :capa_report_id
    """)

    payload["capa_report_id"] = capa_report_id
    db.execute(sql, payload)

    insert_capa_report_history(db, capa_report_id)

    db.commit()
    return {"message": "CAPA report updated successfully"}


# -------------------------------------------------
# GET BY ID
# -------------------------------------------------
def get_capa_report_by_id(db: Session, capa_report_id: int):
    # -------------------------
    # 1️⃣ MASTER
    # -------------------------
    master = db.execute(
        text("""
            SELECT *
            FROM capa_report
            WHERE capa_report_id = :capa_report_id
        """),
        {"capa_report_id": capa_report_id}
    ).mappings().first()

    if not master:
        return None

    # -------------------------
    # 2️⃣ CHILD (document changes)
    # -------------------------
    document_changes = db.execute(
        text("""
            SELECT *
            FROM capa_document_change
            WHERE capa_id = :capa_report_id
            ORDER BY capa_doc_id ASC
        """),
        {"capa_report_id": capa_report_id}
    ).mappings().all()

    # -------------------------
    # 3️⃣ FINAL RESPONSE
    # -------------------------
    return {
        "data": {
            **master,
            "document_changes": document_changes
        }
    }


# -------------------------------------------------
# GET BY INCIDENT ID
# -------------------------------------------------
def get_capa_report_by_incident_id(db: Session, incident_id: int):
    sql = text("""
        SELECT * FROM capa_report WHERE incident_id = :incident_id
    """)
    result = db.execute(sql, {"incident_id": incident_id}).fetchall()
    return [dict(row._mapping) for row in result]


# -------------------------------------------------
# GET ALL
# -------------------------------------------------
def get_all_capa_reports(db: Session):
    sql = text("""
        SELECT * FROM capa_report ORDER BY created_at DESC
    """)
    result = db.execute(sql).fetchall()
    return [dict(row._mapping) for row in result]


# -------------------------------------------------
# DELETE
# -------------------------------------------------
def delete_capa_report(db: Session, capa_report_id: int):
    sql = text("""
        DELETE FROM capa_report WHERE capa_report_id = :capa_report_id
    """)
    db.execute(sql, {"capa_report_id": capa_report_id})
    db.commit()
    return {"message": "CAPA report deleted successfully"}
