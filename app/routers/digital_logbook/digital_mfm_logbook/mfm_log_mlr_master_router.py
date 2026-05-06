from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

from typing import List, Dict, Any
from collections import defaultdict

router = APIRouter(
    prefix="/mfm-log-mlr-master",
    tags=["MFM Log MLR Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class MFMLogMLRMasterCreate(BaseModel):
    station: str
    station_in_charge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]

    tank_no: Optional[str]
    hpcl_batch_no: Optional[str]
    mrpl_batch_no: Optional[str]
    pmhbl_batch_no: Optional[str]

    product_name: Optional[str]
    cycle_no: Optional[str]
    tank_temp: Optional[str]
    tank_factor: Optional[str]

    flow_meter: Optional[str]

    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    ms_logbook_id: Optional[int] = None


class MFMLogMLRMasterUpdate(MFMLogMLRMasterCreate):
    pass


# =====================================================
# POST — CREATE MASTER
# =====================================================

@router.post("")
def create_mfm_log_mlr_master(
    payload: MFMLogMLRMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_mlr_master (
            station,
            station_in_charge,
            shift,
            start_time,
            log_date,

            tank_no,
            hpcl_batch_no,
            mrpl_batch_no,
            pmhbl_batch_no,

            product_name,
            cycle_no,
            tank_temp,
            tank_factor,

            flow_meter,

            created_at,
            created_by,
            ms_logbook_id
                 
        )
        VALUES (
            :station,
            :station_in_charge,
            :shift,
            :start_time,
            :log_date,

            :tank_no,
            :hpcl_batch_no,
            :mrpl_batch_no,
            :pmhbl_batch_no,

            :product_name,
            :cycle_no,
            :tank_temp,
            :tank_factor,

            :flow_meter,

            NOW(),
            :created_by,
            :ms_logbook_id
        )
        RETURNING mfm_log_mlr_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MLR Master created successfully",
        "mfm_log_mlr_id": result.scalar()
    }

# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_log_mlr_id}")
def update_mfm_log_mlr_master(
    mfm_log_mlr_id: int,
    payload: MFMLogMLRMasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_log_mlr_id

    query = text("""
        UPDATE mfm_log_mlr_master
        SET
            station = :station,
            station_in_charge = :station_in_charge,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,

            tank_no = :tank_no,
            hpcl_batch_no = :hpcl_batch_no,
            mrpl_batch_no = :mrpl_batch_no,
            pmhbl_batch_no = :pmhbl_batch_no,

            product_name = :product_name,
            cycle_no = :cycle_no,
            tank_temp = :tank_temp,
            tank_factor = :tank_factor,

            flow_meter = :flow_meter,

            updated_at = NOW(),
            updated_by = :updated_by

        WHERE mfm_log_mlr_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Master not found")

    return {"message": "MLR Master updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_mlr_id}")
def delete_mfm_log_mlr_master(
    mfm_log_mlr_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_mlr_master
            WHERE mfm_log_mlr_id = :id
        """),
        {"id": mfm_log_mlr_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Master not found")

    return {"message": "MLR Master deleted successfully"}

# =====================================================
# GET BY DATE
# =====================================================
@router.get("/by-date-with-entry", response_model=List[Dict[str, Any]])
def fetch_mfm_log_mlr_by_date_with_entries(
    log_date: date,
    db: Session = Depends(get_db)
):
    # 1️⃣ MASTER QUERY (FIXED TABLE)
    master_query = text("""
        SELECT MLHM.*,

            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mfm_log_mlr_master MLHM

        JOIN logbook_shift_master LSM
            ON LSM.ms_logbook_id = MLHM.ms_logbook_id

        LEFT JOIN users u1 ON u1.user_id = MLHM.created_by
        LEFT JOIN users u2 ON u2.user_id = MLHM.updated_by

        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    masters = db.execute(master_query, {"log_date": log_date}).mappings().all()

    if not masters:
        return []

    # ✅ FIXED PRIMARY KEY
    master_ids = [m["mfm_log_mlr_id"] for m in masters]

    # 2️⃣ CHILD QUERY (CORRECT TABLE)
    entry_query = text("""
        SELECT MLE.*,

            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mfm_log_mlr_entry MLE

        LEFT JOIN users u1 ON u1.user_id = MLE.created_by
        LEFT JOIN users u2 ON u2.user_id = MLE.updated_by

        WHERE MLE.master_id = ANY(:master_ids)
    """)

    entries = db.execute(entry_query, {"master_ids": master_ids}).mappings().all()

    # 3️⃣ GROUP CHILDREN
    from collections import defaultdict
    entry_map = defaultdict(list)

    for e in entries:
        entry_map[e["master_id"]].append(dict(e))  # ✅ important

    # 4️⃣ FINAL RESPONSE
    final_data = []

    for m in masters:
        m_dict = dict(m)

        mid = m["mfm_log_mlr_id"]

        m_dict["entries"] = entry_map.get(mid, [])

        final_data.append(m_dict)

    return final_data