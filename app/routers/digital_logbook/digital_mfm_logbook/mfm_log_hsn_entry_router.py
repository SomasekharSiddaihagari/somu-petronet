from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from decimal import Decimal

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-log-hsn-entry",
    tags=["MFM Log HSN Entry"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class MFMLogHSNEntryCreate(BaseModel):
    master_id: Optional[int]

    entry_date: Optional[date]
    entry_time: Optional[time]

    pt_1308_pressure: Optional[Decimal]
    pt_1306_pressure: Optional[Decimal]

    flow_rate_net: Optional[Decimal]
    flow_rate_gross: Optional[Decimal]

    hpcl_fcv_opening_1315: Optional[Decimal]

    gross_vol_reading_fqy: Optional[Decimal]
    gross_qty_delivered_kl: Optional[Decimal]

    net_vol_reading_fqy: Optional[Decimal]
    net_qty_delivered_kl: Optional[Decimal]

    mass_reading_mt_fqy: Optional[Decimal]
    mass_qty_delivered_mt_kl: Optional[Decimal]

    product_density: Optional[Decimal]
    product_temp: Optional[Decimal]
    density_15deg: Optional[Decimal]

    hpcl_line_no: Optional[str]
    tank_dip_during_plt_cm: Optional[Decimal]
    qty_as_per_atg: Optional[Decimal]

    diff_atg_fmr: Optional[Decimal]
    sign_shift_ee: Optional[str]

    remarks: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class MFMLogHSNEntryUpdate(MFMLogHSNEntryCreate):
    pass


# =====================================================
# POST API – CREATE ENTRY
# =====================================================

@router.post("")
def create_mfm_log_hsn_entry(
    payload: MFMLogHSNEntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_hsn_entry (
            master_id,
            entry_date,
            entry_time,

            pt_1308_pressure,
            pt_1306_pressure,

            flow_rate_net,
            flow_rate_gross,

            hpcl_fcv_opening_1315,

            gross_vol_reading_fqy,
            gross_qty_delivered_kl,

            net_vol_reading_fqy,
            net_qty_delivered_kl,

            mass_reading_mt_fqy,
            mass_qty_delivered_mt_kl,

            product_density,
            product_temp,
            density_15deg,

            hpcl_line_no,
            tank_dip_during_plt_cm,
            qty_as_per_atg,

            diff_atg_fmr,
            sign_shift_ee,
            remarks   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :entry_date,
            :entry_time,

            :pt_1308_pressure,
            :pt_1306_pressure,

            :flow_rate_net,
            :flow_rate_gross,

            :hpcl_fcv_opening_1315,

            :gross_vol_reading_fqy,
            :gross_qty_delivered_kl,

            :net_vol_reading_fqy,
            :net_qty_delivered_kl,

            :mass_reading_mt_fqy,
            :mass_qty_delivered_mt_kl,

            :product_density,
            :product_temp,
            :density_15deg,

            :hpcl_line_no,
            :tank_dip_during_plt_cm,
            :qty_as_per_atg,

            :diff_atg_fmr,
            :sign_shift_ee,
            :remarks,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_log_hsn_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM Log HSN Entry created successfully",
        "mfm_log_hsn_entry_id": result.scalar()
    }


# =====================================================
# PUT API – UPDATE ENTRY
# =====================================================

@router.put("/{entry_id}")
def update_mfm_log_hsn_entry(
    entry_id: int,
    payload: MFMLogHSNEntryUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE mfm_log_hsn_entry
        SET
            master_id = :master_id,
            entry_date = :entry_date,
            entry_time = :entry_time,

            pt_1308_pressure = :pt_1308_pressure,
            pt_1306_pressure = :pt_1306_pressure,

            flow_rate_net = :flow_rate_net,
            flow_rate_gross = :flow_rate_gross,

            hpcl_fcv_opening_1315 = :hpcl_fcv_opening_1315,

            gross_vol_reading_fqy = :gross_vol_reading_fqy,
            gross_qty_delivered_kl = :gross_qty_delivered_kl,

            net_vol_reading_fqy = :net_vol_reading_fqy,
            net_qty_delivered_kl = :net_qty_delivered_kl,

            mass_reading_mt_fqy = :mass_reading_mt_fqy,
            mass_qty_delivered_mt_kl = :mass_qty_delivered_mt_kl,

            product_density = :product_density,
            product_temp = :product_temp,
            density_15deg = :density_15deg,

            hpcl_line_no = :hpcl_line_no,
            tank_dip_during_plt_cm = :tank_dip_during_plt_cm,
            qty_as_per_atg = :qty_as_per_atg,

            diff_atg_fmr = :diff_atg_fmr,
            sign_shift_ee = :sign_shift_ee,
            remarks = :remarks ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE mfm_log_hsn_entry_id = :entry_id
    """)

    params = payload.dict()
    params["entry_id"] = entry_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM log HSN entry not found")

    return {"message": "MFM Log HSN Entry updated successfully"}

# =====================================================
# GET BY ID
# =====================================================

@router.get("/{entry_id}")
def get_mfm_log_hsn_entry_by_id(
    entry_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT *
        FROM mfm_log_hsn_entry
        WHERE mfm_log_hsn_entry_id = :entry_id
    """)

    result = db.execute(query, {"entry_id": entry_id}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="MFM log HSN entry not found")

    # Convert result to dict
    return dict(result._mapping)


# =====================================================
# DELETE API – DELETE ENTRY
# =====================================================

@router.delete("/{entry_id}")
def delete_mfm_log_hsn_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM mfm_log_hsn_entry
        WHERE mfm_log_hsn_entry_id = :entry_id
    """)

    result = db.execute(query, {"entry_id": entry_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM log HSN entry not found")

    return {"message": "MFM Log HSN Entry deleted successfully"}
