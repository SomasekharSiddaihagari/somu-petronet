from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-log-mlr-two-entry",
    tags=["ERV Log MLR Entry"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class ERVLogMLREntryCreate(BaseModel):
    master_id: int

    entry_date: Optional[date]
    entry_time: Optional[time]

    pump_disch_hdr_press_1108: Optional[str]
    pump_inlet_press_1104: Optional[str]
    press_after_pcv_1110: Optional[str]
    pcv_open_percent: Optional[str]

    water_temp: Optional[str]

    mtr_de_nde_casing_temp_1: Optional[str]
    pump_de_nde_vibration_1: Optional[str]
    thrust_brg_xy: Optional[str]

    water_temp_2: Optional[str]

    mtr_de_nde_casing_temp_2: Optional[str]
    pump_de_vibration_xy: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class ERVLogMLREntryUpdate(ERVLogMLREntryCreate):
    pass


# =====================================================
# POST — CREATE ENTRY
# =====================================================

@router.post("")
def create_erv_log_mlr_entry(
    payload: ERVLogMLREntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_mlr_two_entry (
            master_id,
            entry_date,
            entry_time,

            pump_disch_hdr_press_1108,
            pump_inlet_press_1104,
            press_after_pcv_1110,
            pcv_open_percent,

            water_temp,

            mtr_de_nde_casing_temp_1,
            pump_de_nde_vibration_1,
            thrust_brg_xy,

            water_temp_2,

            mtr_de_nde_casing_temp_2,
            pump_de_vibration_xy   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :entry_date,
            :entry_time,

            :pump_disch_hdr_press_1108,
            :pump_inlet_press_1104,
            :press_after_pcv_1110,
            :pcv_open_percent,

            :water_temp,

            :mtr_de_nde_casing_temp_1,
            :pump_de_nde_vibration_1,
            :thrust_brg_xy,

            :water_temp_2,

            :mtr_de_nde_casing_temp_2,
            :pump_de_vibration_xy,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_log_mlr_two_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "ERV Log MLR Entry created successfully",
        "mfm_log_mlr_two_entry_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_log_mlr_two_entry_id}")
def update_erv_log_mlr_entry(
    mfm_log_mlr_two_entry_id: int,
    payload: ERVLogMLREntryUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_log_mlr_two_entry_id

    query = text("""
        UPDATE mfm_log_mlr_two_entry
        SET
            master_id = :master_id,
            entry_date = :entry_date,
            entry_time = :entry_time,

            pump_disch_hdr_press_1108 = :pump_disch_hdr_press_1108,
            pump_inlet_press_1104 = :pump_inlet_press_1104,
            press_after_pcv_1110 = :press_after_pcv_1110,
            pcv_open_percent = :pcv_open_percent,

            water_temp = :water_temp,

            mtr_de_nde_casing_temp_1 = :mtr_de_nde_casing_temp_1,
            pump_de_nde_vibration_1 = :pump_de_nde_vibration_1,
            thrust_brg_xy = :thrust_brg_xy,

            water_temp_2 = :water_temp_2,

            mtr_de_nde_casing_temp_2 = :mtr_de_nde_casing_temp_2,
            pump_de_vibration_xy = :pump_de_vibration_xy ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE mfm_log_mlr_two_entry_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="ERV Log MLR entry not found"
        )

    return {"message": "ERV Log MLR Entry updated successfully"}

# =====================================================
# GET BY ID
# =====================================================
@router.get("/{mfm_log_mlr_two_entry_id}")
def get_mfm_log_mlr_two_entry_by_id(
    mfm_log_mlr_two_entry_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT *
            FROM mfm_log_mlr_two_entry
            WHERE mfm_log_mlr_two_entry_id = :id
        """),
        {"id": mfm_log_mlr_two_entry_id}
    ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="ERV Log MLR entry not found"
        )

    return dict(result._mapping)

# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_mlr_two_entry_id}")
def delete_erv_log_mlr_entry(
    mfm_log_mlr_two_entry_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_mlr_two_entry
            WHERE mfm_log_mlr_two_entry_id = :id
        """),
        {"id": mfm_log_mlr_two_entry_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="ERV Log MLR entry not found"
        )

    return {"message": "ERV Log MLR Entry deleted successfully"}
