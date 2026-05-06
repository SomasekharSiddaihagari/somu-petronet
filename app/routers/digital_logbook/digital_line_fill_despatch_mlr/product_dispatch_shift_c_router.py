# app/routers/erv_c_shift_log_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_c_schema import (
    ERVCShiftLogCreate,
    ERVCShiftLogUpdate
)
from app.crud.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_c_crud import (
    create_erv_c_shift_log,
    update_erv_c_shift_log,
    delete_erv_c_shift_log
)
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/erv-c-shift-log",
    tags=["ERV C Shift Log"],dependencies=[Depends(validate_token)]
)


@router.post("/")
def create_erv_c_shift_log_api(
    payload: ERVCShiftLogCreate,
    db: Session = Depends(get_db)
):
    log_id = create_erv_c_shift_log(db, payload)
    return {
        "message": "ERV C shift log created successfully",
        "erv_c_shift_log_id": log_id
    }


@router.put("/{erv_c_shift_log_id}")
def update_erv_c_shift_log_api(
    erv_c_shift_log_id: int,
    payload: ERVCShiftLogUpdate,
    db: Session = Depends(get_db)
):
    updated = update_erv_c_shift_log(db, erv_c_shift_log_id, payload)
    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return {"message": "ERV C shift log updated successfully"}


@router.delete("/{erv_c_shift_log_id}")
def delete_erv_c_shift_log_api(
    erv_c_shift_log_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_erv_c_shift_log(db, erv_c_shift_log_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="ERV C shift log not found"
        )

    return {"message": "ERV C shift log deleted successfully"}
