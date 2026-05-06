from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from typing import List,Dict, Any

from collections import defaultdict

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-log-hsn2-master",
    tags=["MFM Log HSN2 Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class MFMLogHSN2MasterCreate(BaseModel):
    station: str
    station_in_charge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]

    fqy_changed_from: Optional[str]
    fqy_changed_to: Optional[str]
    fqy_changed_at: Optional[time]

    initial_fmr_of:Optional[str]
    final_fmr:Optional[str]

    initial_fmr_g: Optional[str]
    initial_fmr_n: Optional[str]
    initial_fmr_m: Optional[str]

    final_fmr_g: Optional[str]
    final_fmr_n: Optional[str]
    final_fmr_m: Optional[str]

    sic_name: Optional[str]


    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    ms_logbook_id: Optional[int] = None
class MFMLogHSN2MasterUpdate(MFMLogHSN2MasterCreate):
    pass


# =====================================================
# POST API – CREATE MASTER
# =====================================================

@router.post("")
def create_mfm_log_hsn2_master(
    payload: MFMLogHSN2MasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_hsn2_master (
            station,
            station_in_charge,
            shift,
            start_time,
            log_date,

            fqy_changed_from,
            fqy_changed_to,
            fqy_changed_at,

            initial_fmr_g,
            initial_fmr_n,
            initial_fmr_m,

            final_fmr_g,
            final_fmr_n,
            final_fmr_m,

            sic_name   ,created_at,created_by ,updated_at ,updated_by,ms_logbook_id,initial_fmr_of,final_fmr

        )
        VALUES (
            :station,
            :station_in_charge,
            :shift,
            :start_time,
            :log_date,

            :fqy_changed_from,
            :fqy_changed_to,
            :fqy_changed_at,

            :initial_fmr_g,
            :initial_fmr_n,
            :initial_fmr_m,

            :final_fmr_g,
            :final_fmr_n,
            :final_fmr_m,

            :sic_name,:created_at,:created_by ,:updated_at ,:updated_by,:ms_logbook_id,:initial_fmr_of,:final_fmr

        )
        RETURNING mfm_hsn_two_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM Log HSN2 Master created successfully",
        "mfm_hsn_two_id": result.scalar()
    }


# =====================================================
# PUT API – UPDATE MASTER
# =====================================================

@router.put("/{mfm_hsn_two_id}")
def update_mfm_log_hsn2_master(
    mfm_hsn_two_id: int,
    payload: MFMLogHSN2MasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["mfm_hsn_two_id"] = mfm_hsn_two_id

    query = text("""
        UPDATE mfm_log_hsn2_master
        SET
            station = :station,
            station_in_charge = :station_in_charge,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,

            fqy_changed_from = :fqy_changed_from,
            fqy_changed_to = :fqy_changed_to,
            fqy_changed_at = :fqy_changed_at,
                 
            initial_fmr_of = :initial_fmr_of,
            final_fmr = :final_fmr,

            initial_fmr_g = :initial_fmr_g,
            initial_fmr_n = :initial_fmr_n,
            initial_fmr_m = :initial_fmr_m,

            final_fmr_g = :final_fmr_g,
            final_fmr_n = :final_fmr_n,
            final_fmr_m = :final_fmr_m,

            sic_name = :sic_name ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by, ms_logbook_id=:ms_logbook_id

        WHERE mfm_hsn_two_id = :mfm_hsn_two_id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM Log HSN2 master not found")

    return {"message": "MFM Log HSN2 Master updated successfully"}


# =====================================================
# DELETE API – DELETE MASTER
# =====================================================

@router.delete("/{mfm_hsn_two_id}")
def delete_mfm_log_hsn2_master(
    mfm_hsn_two_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_hsn2_master
            WHERE mfm_hsn_two_id = :id
        """),
        {"id": mfm_hsn_two_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM Log HSN2 master not found")

    return {"message": "MFM Log HSN2 Master deleted successfully"}


# @router.get("/by-date", response_model=List[dict])
# def fetch_mfm_log_by_date(
#     log_date: date,
#     db: Session = Depends(get_db)
# ):
#     query = text("""
#         select MLHM2.* from mfm_log_hsn2_master MLHM2
# JOIN logbook_shift_master LSM 
# 	ON LSM.ms_logbook_id = MLHM2.ms_logbook_id
# WHERE DATE(LSM.created_at) = :log_date
#     """)

#     result = db.execute(query, {"log_date": log_date}).mappings().all()

#     return result

@router.get("/by-date", response_model=List[dict])
def fetch_mfm_log_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT MLHM2.*
        FROM mfm_log_hsn2_master MLHM2
        JOIN logbook_shift_master LSM 
            ON LSM.ms_logbook_id = MLHM2.ms_logbook_id
        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    result = db.execute(query, {"log_date": log_date}).mappings().all()

    return result

@router.get("/by-date-with-entry", response_model=List[Dict[str, Any]])
def fetch_hsn2_log_with_entries_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    # 1. MASTER QUERY
    master_query = text("""
        SELECT MLHM2.*,

            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_hsn2_master MLHM2
        JOIN logbook_shift_master LSM 
            ON LSM.ms_logbook_id = MLHM2.ms_logbook_id

        LEFT JOIN users u1 ON u1.user_id = MLHM2.created_by
        LEFT JOIN users u2 ON u2.user_id = MLHM2.updated_by

        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    masters = db.execute(master_query, {"log_date": log_date}).mappings().all()

    if not masters:
        return []

    master_ids = [m["mfm_hsn_two_id"] for m in masters]

    # 2. CHILD QUERY
    entry_query = text("""
        SELECT MLE2.*,

            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_hsn2_entry MLE2

        LEFT JOIN users u1 ON u1.user_id = MLE2.created_by
        LEFT JOIN users u2 ON u2.user_id = MLE2.updated_by

        WHERE MLE2.master_id = ANY(:master_ids)
    """)

    entries = db.execute(entry_query, {"master_ids": master_ids}).mappings().all()

    # 3. GROUP CHILDREN
    entry_map = defaultdict(list)

    for e in entries:
        entry_map[e["master_id"]].append(dict(e))  # ✅ important

    # 4. FINAL RESPONSE
    final_data = []

    for m in masters:
        m_dict = dict(m)

        mid = m["mfm_hsn_two_id"]

        m_dict["entries"] = entry_map.get(mid, [])

        final_data.append(m_dict)

    return final_data