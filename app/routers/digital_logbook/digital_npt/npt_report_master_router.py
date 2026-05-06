from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_npt.npt_report_master_schema import (
    NPTReportMasterResponse,
    NPTReportMasterCreate,
    NPTReportMasterUpdate,
)
from app.crud.digital_logbook.digital_npt.npt_report_master_crud import (
    get_npt_by_created_date, 
    get_npt_master_by_id,
    create_npt_master,
    update_npt_master,
    delete_npt_master,
)

router = APIRouter(
    prefix="/npt-report-master",
    tags=["NPT Report Master"],
    dependencies=[Depends(validate_token)]
)




@router.post("", status_code=status.HTTP_201_CREATED)
def create_master_logbook(
    payload: NPTReportMasterCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Create a new NPT Report Master manually and return its ID."""
    npt_id = create_npt_master(db, payload, current_user.get("user_id"))
    return {"message": "NPT Master Logbook created successfully", "npt_id": npt_id}

@router.put("/{npt_id}")
def update_master(
    npt_id: int,
    payload: NPTReportMasterUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Update an NPT Report Master record and record to history."""
    updated = update_npt_master(db, npt_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "NPT Master Logbook updated successfully"}

@router.delete("/{npt_id}")
def delete_master(
    npt_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Delete an NPT Report Master record and archive it to history."""
    deleted = delete_npt_master(db, npt_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "NPT Master Logbook deleted successfully"}

@router.get("/{npt_id}", response_model=NPTReportMasterResponse)
def fetch_by_id(npt_id: int, db: Session = Depends(get_db)):
    """Fetch a single NPT report master record by Master ID."""
    record = get_npt_master_by_id(db, npt_id)
    if not record:
        raise HTTPException(status_code=404, detail="Master record not found")
    return record

@router.get("/by-created-date/{search_date}", response_model=List[NPTReportMasterResponse])
def fetch_by_date(search_date: date, station_id: int, db: Session = Depends(get_db)):
    """Fetch NPT reports combined with shift master data for a specific date."""
    return get_npt_by_created_date(db, search_date, station_id)

