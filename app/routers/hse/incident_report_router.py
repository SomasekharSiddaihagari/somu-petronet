from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from app.database import get_db

from app.schemas.hse.incident_report_schema import (
    IncidentReportCreate,
    IncidentReportUpdate
)

from app.crud.hse.incident_report_crud import (
    create_incident_report,
    update_incident_report,
    get_all_incident_reports  
    , get_incidents_by_user,
    get_incident_by_id
)

router = APIRouter(
    prefix="/hse/incident-report",
    tags=["HSE - Incident Report"]
)



# =========================
# CREATE INCIDENT REPORT
# =========================
@router.post("/create")
def create_incident(
    data: IncidentReportCreate,
    db: Session = Depends(get_db)
):
    return create_incident_report(db, data)


# =========================
# UPDATE INCIDENT REPORT
# =========================
@router.put("/update/{incident_id}")
def update_incident(
    incident_id: int,
    data: IncidentReportUpdate,
    db: Session = Depends(get_db)
):
    success = update_incident_report(db, incident_id, data)
    if not success:
        raise HTTPException(status_code=400, detail="No fields to update")
    return {"message": "Incident report updated successfully"}



# =========================
# GET ALL INCIDENT REPORTS
# =========================
@router.get("/list")
def list_incidents(
    db: Session = Depends(get_db)
):
    return get_all_incident_reports(db)

@router.get("/incidents/by-user")
def fetch_incidents_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    data = get_incidents_by_user(db, user_id)

    return {
        "success": True,
        "count": len(data),
        "data": data
    }


@router.get("/{incident_id}")
def fetch_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    return get_incident_by_id(db, incident_id)