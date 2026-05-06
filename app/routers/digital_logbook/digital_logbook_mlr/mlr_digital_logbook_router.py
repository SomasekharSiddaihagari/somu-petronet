from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.crud.digital_logbook.digital_logbook_mlr.mlr_digital_logbook_crud import create_mlr_logbook, delete_mlr_logbook, get_logbook_by_date_api_with_technicians, update_mlr_logbook, get_logbook_by_date
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_mlr.mlr_digital_logbook_schemas import MlrDigitalLogBookCreate, MlrDigitalLogBookUpdate

from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mlr-logbook",
    tags=["MLR Digital Logbook"],dependencies=[Depends(validate_token)]
)


@router.post("", response_model=dict)
def create_logbook(payload: MlrDigitalLogBookCreate, db: Session = Depends(get_db)):
    logbook_id = create_mlr_logbook(db, payload)
    return {
        "message": "MLR logbook created successfully",
        "mlr_logbook_id": logbook_id
    }


@router.put("/{logbook_id}", response_model=dict)
def update_logbook(
    logbook_id: int,
    payload: MlrDigitalLogBookUpdate,
    db: Session = Depends(get_db)
):
    update_mlr_logbook(db, logbook_id, payload)
    return {"message": "MLR logbook updated successfully"}


@router.delete("/{logbook_id}", response_model=dict)
def delete_logbook(logbook_id: int, db: Session = Depends(get_db)):
    delete_mlr_logbook(db, logbook_id)
    return {"message": "MLR logbook deleted successfully"}


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

@router.get("/by-date-with-technicians")
def get_logbook_by_date_api_with_technician(
    log_date: date,
    db: Session = Depends(get_db)
):
    data = get_logbook_by_date_api_with_technicians(db, log_date)
    return data