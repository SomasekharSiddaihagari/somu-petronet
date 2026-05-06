from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-log-ner-entry",
    tags=["MFM Log NER Entry"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class MFMLogNEREntryCreate(BaseModel):
    master_id: Optional[int]

    entry_date: Optional[date]
    entry_time: Optional[time]

    entry_date_two: Optional[date]
    entry_time_two: Optional[time]

    product: Optional[str]
    batch: Optional[str]

    density: Optional[float]
    temperature: Optional[float]

    pump_abc: Optional[str]
    lube_oil_pressure: Optional[float]
    lube_oil_diff_pressure: Optional[float]
    diff_basket_filter_ab: Optional[float]

    fmr_gross: Optional[float]
    fmr_net: Optional[float]
    fmr_mass: Optional[float]

    flow_rate_net: Optional[float]
    flow_rate_mass: Optional[float]

    pcv_percent: Optional[float]

    ic_voltage_1: Optional[float]
    ic_voltage_2: Optional[float]

    load_current_r: Optional[float]
    load_current_y: Optional[float]
    load_current_b: Optional[float]

    frequency: Optional[float]
    load_percent: Optional[float]

    remarks: Optional[str]


    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
class MFMLogNEREntryUpdate(MFMLogNEREntryCreate):
    pass


# =====================================================
# POST — CREATE ENTRY
# =====================================================

@router.post("")
def create_mfm_log_ner_entry(
    payload: MFMLogNEREntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_ner_entry (
            master_id,

            entry_date,
            entry_time,
            entry_date_two,
            entry_time_two,

            product,
            batch,

            density,
            temperature,

            pump_abc,
            lube_oil_pressure,
            lube_oil_diff_pressure,
            diff_basket_filter_ab,

            fmr_gross,
            fmr_net,
            fmr_mass,

            flow_rate_net,
            flow_rate_mass,

            pcv_percent,

            ic_voltage_1,
            ic_voltage_2,

            load_current_r,
            load_current_y,
            load_current_b,

            frequency,
            load_percent,

            remarks   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,

            :entry_date,
            :entry_time,
            :entry_date_two,
            :entry_time_two,

            :product,
            :batch,

            :density,
            :temperature,

            :pump_abc,
            :lube_oil_pressure,
            :lube_oil_diff_pressure,
            :diff_basket_filter_ab,

            :fmr_gross,
            :fmr_net,
            :fmr_mass,

            :flow_rate_net,
            :flow_rate_mass,

            :pcv_percent,

            :ic_voltage_1,
            :ic_voltage_2,

            :load_current_r,
            :load_current_y,
            :load_current_b,

            :frequency,
            :load_percent,

            :remarks,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_log_ner_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM Log NER Entry created successfully",
        "mfm_log_ner_entry_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_log_ner_entry_id}")
def update_mfm_log_ner_entry(
    mfm_log_ner_entry_id: int,
    payload: MFMLogNEREntryUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_log_ner_entry_id

    query = text("""
        UPDATE mfm_log_ner_entry
        SET
            master_id = :master_id,

            entry_date = :entry_date,
            entry_time = :entry_time,
            entry_date_two = :entry_date_two,
            entry_time_two = :entry_time_two,

            product = :product,
            batch = :batch,

            density = :density,
            temperature = :temperature,

            pump_abc = :pump_abc,
            lube_oil_pressure = :lube_oil_pressure,
            lube_oil_diff_pressure = :lube_oil_diff_pressure,
            diff_basket_filter_ab = :diff_basket_filter_ab,

            fmr_gross = :fmr_gross,
            fmr_net = :fmr_net,
            fmr_mass = :fmr_mass,

            flow_rate_net = :flow_rate_net,
            flow_rate_mass = :flow_rate_mass,

            pcv_percent = :pcv_percent,

            ic_voltage_1 = :ic_voltage_1,
            ic_voltage_2 = :ic_voltage_2,

            load_current_r = :load_current_r,
            load_current_y = :load_current_y,
            load_current_b = :load_current_b,

            frequency = :frequency,
            load_percent = :load_percent,

            remarks = :remarks ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE mfm_log_ner_entry_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="MFM Log NER entry not found"
        )

    return {"message": "MFM Log NER Entry updated successfully"}

# =====================================================
# GET BY ID
# =====================================================
@router.get("/{mfm_log_ner_entry_id}")
def get_mfm_log_ner_entry_by_id(
    mfm_log_ner_entry_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT *
            FROM mfm_log_ner_entry
            WHERE mfm_log_ner_entry_id = :id
        """),
        {"id": mfm_log_ner_entry_id}
    ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="MFM Log NER entry not found"
        )

    return dict(result._mapping)


# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_ner_entry_id}")
def delete_mfm_log_ner_entry(
    mfm_log_ner_entry_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_ner_entry
            WHERE mfm_log_ner_entry_id = :id
        """),
        {"id": mfm_log_ner_entry_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="MFM Log NER entry not found"
        )

    return {"message": "MFM Log NER Entry deleted successfully"}
