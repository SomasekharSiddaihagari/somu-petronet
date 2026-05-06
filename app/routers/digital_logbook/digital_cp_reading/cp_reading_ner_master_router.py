# app/routers/digital_logbook/digital_cp_reading/cp_reading_ner_master_router.py
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.access_service import validate_token
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_ner_master_schema import (
    CPReadingNERMasterCreate,
    CPReadingNERMasterUpdate,
    CPReadingNERMasterResponse
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_ner_master_crud import (
    create_ner_master,
    update_ner_master,
    delete_ner_master,
    get_ner_master_by_id,
    get_ner_masters_by_date_range
)

router = APIRouter(
    prefix="/cp-reading-ner-master",
    tags=["CP Reading NER Master"],
    dependencies=[Depends(validate_token)]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_master(
    payload: CPReadingNERMasterCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    new_id = create_ner_master(db, payload, current_user.get("user_id"))
    return {"message": "CP Reading NER Master created successfully", "ner_master_id": new_id}

@router.put("/{cp_ner_id}")
def update_master(
    cp_ner_id: int,
    payload: CPReadingNERMasterUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    updated = update_ner_master(db, cp_ner_id, payload, current_user.get("user_id"))
    if not updated:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "CP Reading NER Master updated successfully"}

@router.delete("/{cp_ner_id}")
def delete_master(
    cp_ner_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(validate_token),
):
    deleted = delete_ner_master(db, cp_ner_id, current_user.get("user_id"))
    if not deleted:
        raise HTTPException(status_code=404, detail="Master record not found")
    return {"message": "CP Reading NER Master deleted successfully"}

@router.get("/get-all-entries-by-date-range", response_model=List[CPReadingNERMasterResponse])
def fetch_by_date_range(from_date: date, to_date: date, db: Session = Depends(get_db)):
    return get_ner_masters_by_date_range(db, from_date, to_date)

@router.get("/{cp_ner_id}", response_model=CPReadingNERMasterResponse)
def fetch_by_id(cp_ner_id: int, db: Session = Depends(get_db)):
    data = get_ner_master_by_id(db, cp_ner_id)
    if not data:
        raise HTTPException(status_code=404, detail="Master record not found")
    return data

