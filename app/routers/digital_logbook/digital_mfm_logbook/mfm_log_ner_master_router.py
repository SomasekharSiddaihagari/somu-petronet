from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

from collections import defaultdict
from typing import List,Dict, Any

router = APIRouter(
    prefix="/mfm-log-ner-master",
    tags=["MFM Log NER Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class MFMLogNERMasterCreate(BaseModel):
    station: Optional[str]
    station_in_charge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]

    # =========================
    # SV03
    # =========================
    sv03_psp: Optional[float]
    sv03_dc_voltage_op: Optional[float]
    sv03_dc_current_op: Optional[float]

    sv03_cp_charger: Optional[str]
    sv03_cp_ac_ip_voltage: Optional[float]
    sv03_cp_ac_ip_current: Optional[float]

    sv03_cp_dc_op_voltage: Optional[float]
    sv03_cp_dc_op_current: Optional[float]

    sv03_cp_battery_cell_voltage: Optional[float]
    sv03_cp_battery_earth_leak: Optional[float]

    sv03_telecom_charger: Optional[str]

    sv03_ac_ip_voltage_telecom: Optional[float]
    sv03_ac_ip_current_telecom: Optional[float]

    sv03_telecom_charger_dc_op_voltage: Optional[float]
    sv03_telecom_charger_dc_op_current: Optional[float]

    sv03_telecom_charger_battery_cell_voltage: Optional[float]
    sv03_telecom_charger_battery_earth_leak: Optional[float]

    sv03_dg_15kva: Optional[float]

    # =========================
    # SV04
    # =========================
    sv04_psp: Optional[float]
    sv04_dc_voltage_op: Optional[float]
    sv04_dc_current_op: Optional[float]

    sv04_cp_charger: Optional[str]
    sv04_cp_ac_ip_voltage: Optional[float]
    sv04_cp_ac_ip_current: Optional[float]

    sv04_cp_dc_op_voltage: Optional[float]
    sv04_cp_dc_op_current: Optional[float]

    sv04_cp_battery_cell_voltage: Optional[float]
    sv04_cp_battery_earth_leak: Optional[float]

    sv04_telecom_charger: Optional[str]

    sv04_ac_ip_voltage_telecom: Optional[float]
    sv04_ac_ip_current_telecom: Optional[float]

    sv04_telecom_charger_dc_op_voltage: Optional[float]
    sv04_telecom_charger_dc_op_current: Optional[float]

    sv04_telecom_charger_battery_cell_voltage: Optional[float]
    sv04_telecom_charger_battery_earth_leak: Optional[float]

    sv04_dg_15kva: Optional[float]

    dg_ltrs: Optional[float]

    # ---------- SV-3 ----------
    sv3_import: Optional[float]
    sv3_export: Optional[float]
    sv3_dg_ltrs: Optional[float]
    sv3_neriya_station: Optional[str]
    sv3_kwh: Optional[float]
    sv3_kvarh: Optional[float]
    sv3_pf: Optional[float]
    sv3_psp: Optional[float]
    sv3_volt: Optional[float]
    sv3_curr: Optional[float]
    sv3_tc: Optional[float]
    sv3_fwt_level: Optional[float]
    sv3_fwt_1: Optional[float]
    sv3_fwt_2: Optional[float]
    sv3_dg_ltrs_2: Optional[float]

    # ---------- SV-4 ----------
    sv4_import: Optional[float]
    sv4_export: Optional[float]
    sv4_dg_ltrs: Optional[float]
    sv4_neriya_station: Optional[str]
    sv4_kwh: Optional[float]
    sv4_kvarh: Optional[float]
    sv4_pf: Optional[float]
    sv4_psp: Optional[float]
    sv4_volt: Optional[float]
    sv4_curr: Optional[float]
    sv4_tc: Optional[float]
    sv4_fwt_level: Optional[float]
    sv4_fwt_1: Optional[float]
    sv4_fwt_2: Optional[float]
    sv4_dg_ltrs_2: Optional[float]

    remarks: Optional[str]
    status: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    ms_logbook_id: Optional[int] = None

class MFMLogNERMasterUpdate(MFMLogNERMasterCreate):
    pass


# =====================================================
# POST — CREATE MASTER
# =====================================================

@router.post("")
def create_mfm_log_ner_master(
    payload: MFMLogNERMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO mfm_log_ner_master (
            station, station_in_charge, shift, start_time, log_date,

            -- SV03
            sv03_psp, sv03_dc_voltage_op, sv03_dc_current_op,
            sv03_cp_charger, sv03_cp_ac_ip_voltage, sv03_cp_ac_ip_current,
            sv03_cp_dc_op_voltage, sv03_cp_dc_op_current,
            sv03_cp_battery_cell_voltage, sv03_cp_battery_earth_leak,
            sv03_telecom_charger,
            sv03_ac_ip_voltage_telecom, sv03_ac_ip_current_telecom,
            sv03_telecom_charger_dc_op_voltage, sv03_telecom_charger_dc_op_current,
            sv03_telecom_charger_battery_cell_voltage, sv03_telecom_charger_battery_earth_leak,
            sv03_dg_15kva,

            -- SV04
            sv04_psp, sv04_dc_voltage_op, sv04_dc_current_op,
            sv04_cp_charger, sv04_cp_ac_ip_voltage, sv04_cp_ac_ip_current,
            sv04_cp_dc_op_voltage, sv04_cp_dc_op_current,
            sv04_cp_battery_cell_voltage, sv04_cp_battery_earth_leak,
            sv04_telecom_charger,
            sv04_ac_ip_voltage_telecom, sv04_ac_ip_current_telecom,
            sv04_telecom_charger_dc_op_voltage, sv04_telecom_charger_dc_op_current,
            sv04_telecom_charger_battery_cell_voltage, sv04_telecom_charger_battery_earth_leak,
            sv04_dg_15kva, 
                 
            dg_ltrs,

            sv3_import, sv3_export, sv3_dg_ltrs, sv3_neriya_station,
            sv3_kwh, sv3_kvarh, sv3_pf, sv3_psp, sv3_volt, sv3_curr,
            sv3_tc, sv3_fwt_level, sv3_fwt_1, sv3_fwt_2, sv3_dg_ltrs_2,

            sv4_import, sv4_export, sv4_dg_ltrs, sv4_neriya_station,
            sv4_kwh, sv4_kvarh, sv4_pf, sv4_psp, sv4_volt, sv4_curr,
            sv4_tc, sv4_fwt_level, sv4_fwt_1, sv4_fwt_2, sv4_dg_ltrs_2,

            remarks, status   ,created_at,created_by ,updated_at ,updated_by,ms_logbook_id

        )
        VALUES (
            :station, :station_in_charge, :shift, :start_time, :log_date,

            :sv03_psp, :sv03_dc_voltage_op, :sv03_dc_current_op,
            :sv03_cp_charger, :sv03_cp_ac_ip_voltage, :sv03_cp_ac_ip_current,
            :sv03_cp_dc_op_voltage, :sv03_cp_dc_op_current,
            :sv03_cp_battery_cell_voltage, :sv03_cp_battery_earth_leak,
            :sv03_telecom_charger,
            :sv03_ac_ip_voltage_telecom, :sv03_ac_ip_current_telecom,
            :sv03_telecom_charger_dc_op_voltage, :sv03_telecom_charger_dc_op_current,
            :sv03_telecom_charger_battery_cell_voltage, :sv03_telecom_charger_battery_earth_leak,
            :sv03_dg_15kva,

            :sv04_psp, :sv04_dc_voltage_op, :sv04_dc_current_op,
            :sv04_cp_charger, :sv04_cp_ac_ip_voltage, :sv04_cp_ac_ip_current,
            :sv04_cp_dc_op_voltage, :sv04_cp_dc_op_current,
            :sv04_cp_battery_cell_voltage, :sv04_cp_battery_earth_leak,
            :sv04_telecom_charger,
            :sv04_ac_ip_voltage_telecom, :sv04_ac_ip_current_telecom,
            :sv04_telecom_charger_dc_op_voltage, :sv04_telecom_charger_dc_op_current,
            :sv04_telecom_charger_battery_cell_voltage, :sv04_telecom_charger_battery_earth_leak,
            :sv04_dg_15kva, 
                 
            :dg_ltrs,

            :sv3_import, :sv3_export, :sv3_dg_ltrs, :sv3_neriya_station,
            :sv3_kwh, :sv3_kvarh, :sv3_pf, :sv3_psp, :sv3_volt, :sv3_curr,
            :sv3_tc, :sv3_fwt_level, :sv3_fwt_1, :sv3_fwt_2, :sv3_dg_ltrs_2,

            :sv4_import, :sv4_export, :sv4_dg_ltrs, :sv4_neriya_station,
            :sv4_kwh, :sv4_kvarh, :sv4_pf, :sv4_psp, :sv4_volt, :sv4_curr,
            :sv4_tc, :sv4_fwt_level, :sv4_fwt_1, :sv4_fwt_2, :sv4_dg_ltrs_2,

            :remarks, :status,:created_at,:created_by ,:updated_at ,:updated_by,:ms_logbook_id

        )
        RETURNING mfm_log_ner_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "MFM Log NER Master created successfully",
        "mfm_log_ner_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{mfm_log_ner_id}")
def update_mfm_log_ner_master(
    mfm_log_ner_id: int,
    payload: MFMLogNERMasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = mfm_log_ner_id

    query = text("""
        UPDATE mfm_log_ner_master
        SET
            station = :station,
            station_in_charge = :station_in_charge,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,
            
            sv03_psp = :sv03_psp,
            sv03_dc_voltage_op = :sv03_dc_voltage_op,
            sv03_dc_current_op = :sv03_dc_current_op,

            sv03_cp_charger = :sv03_cp_charger,
            sv03_cp_ac_ip_voltage = :sv03_cp_ac_ip_voltage,
            sv03_cp_ac_ip_current = :sv03_cp_ac_ip_current,

            sv03_cp_dc_op_voltage = :sv03_cp_dc_op_voltage,
            sv03_cp_dc_op_current = :sv03_cp_dc_op_current,

            sv03_cp_battery_cell_voltage = :sv03_cp_battery_cell_voltage,
            sv03_cp_battery_earth_leak = :sv03_cp_battery_earth_leak,

            sv03_telecom_charger = :sv03_telecom_charger,

            sv03_ac_ip_voltage_telecom = :sv03_ac_ip_voltage_telecom,
            sv03_ac_ip_current_telecom = :sv03_ac_ip_current_telecom,

            sv03_telecom_charger_dc_op_voltage = :sv03_telecom_charger_dc_op_voltage,
            sv03_telecom_charger_dc_op_current = :sv03_telecom_charger_dc_op_current,

            sv03_telecom_charger_battery_cell_voltage = :sv03_telecom_charger_battery_cell_voltage,
            sv03_telecom_charger_battery_earth_leak = :sv03_telecom_charger_battery_earth_leak,

            sv03_dg_15kva = :sv03_dg_15kva,

            sv04_psp = :sv04_psp,
            sv04_dc_voltage_op = :sv04_dc_voltage_op,
            sv04_dc_current_op = :sv04_dc_current_op,

            sv04_cp_charger = :sv04_cp_charger,
            sv04_cp_ac_ip_voltage = :sv04_cp_ac_ip_voltage,
            sv04_cp_ac_ip_current = :sv04_cp_ac_ip_current,

            sv04_cp_dc_op_voltage = :sv04_cp_dc_op_voltage,
            sv04_cp_dc_op_current = :sv04_cp_dc_op_current,

            sv04_cp_battery_cell_voltage = :sv04_cp_battery_cell_voltage,
            sv04_cp_battery_earth_leak = :sv04_cp_battery_earth_leak,

            sv04_telecom_charger = :sv04_telecom_charger,

            sv04_ac_ip_voltage_telecom = :sv04_ac_ip_voltage_telecom,
            sv04_ac_ip_current_telecom = :sv04_ac_ip_current_telecom,

            sv04_telecom_charger_dc_op_voltage = :sv04_telecom_charger_dc_op_voltage,
            sv04_telecom_charger_dc_op_current = :sv04_telecom_charger_dc_op_current,

            sv04_telecom_charger_battery_cell_voltage = :sv04_telecom_charger_battery_cell_voltage,
            sv04_telecom_charger_battery_earth_leak = :sv04_telecom_charger_battery_earth_leak,

            sv04_dg_15kva = :sv04_dg_15kva,

            
            dg_ltrs = :dg_ltrs,

            sv3_import = :sv3_import,
            sv3_export = :sv3_export,
            sv3_dg_ltrs = :sv3_dg_ltrs,
            sv3_neriya_station = :sv3_neriya_station,
            sv3_kwh = :sv3_kwh,
            sv3_kvarh = :sv3_kvarh,
            sv3_pf = :sv3_pf,
            sv3_psp = :sv3_psp,
            sv3_volt = :sv3_volt,
            sv3_curr = :sv3_curr,
            sv3_tc = :sv3_tc,
            sv3_fwt_level = :sv3_fwt_level,
            sv3_fwt_1 = :sv3_fwt_1,
            sv3_fwt_2 = :sv3_fwt_2,
            sv3_dg_ltrs_2 = :sv3_dg_ltrs_2,

            sv4_import = :sv4_import,
            sv4_export = :sv4_export,
            sv4_dg_ltrs = :sv4_dg_ltrs,
            sv4_neriya_station = :sv4_neriya_station,
            sv4_kwh = :sv4_kwh,
            sv4_kvarh = :sv4_kvarh,
            sv4_pf = :sv4_pf,
            sv4_psp = :sv4_psp,
            sv4_volt = :sv4_volt,
            sv4_curr = :sv4_curr,
            sv4_tc = :sv4_tc,
            sv4_fwt_level = :sv4_fwt_level,
            sv4_fwt_1 = :sv4_fwt_1,
            sv4_fwt_2 = :sv4_fwt_2,
            sv4_dg_ltrs_2 = :sv4_dg_ltrs_2,

            remarks = :remarks,
            status = :status
                  ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by,ms_logbook_id=:ms_logbook_id

        WHERE mfm_log_ner_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="MFM Log NER master not found"
        )

    return {"message": "MFM Log NER Master updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{mfm_log_ner_id}")
def delete_mfm_log_ner_master(
    mfm_log_ner_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM mfm_log_ner_master
            WHERE mfm_log_ner_id = :id
        """),
        {"id": mfm_log_ner_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="MFM Log NER master not found"
        )

    return {"message": "MFM Log NER Master deleted successfully"}


# =====================================================
# GET BY DATE
# =====================================================

@router.get("/ner/by-date-with-entry", response_model=List[Dict[str, Any]])
def fetch_mfm_log_ner_by_date_with_entry(
    log_date: date,
    db: Session = Depends(get_db)
):
    # =====================================================
    # 1️⃣ MASTER QUERY (WITH SHIFT + USER JOIN)
    # =====================================================
    master_query = text("""
        SELECT M.*,

            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mfm_log_ner_master M

        JOIN logbook_shift_master LSM
            ON LSM.ms_logbook_id = M.ms_logbook_id

        LEFT JOIN users u1 ON u1.user_id = M.created_by::INTEGER
        LEFT JOIN users u2 ON u2.user_id = M.updated_by::INTEGER

        WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
    """)

    masters = db.execute(master_query, {"log_date": log_date}).mappings().all()

    if not masters:
        return []

    # =====================================================
    # 2️⃣ MASTER IDS (IMPORTANT FIX)
    # =====================================================
    master_ids = [m["mfm_log_ner_id"] for m in masters]

    # =====================================================
    # 3️⃣ ENTRY QUERY (CHILD TABLE)
    # =====================================================
    entry_query = text("""
        SELECT E.*,

            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mfm_log_ner_entry E

        LEFT JOIN users u1 ON u1.user_id = E.created_by
        LEFT JOIN users u2 ON u2.user_id = E.updated_by

        WHERE E.master_id = ANY(:master_ids)
    """)

    entries = db.execute(entry_query, {"master_ids": master_ids}).mappings().all()

    # =====================================================
    # 4️⃣ GROUP CHILD DATA
    # =====================================================
    from collections import defaultdict
    entry_map = defaultdict(list)

    for e in entries:
        entry_map[e["master_id"]].append(dict(e))   # ✅ correct FK

    # =====================================================
    # 5️⃣ FINAL RESPONSE
    # =====================================================
    final_data = []

    for m in masters:
        m_dict = dict(m)

        mid = m["mfm_log_ner_id"]

        m_dict["entries"] = entry_map.get(mid, [])

        final_data.append(m_dict)

    return final_data