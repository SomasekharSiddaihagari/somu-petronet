from datetime import date
from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.crud.hse.hse_major_notification import handle_incident_notification
from app.crud.hse.hse_notification_crud import handle_prevention_notification
from app.crud.hse.incident_prevention_crud import get_incident_dashboard_counts
from app.crud.hse.incident_report_crud import get_investigation_team_with_user
from app.database import get_db
from app.crud.hse.incident_prevention_crud import (
    create_incident_prevention,
    update_incident_prevention,
    get_all_incident_prevention,
    get_incident_dashboard_by_user
)
from app.models.UserModel import User
from sqlalchemy import text

router = APIRouter(
    prefix="/hse/incident-prevention",
    tags=["HSE - Incident Prevention"]
)


# =========================
# HELPERS
# =========================

def clean_file(f) -> UploadFile | None:
    """
    Discard anything that is not a real uploaded file.
    Swagger sends empty string "" when no file is chosen — this catches that.
    """
    if f is None:
        return None
    if isinstance(f, str):
        return None
    if not getattr(f, "filename", None):
        return None
    return f


def clean_files(files) -> list[UploadFile] | None:
    """
    Filter a list and discard empty-string / no-filename entries.
    Returns None when nothing real remains.
    """
    if not files:
        return None
    cleaned = [
        f for f in files
        if not isinstance(f, str) and getattr(f, "filename", None)
    ]
    return cleaned if cleaned else None


# =========================
# CREATE
# =========================
@router.post("/create")
async def create_prevention(
    incident_id: int = Form(...),

    # ================= COMMON =================
    was_incident_avoidable: bool | None = Form(None),
    avoid_better_supervision: bool | None = Form(None),
    avoid_imparting_training: bool | None = Form(None),
    avoid_work_permit_system: bool | None = Form(None),
    avoid_better_equipment: bool | None = Form(None),
    avoid_maintenance_procedure: bool | None = Form(None),
    avoid_other_information: bool | None = Form(None),
    avoid_operating_procedure: bool | None = Form(None),
    avoid_proper_planning_time: bool | None = Form(None),
    avoid_ppe: bool | None = Form(None),
    avoid_management_control: bool | None = Form(None),
    avoid_inspection_testing: bool | None = Form(None),

    # ================= MINOR =================
    minor_prepared_by_name: str | None = Form(None),
    minor_prepared_by_designation: str | None = Form(None),
    minor_recommendations: str | None = Form(None),
    minor_engineer_corrective_actions_taken: str | None = Form(None),
    minor_prepared_by_corrective_action: str | None = Form(None),
    minor_corrective_actions: str | None = Form(None),
    minor_prepared_by_remarks: str | None = Form(None),
    minor_preventive_action_taken: str | None = Form(None),

    minor_allotted_engineer_id: int | None = Form(None),
    minor_allotted_responsible_id: int | None = Form(None),
    minor_responsible_engineer_name: str | None = Form(None),
    minor_responsible_engineer_designation: str | None = Form(None),

    minor_approved_by_name: str | None = Form(None),
    minor_approved_by_station_incharge: str | None = Form(None),
    minor_approved_by_remarks: str | None = Form(None),

    minor_sic_name: str | None = Form(None),
    minor_sic_updated_date: date | None = Form(None),
    minor_alloted_engineer_name: str | None = Form(None),
    minor_alloted_eng_updated_date: date | None = Form(None),
    minor_final_approve_name: str | None = Form(None),
    minor_final_approved_date: date | None = Form(None),

    # ================= MAJOR =================
    major_prepared_by_name: str | None = Form(None),
    major_prepared_by_designation: str | None = Form(None),
    major_immediate_actions_taken: str | None = Form(None),
    major_recommendations: str | None = Form(None),
    major_prepared_by_remarks_si: str | None = Form(None),
    major_hse_head_remarks: str | None = Form(None),

    # ================= MAJOR WORKFLOW =================
    major_team_leader_by: str | None = Form(None),
    major_team_leader_date: date | None = Form(None),
    major_team_acknowledged_by: str | None = Form(None),
    major_team_acknowledged_date: date | None = Form(None),
    major_report_filled_by: str | None = Form(None),
    major_report_filled_date: date | None = Form(None),
    major_investigation_ack_by: str | None = Form(None),
    major_investigation_ack_date: date | None = Form(None),
    major_safety_officer_by: str | None = Form(None),
    major_safety_officer_date: date | None = Form(None),
    major_md_review_by: str | None = Form(None),
    major_md_review_date: date | None = Form(None),
    major_hse_review_by: str | None = Form(None),
    major_hse_review_date: date | None = Form(None),
    major_capa_filled_by: str | None = Form(None),
    major_capa_filled_date: date | None = Form(None),
    major_hse_capa_review_by: str | None = Form(None),
    major_hse_capa_review_date: date | None = Form(None),
    major_closure_by: str | None = Form(None),
    major_closure_date: date | None = Form(None),

    # ===================================================
    # ALL FILE FIELDS — all 100% optional
    # FastAPI / Swagger may send "" (empty string) when
    # no file is chosen; clean_file / clean_files handles that.
    # ===================================================
    minor_evidence_file: Optional[UploadFile] = File(default=None),
    major_evidence_file: Optional[UploadFile] = File(default=None),
    minor_evidence_files_multi: Optional[List[UploadFile]] = File(default=None),
    major_evidence_files_multi: Optional[List[UploadFile]] = File(default=None),

    # ================= SYSTEM =================
    status: str | None = Form(None),
    created_by: int | None = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    payload = locals().copy()

    for key in [
        "db", "background_tasks",
        "minor_evidence_file", "major_evidence_file",
        "minor_evidence_files_multi", "major_evidence_files_multi",
    ]:
        payload.pop(key, None)

    # ✅ Sanitise file inputs — empty strings become None
    minor_file  = clean_file(minor_evidence_file)
    major_file  = clean_file(major_evidence_file)
    minor_multi = clean_files(minor_evidence_files_multi)
    major_multi = clean_files(major_evidence_files_multi)

    created_record = create_incident_prevention(
        db,
        payload,
        minor_file,
        major_file,
        minor_files_multi=minor_multi,
        major_files_multi=major_multi,
    )

    if not payload.get("status"):
        payload["status"] = "Draft"

    if created_record:
        await handle_prevention_notification(
            db=db,
            prevention=created_record,
            background_tasks=background_tasks
        )
        await handle_incident_notification(
            db=db,
            prevention=created_record,
            acted_by_username="system",
            background_tasks=background_tasks
        )

    return created_record


# =========================
# UPDATE
# =========================
@router.put("/update/{ip_id}")
async def update_prevention(
    ip_id: int,
    incident_id: int = Form(...),

    # ================= COMMON =================
    was_incident_avoidable: bool | None = Form(None),
    avoid_better_supervision: bool | None = Form(None),
    avoid_imparting_training: bool | None = Form(None),
    avoid_work_permit_system: bool | None = Form(None),
    avoid_better_equipment: bool | None = Form(None),
    avoid_maintenance_procedure: bool | None = Form(None),
    avoid_other_information: bool | None = Form(None),
    avoid_operating_procedure: bool | None = Form(None),
    avoid_proper_planning_time: bool | None = Form(None),
    avoid_ppe: bool | None = Form(None),
    avoid_management_control: bool | None = Form(None),
    avoid_inspection_testing: bool | None = Form(None),

    # ================= MINOR =================
    minor_prepared_by_name: str | None = Form(None),
    minor_prepared_by_designation: str | None = Form(None),
    minor_recommendations: str | None = Form(None),
    minor_engineer_corrective_actions_taken: str | None = Form(None),
    minor_prepared_by_corrective_action: str | None = Form(None),
    minor_corrective_actions: str | None = Form(None),
    minor_prepared_by_remarks: str | None = Form(None),
    minor_preventive_action_taken: str | None = Form(None),

    minor_allotted_engineer_id: int | None = Form(None),
    minor_allotted_responsible_id: int | None = Form(None),
    minor_responsible_engineer_name: str | None = Form(None),
    minor_responsible_engineer_designation: str | None = Form(None),

    minor_approved_by_name: str | None = Form(None),
    minor_approved_by_station_incharge: str | None = Form(None),
    minor_approved_by_remarks: str | None = Form(None),

    minor_sic_name: str | None = Form(None),
    minor_sic_updated_date: date | None = Form(None),
    minor_alloted_engineer_name: str | None = Form(None),
    minor_alloted_eng_updated_date: date | None = Form(None),
    minor_final_approve_name: str | None = Form(None),
    minor_final_approved_date: date | None = Form(None),

    # ================= MAJOR =================
    major_prepared_by_name: str | None = Form(None),
    major_prepared_by_designation: str | None = Form(None),
    major_immediate_actions_taken: str | None = Form(None),
    major_recommendations: str | None = Form(None),
    major_prepared_by_remarks_si: str | None = Form(None),
    major_hse_head_remarks: str | None = Form(None),

    # ================= MAJOR WORKFLOW =================
    major_team_leader_by: str | None = Form(None),
    major_team_leader_date: date | None = Form(None),
    major_team_acknowledged_by: str | None = Form(None),
    major_team_acknowledged_date: date | None = Form(None),
    major_report_filled_by: str | None = Form(None),
    major_report_filled_date: date | None = Form(None),
    major_investigation_ack_by: str | None = Form(None),
    major_investigation_ack_date: date | None = Form(None),
    major_safety_officer_by: str | None = Form(None),
    major_safety_officer_date: date | None = Form(None),
    major_md_review_by: str | None = Form(None),
    major_md_review_date: date | None = Form(None),
    major_hse_review_by: str | None = Form(None),
    major_hse_review_date: date | None = Form(None),
    major_capa_filled_by: str | None = Form(None),
    major_capa_filled_date: date | None = Form(None),
    major_hse_capa_review_by: str | None = Form(None),
    major_hse_capa_review_date: date | None = Form(None),
    major_closure_by: str | None = Form(None),
    major_closure_date: date | None = Form(None),

    # ===================================================
    # ALL FILE FIELDS — all 100% optional
    # ===================================================
    minor_evidence_file: Optional[UploadFile] = File(default=None),
    major_evidence_file: Optional[UploadFile] = File(default=None),
    minor_evidence_files_multi: Optional[List[UploadFile]] = File(default=None),
    major_evidence_files_multi: Optional[List[UploadFile]] = File(default=None),

    # ================= SYSTEM =================
    status: str | None = Form(None),
    updated_by: int | None = Form(None),

    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    payload = locals().copy()

    for key in [
        "db", "ip_id", "background_tasks",
        "minor_evidence_file", "major_evidence_file",
        "minor_evidence_files_multi", "major_evidence_files_multi",
    ]:
        payload.pop(key, None)

    # ✅ Sanitise file inputs — empty strings become None
    minor_file  = clean_file(minor_evidence_file)
    major_file  = clean_file(major_evidence_file)
    minor_multi = clean_files(minor_evidence_files_multi)
    major_multi = clean_files(major_evidence_files_multi)

    # Fetch old status before update
    old_row = db.execute(
        text("SELECT status FROM incident_prevention WHERE ip_id = :id"),
        {"id": ip_id}
    ).fetchone()
    old_status = old_row[0] if old_row else None

    prevention = update_incident_prevention(
        db,
        ip_id,
        payload,
        minor_file,
        major_file,
        minor_files_multi=minor_multi,
        major_files_multi=major_multi,
    )

    acted_by_username = "system"
    if updated_by:
        user = db.query(User).filter(User.user_id == updated_by).first()
        if user:
            acted_by_username = user.username

    new_status = prevention.get("status") if isinstance(prevention, dict) else prevention.status

    print("OLD STATUS:", old_status)
    print("NEW STATUS:", new_status)

    if prevention:
        await handle_prevention_notification(
            db=db,
            prevention=prevention,
            background_tasks=background_tasks
        )
        if old_status != new_status:
            await handle_incident_notification(
                db=db,
                prevention=prevention,
                acted_by_username=acted_by_username,
                background_tasks=background_tasks
            )

    return prevention


# =========================
# LIST
# =========================
@router.get("/list")
def list_incident_prevention(db: Session = Depends(get_db)):
    return get_all_incident_prevention(db)


# =========================
# DASHBOARD CARDS
# =========================
@router.get("/dashboard/cards/all")
def dashboard_cards(db: Session = Depends(get_db)):
    return get_incident_dashboard_counts(db)

@router.get("/dashboard/cards/user-id")
def dashboard(
    user_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    station_id: int | None = None,
    days: int | None = None,
    db: Session = Depends(get_db)
):
    return get_incident_dashboard_counts(db, user_id, from_date, to_date, station_id, days)


@router.get("/investigation-team-users")
def fetch_investigation_team_users(db: Session = Depends(get_db)):
    return get_investigation_team_with_user(db)


@router.get("/dashboard/by-user/{user_id}")
def dashboard_by_user(
    user_id: int,
    filter_station_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    days: int | None = None,
    db: Session = Depends(get_db)
):
    return get_incident_dashboard_by_user(db, user_id, filter_station_id, from_date, to_date, days)