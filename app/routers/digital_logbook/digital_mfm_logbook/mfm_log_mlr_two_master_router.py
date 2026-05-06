from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

from typing import List,Dict, Any
from collections import defaultdict

router = APIRouter(
    prefix="/mfm-log-mlr-two-master",
    tags=["ERV Log MLR Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class ERVLogMLRMasterCreate(BaseModel):
    station: str
    station_in_charge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]

    mrpl_qc_den_15c: Optional[str]
    flash_point_fbp: Optional[str]
    kv: Optional[str]

    ci: Optional[str]
    ron_no: Optional[str]
    cn: Optional[str]

    mainline_pump_no: Optional[str]
    booster_pump: Optional[str]

    total_sulphur: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class ERVLogMLRMasterUpdate(ERVLogMLRMasterCreate):
    pass


# =====================================================
# POST — CREATE MASTER
# =====================================================

@router.post("")
def create_erv_log_mlr_master(
    payload: ERVLogMLRMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_mlr_master_two (
            station,
            station_in_charge,
            shift,
            start_time,
            log_date,

            mrpl_qc_den_15c,
            flash_point_fbp,
            kv,

            ci,
            ron_no,
            cn,

            mainline_pump_no,
            booster_pump,
            total_sulphur   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :station,
            :station_in_charge,
            :shift,
            :start_time,
            :log_date,

            :mrpl_qc_den_15c,
            :flash_point_fbp,
            :kv,

            :ci,
            :ron_no,
            :cn,

            :mainline_pump_no,
            :booster_pump,
            :total_sulphur,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_log_mlr_two_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "ERV Log MLR Master created successfully",
        "mfm_log_mlr_two_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_log_mlr_two_id}")
def update_erv_log_mlr_master(
    mfm_log_mlr_two_id: int,
    payload: ERVLogMLRMasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_log_mlr_two_id

    query = text("""
        UPDATE mfm_log_mlr_master_two
        SET
            station = :station,
            station_in_charge = :station_in_charge,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,

            mrpl_qc_den_15c = :mrpl_qc_den_15c,
            flash_point_fbp = :flash_point_fbp,
            kv = :kv,

            ci = :ci,
            ron_no = :ron_no,
            cn = :cn,

            mainline_pump_no = :mainline_pump_no,
            booster_pump = :booster_pump,
            total_sulphur = :total_sulphur ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE mfm_log_mlr_two_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="ERV Log MLR master not found"
        )

    return {"message": "ERV Log MLR Master updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_mlr_two_id}")
def delete_erv_log_mlr_master(
    mfm_log_mlr_two_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_mlr_master_two
            WHERE mfm_log_mlr_two_id = :id
        """),
        {"id": mfm_log_mlr_two_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="ERV Log MLR master not found"
        )

    return {"message": "ERV Log MLR Master deleted successfully"}


# =====================================================
# GET BY DATE WITH CHILD DATA
# =====================================================
@router.get("/by-date-with-entry", response_model=List[Dict[str, Any]])
def fetch_mfm_log_mlr_two_by_date_with_entries(
    log_date: date,
    db: Session = Depends(get_db)
):
    # 1️⃣ MASTER QUERY
    master_query = text("""
        SELECT M.*,

            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mfm_log_mlr_master_two M

        LEFT JOIN users u1 ON u1.user_id = M.created_by
        LEFT JOIN users u2 ON u2.user_id = M.updated_by

        WHERE M.created_at >= :log_date + INTERVAL '7 hour'
        AND M.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    masters = db.execute(master_query, {"log_date": log_date}).mappings().all()

    if not masters:
        return []

    # ✅ PRIMARY KEY
    master_ids = [m["mfm_log_mlr_two_id"] for m in masters]

    # 2️⃣ CHILD QUERY
    entry_query = text("""
        SELECT E.*,

            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mfm_log_mlr_two_entry E

        LEFT JOIN users u1 ON u1.user_id = E.created_by
        LEFT JOIN users u2 ON u2.user_id = E.updated_by

        WHERE E.master_id = ANY(:master_ids)
    """)

    entries = db.execute(entry_query, {"master_ids": master_ids}).mappings().all()

    # 3️⃣ GROUP CHILDREN
    from collections import defaultdict
    entry_map = defaultdict(list)

    for e in entries:
        entry_map[e["master_id"]].append(dict(e))

    # 4️⃣ FINAL RESPONSE
    final_data = []

    for m in masters:
        m_dict = dict(m)

        mid = m["mfm_log_mlr_two_id"]

        m_dict["entries"] = entry_map.get(mid, [])

        final_data.append(m_dict)

    return final_data