from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.hse.incident_impact_assessment_schema import (
    IncidentImpactAssessmentCreate,
    IncidentImpactAssessmentUpdate
)
from app.crud.hse.incident_impact_assessment_crud import (
    create_incident_impact_assessment,
    update_incident_impact_assessment,
    get_all_incident_impact_assessments
)

router = APIRouter(
    prefix="/hse/incident-impact",
    tags=["HSE - Incident Impact Assessment"]
)


# =========================
# CREATE
# =========================
@router.post("/create")
def create_impact(
    data: IncidentImpactAssessmentCreate,
    db: Session = Depends(get_db)
):
    return create_incident_impact_assessment(db, data)


# =========================
# UPDATE
# =========================
@router.put("/update/{impact_id}")
def update_impact(
    impact_id: int,
    data: IncidentImpactAssessmentUpdate,
    db: Session = Depends(get_db)
):
    success = update_incident_impact_assessment(db, impact_id, data)
    if not success:
        raise HTTPException(status_code=400, detail="No fields to update")
    return {"message": "Impact assessment updated successfully"}


# =========================
# GET ALL
# =========================
@router.get("/list")
def list_impact_assessments(
    db: Session = Depends(get_db)
):
    return get_all_incident_impact_assessments(db)
