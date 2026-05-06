from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.access_service import validate_token
from datetime import date, datetime, time
from collections import defaultdict
from typing import List,Dict, Any

router = APIRouter(
    prefix="/mfm-log-ner-page2-master",
    tags=["MFM Log NER Page 2 Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class MFMLogNERPage2MasterCreate(BaseModel):
    master_log_id: Optional[int]

    # -------- SHIFT A --------
    shift_a_101a_prev: Optional[float]
    shift_a_101a_curr: Optional[float]
    shift_a_101a_total: Optional[float]

    shift_a_101b_prev: Optional[float]
    shift_a_101b_curr: Optional[float]
    shift_a_101b_total: Optional[float]

    shift_a_101c_prev: Optional[float]
    shift_a_101c_curr: Optional[float]
    shift_a_101c_total: Optional[float]

    shift_a_sumpump_prev: Optional[float]
    shift_a_sumpump_curr: Optional[float]
    shift_a_sumpump_total: Optional[float]

    shift_a_net_shift: Optional[float]
    shift_a_gross_shift: Optional[float]
    shift_a_sump_level_int: Optional[float]
    shift_a_sump_level_fin: Optional[float]

    shift_a_line_mlr_ner_batch: Optional[str]
    shift_a_line_mlr_ner_qty: Optional[float]

    shift_a_line_ner_hsn_batch: Optional[str]
    shift_a_line_ner_hsn_qty: Optional[float]

    shift_a_shutdown_prev: Optional[float]
    shift_a_shutdown_curr: Optional[float]
    shift_a_shutdown_total: Optional[float]

    shift_a_shift_engg: Optional[str]
    shift_a_shutdown_details: Optional[str]

    # -------- SHIFT B --------
    shift_b_101a_prev: Optional[float]
    shift_b_101a_curr: Optional[float]
    shift_b_101a_total: Optional[float]

    shift_b_101b_prev: Optional[float]
    shift_b_101b_curr: Optional[float]
    shift_b_101b_total: Optional[float]

    shift_b_101c_prev: Optional[float]
    shift_b_101c_curr: Optional[float]
    shift_b_101c_total: Optional[float]

    shift_b_sumpump_prev: Optional[float]
    shift_b_sumpump_curr: Optional[float]
    shift_b_sumpump_total: Optional[float]

    shift_b_net_shift: Optional[float]
    shift_b_gross_shift: Optional[float]
    shift_b_sump_level_int: Optional[float]
    shift_b_sump_level_fin: Optional[float]

    shift_b_line_mlr_ner_batch: Optional[str]
    shift_b_line_mlr_ner_qty: Optional[float]

    shift_b_line_ner_hsn_batch: Optional[str]
    shift_b_line_ner_hsn_qty: Optional[float]

    shift_b_shutdown_prev: Optional[float]
    shift_b_shutdown_curr: Optional[float]
    shift_b_shutdown_total: Optional[float]

    shift_b_shift_engg: Optional[str]
    shift_b_shutdown_remarks: Optional[str]

    # -------- SHIFT C --------
    shift_c_101a_prev: Optional[float]
    shift_c_101a_curr: Optional[float]
    shift_c_101a_total: Optional[float]

    shift_c_101b_prev: Optional[float]
    shift_c_101b_curr: Optional[float]
    shift_c_101b_total: Optional[float]

    shift_c_101c_prev: Optional[float]
    shift_c_101c_curr: Optional[float]
    shift_c_101c_total: Optional[float]

    shift_c_sumpump_prev: Optional[float]
    shift_c_sumpump_curr: Optional[float]
    shift_c_sumpump_total: Optional[float]

    shift_c_net_shift: Optional[float]
    shift_c_gross_shift: Optional[float]
    shift_c_sump_level_int: Optional[float]
    shift_c_sump_level_fin: Optional[float]

    shift_c_line_mlr_ner_batch: Optional[str]
    shift_c_line_mlr_ner_qty: Optional[float]

    shift_c_line_ner_hsn_batch: Optional[str]
    shift_c_line_ner_hsn_qty: Optional[float]

    shift_c_shutdown_prev: Optional[float]
    shift_c_shutdown_curr: Optional[float]
    shift_c_shutdown_total: Optional[float]

    shift_c_shift_engg: Optional[str]
    shift_c_shutdown_remarks: Optional[str]

    # -------- SUMMARY --------
    power_day: Optional[float]
    power_month: Optional[float]
    power_year: Optional[float]

    

    interface_details: Optional[str]

    net_day: Optional[float]
    net_month: Optional[float]
    net_year: Optional[float]

    gross_day: Optional[float]
    gross_month: Optional[float]
    gross_year: Optional[float]
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class MFMLogNERPage2MasterUpdate(MFMLogNERPage2MasterCreate):
    pass


# =====================================================
# POST — CREATE
# =====================================================
@router.post("")
def create_mfm_log_ner_page2_master(
    payload: MFMLogNERPage2MasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_ner_page2_master (
            master_log_id,

            shift_a_101a_prev, shift_a_101a_curr, shift_a_101a_total,
            shift_a_101b_prev, shift_a_101b_curr, shift_a_101b_total,
            shift_a_101c_prev, shift_a_101c_curr, shift_a_101c_total,
            shift_a_sumpump_prev, shift_a_sumpump_curr, shift_a_sumpump_total,
            shift_a_net_shift, shift_a_gross_shift,
            shift_a_sump_level_int, shift_a_sump_level_fin,
            shift_a_line_mlr_ner_batch, shift_a_line_mlr_ner_qty,
            shift_a_line_ner_hsn_batch, shift_a_line_ner_hsn_qty,
            shift_a_shutdown_prev, shift_a_shutdown_curr, shift_a_shutdown_total,
            shift_a_shift_engg, shift_a_shutdown_details,

            shift_b_101a_prev, shift_b_101a_curr, shift_b_101a_total,
            shift_b_101b_prev, shift_b_101b_curr, shift_b_101b_total,
            shift_b_101c_prev, shift_b_101c_curr, shift_b_101c_total,
            shift_b_sumpump_prev, shift_b_sumpump_curr, shift_b_sumpump_total,
            shift_b_net_shift, shift_b_gross_shift,
            shift_b_sump_level_int, shift_b_sump_level_fin,
            shift_b_line_mlr_ner_batch, shift_b_line_mlr_ner_qty,
            shift_b_line_ner_hsn_batch, shift_b_line_ner_hsn_qty,
            shift_b_shutdown_prev, shift_b_shutdown_curr, shift_b_shutdown_total,
            shift_b_shift_engg, shift_b_shutdown_remarks,

            shift_c_101a_prev, shift_c_101a_curr, shift_c_101a_total,
            shift_c_101b_prev, shift_c_101b_curr, shift_c_101b_total,
            shift_c_101c_prev, shift_c_101c_curr, shift_c_101c_total,
            shift_c_sumpump_prev, shift_c_sumpump_curr, shift_c_sumpump_total,
            shift_c_net_shift, shift_c_gross_shift,
            shift_c_sump_level_int, shift_c_sump_level_fin,
            shift_c_line_mlr_ner_batch, shift_c_line_mlr_ner_qty,
            shift_c_line_ner_hsn_batch, shift_c_line_ner_hsn_qty,
            shift_c_shutdown_prev, shift_c_shutdown_curr, shift_c_shutdown_total,
            shift_c_shift_engg, shift_c_shutdown_remarks,

            power_day, power_month, power_year,
            
            interface_details,
            net_day, net_month, net_year,
            gross_day, gross_month, gross_year,
            created_at, created_by, updated_at, updated_by
        )
        VALUES (
            :master_log_id,

            :shift_a_101a_prev, :shift_a_101a_curr, :shift_a_101a_total,
            :shift_a_101b_prev, :shift_a_101b_curr, :shift_a_101b_total,
            :shift_a_101c_prev, :shift_a_101c_curr, :shift_a_101c_total,
            :shift_a_sumpump_prev, :shift_a_sumpump_curr, :shift_a_sumpump_total,
            :shift_a_net_shift, :shift_a_gross_shift,
            :shift_a_sump_level_int, :shift_a_sump_level_fin,
            :shift_a_line_mlr_ner_batch, :shift_a_line_mlr_ner_qty,
            :shift_a_line_ner_hsn_batch, :shift_a_line_ner_hsn_qty,
            :shift_a_shutdown_prev, :shift_a_shutdown_curr, :shift_a_shutdown_total,
            :shift_a_shift_engg, :shift_a_shutdown_details,

            :shift_b_101a_prev, :shift_b_101a_curr, :shift_b_101a_total,
            :shift_b_101b_prev, :shift_b_101b_curr, :shift_b_101b_total,
            :shift_b_101c_prev, :shift_b_101c_curr, :shift_b_101c_total,
            :shift_b_sumpump_prev, :shift_b_sumpump_curr, :shift_b_sumpump_total,
            :shift_b_net_shift, :shift_b_gross_shift,
            :shift_b_sump_level_int, :shift_b_sump_level_fin,
            :shift_b_line_mlr_ner_batch, :shift_b_line_mlr_ner_qty,
            :shift_b_line_ner_hsn_batch, :shift_b_line_ner_hsn_qty,
            :shift_b_shutdown_prev, :shift_b_shutdown_curr, :shift_b_shutdown_total,
            :shift_b_shift_engg, :shift_b_shutdown_remarks,

            :shift_c_101a_prev, :shift_c_101a_curr, :shift_c_101a_total,
            :shift_c_101b_prev, :shift_c_101b_curr, :shift_c_101b_total,
            :shift_c_101c_prev, :shift_c_101c_curr, :shift_c_101c_total,
            :shift_c_sumpump_prev, :shift_c_sumpump_curr, :shift_c_sumpump_total,
            :shift_c_net_shift, :shift_c_gross_shift,
            :shift_c_sump_level_int, :shift_c_sump_level_fin,
            :shift_c_line_mlr_ner_batch, :shift_c_line_mlr_ner_qty,
            :shift_c_line_ner_hsn_batch, :shift_c_line_ner_hsn_qty,
            :shift_c_shutdown_prev, :shift_c_shutdown_curr, :shift_c_shutdown_total,
            :shift_c_shift_engg, :shift_c_shutdown_remarks,
           
            :power_day,:power_month,:power_year,

            :interface_details,
            :net_day, :net_month, :net_year,
            :gross_day, :gross_month, :gross_year,
            :created_at, :created_by, :updated_at, :updated_by
        )
        RETURNING mfm_log_ner_paget_two_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM Log NER Page-2 Master created successfully",
        "mfm_log_ner_paget_two_id": result.scalar()
    }



# =====================================================
# PUT — UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_log_ner_paget_two_id}")
def update_mfm_log_ner_page2_master(
    mfm_log_ner_paget_two_id: int,
    payload: MFMLogNERPage2MasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_log_ner_paget_two_id

    query = text("""
        UPDATE mfm_log_ner_page2_master
        SET
            master_log_id = :master_log_id,

            -- -------- SHIFT A --------
            shift_a_101a_prev = :shift_a_101a_prev,
            shift_a_101a_curr = :shift_a_101a_curr,
            shift_a_101a_total = :shift_a_101a_total,

            shift_a_101b_prev = :shift_a_101b_prev,
            shift_a_101b_curr = :shift_a_101b_curr,
            shift_a_101b_total = :shift_a_101b_total,

            shift_a_101c_prev = :shift_a_101c_prev,
            shift_a_101c_curr = :shift_a_101c_curr,
            shift_a_101c_total = :shift_a_101c_total,

            shift_a_sumpump_prev = :shift_a_sumpump_prev,
            shift_a_sumpump_curr = :shift_a_sumpump_curr,
            shift_a_sumpump_total = :shift_a_sumpump_total,

            shift_a_net_shift = :shift_a_net_shift,
            shift_a_gross_shift = :shift_a_gross_shift,
            shift_a_sump_level_int = :shift_a_sump_level_int,
            shift_a_sump_level_fin = :shift_a_sump_level_fin,

            shift_a_line_mlr_ner_batch = :shift_a_line_mlr_ner_batch,
            shift_a_line_mlr_ner_qty = :shift_a_line_mlr_ner_qty,

            shift_a_line_ner_hsn_batch = :shift_a_line_ner_hsn_batch,
            shift_a_line_ner_hsn_qty = :shift_a_line_ner_hsn_qty,

            shift_a_shutdown_prev = :shift_a_shutdown_prev,
            shift_a_shutdown_curr = :shift_a_shutdown_curr,
            shift_a_shutdown_total = :shift_a_shutdown_total,

            shift_a_shift_engg = :shift_a_shift_engg,
            shift_a_shutdown_details = :shift_a_shutdown_details,

            -- -------- SHIFT B --------
            shift_b_101a_prev = :shift_b_101a_prev,
            shift_b_101a_curr = :shift_b_101a_curr,
            shift_b_101a_total = :shift_b_101a_total,

            shift_b_101b_prev = :shift_b_101b_prev,
            shift_b_101b_curr = :shift_b_101b_curr,
            shift_b_101b_total = :shift_b_101b_total,

            shift_b_101c_prev = :shift_b_101c_prev,
            shift_b_101c_curr = :shift_b_101c_curr,
            shift_b_101c_total = :shift_b_101c_total,

            shift_b_sumpump_prev = :shift_b_sumpump_prev,
            shift_b_sumpump_curr = :shift_b_sumpump_curr,
            shift_b_sumpump_total = :shift_b_sumpump_total,

            shift_b_net_shift = :shift_b_net_shift,
            shift_b_gross_shift = :shift_b_gross_shift,
            shift_b_sump_level_int = :shift_b_sump_level_int,
            shift_b_sump_level_fin = :shift_b_sump_level_fin,

            shift_b_line_mlr_ner_batch = :shift_b_line_mlr_ner_batch,
            shift_b_line_mlr_ner_qty = :shift_b_line_mlr_ner_qty,

            shift_b_line_ner_hsn_batch = :shift_b_line_ner_hsn_batch,
            shift_b_line_ner_hsn_qty = :shift_b_line_ner_hsn_qty,

            shift_b_shutdown_prev = :shift_b_shutdown_prev,
            shift_b_shutdown_curr = :shift_b_shutdown_curr,
            shift_b_shutdown_total = :shift_b_shutdown_total,

            shift_b_shift_engg = :shift_b_shift_engg,
            shift_b_shutdown_remarks = :shift_b_shutdown_remarks,

            -- -------- SHIFT C --------
            shift_c_101a_prev = :shift_c_101a_prev,
            shift_c_101a_curr = :shift_c_101a_curr,
            shift_c_101a_total = :shift_c_101a_total,

            shift_c_101b_prev = :shift_c_101b_prev,
            shift_c_101b_curr = :shift_c_101b_curr,
            shift_c_101b_total = :shift_c_101b_total,

            shift_c_101c_prev = :shift_c_101c_prev,
            shift_c_101c_curr = :shift_c_101c_curr,
            shift_c_101c_total = :shift_c_101c_total,

            shift_c_sumpump_prev = :shift_c_sumpump_prev,
            shift_c_sumpump_curr = :shift_c_sumpump_curr,
            shift_c_sumpump_total = :shift_c_sumpump_total,

            shift_c_net_shift = :shift_c_net_shift,
            shift_c_gross_shift = :shift_c_gross_shift,
            shift_c_sump_level_int = :shift_c_sump_level_int,
            shift_c_sump_level_fin = :shift_c_sump_level_fin,

            shift_c_line_mlr_ner_batch = :shift_c_line_mlr_ner_batch,
            shift_c_line_mlr_ner_qty = :shift_c_line_mlr_ner_qty,

            shift_c_line_ner_hsn_batch = :shift_c_line_ner_hsn_batch,
            shift_c_line_ner_hsn_qty = :shift_c_line_ner_hsn_qty,

            shift_c_shutdown_prev = :shift_c_shutdown_prev,
            shift_c_shutdown_curr = :shift_c_shutdown_curr,
            shift_c_shutdown_total = :shift_c_shutdown_total,

            shift_c_shift_engg = :shift_c_shift_engg,
            shift_c_shutdown_remarks = :shift_c_shutdown_remarks,

            -- -------- SUMMARY --------
            power_day = :power_day,
            power_month = :power_month,
            power_year = :power_year,

            interface_details = :interface_details,

            net_day = :net_day,
            net_month = :net_month,
            net_year = :net_year,

            gross_day = :gross_day,
            gross_month = :gross_month,
            gross_year = :gross_year,

            created_at = :created_at,
            created_by = :created_by,
            updated_at = :updated_at,
            updated_by = :updated_by

        WHERE mfm_log_ner_paget_two_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(404, "NER Page-2 master not found")

    return {"message": "MFM Log NER Page-2 Master updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_ner_paget_two_id}")
def delete_mfm_log_ner_page2_master(
    mfm_log_ner_paget_two_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_ner_page2_master
            WHERE mfm_log_ner_paget_two_id = :id
        """),
        {"id": mfm_log_ner_paget_two_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(404, "NER Page-2 master not found")

    return {"message": "MFM Log NER Page-2 Master deleted successfully"}


# =====================================================
# FETCH BY DATE
# =====================================================
@router.get("/by-date", response_model=List[Dict[str, Any]])
def fetch_mfm_log_ner_page2_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT P2.*,

            -- USER NAMES
            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name,

            -- OPTIONAL: Master Info
            M.mfm_log_ner_id,
            M.ms_logbook_id

        FROM mfm_log_ner_page2_master P2
        INNER JOIN mfm_log_ner_master M
            ON M.mfm_log_ner_id = P2.master_log_id
        INNER JOIN logbook_shift_master LSM
            ON LSM.ms_logbook_id = M.ms_logbook_id
        LEFT JOIN users u1 
            ON u1.user_id = P2.created_by::INTEGER
        LEFT JOIN users u2 
            ON u2.user_id = P2.updated_by
        WHERE 
            LSM.created_at >= :log_date + INTERVAL '7 hour'
            AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')

        ORDER BY P2.mfm_log_ner_paget_two_id DESC
    """)

    result = db.execute(query, {"log_date": log_date}).mappings().all()

    return [dict(r) for r in result]
