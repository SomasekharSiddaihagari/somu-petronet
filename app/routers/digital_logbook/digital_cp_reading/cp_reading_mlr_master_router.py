# app/routers/digital_logbook/digital_cp_reading/cp_reading_mlr_master_router.py
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_mlr_master_schema import (
    CPReadingMLRMasterCreate,
    CPReadingMLRMasterUpdate,
    CPReadingMLRMasterResponse
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_mlr_master_crud import (
    create_mlr_master,
    update_mlr_master,
    delete_mlr_master,
    get_mlr_master_by_id,
    get_mlr_masters_by_date_range
)

router = APIRouter(
    prefix="/cp-reading-mlr-master",
    tags=["CP Reading MLR Master"],
    dependencies=[Depends(validate_token)]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_master(
    payload: CPReadingMLRMasterCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    new_id = create_mlr_master(db, payload, current_user.get("user_id"))
    return {"message": "CP Reading MLR Master created successfully", "mlr_master_id": new_id}

@router.put("/{cp_mlr_id}")
def update_master(
    cp_mlr_id: int,
    payload: CPReadingMLRMasterUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    updated = update_mlr_master(db, cp_mlr_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "CP Reading MLR Master updated successfully"}

@router.delete("/{cp_mlr_id}")
def delete_master(
    cp_mlr_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    deleted = delete_mlr_master(db, cp_mlr_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "CP Reading MLR Master deleted successfully"}

@router.get("/get-all-entries-by-date-range", response_model=List[CPReadingMLRMasterResponse])
def fetch_by_date_range(from_date: date, to_date: date, db: Session = Depends(get_db)):
    return get_mlr_masters_by_date_range(db, from_date, to_date)

@router.get("/{cp_mlr_id}", response_model=CPReadingMLRMasterResponse)
def fetch_by_id(cp_mlr_id: int, db: Session = Depends(get_db)):
    data = get_mlr_master_by_id(db, cp_mlr_id)
    if not data:
        raise HTTPException(status_code=404, detail="Master record not found")
    return data

