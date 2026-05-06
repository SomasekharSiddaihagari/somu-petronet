from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from typing import List, Any,Dict
import json
from collections import defaultdict

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/mfm-log-master-dkn",
    tags=["MFM Log Master DKN"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class MFMLogMasterCreate(BaseModel):
    station: Optional[str]
    station_in_charge: Optional[str]
    document_no: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]
    status: Optional[str]

    shift_a_tank_taken_over: Optional[str]
    shift_a_tank_handed_over: Optional[str]

    shift_b_tank_taken_over: Optional[str]
    shift_b_tank_handed_over: Optional[str]

    shift_c_tank_taken_over: Optional[str]
    shift_c_tank_handed_over: Optional[str]

    qty_pumped_from_mangalore: Optional[float]
    receipt_at_hassan: Optional[float]
    receipt_at_bangalore: Optional[float]

    qty_available_interface_tank_101: Optional[float]
    qty_available_interface_tank_102: Optional[float]

    loss_gain_101: Optional[float]
    loss_gain_102: Optional[float]

    qty_pumped_last_24hrs: Optional[float]
    qty_pumped_pl_t: Optional[float]
    qty_pumped_month: Optional[float]
    qty_pumped_year: Optional[float]

    euro_hsd: List[Any]
    bsv_hsd: List[Any]
    sk_o: List[Any]
    ms: List[Any]
    total_product: List[Any]

    hrs_operation_last_24hrs: Optional[float]
    hrs_operation_month: Optional[float]
    hrs_operation_year: Optional[float]

    sump_tank_dip_0700hrs: Optional[float]

    diesel_dg_tank: Optional[float]
    diesel_dg_set_tank: Optional[float]
    diesel_ffdu_3_ser_tank: Optional[float]
    diesel_ffdu_4_ser_tank: Optional[float]
    diesel_ffdu_5_ser_tank: Optional[float]

    remarks: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    ms_logbook_id: Optional[int] = None
    plt_sd_start_time: Optional[time] = None
    plt_sd_end_time: Optional[time] = None
    prevcumrunhour: Optional[int] = None
    cummrunhour: Optional[int] = None

class MFMLogMasterUpdate(MFMLogMasterCreate):
    pass


# =====================================================
# POST — CREATE MASTER
# =====================================================

@router.post("")
def create_mfm_log_master_dkn(
    payload: MFMLogMasterCreate,
    db: Session = Depends(get_db)
):
 
    data = payload.dict()
 
    # Convert list → JSON for jsonb columns
    data["euro_hsd"] = json.dumps(data.get("euro_hsd"))
    data["bsv_hsd"] = json.dumps(data.get("bsv_hsd"))
    data["sk_o"] = json.dumps(data.get("sk_o"))
    data["ms"] = json.dumps(data.get("ms"))
    data["total_product"] = json.dumps(data.get("total_product"))
 
    query = text("""
        INSERT INTO mfm_log_master_dkn (
            station, station_in_charge, document_no, shift,
            start_time, log_date, status,
 
            shift_a_tank_taken_over, shift_a_tank_handed_over,
            shift_b_tank_taken_over, shift_b_tank_handed_over,
            shift_c_tank_taken_over, shift_c_tank_handed_over,
 
            qty_pumped_from_mangalore, receipt_at_hassan, receipt_at_bangalore,
            qty_available_interface_tank_101, qty_available_interface_tank_102,
            loss_gain_101, loss_gain_102,
            qty_pumped_last_24hrs, qty_pumped_pl_t,
            qty_pumped_month, qty_pumped_year,
 
            euro_hsd, bsv_hsd, sk_o, ms, total_product,
 
            hrs_operation_last_24hrs, hrs_operation_month, hrs_operation_year,
            sump_tank_dip_0700hrs,
 
            diesel_dg_tank, diesel_dg_set_tank,
            diesel_ffdu_3_ser_tank, diesel_ffdu_4_ser_tank, diesel_ffdu_5_ser_tank,
 
            remarks, created_at, created_by, updated_at, updated_by, ms_logbook_id,plt_sd_start_time,plt_sd_end_time,prevcumrunhour,cummrunhour
        )
        VALUES (
            :station, :station_in_charge, :document_no, :shift,
            :start_time, :log_date, :status,
 
            :shift_a_tank_taken_over, :shift_a_tank_handed_over,
            :shift_b_tank_taken_over, :shift_b_tank_handed_over,
            :shift_c_tank_taken_over, :shift_c_tank_handed_over,
 
            :qty_pumped_from_mangalore, :receipt_at_hassan, :receipt_at_bangalore,
            :qty_available_interface_tank_101, :qty_available_interface_tank_102,
            :loss_gain_101, :loss_gain_102,
            :qty_pumped_last_24hrs, :qty_pumped_pl_t,
            :qty_pumped_month, :qty_pumped_year,
 
            :euro_hsd, :bsv_hsd, :sk_o, :ms, :total_product,
 
            :hrs_operation_last_24hrs, :hrs_operation_month, :hrs_operation_year,
            :sump_tank_dip_0700hrs,
 
            :diesel_dg_tank, :diesel_dg_set_tank,
            :diesel_ffdu_3_ser_tank, :diesel_ffdu_4_ser_tank, :diesel_ffdu_5_ser_tank,
 
            :remarks, :created_at, :created_by, :updated_at, :updated_by, :ms_logbook_id, :plt_sd_start_time, :plt_sd_end_time, :prevcumrunhour, :cummrunhour
        )
        RETURNING mfm_log_dkn_id
    """)
 
    result = db.execute(query, data)
    db.commit()
 
    return {
        "message": "MFM Log Master (DKN) created successfully",
        "mfm_log_dkn_id": result.scalar()
    }

# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================
@router.put("/{mfm_log_dkn_id}")
def update_mfm_log_master_dkn(
    mfm_log_dkn_id: int,
    payload: MFMLogMasterUpdate,
    db: Session = Depends(get_db)
):   

    params = payload.dict()
    params["id"] = mfm_log_dkn_id

    # ✅ FIX: Convert list → JSON for jsonb columns
    json_fields = ["euro_hsd", "bsv_hsd", "sk_o", "ms", "total_product"]

    for field in json_fields:
        if params.get(field) is not None:
            params[field] = json.dumps(params[field])

    query = text("""
        UPDATE mfm_log_master_dkn
        SET
            station = :station,
            station_in_charge = :station_in_charge,
            document_no = :document_no,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,
            status = :status,

            shift_a_tank_taken_over = :shift_a_tank_taken_over,
            shift_a_tank_handed_over = :shift_a_tank_handed_over,
            shift_b_tank_taken_over = :shift_b_tank_taken_over,
            shift_b_tank_handed_over = :shift_b_tank_handed_over,
            shift_c_tank_taken_over = :shift_c_tank_taken_over,
            shift_c_tank_handed_over = :shift_c_tank_handed_over,

            qty_pumped_from_mangalore = :qty_pumped_from_mangalore,
            receipt_at_hassan = :receipt_at_hassan,
            receipt_at_bangalore = :receipt_at_bangalore,

            qty_available_interface_tank_101 = :qty_available_interface_tank_101,
            qty_available_interface_tank_102 = :qty_available_interface_tank_102,

            loss_gain_101 = :loss_gain_101,
            loss_gain_102 = :loss_gain_102,

            qty_pumped_last_24hrs = :qty_pumped_last_24hrs,
            qty_pumped_pl_t = :qty_pumped_pl_t,
            qty_pumped_month = :qty_pumped_month,
            qty_pumped_year = :qty_pumped_year,

            euro_hsd = :euro_hsd,
            bsv_hsd = :bsv_hsd,
            sk_o = :sk_o,
            ms = :ms,
            total_product = :total_product,

            hrs_operation_last_24hrs = :hrs_operation_last_24hrs,
            hrs_operation_month = :hrs_operation_month,
            hrs_operation_year = :hrs_operation_year,

            sump_tank_dip_0700hrs = :sump_tank_dip_0700hrs,

            diesel_dg_tank = :diesel_dg_tank,
            diesel_dg_set_tank = :diesel_dg_set_tank,
            diesel_ffdu_3_ser_tank = :diesel_ffdu_3_ser_tank,
            diesel_ffdu_4_ser_tank = :diesel_ffdu_4_ser_tank,
            diesel_ffdu_5_ser_tank = :diesel_ffdu_5_ser_tank,

            remarks = :remarks,
            created_at = :created_at,
            created_by = :created_by,
            updated_at = :updated_at,
            updated_by = :updated_by,
            ms_logbook_id = :ms_logbook_id,
            plt_sd_start_time = :plt_sd_start_time,
            plt_sd_end_time = :plt_sd_end_time,
            prevcumrunhour = :prevcumrunhour,    
            cummrunhour = :cummrunhour

        WHERE mfm_log_dkn_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM Log Master not found")

    return {"message": "MFM Log Master (DKN) updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_dkn_id}")
def delete_mfm_log_master_dkn(
    mfm_log_dkn_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("DELETE FROM mfm_log_master_dkn WHERE mfm_log_dkn_id = :id"),
        {"id": mfm_log_dkn_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="MFM Log Master not found")

    return {"message": "MFM Log Master (DKN) deleted successfully"}


# @router.get("/by-date", response_model=List[dict])
# def fetch_mfm_log_by_date(
#     log_date: date,
#     db: Session = Depends(get_db)
# ):
#     query = text("""
#         SELECT MLMD.*
#         FROM mfm_log_master_dkn MLMD
#         JOIN logbook_shift_master LSM 
#             ON LSM.ms_logbook_id = MLMD.ms_logbook_id
#         WHERE DATE(LSM.created_at) = :log_date
#     """)

#     result = db.execute(query, {"log_date": log_date}).mappings().all()

#     return result

@router.get("/by-date", response_model=List[dict])
def fetch_mfm_log_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT MLMD.*,
                -- Created By Name
                TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,

                -- Updated By Name
                TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_master_dkn MLMD
        JOIN logbook_shift_master LSM 
            ON LSM.ms_logbook_id = MLMD.ms_logbook_id
        -- Join for created_by
        LEFT JOIN users u1 
            ON u1.user_id = MLMD.created_by

        -- Join for updated_by
        LEFT JOIN users u2 
            ON u2.user_id = MLMD.updated_by
        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    result = db.execute(query, {"log_date": log_date}).mappings().all()

    return result


@router.get("/by-date-with-entry", response_model=List[Dict[str, Any]])
def fetch_complete_mfm_log_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    # 1. MASTER
    master_query = text("""
        SELECT MLMD.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_master_dkn MLMD
        JOIN logbook_shift_master LSM 
            ON LSM.ms_logbook_id = MLMD.ms_logbook_id
        LEFT JOIN users u1 ON u1.user_id = MLMD.created_by
        LEFT JOIN users u2 ON u2.user_id = MLMD.updated_by

        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    masters = db.execute(master_query, {"log_date": log_date}).mappings().all()

    if not masters:
        return []

    master_ids = [m["mfm_log_dkn_id"] for m in masters]

    # ⚠️ IMPORTANT: PostgreSQL ARRAY binding
    params = {"master_ids": master_ids}

    # 2. ENTRY
    entry_query = text("""
        SELECT MLED.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_entry_dkn MLED
        LEFT JOIN users u1 ON u1.user_id = MLED.created_by
        LEFT JOIN users u2 ON u2.user_id = MLED.updated_by

        WHERE MLED.master_id = ANY(:master_ids)
    """)

    entries = db.execute(entry_query, params).mappings().all()

    # 3. SHUTDOWN
    shutdown_query = text("""
        SELECT MSDD.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_shutdown_detail_dkn MSDD
        LEFT JOIN users u1 ON u1.user_id = MSDD.created_by
        LEFT JOIN users u2 ON u2.user_id = MSDD.updated_by

        WHERE MSDD.master_id = ANY(:master_ids)
    """)

    shutdowns = db.execute(shutdown_query, params).mappings().all()

    # 4. PLT
    plt_query = text("""
        SELECT MPDD.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_plt_detail_dkn MPDD
        LEFT JOIN users u1 ON u1.user_id = MPDD.created_by
        LEFT JOIN users u2 ON u2.user_id = MPDD.updated_by

        WHERE MPDD.master_id = ANY(:master_ids)
    """)

    plts = db.execute(plt_query, params).mappings().all()

    # 5. GROUPING
    entry_map = defaultdict(list)
    shutdown_map = defaultdict(list)
    plt_map = defaultdict(list)

    for e in entries:
        entry_map[e["master_id"]].append(dict(e))

    for s in shutdowns:
        shutdown_map[s["master_id"]].append(dict(s))

    for p in plts:
        plt_map[p["master_id"]].append(dict(p))

    # 6. FINAL RESPONSE
    final_data = []

    for m in masters:
        m_dict = dict(m)

        mid = m["mfm_log_dkn_id"]

        m_dict["entries"] = entry_map.get(mid, [])
        m_dict["shutdown_details"] = shutdown_map.get(mid, [])
        m_dict["plt_details"] = plt_map.get(mid, [])

        final_data.append(m_dict)

    return final_data


@router.get("/{mfm_log_dkn_id}", response_model=dict)
def fetch_mfm_log_by_id(
    mfm_log_dkn_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            MLMD.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) AS updated_by_name

        FROM mfm_log_master_dkn MLMD

        -- Join for created_by
        LEFT JOIN users u1 
            ON u1.user_id = MLMD.created_by

        -- Join for updated_by
        LEFT JOIN users u2 
            ON u2.user_id = MLMD.updated_by

        WHERE MLMD.mfm_log_dkn_id = :mfm_log_dkn_id
    """)

    result = db.execute(
        query, {"mfm_log_dkn_id": mfm_log_dkn_id}
    ).mappings().first()

    return result

