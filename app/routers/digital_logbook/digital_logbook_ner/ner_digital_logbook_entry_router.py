# app/routers/ner_digital_logbook_entry_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_ner.ner_digital_logbook_entry_schema import (
    NerDigitalLogBookEntryCreate,
    NerDigitalLogBookEntryUpdate
)
from app.crud.digital_logbook.digital_logbook_ner.ner_digital_logbook_entry_crud import (
    create_ner_digital_logbook_entry,
    update_ner_digital_logbook_entry,
    delete_ner_digital_logbook_entry
)
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/ner-digital-logbook-entry",
    tags=["NER Digital Logbook Entry"],dependencies=[Depends(validate_token)]
)


@router.post("")
def create_ner_digital_logbook_entry_api(
    payload: NerDigitalLogBookEntryCreate,
    db: Session = Depends(get_db)
):
    entry_id = create_ner_digital_logbook_entry(db, payload)
    return {
        "message": "NER digital logbook entry created successfully",
        "ner_entry_id": entry_id
    }


@router.put("/{ner_entry_id}")
def update_ner_digital_logbook_entry_api(
    ner_entry_id: int,
    payload: NerDigitalLogBookEntryUpdate,
    db: Session = Depends(get_db)
):
    updated = update_ner_digital_logbook_entry(db, ner_entry_id, payload)
    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return {"message": "NER digital logbook entry updated successfully"}


@router.delete("/{ner_entry_id}")
def delete_ner_digital_logbook_entry_api(
    ner_entry_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_ner_digital_logbook_entry(db, ner_entry_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="NER digital logbook entry not found"
        )

    return {"message": "NER digital logbook entry deleted successfully"}
