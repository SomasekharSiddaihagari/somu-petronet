from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-log-mlr-entry",
    tags=["MFM Log MLR Entry"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class MFMLogMLREntryCreate(BaseModel):
    master_id: int

    entry_date: Optional[date]
    entry_time: Optional[time]

    mrpl_dip: Optional[str]

    gross: Optional[str]
    net: Optional[str]
    mt: Optional[str]
    den_at_nat: Optional[str]
    temperature: Optional[str]
    den_at_15_deg: Optional[str]

    mrpl_atg: Optional[str]
    mrpl_mfm: Optional[str]

    mrpl_atg_flow: Optional[str]
    mrpl_mfm_flow: Optional[str]

    diff_in_percent: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class MFMLogMLREntryUpdate(MFMLogMLREntryCreate):
    pass


# =====================================================
# POST — CREATE ENTRY
# =====================================================

@router.post("")
def create_mfm_log_mlr_entry(
    payload: MFMLogMLREntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_mlr_entry (
            master_id,
            entry_date,
            entry_time,

            mrpl_dip,

            gross,
            net,
            mt,
            den_at_nat,
            temperature,
            den_at_15_deg,

            mrpl_atg,
            mrpl_mfm,

            mrpl_atg_flow,
            mrpl_mfm_flow,

            diff_in_percent   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :entry_date,
            :entry_time,

            :mrpl_dip,

            :gross,
            :net,
            :mt,
            :den_at_nat,
            :temperature,
            :den_at_15_deg,

            :mrpl_atg,
            :mrpl_mfm,

            :mrpl_atg_flow,
            :mrpl_mfm_flow,

            :diff_in_percent,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_log_mlr_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM Log MLR Entry created successfully",
        "mfm_log_mlr_entry_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_log_mlr_entry_id}")
def update_mfm_log_mlr_entry(
    mfm_log_mlr_entry_id: int,
    payload: MFMLogMLREntryUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_log_mlr_entry_id

    query = text("""
        UPDATE mfm_log_mlr_entry
        SET
            master_id = :master_id,
            entry_date = :entry_date,
            entry_time = :entry_time,

            mrpl_dip = :mrpl_dip,

            gross = :gross,
            net = :net,
            mt = :mt,
            den_at_nat = :den_at_nat,
            temperature = :temperature,
            den_at_15_deg = :den_at_15_deg,

            mrpl_atg = :mrpl_atg,
            mrpl_mfm = :mrpl_mfm,

            mrpl_atg_flow = :mrpl_atg_flow,
            mrpl_mfm_flow = :mrpl_mfm_flow,

            diff_in_percent = :diff_in_percent ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE mfm_log_mlr_entry_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM Log MLR entry not found")

    return {"message": "MFM Log MLR Entry updated successfully"}

# =====================================================
# GET BY ID
# =====================================================
@router.get("/{mfm_log_mlr_entry_id}")
def get_mfm_log_mlr_entry_by_id(
    mfm_log_mlr_entry_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT *
            FROM mfm_log_mlr_entry
            WHERE mfm_log_mlr_entry_id = :id
        """),
        {"id": mfm_log_mlr_entry_id}
    ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="MFM Log MLR entry not found"
        )

    return dict(result._mapping)

# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_mlr_entry_id}")
def delete_mfm_log_mlr_entry(
    mfm_log_mlr_entry_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_mlr_entry
            WHERE mfm_log_mlr_entry_id = :id
        """),
        {"id": mfm_log_mlr_entry_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM Log MLR entry not found")

    return {"message": "MFM Log MLR Entry deleted successfully"}
