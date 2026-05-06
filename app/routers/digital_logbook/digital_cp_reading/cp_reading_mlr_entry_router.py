# app/routers/digital_logbook/digital_cp_reading/cp_reading_mlr_entry_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_mlr_entry_schema import (
    CPReadingMLREntryCreate,
    CPReadingMLREntryUpdate,
    CPReadingMLREntryResponse
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_mlr_entry_crud import (
    create_mlr_entry,
    update_mlr_entry,
    delete_mlr_entry,
    get_mlr_entry_by_id
)

router = APIRouter(
    prefix="/cp-reading-mlr-entry",
    tags=["CP Reading MLR Entry"],
    dependencies=[Depends(validate_token)]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_entry(
    payload: CPReadingMLREntryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    new_id = create_mlr_entry(db, payload, current_user.get("user_id"))
    return {"message": "CP Reading MLR Entry created successfully", "cp_mlr_entry_id": new_id}

@router.put("/{cp_mlr_entry_id}")
def update_entry(
    cp_mlr_entry_id: int,
    payload: CPReadingMLREntryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    updated = update_mlr_entry(db, cp_mlr_entry_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return {"message": "CP Reading MLR Entry updated successfully"}

@router.delete("/{cp_mlr_entry_id}")
def delete_entry(
    cp_mlr_entry_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    deleted = delete_mlr_entry(db, cp_mlr_entry_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return {"message": "CP Reading MLR Entry deleted successfully"}

@router.get("/{cp_mlr_entry_id}", response_model=CPReadingMLREntryResponse)
def fetch_by_id(cp_mlr_entry_id: int, db: Session = Depends(get_db)):
    data = get_mlr_entry_by_id(db, cp_mlr_entry_id)
    if not data:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return data

