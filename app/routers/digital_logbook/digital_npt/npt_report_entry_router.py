from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_npt.npt_report_entry_schema import (
    NPTReportEntryCreate,
    NPTReportEntryUpdate,
    NPTReportEntryResponse
)
from app.crud.digital_logbook.digital_npt.npt_report_entry_crud import (
    get_npt_entry_by_id,
    create_npt_entry,
    update_npt_entry,
    delete_npt_entry
)

router = APIRouter(
    prefix="/npt-report-entry",
    tags=["NPT Report Entry"],
    dependencies=[Depends(validate_token)]
)




@router.post("", status_code=status.HTTP_201_CREATED)
def create(
    payload: NPTReportEntryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Create a new NPT report entry. Requires an existing npt_master_id (npt_id)."""
    master_exists = db.execute(
        text("SELECT 1 FROM npt_report_master WHERE npt_id = :mid"),
        {"mid": payload.npt_master_id},
    ).first()
    if not master_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"NPT Master record with ID {payload.npt_master_id} not found",
        )

    npe_id = create_npt_entry(db, payload, current_user.get("user_id"))
    return {"message": "NPT report entry created successfully", "npe_id": npe_id}

@router.put("/{npe_id}")
def update(
    npe_id: int,
    payload: NPTReportEntryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Update an existing NPT report entry and log to history."""
    updated = update_npt_entry(db, npe_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NPT report entry not found"
        )
    return {"message": "NPT report entry updated successfully"}

@router.delete("/{npe_id}")
def delete(
    npe_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Delete an NPT report entry and archive to history."""
    deleted = delete_npt_entry(db, npe_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NPT report entry not found"
        )
    return {"message": "NPT report entry deleted successfully"}

@router.get("/{npe_id}", response_model=NPTReportEntryResponse)
def fetch_by_id(npe_id: int, db: Session = Depends(get_db)):
    """Fetch a specific NPT report entry by ID."""
    entry = get_npt_entry_by_id(db, npe_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NPT report entry not found"
        )
    return entry

