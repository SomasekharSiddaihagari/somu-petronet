# app/routers/ner_digital_logbook_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_ner.ner_digital_logbook_schema import (
    NerDigitalLogBookCreate,
    NerDigitalLogBookUpdate
)
from app.crud.digital_logbook.digital_logbook_ner.ner_digital_logbook_crud import (
    create_ner_digital_logbook,
    update_ner_digital_logbook,
    delete_ner_digital_logbook,
    get_logbook_by_date
)
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/ner-digital-logbook",
    tags=["NER Digital Logbook"],dependencies=[Depends(validate_token)]
)


@router.post("")
def create_ner_digital_logbook_api(
    payload: NerDigitalLogBookCreate,
    db: Session = Depends(get_db)
):
    logbook_id = create_ner_digital_logbook(db, payload)
    return {
        "message": "NER digital logbook created successfully",
        "ner_logbook_id": logbook_id
    }


@router.put("/{ner_logbook_id}")
def update_ner_digital_logbook_api(
    ner_logbook_id: int,
    payload: NerDigitalLogBookUpdate,
    db: Session = Depends(get_db)
):
    updated = update_ner_digital_logbook(db, ner_logbook_id, payload)
    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return {"message": "NER digital logbook updated successfully"}


@router.delete("/{ner_logbook_id}")
def delete_ner_digital_logbook_api(
    ner_logbook_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_ner_digital_logbook(db, ner_logbook_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="NER digital logbook not found"
        )

    return {"message": "NER digital logbook deleted successfully"}


# @router.get("/by-date",response_model=List[dict])
# def fetch_logbook_by_date(
#     log_date: date,
#     db: Session = Depends(get_db)
# ):
#     return get_logbook_by_date(db, log_date)

@router.get("/by-date")
def get_logbook_by_date_api(
    log_date: date,
    db: Session = Depends(get_db)
):
    data = get_logbook_by_date(db, log_date)
    return data