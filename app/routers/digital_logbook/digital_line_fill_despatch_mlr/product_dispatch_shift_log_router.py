from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.access_service import validate_token

from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_log_schema import (
    ProductDispatchShiftLogCreate,
    ProductDispatchShiftLogUpdate,
    ProductDispatchShiftLogResponse,
)
from app.crud.digital_logbook.digital_line_fill_despatch_mlr import (
    product_dispatch_shift_log_crud as crud,
)

router = APIRouter(
    prefix="/product-dispatch-shift-log",
    tags=["Product Dispatch Shift Log"],
    dependencies=[Depends(validate_token)],
)


@router.post("", summary="Create Shift Log")
def create_log(payload: ProductDispatchShiftLogCreate, db: Session = Depends(get_db)):
    log_id = crud.create_shift_log(db, payload)
    return {"message": "Shift log created successfully", "shift_log_id": log_id}


@router.get(
    "/get-by-date-with-cumulative-data",
    summary="Get Cumulative Data for Carry-Forward (A/B/C Mapping)",
)
def get_cumulative_data(log_date: date, shift_id: int, db: Session = Depends(get_db)):
    return crud.get_cumulative_carry_forward(db, log_date, shift_id)


@router.put("/{p_dispatch_shift_id}", summary="Update Shift Log")
def update_log(
    p_dispatch_shift_id: int,
    payload: ProductDispatchShiftLogUpdate,
    db: Session = Depends(get_db),
):
    updated = crud.update_shift_log(db, p_dispatch_shift_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Shift log not found")
    return {"message": "Shift log updated successfully"}


@router.get(
    "/{p_dispatch_shift_id}",
    response_model=ProductDispatchShiftLogResponse,
    summary="Fetch Log by ID",
)
def get_log(p_dispatch_shift_id: int, db: Session = Depends(get_db)):
    data = crud.get_shift_log_by_id(db, p_dispatch_shift_id)
    if not data:
        raise HTTPException(status_code=404, detail="Shift log not found")
    return data


@router.delete("/{p_dispatch_shift_id}", summary="Delete Shift Log")
def delete_log(p_dispatch_shift_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_shift_log(db, p_dispatch_shift_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shift log not found")
    return {"message": "Shift log deleted successfully"}
