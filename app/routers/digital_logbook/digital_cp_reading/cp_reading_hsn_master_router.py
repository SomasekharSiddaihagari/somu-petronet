from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_hsn_master_schema import (
    CPReadingHSNMasterCreate,
    CPReadingHSNMasterUpdate,
    CPReadingHSNMasterResponse
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_hsn_master_crud import (
    create_hsn_master,
    update_hsn_master,
    delete_hsn_master,
    get_hsn_master_by_id,
    get_hsn_masters_by_date_range
)

router = APIRouter(
    prefix="/cp-reading-hsn-master",
    tags=["CP Reading HSN Master"],
    dependencies=[Depends(validate_token)]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_master(
    payload: CPReadingHSNMasterCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    new_id = create_hsn_master(db, payload, current_user.get("user_id"))
    return {"message": "CP Reading HSN Master created successfully", "hsn_master_id": new_id}

@router.put("/{cp_hsn_id}")
def update_master(
    cp_hsn_id: int,
    payload: CPReadingHSNMasterUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    updated = update_hsn_master(db, cp_hsn_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "CP Reading HSN Master updated successfully"}

@router.delete("/{cp_hsn_id}")
def delete_master(
    cp_hsn_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    deleted = delete_hsn_master(db, cp_hsn_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "CP Reading HSN Master deleted successfully"}

@router.get("/get-all-entries-by-date-range", response_model=List[CPReadingHSNMasterResponse])
def fetch_by_date_range(from_date: date, to_date: date, db: Session = Depends(get_db)):
    return get_hsn_masters_by_date_range(db, from_date, to_date)

@router.get("/{cp_hsn_id}", response_model=CPReadingHSNMasterResponse)
def fetch_by_id(cp_hsn_id: int, db: Session = Depends(get_db)):
    data = get_hsn_master_by_id(db, cp_hsn_id)
    if not data:
        raise HTTPException(status_code=404, detail="Master record not found")
    return data

