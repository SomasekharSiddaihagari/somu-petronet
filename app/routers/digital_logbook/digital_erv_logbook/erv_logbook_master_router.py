from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.digital_logbook.digital_erv_logbook.erv_logbook_master_crud import (
    get_combined_erv_by_date,
    get_erv_logbook_by_id,
    create_erv_logbook,
    update_erv_logbook,
    delete_erv_logbook,
)
from app.schemas.digital_logbook.digital_erv_logbook.erv_logbook_master_schema import (
    ErvLogbookResponse,
    ErvLogbookCreate,
    ErvLogbookUpdate,
)
from app.utils.access_service import validate_token

from datetime import date

router = APIRouter(
    prefix="/erv-logbook-master",
    tags=["ERV Logbook Master"],
    dependencies=[Depends(validate_token)],
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_master_logbook(
    payload: ErvLogbookCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Create a new ERV Logbook Master manually and return its ID."""
    erv_id = create_erv_logbook(db, payload, current_user.get("user_id"))
    return {"message": "ERV Master Logbook created successfully", "erv_id": erv_id}


@router.put("/{erv_id}")
def update_master(
    erv_id: int,
    payload: ErvLogbookUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Update an ERV Logbook Master record and record to history."""
    updated = update_erv_logbook(db, erv_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "ERV Master Logbook updated successfully"}


@router.delete("/{erv_id}")
def delete_master(
    erv_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    """Delete an ERV Logbook Master record and archive it to history."""
    deleted = delete_erv_logbook(db, erv_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "ERV Master Logbook deleted successfully"}


@router.get("/{erv_id}", response_model=ErvLogbookResponse)
def fetch_by_id(erv_id: int, db: Session = Depends(get_db)):
    """Fetch a single ERV logbook master record by Master ID."""
    data = get_erv_logbook_by_id(db, erv_id)
    if not data:
        raise HTTPException(status_code=404, detail="Master record not found")
    return data


@router.get("/by-created-date/{search_date}", response_model=List[ErvLogbookResponse])
def fetch_by_date(search_date: date, db: Session = Depends(get_db)):
    """Fetch ERV logbooks combined with shift master data for a specific date."""
    return get_combined_erv_by_date(db, search_date)
