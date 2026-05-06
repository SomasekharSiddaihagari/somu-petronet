from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, time
from app.database import get_db
from app.utils.access_service import validate_token
from typing import List
from datetime import date, datetime, time

router = APIRouter(
    prefix="/mfm-log-entry-dkn",
    tags=["MFM Log Entry DKN"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class MFMLogEntryCreate(BaseModel):
    master_id: Optional[int]

    entry_time: Optional[time]

    mainline_density: Optional[float]
    mainline_temp: Optional[float]

    sampling_density: Optional[float]
    sampling_temp: Optional[float]

    manifold_density: Optional[float]
    manifold_temp: Optional[float]

    corresponding_density: Optional[float]

    receiving_tank_no: Optional[str]
    tank_dip: Optional[float]
    tank_quantity: Optional[float]

    flow_gross: Optional[float]
    flow_net: Optional[float]
    flow_mass: Optional[float]

    delivered_fc_klhr: Optional[float]
    delivered_fc_cumu: Optional[float]
    delivered_qd_klhr: Optional[float]
    delivered_qd_cumu: Optional[float]

    delivered_tank_dip: Optional[float]

    remarks: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class MFMLogEntryUpdate(MFMLogEntryCreate):
    pass


# =====================================================
# POST API – CREATE ENTRY
# =====================================================

@router.post("")
def create_mfm_log_entry_dkn(
    payload: MFMLogEntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_entry_dkn (
            master_id,
            entry_time,

            mainline_density,
            mainline_temp,

            sampling_density,
            sampling_temp,

            manifold_density,
            manifold_temp,

            corresponding_density,

            receiving_tank_no,
            tank_dip,
            tank_quantity,

            flow_gross,
            flow_net,
            flow_mass,

            delivered_fc_klhr,
            delivered_fc_cumu,
            delivered_qd_klhr,
            delivered_qd_cumu,

            delivered_tank_dip,
            remarks   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :entry_time,

            :mainline_density,
            :mainline_temp,

            :sampling_density,
            :sampling_temp,

            :manifold_density,
            :manifold_temp,

            :corresponding_density,

            :receiving_tank_no,
            :tank_dip,
            :tank_quantity,

            :flow_gross,
            :flow_net,
            :flow_mass,

            :delivered_fc_klhr,
            :delivered_fc_cumu,
            :delivered_qd_klhr,
            :delivered_qd_cumu,

            :delivered_tank_dip,
            :remarks,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_log_dsk_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM Log Entry created successfully",
        "mfm_log_dsk_id": result.scalar()
    }


# =====================================================
# PUT API – UPDATE ENTRY
# =====================================================

@router.put("/{entry_id}")
def update_mfm_log_entry_dkn(
    entry_id: int,
    payload: MFMLogEntryUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE mfm_log_entry_dkn
        SET
            master_id = :master_id,
            entry_time = :entry_time,

            mainline_density = :mainline_density,
            mainline_temp = :mainline_temp,

            sampling_density = :sampling_density,
            sampling_temp = :sampling_temp,

            manifold_density = :manifold_density,
            manifold_temp = :manifold_temp,

            corresponding_density = :corresponding_density,

            receiving_tank_no = :receiving_tank_no,
            tank_dip = :tank_dip,
            tank_quantity = :tank_quantity,

            flow_gross = :flow_gross,
            flow_net = :flow_net,
            flow_mass = :flow_mass,

            delivered_fc_klhr = :delivered_fc_klhr,
            delivered_fc_cumu = :delivered_fc_cumu,
            delivered_qd_klhr = :delivered_qd_klhr,
            delivered_qd_cumu = :delivered_qd_cumu,

            delivered_tank_dip = :delivered_tank_dip,
            remarks = :remarks ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE mfm_log_dsk_id = :entry_id
    """)

    params = payload.dict()
    params["entry_id"] = entry_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM log entry not found")

    return {"message": "MFM Log Entry updated successfully"}


# =====================================================
# DELETE API – DELETE ENTRY
# =====================================================

@router.delete("/{entry_id}")
def delete_mfm_log_entry_dkn(
    entry_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM mfm_log_entry_dkn
        WHERE mfm_log_dsk_id = :entry_id
    """)

    result = db.execute(query, {"entry_id": entry_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM log entry not found")

    return {"message": "MFM Log Entry deleted successfully"}


# @router.get("/by-date", response_model=List[dict])
# def fetch_mfm_log_by_date(
#     log_date: date,
#     db: Session = Depends(get_db)
# ):
#     query = text("""
#         SELECT MLED.*
# FROM mfm_log_entry_dkn MLED
# JOIN mfm_log_master_dkn MLMD 
#     ON MLED.master_id = MLMD.mfm_log_dkn_id
# JOIN logbook_shift_master LSM 
#     ON LSM.ms_logbook_id = MLMD.ms_logbook_id
# WHERE DATE(LSM.created_at) =:log_date;
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
            MLED.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_entry_dkn MLED

        JOIN mfm_log_master_dkn MLMD 
            ON MLED.master_id = MLMD.mfm_log_dkn_id

        JOIN logbook_shift_master LSM 
            ON LSM.ms_logbook_id = MLMD.ms_logbook_id

        -- Join for created_by (entry table)
        LEFT JOIN users u1 
            ON u1.user_id = MLED.created_by

        -- Join for updated_by (entry table)
        LEFT JOIN users u2 
            ON u2.user_id = MLED.updated_by

        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    result = db.execute(query, {"log_date": log_date}).mappings().all()

    return result


@router.get("/{mfm_log_dkn_entryid}", response_model=dict)
def fetch_mfm_log_by_id(
    mfm_log_dkn_entryid: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            MLED.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_entry_dkn MLED

        -- Join for created_by
        LEFT JOIN users u1 
            ON u1.user_id = MLED.created_by

        -- Join for updated_by
        LEFT JOIN users u2 
            ON u2.user_id = MLED.updated_by

        WHERE MLED.mfm_log_dsk_id = :mfm_log_dkn_entryid
    """)

    result = db.execute(
        query, {"mfm_log_dkn_entryid": mfm_log_dkn_entryid}
    ).mappings().first()

    return result