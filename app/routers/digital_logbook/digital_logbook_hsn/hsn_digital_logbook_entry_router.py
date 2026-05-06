from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.digital_logbook.digital_logbook_hsn.hsn_digital_logbook_entry_crud import create_hsn_entry, delete_hsn_entry, update_hsn_entry
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_hsn.hsn_digital_logbook_entry_schemas import HsnDigitalLogBookEntryCreate, HsnDigitalLogBookEntryUpdate
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/hsn-logbook-entry",
    tags=["HSN Digital Logbook Entry"],dependencies=[Depends(validate_token)]
)


@router.post("", response_model=dict)
def create_entry(payload: HsnDigitalLogBookEntryCreate, db: Session = Depends(get_db)):
    entry_id = create_hsn_entry(db, payload)
    return {
        "message": "HSN logbook entry created successfully",
        "hsn_entry_id": entry_id
    }


@router.put("/{entry_id}", response_model=dict)
def update_entry(
    entry_id: int,
    payload: HsnDigitalLogBookEntryUpdate,
    db: Session = Depends(get_db)
):
    update_hsn_entry(db, entry_id, payload)
    return {"message": "HSN logbook entry updated successfully"}


@router.delete("/{entry_id}", response_model=dict)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    delete_hsn_entry(db, entry_id)
    return {"message": "HSN logbook entry deleted successfully"}
