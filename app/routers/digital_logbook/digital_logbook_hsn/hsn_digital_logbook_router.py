from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from app.crud.digital_logbook.digital_logbook_hsn.hsn_digital_logbook_crud import create_hsn_logbook, delete_hsn_logbook, update_hsn_logbook, get_logbook_by_date
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_hsn.hsn_digital_logbook_schemas import HsnDigitalLogBookCreate, HsnDigitalLogBookUpdate
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/hsn-logbook",
    tags=["HSN Digital Logbook"],dependencies=[Depends(validate_token)]
)


@router.post("", response_model=dict)
def create_logbook(payload: HsnDigitalLogBookCreate, db: Session = Depends(get_db)):
    logbook_id = create_hsn_logbook(db, payload)
    return {
        "message": "HSN logbook created successfully",
        "hsn_logbook_id": logbook_id
    }


@router.put("/{logbook_id}", response_model=dict)
def update_logbook(
    logbook_id: int,
    payload: HsnDigitalLogBookUpdate,
    db: Session = Depends(get_db)
):
    update_hsn_logbook(db, logbook_id, payload)
    return {"message": "HSN logbook updated successfully"}


@router.delete("/{logbook_id}", response_model=dict)
def delete_logbook(logbook_id: int, db: Session = Depends(get_db)):
    delete_hsn_logbook(db, logbook_id)
    return {"message": "HSN logbook deleted successfully"}

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