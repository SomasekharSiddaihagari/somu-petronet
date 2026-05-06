# app/routers/mfm_accounting_dkn_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import text

from app.database import get_db
from app.schemas.digital_logbook.digital_mfm_accounting.mfm_accounting_dkn_schema import (
    MFMAccountingDKNCreate,
    MFMAccountingDKNUpdate
)
from app.crud.digital_logbook.digital_mfm_accounting.mfm_accounting_dkn_crud import (
    create_mfm_accounting_dkn,
    update_mfm_accounting_dkn,
    delete_mfm_accounting_dkn
)
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-accounting-dkn",
    tags=["MFM Accounting DKN"],dependencies=[Depends(validate_token)]
)


@router.post("")
def create_mfm_accounting_dkn_api(
    payload: MFMAccountingDKNCreate,
    db: Session = Depends(get_db)
):
    rec_id = create_mfm_accounting_dkn(db, payload)
    return {
        "message": "MFM Accounting DKN record created successfully",
        "mfm_acc_dkn_id": rec_id
    }


@router.put("/{mfm_acc_dkn_id}")
def update_mfm_accounting_dkn_api(
    mfm_acc_dkn_id: int,
    payload: MFMAccountingDKNUpdate,
    db: Session = Depends(get_db)
):
    updated = update_mfm_accounting_dkn(db, mfm_acc_dkn_id, payload)
    if not updated:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    return {"message": "MFM Accounting DKN record updated successfully"}


@router.delete("/{mfm_acc_dkn_id}")
def delete_mfm_accounting_dkn_api(
    mfm_acc_dkn_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_mfm_accounting_dkn(db, mfm_acc_dkn_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="MFM Accounting DKN record not found")

    return {"message": "MFM Accounting DKN record deleted successfully"}


@router.get("/by-date")
def get_mfm_accounting_dkn_by_date_api(
    log_date: date,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT 
            MAD.*,
            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mfm_accounting_dkn MAD

        LEFT JOIN users u1
            ON u1.user_id = MAD.created_by

        LEFT JOIN users u2
            ON u2.user_id = MAD.updated_by

        WHERE MAD.created_at >= :log_date + INTERVAL '7 hour'
        AND MAD.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
        """),
        {"log_date": log_date}
    ).mappings().all()

    return result

@router.get("/{mfm_acc_dkn_id}")
def get_mfm_accounting_dkn_by_id_api(
    mfm_acc_dkn_id: int,
    db: Session = Depends(get_db)
):
    record = db.execute(
        text("""
            SELECT 
                MAD.*,

                TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

            FROM mfm_accounting_dkn MAD

            LEFT JOIN users u1
                ON u1.user_id = MAD.created_by

            LEFT JOIN users u2
                ON u2.user_id = MAD.updated_by

            WHERE MAD.mfm_acc_dkn_id = :mfm_acc_dkn_id
        """),
        {"mfm_acc_dkn_id": mfm_acc_dkn_id}
    ).mappings().first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return dict(record)