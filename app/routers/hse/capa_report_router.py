from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
import os
import shutil
from fastapi import UploadFile, File, Form

from app.crud.hse.hse_major_notification import notify_capa_approved, notify_capa_changes_requested, notify_capa_closed, notify_capa_form_filled
from app.database import get_db
from app.models.hse.capa_report import CapaReport
from app.schemas.hse.capa_report_schema import (
    CapaReportCreate,
    CapaReportUpdate
)
from app.crud.hse.capa_report_crud import (
    create_capa_report,
    update_capa_report,
    get_capa_report_by_id,
    get_capa_report_by_incident_id,
    get_all_capa_reports,
    delete_capa_report
)

router = APIRouter(
    prefix="/api/hse/capa-report",
    tags=["HSE CAPA Report"]
)

UPLOAD_DIR = "files/hse/incident_prevention"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------- POST - CREATE ----------------------
# @router.post("/create")
# def create_report(
#     data: CapaReportCreate,
#     db: Session = Depends(get_db)
# ):
#     result = create_capa_report(db, data)
#     return {
#         "status": "success",
#         "capa_report_id": result["capa_report_id"],
#         "message": result["message"]
#     }

@router.get("/all")
def get_all_reports(db: Session = Depends(get_db)):
    result = get_all_capa_reports(db)
    return {
        "status": "success",
        "data": result
    }

@router.post("/create")
async def create_report(
    incident_id: int = Form(...),

    format_no: str = Form(None),
    revision_date: str = Form(None),
    report_no: str = Form(None),

    department: str = Form(None),
    start_date: str = Form(None),
    team_or_capa_study: str = Form(None),
    planned_completion_date: str = Form(None),
    reference_no: str = Form(None),
    hse_head_id: int = Form(None),

    problem_description: str = Form(None),

    correction_action: str = Form(None),
    correction_target_date: str = Form(None),
    correction_actual_date: str = Form(None),

    root_cause_analysis: str = Form(None),

    corrective_action: str = Form(None),
    corrective_target_date: str = Form(None),
    corrective_actual_date: str = Form(None),

    preventive_action: str = Form(None),
    preventive_target_date: str = Form(None),
    preventive_actual_date: str = Form(None),

    prepared_by_name: str = Form(None),
    prepared_by_designation: str = Form(None),
    approved_by_name: str = Form(None),
    approved_by_designation: str = Form(None),

    remarks: str = Form(None),
    status: str = Form(None),

    evidence_file: UploadFile = File(None),

    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):

    file_name = None
    file_path = None
    file_type = None

    if evidence_file:
        file_name = evidence_file.filename
        file_type = evidence_file.content_type

        save_path = os.path.join(UPLOAD_DIR, file_name)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(evidence_file.file, buffer)

        file_path = save_path

    payload = {
        "incident_id": incident_id,
        "format_no": format_no,
        "revision_date": revision_date,
        "report_no": report_no,
        "department": department,
        "start_date": start_date,
        "team_or_capa_study": team_or_capa_study,
        "planned_completion_date": planned_completion_date,
        "reference_no": reference_no,
        "hse_head_id": hse_head_id,
        "problem_description": problem_description,
        "correction_action": correction_action,
        "correction_target_date": correction_target_date,
        "correction_actual_date": correction_actual_date,
        "root_cause_analysis": root_cause_analysis,
        "corrective_action": corrective_action,
        "corrective_target_date": corrective_target_date,
        "corrective_actual_date": corrective_actual_date,
        "preventive_action": preventive_action,
        "preventive_target_date": preventive_target_date,
        "preventive_actual_date": preventive_actual_date,
        "prepared_by_name": prepared_by_name,
        "prepared_by_designation": prepared_by_designation,
        "approved_by_name": approved_by_name,
        "approved_by_designation": approved_by_designation,
        "remarks": remarks,
        "status": status,
        "evidence_file_name": file_name,
        "evidence_file_path": file_path,
        "evidence_file_type": file_type,
    }

    data = CapaReportCreate(**payload)
    result = create_capa_report(db, data)

    return {
        "status": "success",
        "capa_report_id": result["capa_report_id"],
        "message": result["message"]
    }

# ---------------------- GET - BY ID ----------------------
@router.get("/{capa_report_id}")
def get_report(
    capa_report_id: int,
    db: Session = Depends(get_db)
):
    result = get_capa_report_by_id(db, capa_report_id)
    if not result:
        raise HTTPException(status_code=404, detail="CAPA report not found")
    return {
        "status": "success",
        "data": result
    }




# ---------------------- GET - ALL ----------------------
@router.get("/all")
def get_all_reports(db: Session = Depends(get_db)):
    result = get_all_capa_reports(db)
    return {
        "status": "success",
        "data": result
    }


# ---------------------- PUT - UPDATE ----------------------
# @router.put("/update/{capa_report_id}")
# def update_report(
#     capa_report_id: int,
#     data: CapaReportUpdate,
#     db: Session = Depends(get_db)
# ):
#     existing = get_capa_report_by_id(db, capa_report_id)
#     if not existing:
#         raise HTTPException(status_code=404, detail="CAPA report not found")

#     result = update_capa_report(db, capa_report_id, data)
#     return {
#         "status": "success",
#         "message": result["message"]
#     }
@router.put("/update/{capa_report_id}")
async def update_report(
    capa_report_id: int,

    # 👇 CHANGE: Using Form instead of Pydantic body for Swagger file upload
    format_no: str = Form(None),
    revision_date: str = Form(None),
    report_no: str = Form(None),
    department: str = Form(None),
    start_date: str = Form(None),
    team_or_capa_study: str = Form(None),
    planned_completion_date: str = Form(None),
    reference_no: str = Form(None),
    hse_head_id: int = Form(None),

    problem_description: str = Form(None),
    correction_action: str = Form(None),
    correction_target_date: str = Form(None),
    correction_actual_date: str = Form(None),

    root_cause_analysis: str = Form(None),

    corrective_action: str = Form(None),
    corrective_target_date: str = Form(None),
    corrective_actual_date: str = Form(None),

    preventive_action: str = Form(None),
    preventive_target_date: str = Form(None),
    preventive_actual_date: str = Form(None),

    prepared_by_name: str = Form(None),
    prepared_by_designation: str = Form(None),
    approved_by_name: str = Form(None),
    approved_by_designation: str = Form(None),

    remarks: str = Form(None),
    status: str = Form(None),

    # 👇 NEW FILE FIELD
    evidence_file: UploadFile = File(None),

    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):

    existing = get_capa_report_by_id(db, capa_report_id)

    if not existing:
        raise HTTPException(status_code=404, detail="CAPA report not found")

    old_status = existing.get("status") if isinstance(existing, dict) else existing.status

    # =====================================================
    # FILE HANDLING (NEWLY ADDED — DOES NOT BREAK LOGIC)
    # =====================================================
    file_name = None
    file_path = None
    file_type = None

    if evidence_file:
        file_name = evidence_file.filename
        file_type = evidence_file.content_type

        save_path = os.path.join(UPLOAD_DIR, file_name)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(evidence_file.file, buffer)

        file_path = save_path

    # =====================================================
    # PREPARE PAYLOAD DICT
    # =====================================================
    payload = {
        "format_no": format_no,
        "revision_date": revision_date,
        "report_no": report_no,
        "department": department,
        "start_date": start_date,
        "team_or_capa_study": team_or_capa_study,
        "planned_completion_date": planned_completion_date,
        "reference_no": reference_no,
        "hse_head_id": hse_head_id,
        "problem_description": problem_description,
        "correction_action": correction_action,
        "correction_target_date": correction_target_date,
        "correction_actual_date": correction_actual_date,
        "root_cause_analysis": root_cause_analysis,
        "corrective_action": corrective_action,
        "corrective_target_date": corrective_target_date,
        "corrective_actual_date": corrective_actual_date,
        "preventive_action": preventive_action,
        "preventive_target_date": preventive_target_date,
        "preventive_actual_date": preventive_actual_date,
        "prepared_by_name": prepared_by_name,
        "prepared_by_designation": prepared_by_designation,
        "approved_by_name": approved_by_name,
        "approved_by_designation": approved_by_designation,
        "remarks": remarks,
        "status": status,
    }

    # 👇 If file uploaded, include it
    if file_name:
        payload["evidence_file_name"] = file_name
        payload["evidence_file_path"] = file_path
        payload["evidence_file_type"] = file_type

    # Remove None values (same as your CRUD logic expectation)
    payload = {k: v for k, v in payload.items() if v is not None}

    # Convert to schema object
    data = CapaReportUpdate(**payload)

    # =====================================================
    # CALL EXISTING CRUD (UNCHANGED)
    # =====================================================
    result = update_capa_report(db, capa_report_id, data)

    capa_obj = db.query(CapaReport).filter(
        CapaReport.capa_report_id == capa_report_id
    ).first()

    new_status = capa_obj.status if capa_obj else None

    print("OLD STATUS:", old_status)
    print("NEW STATUS:", new_status)

    # =====================================
    # CAPA APPROVED
    # =====================================
    if old_status != new_status and new_status == "CAPA-Approved":

        await notify_capa_approved(
            db=db,
            capa=capa_obj,
            background_tasks=background_tasks
        )

    # =====================================
    # CAPA CHANGES REQUESTED
    # =====================================
    if old_status != new_status and new_status == "CAPA-Changes-Requested":

        await notify_capa_changes_requested(
            db=db,
            capa=capa_obj,
            background_tasks=background_tasks
        )

    # =====================================
    # CAPA CLOSED
    # =====================================
    if old_status != new_status and new_status == "Closed":

        await notify_capa_closed(
            db=db,
            capa=capa_obj,
            background_tasks=background_tasks
        )

    return {
        "status": "success",
        "message": result["message"]
    }

# ---------------------- DELETE ----------------------
@router.delete("/delete/{capa_report_id}")
def delete_report(
    capa_report_id: int,
    db: Session = Depends(get_db)
):
    existing = get_capa_report_by_id(db, capa_report_id)
    if not existing:
        raise HTTPException(status_code=404, detail="CAPA report not found")

    result = delete_capa_report(db, capa_report_id)
    return {
        "status": "success",
        "message": result["message"]
    }
