from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_hsn_entry_schema import (
    CPReadingHSNEntryCreate,
    CPReadingHSNEntryUpdate,
    CPReadingHSNEntryResponse
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_hsn_entry_crud import (
    create_hsn_entry,
    update_hsn_entry,
    delete_hsn_entry,
    get_hsn_entry_by_id
)

router = APIRouter(
    prefix="/cp-reading-hsn-entry",
    tags=["CP Reading HSN Entry"],
    dependencies=[Depends(validate_token)]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_entry(
    payload: CPReadingHSNEntryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    new_id = create_hsn_entry(db, payload, current_user.get("user_id"))
    return {"message": "CP Reading HSN Entry created successfully", "cp_hsn_entry_id": new_id}

@router.put("/{cp_hsn_entry_id}")
def update_entry(
    cp_hsn_entry_id: int,
    payload: CPReadingHSNEntryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    updated = update_hsn_entry(db, cp_hsn_entry_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return {"message": "CP Reading HSN Entry updated successfully"}

@router.delete("/{cp_hsn_entry_id}")
def delete_entry(
    cp_hsn_entry_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    deleted = delete_hsn_entry(db, cp_hsn_entry_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return {"message": "CP Reading HSN Entry deleted successfully"}

@router.get("/{cp_hsn_entry_id}", response_model=CPReadingHSNEntryResponse)
def fetch_by_id(cp_hsn_entry_id: int, db: Session = Depends(get_db)):
    data = get_hsn_entry_by_id(db, cp_hsn_entry_id)
    if not data:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return data

