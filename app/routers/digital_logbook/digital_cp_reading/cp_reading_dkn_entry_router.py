from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_dkn_entry_schema import (
    CPReadingDKNEntryCreate,
    CPReadingDKNEntryUpdate,
    CPReadingDKNEntryResponse,
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_dkn_entry_crud import (
    create_dkn_entry,
    update_dkn_entry,
    delete_dkn_entry,
    get_dkn_entry_by_id,
)

router = APIRouter(
    prefix="/cp-reading-dkn-entry",
    tags=["CP Reading DKN Entry"],
    dependencies=[Depends(validate_token)],
)



@router.post("", status_code=status.HTTP_201_CREATED)
def create_entry(
    payload: CPReadingDKNEntryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    new_id = create_dkn_entry(db, payload, current_user.get("user_id"))
    return {
        "message": "CP Reading DKN Entry created successfully",
        "cp_dkn_entry_id": new_id,
    }

@router.put("/{cp_dkn_entry_id}")
def update_entry(
    cp_dkn_entry_id: int,
    payload: CPReadingDKNEntryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    updated = update_dkn_entry(
        db, cp_dkn_entry_id, payload, current_user.get("user_id")
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return {"message": "CP Reading DKN Entry updated successfully"}

@router.delete("/{cp_dkn_entry_id}")
def delete_entry(
    cp_dkn_entry_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    deleted = delete_dkn_entry(db, cp_dkn_entry_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return {"message": "CP Reading DKN Entry deleted successfully"}

@router.get("/{cp_dkn_entry_id}", response_model=CPReadingDKNEntryResponse)
def fetch_by_id(cp_dkn_entry_id: int, db: Session = Depends(get_db)):
    data = get_dkn_entry_by_id(db, cp_dkn_entry_id)
    if not data:
        raise HTTPException(status_code=404, detail="Entry record not found")
    return data

