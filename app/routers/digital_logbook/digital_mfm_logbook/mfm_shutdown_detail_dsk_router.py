# app/routers/mfm_shutdown_detail_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime, time
from sqlalchemy import text

from app.database import get_db
from app.schemas.digital_logbook.digital_mfm_logbook.mfm_shutdown_detail_dsk_schema import (
    MFMShutdownDetailCreate,
    MFMShutdownDetailUpdate
)
from app.crud.digital_logbook.digital_mfm_logbook.mfm_shutdown_detail_dsk_crud import (
    create_mfm_shutdown_detail,
    update_mfm_shutdown_detail,
    delete_mfm_shutdown_detail
)
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-shutdown-detail",
    tags=["MFM Shutdown Detail"],dependencies=[Depends(validate_token)]
)


@router.post("")
def create_mfm_shutdown_detail_api(
    payload: MFMShutdownDetailCreate,
    db: Session = Depends(get_db)
):
    shutdown_id = create_mfm_shutdown_detail(db, payload)
    return {
        "message": "MFM shutdown detail created successfully",
        "mfm_shutdown_id": shutdown_id
    }


@router.put("/{mfm_shutdown_id}")
def update_mfm_shutdown_detail_api(
    mfm_shutdown_id: int,
    payload: MFMShutdownDetailUpdate,
    db: Session = Depends(get_db)
):
    updated = update_mfm_shutdown_detail(db, mfm_shutdown_id, payload)
    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return {"message": "MFM shutdown detail updated successfully"}


@router.delete("/{mfm_shutdown_id}")
def delete_mfm_shutdown_detail_api(
    mfm_shutdown_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_mfm_shutdown_detail(db, mfm_shutdown_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="MFM shutdown detail not found"
        )

    return {"message": "MFM shutdown detail deleted successfully"}


# @router.get("/by-date", response_model=List[dict])
# def fetch_mfm_log_by_date(
#     log_date: date,
#     db: Session = Depends(get_db)
# ):
#     query = text("""
#         select MSDD.* from mfm_shutdown_detail_dkn MSDD
# JOIN mfm_log_master_dkn MLMD 
#     ON MSDD.master_id = MLMD.mfm_log_dkn_id
# JOIN logbook_shift_master LSM 
#     ON LSM.ms_logbook_id = MLMD.ms_logbook_id
# WHERE DATE(LSM.created_at) =:log_date;
#     """)

#     result = db.execute(query, {"log_date": log_date}).mappings().all()

#     return result

@router.get("/by-date", response_model=List[dict])
def fetch_mfm_shutdown_log_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            MSDD.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_shutdown_detail_dkn MSDD

        JOIN mfm_log_master_dkn MLMD
            ON MSDD.master_id = MLMD.mfm_log_dkn_id

        JOIN logbook_shift_master LSM
            ON LSM.ms_logbook_id = MLMD.ms_logbook_id

        -- Join for created_by
        LEFT JOIN users u1 
            ON u1.user_id = MSDD.created_by

        -- Join for updated_by
        LEFT JOIN users u2 
            ON u2.user_id = MSDD.updated_by

        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    result = db.execute(query, {"log_date": log_date}).mappings().all()

    return result


@router.get("/{mfm_shutdown_id}", response_model=dict)
def fetch_mfm_log_by_id(
    mfm_shutdown_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            MSDD.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_shutdown_detail_dkn MSDD

        -- Join for created_by
        LEFT JOIN users u1 
            ON u1.user_id = MSDD.created_by

        -- Join for updated_by
        LEFT JOIN users u2 
            ON u2.user_id = MSDD.updated_by

        WHERE MSDD.mfm_shutdown_id = :mfm_shutdown_id
    """)

    result = db.execute(
        query, {"mfm_shutdown_id": mfm_shutdown_id}
    ).mappings().first()

    return result