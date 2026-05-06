from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.digital_logbook.digital_logbook_dkn.dkn_digital_logbook_entry_crud import delete_entry
from app.database import get_db
from app.crud.digital_logbook.digital_logbook_dkn.dkn_digital_logbook_entry_crud import create_entry, update_entry
from app.schemas.digital_logbook.digital_logbook_dkn.dkn_digital_logbook_entry_schemas import DknDigitalLogBookEntryCreate, DknDigitalLogBookEntryUpdate
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/dkn-logbook-entry",
    tags=["DKN Digital Logbook Entry"],dependencies=[Depends(validate_token)]
)


@router.post("", response_model=dict)
def create_dkn_entry(payload: DknDigitalLogBookEntryCreate, db: Session = Depends(get_db)):
    entry_id = create_entry(db, payload)
    return {
        "message": "Entry created successfully",
        "dkn_entry_id": entry_id
    }


@router.put("/{entry_id}", response_model=dict)
def update_dkn_entry(
    entry_id: int,
    payload: DknDigitalLogBookEntryUpdate,
    db: Session = Depends(get_db)
):
    update_entry(db, entry_id, payload)
    return {"message": "Entry updated successfully"}


@router.delete("/{entry_id}", response_model=dict)
def delete_dkn_entry(entry_id: int, db: Session = Depends(get_db)):
    delete_entry(db, entry_id)
    return {"message": "Entry deleted successfully"}
