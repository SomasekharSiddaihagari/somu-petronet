from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_dkn_master_schema import (
    CPReadingDKNMasterCreate,
    CPReadingDKNMasterUpdate,
    CPReadingDKNMasterResponse
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_dkn_master_crud import (
    create_dkn_master,
    update_dkn_master,
    delete_dkn_master,
    get_dkn_master_by_id,
    get_dkn_masters_by_date_range
)

router = APIRouter(
    prefix="/cp-reading-dkn-master",
    tags=["CP Reading DKN Master"],
    dependencies=[Depends(validate_token)]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_master(
    payload: CPReadingDKNMasterCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    new_id = create_dkn_master(db, payload, current_user.get("user_id"))
    return {"message": "CP Reading DKN Master created successfully", "dkn_master_id": new_id}

@router.put("/{cp_dkn_id}")
def update_master(
    cp_dkn_id: int,
    payload: CPReadingDKNMasterUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    updated = update_dkn_master(db, cp_dkn_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "CP Reading DKN Master updated successfully"}

@router.delete("/{cp_dkn_id}")
def delete_master(
    cp_dkn_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    deleted = delete_dkn_master(db, cp_dkn_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "CP Reading DKN Master deleted successfully"}

@router.get("/get-all-entries-by-date-range", response_model=List[CPReadingDKNMasterResponse])
def fetch_by_date_range(from_date: date, to_date: date, db: Session = Depends(get_db)):
    return get_dkn_masters_by_date_range(db, from_date, to_date)

@router.get("/{cp_dkn_id}", response_model=CPReadingDKNMasterResponse)
def fetch_by_id(cp_dkn_id: int, db: Session = Depends(get_db)):
    data = get_dkn_master_by_id(db, cp_dkn_id)
    if not data:
        raise HTTPException(status_code=404, detail="Master record not found")
    return data

