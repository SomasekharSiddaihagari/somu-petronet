# app/routers/erv_a_shift_log_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_a_schema import (
    ERVAShiftLogCreate,
    ERVAShiftLogUpdate
)
from app.crud.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_a_crud import (
    create_erv_a_shift_log,
    update_erv_a_shift_log,
    delete_erv_a_shift_log
)
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/erv-a-shift-log",
    tags=["ERV A Shift Log"],dependencies=[Depends(validate_token)]
)


@router.post("/")
def create_erv_a_shift_log_api(
    payload: ERVAShiftLogCreate,
    db: Session = Depends(get_db)
):
    log_id = create_erv_a_shift_log(db, payload)
    return {
        "message": "ERV A shift log created successfully",
        "a_shift_log_id": log_id
    }


@router.put("/{a_shift_log_id}")
def update_erv_a_shift_log_api(
    a_shift_log_id: int,
    payload: ERVAShiftLogUpdate,
    db: Session = Depends(get_db)
):
    updated = update_erv_a_shift_log(db, a_shift_log_id, payload)
    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return {"message": "ERV A shift log updated successfully"}


@router.delete("/{a_shift_log_id}")
def delete_erv_a_shift_log_api(
    a_shift_log_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_erv_a_shift_log(db, a_shift_log_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="ERV A shift log not found"
        )

    return {"message": "ERV A shift log deleted successfully"}
