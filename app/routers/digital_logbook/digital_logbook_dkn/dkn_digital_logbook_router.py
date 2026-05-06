from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.crud.digital_logbook.digital_logbook_dkn.dkn_digital_logbook_crud import create_logbook, delete_logbook, update_logbook, get_logbook_by_date
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_dkn.dkn_digital_logbook_schemas import DknDigitalLogBookCreate, DknDigitalLogBookUpdate, DknDigitalLogBookResponse

from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/dkn-logbook",
    tags=["DKN Digital Logbook"],dependencies=[Depends(validate_token)]
)


@router.post("", response_model=dict)
def create_dkn_logbook(payload: DknDigitalLogBookCreate, db: Session = Depends(get_db)):
    logbook_id = create_logbook(db, payload)
    return {
        "message": "Logbook created successfully",
        "dkn_logbook_id": logbook_id
    }


@router.put("/{logbook_id}", response_model=dict)
def update_dkn_logbook(
    logbook_id: int,
    payload: DknDigitalLogBookUpdate,
    db: Session = Depends(get_db)
):
    update_logbook(db, logbook_id, payload)
    return {"message": "Logbook updated successfully"}


@router.delete("/{logbook_id}", response_model=dict)
def delete_dkn_logbook(logbook_id: int, db: Session = Depends(get_db)):
    delete_logbook(db, logbook_id)
    return {"message": "Logbook deleted successfully"}


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