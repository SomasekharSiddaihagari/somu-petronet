from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.access_service import validate_token

from app.crud.digital_logbook.digital_cp_reading.cp_reading_entry_crud import (
    create_entry, update_entry, delete_entry, get_entry_by_id
)
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_entry_schema import (
    CPReadingEntryCreate, CPReadingEntryUpdate, CPReadingEntryResponse
)

router = APIRouter(prefix="/cp-reading-entry", tags=["CP Reading Entry"], dependencies=[Depends(validate_token)])


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create Entry")
def add_cp_entry_op(payload: CPReadingEntryCreate, db: Session = Depends(get_db), user: dict = Depends(validate_token)):
    eid = create_entry(db, payload.model_dump(exclude_unset=True), user.get("user_id"))
    return {"message": "Entry created", "cp_entry_id": eid}

@router.get("/{cp_entry_id}", summary="Fetch By Id")
def get_cp_entry_op(cp_entry_id: int, db: Session = Depends(get_db)):
    res = get_entry_by_id(db, cp_entry_id)
    if not res:
        raise HTTPException(404, "Entry not found")
    return res

@router.put("/{cp_entry_id}", summary="Update Entry")
def edit_cp_entry_op(cp_entry_id: int, payload: CPReadingEntryUpdate, db: Session = Depends(get_db), user: dict = Depends(validate_token)):
    if not update_entry(db, cp_entry_id, payload.model_dump(exclude_unset=True), user.get("user_id")): 
        raise HTTPException(404, "Entry not found")
    return {"message": "Entry updated"}

@router.delete("/{cp_entry_id}", summary="Delete Entry")
def remove_cp_entry_op(cp_entry_id: int, db: Session = Depends(get_db)):
    if not delete_entry(db, cp_entry_id):
        raise HTTPException(404, "Entry not found")
    return {"message": "Entry deleted"}
