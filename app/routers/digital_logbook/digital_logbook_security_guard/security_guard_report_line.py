from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import time, date, datetime
from decimal import Decimal

from app.database import get_db
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/security-guard-report-line",
    tags=["Security Guard Report Line"],
    dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMA
# =====================================================

class SecurityGuardReportLineCreate(BaseModel):
    report_id: int

    location_name: str
    shift: str

    security_guard_name: Optional[str] = None
    security_guard_name_two: Optional[str] = None

    duty_start_time: Optional[time] = None
    duty_end_time: Optional[time] = None

    battery_cp_volt: Optional[Decimal] = None
    battery_tel_volt: Optional[Decimal] = None

    power_status: Optional[str] = None
    report_details: Optional[str] = None
    officer_initials: Optional[str] = None

    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class SecurityGuardReportLineUpdate(SecurityGuardReportLineCreate):
    pass


# =====================================================
# CREATE
# =====================================================

@router.post("")
def create_security_guard_report_line(
    payload: SecurityGuardReportLineCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO security_guard_report_line (
            report_id,
            location_name,
            shift,
            security_guard_name,
            security_guard_name_two,
            duty_start_time,
            duty_end_time,
            battery_cp_volt,
            battery_tel_volt,
            power_status,
            report_details,
            officer_initials,
            created_by,
            created_at,
            updated_by,
            updated_at
        )
        VALUES (
            :report_id,
            :location_name,
            :shift,
            :security_guard_name,
            :security_guard_name_two,
            :duty_start_time,
            :duty_end_time,
            :battery_cp_volt,
            :battery_tel_volt,
            :power_status,
            :report_details,
            :officer_initials,
            :created_by,
            NOW(),
            :updated_by,
            NOW()
        )
        RETURNING sgrl_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Line created successfully",
        "sgrl_id": result.scalar()
    }


# =====================================================
# GET BY ID
# =====================================================

@router.get("/{sgrl_id}")
def get_security_guard_report_line(
    sgrl_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            sgrl.*,
            TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
        FROM security_guard_report_line sgrl
        LEFT JOIN users uc ON uc.user_id = sgrl.created_by AND uc.is_deleted = FALSE
        LEFT JOIN users uu ON uu.user_id = sgrl.updated_by AND uu.is_deleted = FALSE
        WHERE sgrl.sgrl_id = :id
    """)

    result = db.execute(query, {"id": sgrl_id}).mappings().first()

    if not result:
        raise HTTPException(status_code=404, detail="Line not found")

    return result


# =====================================================
# GET BY REPORT ID + DATE  →  grouped by location → shift
# =====================================================

@router.get("/by-report/{report_id}")
def get_lines_by_report_and_date(
    report_id: int,
    report_date: Optional[date] = Query(None, description="Filter by date e.g. 2024-01-15"),
    db: Session = Depends(get_db)
):
    if report_date:
        query = text("""
            SELECT
                sgrl.*,
                TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
            FROM security_guard_report_line sgrl
            JOIN security_guard_report sgr ON sgr.security_guard_id = sgrl.report_id
            LEFT JOIN users uc ON uc.user_id = sgrl.created_by AND uc.is_deleted = FALSE
            LEFT JOIN users uu ON uu.user_id = sgrl.updated_by AND uu.is_deleted = FALSE
            WHERE sgrl.report_id = :report_id
              AND sgr.log_date = :report_date
            ORDER BY sgrl.location_name, sgrl.shift
        """)
        rows = db.execute(query, {
            "report_id": report_id,
            "report_date": report_date
        }).mappings().all()
    else:
        query = text("""
            SELECT
                sgrl.*,
                TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
            FROM security_guard_report_line sgrl
            LEFT JOIN users uc ON uc.user_id = sgrl.created_by AND uc.is_deleted = FALSE
            LEFT JOIN users uu ON uu.user_id = sgrl.updated_by AND uu.is_deleted = FALSE
            WHERE sgrl.report_id = :report_id
            ORDER BY sgrl.location_name, sgrl.shift
        """)
        rows = db.execute(query, {"report_id": report_id}).mappings().all()

    # Group by location → shift
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
# UPDATE
# =====================================================

@router.put("/{sgrl_id}")
def update_security_guard_report_line(
    sgrl_id: int,
    payload: SecurityGuardReportLineUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE security_guard_report_line
        SET
            report_id = :report_id,
            location_name = :location_name,
            shift = :shift,
            security_guard_name = :security_guard_name,
            security_guard_name_two = :security_guard_name_two,
            duty_start_time = :duty_start_time,
            duty_end_time = :duty_end_time,
            battery_cp_volt = :battery_cp_volt,
            battery_tel_volt = :battery_tel_volt,
            power_status = :power_status,
            report_details = :report_details,
            officer_initials = :officer_initials,
            updated_by = :updated_by,
            updated_at = NOW()
        WHERE sgrl_id = :sgrl_id
    """)

    params = payload.dict()
    params["sgrl_id"] = sgrl_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Line not found")

    return {"message": "Line updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{sgrl_id}")
def delete_security_guard_report_line(
    sgrl_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM security_guard_report_line
        WHERE sgrl_id = :id
    """)

    result = db.execute(query, {"id": sgrl_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Line not found")

    return {"message": "Line deleted successfully"}