from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.incident_cause_analysis_schema import (
    IncidentCauseAnalysisCreate,
    IncidentCauseAnalysisUpdate
)
from app.crud.hse.incident_cause_analysis_crud import (
    create_incident_cause_analysis,
    update_incident_cause_analysis,
    get_all_incident_cause_analysis
)

router = APIRouter(
    prefix="/hse/incident-cause",
    tags=["HSE - Incident Cause Analysis"]
)


# =========================
# CREATE
# =========================
@router.post("/create")
def create_cause(
    data: IncidentCauseAnalysisCreate,
    db: Session = Depends(get_db)
):
    return create_incident_cause_analysis(db, data)


# =========================
# UPDATE
# =========================
@router.put("/update/{cause_id}")
def update_cause(
    cause_id: int,
    data: IncidentCauseAnalysisUpdate,
    db: Session = Depends(get_db)
):
    success = update_incident_cause_analysis(db, cause_id, data)
    if not success:
        raise HTTPException(status_code=400, detail="No fields to update")
    return {"message": "Cause analysis updated successfully"}
    



# =========================
# GET ALL
# =========================
@router.get("/list")
def list_incident_cause_analysis(
    db: Session = Depends(get_db)
):
    return get_all_incident_cause_analysis(db)
