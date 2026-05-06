# app/routers/mfm_accounting_hsn_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from sqlalchemy import text

from app.database import get_db
from app.schemas.digital_logbook.digital_mfm_accounting.mfm_accounting_hsn_schema import (
    MFMAccountingHSNCreate,
    MFMAccountingHSNUpdate
)
from app.crud.digital_logbook.digital_mfm_accounting.mfm_accounting_hsn_crud import (
    create_mfm_accounting_hsn,
    update_mfm_accounting_hsn,
    delete_mfm_accounting_hsn
)
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/mfm-accounting-hsn",
    tags=["MFM Accounting HSN"],dependencies=[Depends(validate_token)]
)


@router.post("")
def create_mfm_accounting_hsn_api(
    payload: MFMAccountingHSNCreate,
    db: Session = Depends(get_db)
):
    hsn_id = create_mfm_accounting_hsn(db, payload)
    return {
        "message": "MFM Accounting HSN record created successfully",
        "mfm_acc_hsn_id": hsn_id
    }


@router.put("/{mfm_acc_hsn_id}")
def update_mfm_accounting_hsn_api(
    mfm_acc_hsn_id: int,
    payload: MFMAccountingHSNUpdate,
    db: Session = Depends(get_db)
):
    updated = update_mfm_accounting_hsn(db, mfm_acc_hsn_id, payload)
    if not updated:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    return {"message": "MFM Accounting HSN record updated successfully"}


@router.delete("/{mfm_acc_hsn_id}")
def delete_mfm_accounting_hsn_api(
    mfm_acc_hsn_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_mfm_accounting_hsn(db, mfm_acc_hsn_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="MFM Accounting HSN record not found")

    return {"message": "MFM Accounting HSN record deleted successfully"}


@router.get("/by-date", response_model=List[dict])
def get_mfm_accounting_hsn_by_date_api(
    log_date: date,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            MAH.*,

            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mfm_accounting_hsn MAH

        LEFT JOIN users u1
            ON u1.user_id = MAH.created_by

        LEFT JOIN users u2
            ON u2.user_id = MAH.updated_by

        WHERE MAH.created_at >= :log_date + INTERVAL '7 hour'
        AND MAH.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    result = db.execute(
        query,
        {"log_date": log_date}
    ).mappings().all()

    return result

@router.get("/{mfm_acc_hsn_id}")
def get_mfm_accounting_hsn_by_id_api(
    mfm_acc_hsn_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            mah.*,
            CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, '')) AS created_by_name,
            CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, '')) AS updated_by_name

        FROM mfm_accounting_hsn mah

        LEFT JOIN users u1
            ON u1.user_id = mah.created_by

        LEFT JOIN users u2
            ON u2.user_id = mah.updated_by

        WHERE mah.mfm_acc_hsn_id = :mfm_acc_hsn_id
                 

    """)

    result = db.execute(
        query,
        {"mfm_acc_hsn_id": mfm_acc_hsn_id}
    ).mappings().first()

    if not result:
        raise HTTPException(status_code=404, detail="Record not found")

    return result
