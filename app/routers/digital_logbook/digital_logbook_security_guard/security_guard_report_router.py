from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/security-guard-report",
    tags=["Security Guard Report"],
    dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMA
# =====================================================

class SecurityGuardReportCreate(BaseModel):
    station_name: Optional[str] = None
    station_incharge_name: Optional[str] = None
    shift_code: Optional[str] = None
    shift_start_time: Optional[time] = None
    log_date: Optional[date] = None
    document_number: Optional[str] = None
    status: Optional[str] = None
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None
    critical_report: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class SecurityGuardReportUpdate(SecurityGuardReportCreate):
    pass


# =====================================================
# CREATE
# =====================================================

@router.post("")
def create_security_guard_report(
    payload: SecurityGuardReportCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO security_guard_report (
            station_name,
            station_incharge_name,
            shift_code,
            shift_start_time,
            log_date,
            document_number,
            status,
            ms_logbook_id,
            technician_id,
            critical_report,
            created_by,
            created_at,
            updated_by,
            updated_at
        )
        VALUES (
            :station_name,
            :station_incharge_name,
            :shift_code,
            :shift_start_time,
            :log_date,
            :document_number,
            :status,
            :ms_logbook_id,
            :technician_id,
            :critical_report,
            :created_by,
            NOW(),
            :updated_by,
            NOW()
        )
        RETURNING security_guard_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Security Guard Report created successfully",
        "security_guard_id": result.scalar()
    }


# =====================================================
# GET BY ID  →  master + grouped lines
# =====================================================

@router.get("/{security_guard_id}")
def get_security_guard_report(
    security_guard_id: int,
    db: Session = Depends(get_db)
):
    master_query = text("""
        SELECT
            sgr.*,
            TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name,
            TRIM(CONCAT(COALESCE(ut.first_name, ''), ' ', COALESCE(ut.last_name, ''))) AS technician_full_name
        FROM security_guard_report sgr
        LEFT JOIN users uc ON uc.user_id = sgr.created_by AND uc.is_deleted = FALSE
        LEFT JOIN users uu ON uu.user_id = sgr.updated_by AND uu.is_deleted = FALSE
        LEFT JOIN users ut ON ut.user_id = sgr.technician_id AND ut.is_deleted = FALSE
        WHERE sgr.security_guard_id = :id
    """)

    master = db.execute(master_query, {"id": security_guard_id}).mappings().first()

    if not master:
        raise HTTPException(status_code=404, detail="Report not found")

    lines_query = text("""
        SELECT
            sgrl.*,
            TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
        FROM security_guard_report_line sgrl
        LEFT JOIN users uc ON uc.user_id = sgrl.created_by AND uc.is_deleted = FALSE
        LEFT JOIN users uu ON uu.user_id = sgrl.updated_by AND uu.is_deleted = FALSE
        WHERE sgrl.report_id = :id
        ORDER BY sgrl.location_name, sgrl.shift
    """)

    rows = db.execute(lines_query, {"id": security_guard_id}).mappings().all()
    grouped = _group_lines(rows)

    return {
        "master": dict(master),
        "lines": grouped
    }


# =====================================================
# GET BY DATE + STATION ID  →  master + grouped lines
# =====================================================

@router.get("/by-date/search")
def get_security_guard_report_by_date(
    log_date: date = Query(..., description="Filter by date e.g. 2024-01-15"),
    station_id: int = Query(..., description="Station ID"),
    db: Session = Depends(get_db)
):
    master_query = text("""
        SELECT
            sgr.*,
            TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name,
            TRIM(CONCAT(COALESCE(ut.first_name, ''), ' ', COALESCE(ut.last_name, ''))) AS technician_full_name
        FROM security_guard_report sgr
        LEFT JOIN users uc ON uc.user_id = sgr.created_by AND uc.is_deleted = FALSE
        LEFT JOIN users uu ON uu.user_id = sgr.updated_by AND uu.is_deleted = FALSE
        LEFT JOIN users ut ON ut.user_id = sgr.technician_id AND ut.is_deleted = FALSE
        WHERE sgr.log_date = :log_date
          AND (uc.station_id = :station_id OR ut.station_id = :station_id)
        ORDER BY sgr.security_guard_id DESC
    """)

    masters = db.execute(master_query, {
        "log_date": log_date,
        "station_id": station_id
    }).mappings().all()

    if not masters:
        return {"count": 0, "data": []}

    result = []
    for master in masters:
        master = dict(master)
        sgr_id = master["security_guard_id"]

        lines_query = text("""
            SELECT
                sgrl.*,
                TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
            FROM security_guard_report_line sgrl
            LEFT JOIN users uc ON uc.user_id = sgrl.created_by AND uc.is_deleted = FALSE
            LEFT JOIN users uu ON uu.user_id = sgrl.updated_by AND uu.is_deleted = FALSE
            WHERE sgrl.report_id = :id
            ORDER BY sgrl.location_name, sgrl.shift
        """)

        rows = db.execute(lines_query, {"id": sgr_id}).mappings().all()
        grouped = _group_lines(rows)

        result.append({
            "master": master,
            "lines": grouped
        })

    return {"count": len(result), "data": result}


# =====================================================
# HELPER  →  group lines by location → shift
# =====================================================

def _group_lines(rows) -> Dict:
    grouped: Dict = {}

    for row in rows:
        row = dict(row)
        location = row["location_name"]
        shift = row["shift"]

        if location not in grouped:
            grouped[location] = {}

        grouped[location][shift] = {
            "sgrl_id": row["sgrl_id"],
            "security_guard_name": row["security_guard_name"],
            "security_guard_name_two": row["security_guard_name_two"],
            "duty_start_time": str(row["duty_start_time"]) if row["duty_start_time"] else None,
            "duty_end_time": str(row["duty_end_time"]) if row["duty_end_time"] else None,
            "battery_cp_volt": row["battery_cp_volt"],
            "battery_tel_volt": row["battery_tel_volt"],
            "power_status": row["power_status"],
            "report_details": row["report_details"],
            "officer_initials": row["officer_initials"],
            "created_by": row["created_by"],
            "created_by_name": row["created_by_name"],
            "created_at": str(row["created_at"]) if row["created_at"] else None,
            "updated_by": row["updated_by"],
            "updated_by_name": row["updated_by_name"],
            "updated_at": str(row["updated_at"]) if row["updated_at"] else None,
        }

    return grouped


# =====================================================
# GET ALL
# =====================================================

@router.get("")
def get_all_security_guard_reports(
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            sgr.*,
            TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name,
            TRIM(CONCAT(COALESCE(ut.first_name, ''), ' ', COALESCE(ut.last_name, ''))) AS technician_full_name
        FROM security_guard_report sgr
        LEFT JOIN users uc ON uc.user_id = sgr.created_by AND uc.is_deleted = FALSE
        LEFT JOIN users uu ON uu.user_id = sgr.updated_by AND uu.is_deleted = FALSE
        LEFT JOIN users ut ON ut.user_id = sgr.technician_id AND ut.is_deleted = FALSE
        ORDER BY sgr.security_guard_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


# =====================================================
# UPDATE
# =====================================================

@router.put("/{security_guard_id}")
def update_security_guard_report(
    security_guard_id: int,
    payload: SecurityGuardReportUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE security_guard_report
        SET
            station_name = :station_name,
            station_incharge_name = :station_incharge_name,
            shift_code = :shift_code,
            shift_start_time = :shift_start_time,
            log_date = :log_date,
            document_number = :document_number,
            status = :status,
            ms_logbook_id = :ms_logbook_id,
            technician_id = :technician_id,
            critical_report = :critical_report,
            updated_by = :updated_by,
            updated_at = NOW()
        WHERE security_guard_id = :security_guard_id
    """)

    params = payload.dict()
    params["security_guard_id"] = security_guard_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Report not found")

    return {"message": "Security Guard Report updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{security_guard_id}")
def delete_security_guard_report(
    security_guard_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM security_guard_report
        WHERE security_guard_id = :id
    """)

    result = db.execute(query, {"id": security_guard_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Report not found")

    return {"message": "Security Guard Report deleted successfully"}