from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.access_service import validate_token

from app.crud.digital_logbook.digital_cp_reading.cp_reading_master_crud import (
    create_master, update_master, delete_master, get_master_by_id, get_masters_by_date
)
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_master_schema import (
    CPReadingMasterCreate, CPReadingMasterUpdate, CPReadingMasterResponse
)

router = APIRouter(prefix="/cp-reading-master", tags=["CP Reading Master"], dependencies=[Depends(validate_token)])

@router.post("", status_code=status.HTTP_201_CREATED, summary="Create Master")
def create_cp_master_op(payload: CPReadingMasterCreate, db: Session = Depends(get_db), user: dict = Depends(validate_token)):
    mid = create_master(db, payload.model_dump(exclude_unset=True), user.get("user_id"))
    return {"message": "Master created", "cp_master_id": mid}

@router.get("/get-by-date", summary="Fetch By Date", response_model=List[CPReadingMasterResponse])
def list_cp_masters_op(sid: int = Query(..., alias="station_id"), search_date: date = Query(..., alias="search_date"), db: Session = Depends(get_db)):
    return get_masters_by_date(db, sid, search_date)

@router.get("/{cp_master_id}", summary="Fetch By Id", response_model=CPReadingMasterResponse)
def get_cp_master_op(cp_master_id: int, db: Session = Depends(get_db)):
    res = get_master_by_id(db, cp_master_id)
    if not res:
        raise HTTPException(404, "Master not found")
    return res

@router.put("/{cp_master_id}", summary="Update Master")
def edit_cp_master_op(cp_master_id: int, payload: CPReadingMasterUpdate, db: Session = Depends(get_db), user: dict = Depends(validate_token)):
    if not update_master(db, cp_master_id, payload.model_dump(exclude_unset=True), user.get("user_id")): 
        raise HTTPException(404, "Master not found")
    return {"message": "Master updated"}

@router.delete("/{cp_master_id}", summary="Delete Master")
def remove_cp_master_op(cp_master_id: int, db: Session = Depends(get_db)):
    if not delete_master(db, cp_master_id):
        raise HTTPException(404, "Master not found")
    return {"message": "Master deleted"}
