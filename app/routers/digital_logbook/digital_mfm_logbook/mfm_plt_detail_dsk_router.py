from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-plt-detail-dkn",
    tags=["MFM PLT Detail DKN"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class MFMPLTDetailCreate(BaseModel):
    master_id: Optional[int]

    omc_with_tank_no: Optional[str]
    start_time: Optional[time]
    stop_time: Optional[time]

    opening_dip: Optional[float]
    opening_qty: Optional[float]

    closing_dip: Optional[float]
    closing_qty: Optional[float]

    fmr_opening_net: Optional[float]
    fmr_opening_gross: Optional[float]
    fmr_opening_mass: Optional[float]

    fmr_closing_net: Optional[float]
    fmr_closing_gross: Optional[float]
    fmr_closing_mass: Optional[float]

    qty_as_per_dip: Optional[float]
    
    qty_as_per_fmr_net: Optional[float]
    qty_as_per_fmr_gross: Optional[float]
    qty_as_per_fmr_mass: Optional[float]

    remarks: Optional[str]
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class MFMPLTDetailUpdate(MFMPLTDetailCreate):
    pass


# =====================================================
# POST — CREATE
# =====================================================

@router.post("")
def create_mfm_plt_detail(
    payload: MFMPLTDetailCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_plt_detail_dkn (
            master_id,

            omc_with_tank_no,
            start_time,
            stop_time,

            opening_dip,
            opening_qty,

            closing_dip,
            closing_qty,

            fmr_opening_net,
            fmr_opening_gross,
            fmr_opening_mass,

            fmr_closing_net,
            fmr_closing_gross,
            fmr_closing_mass,

            qty_as_per_dip,
                 
            qty_as_per_fmr_net,
            qty_as_per_fmr_gross,
            qty_as_per_fmr_mass,

            remarks   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,

            :omc_with_tank_no,
            :start_time,
            :stop_time,

            :opening_dip,
            :opening_qty,

            :closing_dip,
            :closing_qty,

            :fmr_opening_net,
            :fmr_opening_gross,
            :fmr_opening_mass,

            :fmr_closing_net,
            :fmr_closing_gross,
            :fmr_closing_mass,

            :qty_as_per_dip,
                 
            :qty_as_per_fmr_net,
            :qty_as_per_fmr_gross,
            :qty_as_per_fmr_mass,

            :remarks,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_plt_dkn_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM PLT Detail created successfully",
        "mfm_plt_dkn_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_plt_dkn_id}")
def update_mfm_plt_detail(
    mfm_plt_dkn_id: int,
    payload: MFMPLTDetailUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_plt_dkn_id

    query = text("""
        UPDATE mfm_plt_detail_dkn
        SET
            master_id = :master_id,

            omc_with_tank_no = :omc_with_tank_no,
            start_time = :start_time,
            stop_time = :stop_time,

            opening_dip = :opening_dip,
            opening_qty = :opening_qty,

            closing_dip = :closing_dip,
            closing_qty = :closing_qty,

            fmr_opening_net = :fmr_opening_net,
            fmr_opening_gross = :fmr_opening_gross,
            fmr_opening_mass = :fmr_opening_mass,

            fmr_closing_net = :fmr_closing_net,
            fmr_closing_gross = :fmr_closing_gross,
            fmr_closing_mass = :fmr_closing_mass,

            qty_as_per_dip = :qty_as_per_dip,
                 
            qty_as_per_fmr_net = :qty_as_per_fmr_net,
            qty_as_per_fmr_gross = :qty_as_per_fmr_gross,
            qty_as_per_fmr_mass = :qty_as_per_fmr_mass,

            remarks = :remarks ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE mfm_plt_dkn_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="MFM PLT Detail not found"
        )

    return {"message": "MFM PLT Detail updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_plt_dkn_id}")
def delete_mfm_plt_detail(
    mfm_plt_dkn_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_plt_detail_dkn
            WHERE mfm_plt_dkn_id = :id
        """),
        {"id": mfm_plt_dkn_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="MFM PLT Detail not found"
        )

    return {"message": "MFM PLT Detail deleted successfully"}


# @router.get("/by-date", response_model=List[dict])
# def fetch_mfm_log_by_date(
#     log_date: date,
#     db: Session = Depends(get_db)
# ):
#     query = text("""
#         select MPDD.* from mfm_plt_detail_dkn MPDD
# JOIN mfm_log_master_dkn MLMD 
#     ON MPDD.master_id = MLMD.mfm_log_dkn_id
# JOIN logbook_shift_master LSM 
#     ON LSM.ms_logbook_id = MLMD.ms_logbook_id
# WHERE DATE(LSM.created_at) = :log_date;
#     """)

#     result = db.execute(query, {"log_date": log_date}).mappings().all()

#     return result

@router.get("/by-date", response_model=List[dict])
def fetch_mfm_log_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    query = text("""
                    SELECT 
                        MPDD.*,

                        -- Created By Name
                        TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,

                        -- Updated By Name
                        TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

                    FROM mfm_plt_detail_dkn MPDD

                    JOIN mfm_log_master_dkn MLMD
                        ON MPDD.master_id = MLMD.mfm_log_dkn_id

                    JOIN logbook_shift_master LSM
                        ON LSM.ms_logbook_id = MLMD.ms_logbook_id

                    -- Join for created_by
                    LEFT JOIN users u1 
                        ON u1.user_id = MPDD.created_by

                    -- Join for updated_by
                    LEFT JOIN users u2 
                        ON u2.user_id = MPDD.updated_by

                    WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
                    AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    result = db.execute(query, {"log_date": log_date}).mappings().all()

    return result

@router.get("/{mfm_plt_dkn_id}", response_model=dict)
def fetch_mfm_log_by_id(
    mfm_plt_dkn_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            MPDD.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_plt_detail_dkn MPDD

        -- Join for created_by
        LEFT JOIN users u1 
            ON u1.user_id = MPDD.created_by

        -- Join for updated_by
        LEFT JOIN users u2 
            ON u2.user_id = MPDD.updated_by

        WHERE MPDD.mfm_plt_dkn_id = :mfm_plt_dkn_id
    """)

    result = db.execute(
        query, {"mfm_plt_dkn_id": mfm_plt_dkn_id}
    ).mappings().first()

    return result
