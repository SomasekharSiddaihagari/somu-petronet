from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, and_, func, text
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date as date_type, datetime
import datetime as dt
from collections import defaultdict

from app.database import get_db
from app.models.permit_management_models.job_safety_analysis_jsa.job_safety_analysis import (
    JobSafetyAnalysis,
)
from app.models.MOC.StationModel import Station

router = APIRouter(prefix="/jsa", tags=["Job Safety Analysis"])


# ─────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────


class JobStepBase(BaseModel):
    row_no: Optional[int] = None
    job_steps: Optional[str] = None
    potential_hazards: Optional[str] = None
    hazard_control_measures: Optional[str] = None
    ppe_required: Optional[str] = None


class JobStepOut(JobStepBase):
    step_id: int
    jsa_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JSABase(BaseModel):
    date: Optional[date_type] = None
    jsa_no: Optional[str] = None
    job_type: Optional[str] = None
    work_permit_ref_no: Optional[str] = None
    job_executed_by: Optional[str] = None
    job_description: Optional[str] = None
    job_location: Optional[str] = None
    additional_comments: Optional[str] = None
    jsa_prepared_by: Optional[str] = None
    jsa_reviewed_approved_by: Optional[str] = None
    status: Optional[str] = "draft"
    station_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class JSACreate(JSABase):
    pass


class JSAUpdate(JSABase):
    pass


class JSAOut(JSABase):
    jsa_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    job_steps: List[JobStepOut] = []

    class Config:
        from_attributes = True


class JSAListOut(JSABase):
    jsa_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# HELPER: GET ROLE USERS DIRECTORY
# ─────────────────────────────────────────────
def get_role_users_directory(db: Session) -> dict:
    """Fetches users mapped to Permit Management (Submenu 4) grouped by role."""
    users_data = (
        db.execute(
            text(
                """
            SELECT rp.user_id, r.role_name
            FROM role_permissions rp
            JOIN roles r ON r.role_id = rp.role_id
            WHERE rp.submenu_id = 4
              AND rp.user_id IS NOT NULL
        """
            )
        )
        .mappings()
        .all()
    )

    users_by_role = defaultdict(list)
    for u in users_data:
        users_by_role[u["role_name"]].append(u["user_id"])

    return {
        "Engineer": users_by_role.get("Engineer", []),
        "EAP": users_by_role.get("EAP", []),
        "SIC": users_by_role.get("SIC", []),
        "ASIC": users_by_role.get("ASIC", []),
        "Admin": users_by_role.get("Admin", []),
    }


# ─────────────────────────────────────────────
# HELPER: FETCH WAH PERMITS WITH ALL CHILD DATA
# ─────────────────────────────────────────────
def get_wah_permits_for_jsa(db: Session, jsa_id: int) -> list:
    # 1. Get all WAH permits for this JSA
    permits = (
        db.execute(
            text(
                """
            SELECT *
            FROM work_at_height_permit
            WHERE jsa_id = :jsa_id
            ORDER BY created_at DESC
        """
            ),
            {"jsa_id": jsa_id},
        )
        .mappings()
        .all()
    )

    # 2. Get role users directory
    role_users = get_role_users_directory(db)

    result = []

    for permit in permits:
        whp_id = permit["whp_id"]
        permit_dict = dict(permit)

        # 3. Add same role_users logic as requested
        permit_dict["role_users"] = role_users

        toolbox_talks = (
            db.execute(
                text(
                    """
                SELECT * FROM work_at_height_toolbox_talk
                WHERE work_at_height_permit_id = :whp_id
                ORDER BY created_at DESC
            """
                ),
                {"whp_id": whp_id},
            )
            .mappings()
            .all()
        )

        talks_with_participants = []
        for talk in toolbox_talks:
            talk_dict = dict(talk)
            participants = (
                db.execute(
                    text(
                        """
                    SELECT * FROM work_at_height_toolbox_talk_participant
                    WHERE toolbox_talk_id = :talk_id
                    ORDER BY created_at DESC
                """
                    ),
                    {"talk_id": talk["whtt_id"]},
                )
                .mappings()
                .all()
            )
            talk_dict["participants"] = [dict(p) for p in participants]
            talks_with_participants.append(talk_dict)

        permit_dict["toolbox_talks"] = talks_with_participants

        isolation = (
            db.execute(
                text(
                    """
                SELECT * FROM work_at_height_electrical_isolation_permit
                WHERE whp_id = :whp_id
                ORDER BY created_at DESC
            """
                ),
                {"whp_id": whp_id},
            )
            .mappings()
            .all()
        )
        permit_dict["isolation_permits"] = [dict(i) for i in isolation]

        energization = (
            db.execute(
                text(
                    """
                SELECT * FROM work_at_height_electrical_energization_permit
                WHERE whp_id = :whp_id
                ORDER BY created_at DESC
            """
                ),
                {"whp_id": whp_id},
            )
            .mappings()
            .all()
        )
        permit_dict["energization_permits"] = [dict(e) for e in energization]

        result.append(permit_dict)

    return result


# ─────────────────────────────────────────────
# HELPER: BUILD FULL JSA RESPONSE
# ─────────────────────────────────────────────
def build_jsa_response(db: Session, jsa: JobSafetyAnalysis) -> dict:
    return {
        "jsa_id": jsa.jsa_id,
        "date": jsa.date,
        "jsa_no": jsa.jsa_no,
        "job_type": jsa.job_type,
        "work_permit_ref_no": jsa.work_permit_ref_no,
        "job_executed_by": jsa.job_executed_by,
        "job_description": jsa.job_description,
        "job_location": jsa.job_location,
        "additional_comments": jsa.additional_comments,
        "jsa_prepared_by": jsa.jsa_prepared_by,
        "jsa_reviewed_approved_by": jsa.jsa_reviewed_approved_by,
        "status": jsa.status,
        "station_id": jsa.station_id,
        "created_by": jsa.created_by,
        "updated_by": jsa.updated_by,
        "created_at": jsa.created_at,
        "updated_at": jsa.updated_at,
        "job_steps": [
            {
                "step_id": s.step_id,
                "jsa_id": s.jsa_id,
                "row_no": s.row_no,
                "job_steps": s.job_steps,
                "potential_hazards": s.potential_hazards,
                "hazard_control_measures": s.hazard_control_measures,
                "ppe_required": s.ppe_required,
                "created_at": s.created_at,
                "updated_at": s.updated_at,
            }
            for s in jsa.job_steps
        ],
        "work_at_height_permits": get_wah_permits_for_jsa(db, jsa.jsa_id),
        "composite_work_permits": get_cwp_permits_for_jsa(db, jsa.jsa_id),
    }


# ─────────────────────────────────────────────
# HELPER: FETCH CWP PERMITS WITH ALL CHILD DATA
# ────────────────────────────────────────────────
def get_cwp_permits_for_jsa(db: Session, jsa_id: int) -> list:
    # 1. Get all CWP permits for this JSA
    permits = (
        db.execute(
            text(
                """
            SELECT *
            FROM composite_work_permit
            WHERE jsa_id = :jsa_id
            ORDER BY created_at DESC
        """
            ),
            {"jsa_id": jsa_id},
        )
        .mappings()
        .all()
    )

    # 2. Get same role users logic as WAH
    role_users = get_role_users_directory(db)

    result = []

    for permit in permits:
        cwp_id = permit["cwp_id"]
        # Convert dictionary-like object to real dict for modification
        permit_dict = dict(permit)

        # 3. Add same role users logic as WAH
        permit_dict["role_users"] = role_users

        # 4. Toolbox talks
        toolbox_talks = (
            db.execute(
                text(
                    """
                SELECT * FROM composite_toolbox_talk
                WHERE composite_work_permit_id = :cwp_id
                ORDER BY created_at DESC
            """
                ),
                {"cwp_id": cwp_id},
            )
            .mappings()
            .all()
        )

        talks_with_participants = []
        for talk in toolbox_talks:
            talk_dict = dict(talk)

            # 5. Participants for each toolbox talk
            participants = (
                db.execute(
                    text(
                        """
                    SELECT * FROM composite_toolbox_talk_participant
                    WHERE toolbox_talk_id = :talk_id
                    ORDER BY created_at DESC
                """
                    ),
                    {"talk_id": talk["ctt_id"]},
                )
                .mappings()
                .all()
            )

            talk_dict["participants"] = [dict(p) for p in participants]
            talks_with_participants.append(talk_dict)

        permit_dict["toolbox_talks"] = talks_with_participants

        # 6. Isolation permits
        isolation = (
            db.execute(
                text(
                    """
                SELECT * FROM composite_electrical_isolation_permit
                WHERE composite_work_permit_id = :cwp_id
                ORDER BY created_at DESC
            """
                ),
                {"cwp_id": cwp_id},
            )
            .mappings()
            .all()
        )
        permit_dict["isolation_permits"] = [dict(i) for i in isolation]

        # 7. Energization permits
        energization = (
            db.execute(
                text(
                    """
                SELECT * FROM composite_electrical_energization_permit
                WHERE composite_work_permit_id = :cwp_id
                ORDER BY created_at DESC
            """
                ),
                {"cwp_id": cwp_id},
            )
            .mappings()
            .all()
        )
        permit_dict["energization_permits"] = [dict(e) for e in energization]

        result.append(permit_dict)

    return result


# ─────────────────────────────────────────────
# HELPER: AUTO GENERATE JSA NUMBER
# ─────────────────────────────────────────────
def generate_jsa_no(db: Session, station_id: int) -> str:
    station = db.get(Station, station_id)
    station_code = station.station_code if station else "GEN"

    today = dt.date.today()
    if today.month >= 4:
        fy_start = today.year
        fy_end = today.year + 1
    else:
        fy_start = today.year - 1
        fy_end = today.year

    financial_year = f"{fy_start}-{str(fy_end)[-2:]}"
    fy_start_date = dt.date(fy_start, 4, 1)
    fy_end_date = dt.date(fy_end, 3, 31)

    count = (
        db.execute(
            select(func.count(JobSafetyAnalysis.jsa_id)).where(
                and_(
                    JobSafetyAnalysis.station_id == station_id,
                    JobSafetyAnalysis.date >= fy_start_date,
                    JobSafetyAnalysis.date <= fy_end_date,
                )
            )
        ).scalar()
        or 0
    )

    seq_no = str(count + 1).zfill(3)
    return f"JSA/{station_code}/{financial_year}/{seq_no}"


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────


@router.post("", status_code=status.HTTP_201_CREATED)
def create_jsa(payload: JSACreate, db: Session = Depends(get_db)):
    """Create a new Job Safety Analysis with auto-generated JSA number."""
    data = payload.model_dump()

    if data.get("station_id"):
        data["jsa_no"] = generate_jsa_no(db, data["station_id"])

    if not data.get("date"):
        data["date"] = dt.date.today()

    jsa = JobSafetyAnalysis(**data)
    db.add(jsa)
    db.commit()
    db.refresh(jsa)
    return build_jsa_response(db, jsa)


@router.get("")
def get_all_jsa(db: Session = Depends(get_db)):
    """Get all JSAs with steps and linked Work at Height permits."""
    result = (
        db.execute(
            select(JobSafetyAnalysis).options(selectinload(JobSafetyAnalysis.job_steps))
        )
        .scalars()
        .all()
    )
    return [build_jsa_response(db, jsa) for jsa in result]


# ── MUST come before /{jsa_id} ────────────────────────────────
@router.get("/generate-jsa-no/{station_id}")
def get_next_jsa_no(station_id: int, db: Session = Depends(get_db)):
    """Get the next auto-generated JSA number for a station (preview before submit)."""
    return {"jsa_no": generate_jsa_no(db, station_id)}


# ✅ FETCH JSA BY USER ─────────────────────────
@router.get("/user/{user_id}")
def get_jsa_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get all JSAs created by a specific user with steps and permits."""
    result = (
        db.execute(
            select(JobSafetyAnalysis)
            .options(selectinload(JobSafetyAnalysis.job_steps))
            .where(JobSafetyAnalysis.created_by == user_id)
            .order_by(JobSafetyAnalysis.created_at.desc())
        )
        .scalars()
        .all()
    )

    if not result:
        return []

    return [build_jsa_response(db, jsa) for jsa in result]


@router.get("/{jsa_id}")
def get_jsa(jsa_id: int, db: Session = Depends(get_db)):
    """Get a single JSA with all steps and linked permits."""
    jsa = (
        db.execute(
            select(JobSafetyAnalysis)
            .options(selectinload(JobSafetyAnalysis.job_steps))
            .where(JobSafetyAnalysis.jsa_id == jsa_id)
        )
        .scalars()
        .first()
    )
    if not jsa:
        raise HTTPException(status_code=404, detail=f"JSA {jsa_id} not found")
    return build_jsa_response(db, jsa)


@router.put("/{jsa_id}")
def update_jsa(jsa_id: int, payload: JSAUpdate, db: Session = Depends(get_db)):
    """Full update of a JSA."""
    jsa = db.get(JobSafetyAnalysis, jsa_id)
    if not jsa:
        raise HTTPException(status_code=404, detail=f"JSA {jsa_id} not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(jsa, field, value)
    db.commit()
    db.refresh(jsa)
    return build_jsa_response(db, jsa)


@router.delete("/{jsa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jsa(jsa_id: int, db: Session = Depends(get_db)):
    """Delete a JSA and all its steps (cascade)."""
    jsa = db.get(JobSafetyAnalysis, jsa_id)
    if not jsa:
        raise HTTPException(status_code=404, detail=f"JSA {jsa_id} not found")
    db.delete(jsa)
    db.commit()
