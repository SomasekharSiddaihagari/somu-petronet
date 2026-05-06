from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-log-hsn2-entry",
    tags=["MFM Log HSN2 Entry"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class MFMLogHSN2EntryCreate(BaseModel):
    master_id: int

    entry_date: Optional[date]
    entry_time: Optional[time]

    pump_inlet_header_pr: Optional[str]
    pump_outlet_header_pr: Optional[str]
    digital_fcva_opening: Optional[str]

    flow_rate_net: Optional[str]
    flow_rate_gross: Optional[str]

    gross_vol_fqy: Optional[str]
    gross_qty_per_gross: Optional[str]

    nett_vol_fqy: Optional[str]
    nett_qty_per_gross: Optional[str]

    mass_vol_fqy: Optional[str]
    qty_delivered_mt: Optional[str]

    # density: Optional[str]
    # temperature: Optional[str]
    # density_15_deg: Optional[str]

    tank_corr_during_cm: Optional[float] 
    ci_pump: Optional[str]
    ci_line_pr: Optional[float]
    stroke_len: Optional[float]
    ci_dosing_rate: Optional[float]

    sign_of_shift_ee: Optional[str]
    remarks: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class MFMLogHSN2EntryUpdate(MFMLogHSN2EntryCreate):
    pass


# =====================================================
# POST API – CREATE ENTRY
# =====================================================

@router.post("")
def create_mfm_log_hsn2_entry(
    payload: MFMLogHSN2EntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_hsn2_entry (
            master_id,
            entry_date,
            entry_time,

            pump_inlet_header_pr,
            pump_outlet_header_pr,
            digital_fcva_opening,

            flow_rate_net,
            flow_rate_gross,

            gross_vol_fqy,
            gross_qty_per_gross,

            nett_vol_fqy,
            nett_qty_per_gross,

            mass_vol_fqy,
            qty_delivered_mt,

            tank_corr_during_cm,
            ci_pump,
            ci_line_pr,
            stroke_len,
            ci_dosing_rate,

            sign_of_shift_ee,
            remarks   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :entry_date,
            :entry_time,

            :pump_inlet_header_pr,
            :pump_outlet_header_pr,
            :digital_fcva_opening,

            :flow_rate_net,
            :flow_rate_gross,

            :gross_vol_fqy,
            :gross_qty_per_gross,

            :nett_vol_fqy,
            :nett_qty_per_gross,

            :mass_vol_fqy,
            :qty_delivered_mt,

            :tank_corr_during_cm,
            :ci_pump,
            :ci_line_pr,
            :stroke_len,
            :ci_dosing_rate,

            :sign_of_shift_ee,
            :remarks,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_log_hsn2_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM Log HSN2 Entry created successfully",
        "mfm_log_hsn2_entry_id": result.scalar()
    }


# =====================================================
# PUT API – UPDATE ENTRY
# =====================================================

@router.put("/{entry_id}")
def update_mfm_log_hsn2_entry(
    entry_id: int,
    payload: MFMLogHSN2EntryUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["entry_id"] = entry_id

    query = text("""
        UPDATE mfm_log_hsn2_entry
        SET
            master_id = :master_id,
            entry_date = :entry_date,
            entry_time = :entry_time,

            pump_inlet_header_pr = :pump_inlet_header_pr,
            pump_outlet_header_pr = :pump_outlet_header_pr,
            digital_fcva_opening = :digital_fcva_opening,

            flow_rate_net = :flow_rate_net,
            flow_rate_gross = :flow_rate_gross,

            gross_vol_fqy = :gross_vol_fqy,
            gross_qty_per_gross = :gross_qty_per_gross,

            nett_vol_fqy = :nett_vol_fqy,
            nett_qty_per_gross = :nett_qty_per_gross,

            mass_vol_fqy = :mass_vol_fqy,
            qty_delivered_mt = :qty_delivered_mt,

            tank_corr_during_cm = :tank_corr_during_cm,
            ci_pump = :ci_pump,
            ci_line_pr = :ci_line_pr,
            stroke_len = :stroke_len,
            ci_dosing_rate = :ci_dosing_rate,

            sign_of_shift_ee = :sign_of_shift_ee,
            remarks = :remarks ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE mfm_log_hsn2_entry_id = :entry_id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM Log HSN2 entry not found")

    return {"message": "MFM Log HSN2 Entry updated successfully"}

# =====================================================
# GET BY ID
# =====================================================

@router.get("/{entry_id}")
def get_mfm_log_hsn2_entry_by_id(
    entry_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT *
            FROM mfm_log_hsn2_entry
            WHERE mfm_log_hsn2_entry_id = :entry_id
        """),
        {"entry_id": entry_id}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="MFM Log HSN2 entry not found")

    return dict(result._mapping)


# =====================================================
# DELETE API – DELETE ENTRY
# =====================================================

@router.delete("/{entry_id}")
def delete_mfm_log_hsn2_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_hsn2_entry
            WHERE mfm_log_hsn2_entry_id = :entry_id
        """),
        {"entry_id": entry_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM Log HSN2 entry not found")

    return {"message": "MFM Log HSN2 Entry deleted successfully"}
