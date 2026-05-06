from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from typing import List,Dict, Any

from app.database import get_db
from app.utils.access_service import validate_token

from collections import defaultdict


router = APIRouter(
    prefix="/mfm-log-hsn-master",
    tags=["MFM Log HSN Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS
# =====================================================

class MFMLogHSNMasterCreate(BaseModel):
    station: Optional[str]
    station_in_charge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]
    document_no: Optional[str]

    left_initial_tank_no: Optional[str]
    left_initial_dip_in_cms: Optional[float]
    left_tank_co_time: Optional[time]
    left_final_tank_dip_in_cms: Optional[float]
    left_new_tank_initial_dip_in_cm: Optional[float]
    left_new_tank_no: Optional[str]
    left_co_fm_reading_gross: Optional[float]
    left_co_fm_reading_nett: Optional[float]
    left_co_fm_reading_mass: Optional[float]

    left2_initial_tank_no: Optional[str]
    left2_initial_dip_in_cms: Optional[float]
    left2_tank_co_time: Optional[time]
    left2_final_tank_dip_in_cms: Optional[float]
    left2_new_tank_initial_dip_in_cm: Optional[float]
    left2_new_tank_no: Optional[str]
    left2_co_fm_reading_gross: Optional[float]
    left2_co_fm_reading_nett: Optional[float]
    left2_co_fm_reading_mass: Optional[float]

    right_initial_tank_no: Optional[str]
    right_initial_dip_in_cms: Optional[float]
    right_tank_co_time: Optional[time]
    right_final_tank_dip_in_cms: Optional[float]
    right_new_tank_initial_dip_in_cm: Optional[float]
    right_new_tank_no: Optional[str]
    right_co_fm_reading_gross: Optional[float]
    right_co_fm_reading_nett: Optional[float]
    right_co_fm_reading_mass: Optional[float]

    faq_changed_from: Optional[str]
    faq_changed_to: Optional[str]
    faq_changed_at: Optional[time]   

    final_fmr:Optional[str] = None
    
    initial_fmr_g: Optional[float]
    initial_fmr_n: Optional[float]
    initial_fmr_m: Optional[float]
    
    initial_fmr_of:Optional[str] = None

    final_fmr_g: Optional[float]
    final_fmr_n: Optional[float]
    final_fmr_m: Optional[float]    

    sic_name: Optional[str]

    # b_left_initial_tank_no: Optional[str]
    # b_left_initial_dip_in_cms: Optional[float]
    # b_left_tank_co_time: Optional[time]
    # b_left_final_tank_dip_in_cms: Optional[float]
    # b_left_new_tank_initial_dip_in_cm: Optional[float]
    # b_left_new_tank_no: Optional[str]
    # b_left_co_fm_reading_gross: Optional[float]
    # b_left_co_fm_reading_nett: Optional[float]
    # b_left_co_fm_reading_mass: Optional[float]

    # b_left2_initial_tank_no: Optional[str]
    # b_left2_initial_dip_in_cms: Optional[float]
    # b_left2_tank_co_time: Optional[time]
    # b_left2_final_tank_dip_in_cms: Optional[float]
    # b_left2_new_tank_initial_dip_in_cm: Optional[float]
    # b_left2_new_tank_no: Optional[str]
    # b_left2_co_fm_reading_gross: Optional[float]
    # b_left2_co_fm_reading_nett: Optional[float]
    # b_left2_co_fm_reading_mass: Optional[float]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    ms_logbook_id: Optional[int] = None
    

class MFMLogHSNMasterUpdate(MFMLogHSNMasterCreate):
    pass


# =====================================================
# POST — CREATE
# =====================================================

@router.post("")
def create_mfm_log_hsn_master(
    payload: MFMLogHSNMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
    INSERT INTO mfm_log_hsn_master (
        station, station_in_charge, shift, start_time, log_date, document_no,

        left_initial_tank_no, left_initial_dip_in_cms, left_tank_co_time,
        left_final_tank_dip_in_cms, left_new_tank_initial_dip_in_cm, left_new_tank_no,
        left_co_fm_reading_gross, left_co_fm_reading_nett, left_co_fm_reading_mass,

        left2_initial_tank_no, left2_initial_dip_in_cms, left2_tank_co_time,
        left2_final_tank_dip_in_cms, left2_new_tank_initial_dip_in_cm, left2_new_tank_no,
        left2_co_fm_reading_gross, left2_co_fm_reading_nett, left2_co_fm_reading_mass,

        right_initial_tank_no, right_initial_dip_in_cms, right_tank_co_time,
        right_final_tank_dip_in_cms, right_new_tank_initial_dip_in_cm, right_new_tank_no,
        right_co_fm_reading_gross, right_co_fm_reading_nett, right_co_fm_reading_mass,

        faq_changed_from, faq_changed_to, faq_changed_at,

        initial_fmr_g, initial_fmr_n, initial_fmr_m,
        final_fmr_g, final_fmr_n, final_fmr_m,

        sic_name, created_at, created_by, updated_at, updated_by,
        ms_logbook_id, initial_fmr_of, final_fmr
    )
    VALUES (
        :station, :station_in_charge, :shift, :start_time, :log_date, :document_no,

        :left_initial_tank_no, :left_initial_dip_in_cms, :left_tank_co_time,
        :left_final_tank_dip_in_cms, :left_new_tank_initial_dip_in_cm, :left_new_tank_no,
        :left_co_fm_reading_gross, :left_co_fm_reading_nett, :left_co_fm_reading_mass,

        :left2_initial_tank_no, :left2_initial_dip_in_cms, :left2_tank_co_time,
        :left2_final_tank_dip_in_cms, :left2_new_tank_initial_dip_in_cm, :left2_new_tank_no,
        :left2_co_fm_reading_gross, :left2_co_fm_reading_nett, :left2_co_fm_reading_mass,

        :right_initial_tank_no, :right_initial_dip_in_cms, :right_tank_co_time,
        :right_final_tank_dip_in_cms, :right_new_tank_initial_dip_in_cm, :right_new_tank_no,
        :right_co_fm_reading_gross, :right_co_fm_reading_nett, :right_co_fm_reading_mass,

        :faq_changed_from, :faq_changed_to, :faq_changed_at,

        :initial_fmr_g, :initial_fmr_n, :initial_fmr_m,
        :final_fmr_g, :final_fmr_n, :final_fmr_m,

        :sic_name, :created_at, :created_by, :updated_at, :updated_by,
        :ms_logbook_id, :initial_fmr_of, :final_fmr
    )
    RETURNING mfm_log_hsn_id
""")

    result = db.execute(query, payload.dict())
    db.commit()

    return {"mfm_log_hsn_id": result.scalar()}


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_log_hsn_id}")
def update_mfm_log_hsn_master(
    mfm_log_hsn_id: int,
    payload: MFMLogHSNMasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_log_hsn_id

    query = text("""
        UPDATE mfm_log_hsn_master
        SET
            station = :station,
            station_in_charge = :station_in_charge,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,
            document_no = :document_no,

            left_initial_tank_no = :left_initial_tank_no,
            left_initial_dip_in_cms = :left_initial_dip_in_cms,
            left_tank_co_time = :left_tank_co_time,
            left_final_tank_dip_in_cms = :left_final_tank_dip_in_cms,
            left_new_tank_initial_dip_in_cm = :left_new_tank_initial_dip_in_cm,
            left_new_tank_no = :left_new_tank_no,
            left_co_fm_reading_gross = :left_co_fm_reading_gross,
            left_co_fm_reading_nett = :left_co_fm_reading_nett,
            left_co_fm_reading_mass = :left_co_fm_reading_mass,

            left2_initial_tank_no = :left2_initial_tank_no,
            left2_initial_dip_in_cms = :left2_initial_dip_in_cms,
            left2_tank_co_time = :left2_tank_co_time,
            left2_final_tank_dip_in_cms = :left2_final_tank_dip_in_cms,
            left2_new_tank_initial_dip_in_cm = :left2_new_tank_initial_dip_in_cm,
            left2_new_tank_no = :left2_new_tank_no,
            left2_co_fm_reading_gross = :left2_co_fm_reading_gross,
            left2_co_fm_reading_nett = :left2_co_fm_reading_nett,
            left2_co_fm_reading_mass = :left2_co_fm_reading_mass,

            right_initial_tank_no = :right_initial_tank_no,
            right_initial_dip_in_cms = :right_initial_dip_in_cms,
            right_tank_co_time = :right_tank_co_time,
            right_final_tank_dip_in_cms = :right_final_tank_dip_in_cms,
            right_new_tank_initial_dip_in_cm = :right_new_tank_initial_dip_in_cm,
            right_new_tank_no = :right_new_tank_no,
            right_co_fm_reading_gross = :right_co_fm_reading_gross,
            right_co_fm_reading_nett = :right_co_fm_reading_nett,
            right_co_fm_reading_mass = :right_co_fm_reading_mass,

            faq_changed_from = :faq_changed_from,
            faq_changed_to = :faq_changed_to,
            faq_changed_at = :faq_changed_at,

            initial_fmr_g = :initial_fmr_g,
            initial_fmr_n = :initial_fmr_n,
            initial_fmr_m = :initial_fmr_m,
            final_fmr_g = :final_fmr_g,
            final_fmr_n = :final_fmr_n,
            final_fmr_m = :final_fmr_m,

            sic_name = :sic_name,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by, ms_logbook_id=:ms_logbook_id,initial_fmr_of=:initial_fmr_of,final_fmr=:final_fmr

        WHERE mfm_log_hsn_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(404, "Record not found")

    return {"message": "Updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_hsn_id}")
def delete_mfm_log_hsn_master(mfm_log_hsn_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("DELETE FROM mfm_log_hsn_master WHERE mfm_log_hsn_id = :id"),
        {"id": mfm_log_hsn_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(404, "Record not found")

    return {"message": "Deleted successfully"}


# @router.get("/by-date", response_model=List[dict])
# def fetch_mfm_log_by_date(
#     log_date: date,
#     db: Session = Depends(get_db)
# ):
#     query = text("""
#         select MLHM.* from mfm_log_hsn_master MLHM
# JOIN logbook_shift_master LSM 
# 	ON LSM.ms_logbook_id = MLHM.ms_logbook_id
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
        SELECT MLHM.*
        FROM mfm_log_hsn_master MLHM
        JOIN logbook_shift_master LSM
            ON LSM.ms_logbook_id = MLHM.ms_logbook_id
        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    result = db.execute(query, {"log_date": log_date}).mappings().all()

    return result

@router.get("/by-date-with-entry", response_model=List[Dict[str, Any]])
def fetch_hsn_log_with_entries_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    # 1. MASTER QUERY
    master_query = text("""
        SELECT MLHM.*,

            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_hsn_master MLHM
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

    master_ids = [m["mfm_log_hsn_id"] for m in masters]

    # 2. CHILD QUERY (ENTRY)
    entry_query = text("""
        SELECT MLE.*,

            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_hsn_entry MLE

        LEFT JOIN users u1 ON u1.user_id = MLE.created_by
        LEFT JOIN users u2 ON u2.user_id = MLE.updated_by

        WHERE MLE.master_id = ANY(:master_ids)
    """)

    entries = db.execute(entry_query, {"master_ids": master_ids}).mappings().all()

    # 3. GROUP CHILDREN
    entry_map = defaultdict(list)

    for e in entries:
        entry_map[e["master_id"]].append(dict(e))  # ✅ convert to dict

    # 4. FINAL RESPONSE
    final_data = []

    for m in masters:
        m_dict = dict(m)

        mid = m["mfm_log_hsn_id"]

        m_dict["entries"] = entry_map.get(mid, [])

        final_data.append(m_dict)

    return final_data