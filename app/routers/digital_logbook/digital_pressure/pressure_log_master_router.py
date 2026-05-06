from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from typing import List

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/pressure-log-master",
    tags=["Pressure Log Master"],
    dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS
# =====================================================

class PressureLogMasterCreate(BaseModel):
    logbook_ref_no: Optional[str] = None
    station_name: Optional[str] = None
    station_incharge: Optional[str] = None
    shift: Optional[str] = None
    log_date: Optional[date] = None
    start_time: Optional[time] = None
    shift_a_technician_name: Optional[str] = None
    shift_a_technician_signature: Optional[str] = None
    shift_a_engineer_name: Optional[str] = None
    shift_a_engineer_signature: Optional[str] = None
    shift_b_technician_name: Optional[str] = None
    shift_b_technician_signature: Optional[str] = None
    shift_b_engineer_name: Optional[str] = None
    shift_b_engineer_signature: Optional[str] = None
    shift_c_technician_name: Optional[str] = None
    shift_c_technician_signature: Optional[str] = None
    shift_c_engineer_name: Optional[str] = None
    shift_c_engineer_signature: Optional[str] = None
    is_closed: Optional[bool] = None
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None


class PressureLogMasterUpdate(PressureLogMasterCreate):
    pass



@router.post("")
def create_pressure_log_master(
    payload: PressureLogMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO pressure_log_master (
            logbook_ref_no, station_name, station_incharge,
            shift, log_date, start_time,
            shift_a_technician_name, shift_a_technician_signature,
            shift_a_engineer_name, shift_a_engineer_signature,
            shift_b_technician_name, shift_b_technician_signature,
            shift_b_engineer_name, shift_b_engineer_signature,
            shift_c_technician_name, shift_c_technician_signature,
            shift_c_engineer_name, shift_c_engineer_signature,
            is_closed, created_at, created_by, updated_at, updated_by,
            ms_logbook_id, technician_id
        )
        VALUES (
            :logbook_ref_no, :station_name, :station_incharge,
            :shift, :log_date, :start_time,
            :shift_a_technician_name, :shift_a_technician_signature,
            :shift_a_engineer_name, :shift_a_engineer_signature,
            :shift_b_technician_name, :shift_b_technician_signature,
            :shift_b_engineer_name, :shift_b_engineer_signature,
            :shift_c_technician_name, :shift_c_technician_signature,
            :shift_c_engineer_name, :shift_c_engineer_signature,
            :is_closed, :created_at, :created_by, :updated_at, :updated_by,
            :ms_logbook_id, :technician_id
        )
        RETURNING pressure_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Pressure Log Master created successfully",
        "pressure_id": result.scalar()
    }



# =====================================================
# GET BY ms_logbook_id
# =====================================================

@router.get("/pressure/{ms_logbook_id}")
def get_pressure_logbook(
    ms_logbook_id: int,
    db: Session = Depends(get_db)
):
    shift = db.execute(
        text("""
            SELECT *
            FROM logbook_shift_master
            WHERE ms_logbook_id = :ms_logbook_id
        """),
        {"ms_logbook_id": ms_logbook_id}
    ).mappings().first()

    if not shift:
        raise HTTPException(status_code=404, detail="Logbook shift master not found")

    pressure_id = shift["pressure_id"]

    if not pressure_id:
        return {
            "ms_logbook_id": ms_logbook_id,
            "module": "pressure",
            "message": "Pressure log not created for this shift",
            "pressure": None
        }

    pressure_master = db.execute(
        text("""
            SELECT
                plm.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(t.first_name, ''), ' ', COALESCE(t.last_name, ''))) AS technician_full_name,
                u.station_id
            FROM pressure_log_master plm
            LEFT JOIN users u ON u.user_id = plm.created_by AND u.is_deleted = FALSE
            LEFT JOIN users t ON t.user_id = plm.technician_id AND t.is_deleted = FALSE
            WHERE plm.pressure_id = :pressure_id
        """),
        {"pressure_id": pressure_id}
    ).mappings().first()

    if not pressure_master:
        return {
            "ms_logbook_id": ms_logbook_id,
            "module": "pressure",
            "message": "Pressure master record missing",
            "pressure": None
        }

    pressure_entries = db.execute(
        text("""
            SELECT *
            FROM pressure_log_entry
            WHERE pressure_id = :pressure_id
            ORDER BY entry_date, entry_time
        """),
        {"pressure_id": pressure_id}
    ).mappings().all()

    return {
        "ms_logbook_id": ms_logbook_id,
        "module": "pressure",
        "pressure": {
            "master": dict(pressure_master),
            "entries": [dict(e) for e in pressure_entries]
        }
    }


# =====================================================
# POST — CREATE
# =====================================================


# =====================================================
# PUT — FULL UPDATE
# =====================================================

@router.put("/{pressure_id}")
def update_pressure_log_master(
    pressure_id: int,
    payload: PressureLogMasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = pressure_id

    query = text("""
        UPDATE pressure_log_master
        SET
            logbook_ref_no               = :logbook_ref_no,
            station_name                 = :station_name,
            station_incharge             = :station_incharge,
            shift                        = :shift,
            log_date                     = :log_date,
            start_time                   = :start_time,
            shift_a_technician_name      = :shift_a_technician_name,
            shift_a_technician_signature = :shift_a_technician_signature,
            shift_a_engineer_name        = :shift_a_engineer_name,
            shift_a_engineer_signature   = :shift_a_engineer_signature,
            shift_b_technician_name      = :shift_b_technician_name,
            shift_b_technician_signature = :shift_b_technician_signature,
            shift_b_engineer_name        = :shift_b_engineer_name,
            shift_b_engineer_signature   = :shift_b_engineer_signature,
            shift_c_technician_name      = :shift_c_technician_name,
            shift_c_technician_signature = :shift_c_technician_signature,
            shift_c_engineer_name        = :shift_c_engineer_name,
            shift_c_engineer_signature   = :shift_c_engineer_signature,
            is_closed                    = :is_closed,
            created_at                   = :created_at,
            created_by                   = :created_by,
            updated_at                   = :updated_at,
            updated_by                   = :updated_by,
            ms_logbook_id                = :ms_logbook_id,
            technician_id                = :technician_id
        WHERE pressure_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pressure Log Master not found")

    return {"message": "Pressure Log Master updated successfully"}


# =====================================================
# GET ALL
# =====================================================

@router.get("")
def get_all_pressure_log_masters(
    station_id: Optional[int] = Query(None, description="Filter by station"),
    db: Session = Depends(get_db)
):
    where = "WHERE u.station_id = :station_id" if station_id else ""
    params = {"station_id": station_id} if station_id else {}

    rows = db.execute(
        text(f"""
            SELECT
                plm.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(t.first_name, ''), ' ', COALESCE(t.last_name, ''))) AS technician_full_name,
                u.station_id
            FROM pressure_log_master plm
            LEFT JOIN users u ON u.user_id = plm.created_by AND u.is_deleted = FALSE
            LEFT JOIN users t ON t.user_id = plm.technician_id AND t.is_deleted = FALSE
            {where}
            ORDER BY plm.pressure_id DESC
        """),
        params
    ).mappings().all()

    return {
        "count": len(rows),
        "data": [dict(r) for r in rows]
    }


# =====================================================
# GET BY DATE
# =====================================================

@router.get("/by-date")
def get_pressure_log_master_by_date(
    log_date: date,
    station_id: Optional[int] = Query(None, description="Filter by station"),
    db: Session = Depends(get_db)
):
    station_filter = "AND (u.station_id = :station_id OR uu.station_id = :station_id)" if station_id else ""
    params = {"log_date": log_date}
    if station_id:
        params["station_id"] = station_id

    masters = db.execute(
        text(f"""
            SELECT
                plm.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(t.first_name, ''), ' ', COALESCE(t.last_name, ''))) AS technician_full_name,
                COALESCE(u.station_id, uu.station_id) AS station_id
            FROM pressure_log_master plm
            LEFT JOIN users u ON u.user_id = plm.created_by AND u.is_deleted = FALSE
            LEFT JOIN users uu ON uu.user_id = plm.updated_by AND uu.is_deleted = FALSE
            LEFT JOIN users t ON t.user_id = plm.technician_id AND t.is_deleted = FALSE
            LEFT JOIN logbook_shift_master LSM
                ON LSM.ms_logbook_id = plm.ms_logbook_id
            WHERE (
                (
                    plm.ms_logbook_id IS NOT NULL
                    AND (
                        CASE
                            WHEN EXTRACT(HOUR FROM LSM.created_at) < 7
                            THEN DATE(LSM.created_at - INTERVAL '1 day')
                            ELSE DATE(LSM.created_at)
                        END
                    ) = :log_date
                )
                OR
                (
                    plm.ms_logbook_id IS NULL
                    AND DATE(plm.created_at) = :log_date
                )
            )
            {station_filter}
        """),
        params
    ).mappings().all()

    if not masters:
        return {"count": 0, "data": []}

    response = []
    for master in masters:
        entries = db.execute(
            text("""
                SELECT
                    e.*,
                    TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
                    TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
                FROM pressure_log_entry e
                LEFT JOIN users uc ON uc.user_id = e.created_by AND uc.is_deleted = FALSE
                LEFT JOIN users uu ON uu.user_id = e.updated_by AND uu.is_deleted = FALSE
                WHERE e.pressure_id = :pressure_id
                ORDER BY e.entry_date ASC, e.entry_time ASC
            """),
            {"pressure_id": master["pressure_id"]}
        ).mappings().all()

        response.append({
            **dict(master),
            "entries": [dict(e) for e in entries]
        })

    return {"count": len(response), "data": response}


# =====================================================
# GET BY ID
# =====================================================

@router.get("/{pressure_id}")
def get_pressure_log_master_by_id(
    pressure_id: int,
    db: Session = Depends(get_db)
):
    master = db.execute(
        text("""
            SELECT
                plm.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,
                TRIM(CONCAT(COALESCE(t.first_name, ''), ' ', COALESCE(t.last_name, ''))) AS technician_full_name,
                u.station_id
            FROM pressure_log_master plm
            LEFT JOIN users u ON u.user_id = plm.created_by AND u.is_deleted = FALSE
            LEFT JOIN users t ON t.user_id = plm.technician_id AND t.is_deleted = FALSE
            WHERE plm.pressure_id = :pressure_id
        """),
        {"pressure_id": pressure_id}
    ).mappings().first()

    if not master:
        raise HTTPException(status_code=404, detail="Pressure Log Master not found")

    entries = db.execute(
        text("""
            SELECT
                e.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name
            FROM pressure_log_entry e
            LEFT JOIN users u ON u.user_id = e.created_by AND u.is_deleted = FALSE
            WHERE e.pressure_id = :pressure_id
            ORDER BY e.entry_date ASC, e.entry_time ASC
        """),
        {"pressure_id": pressure_id}
    ).mappings().all()

    return {
        "data": {
            **dict(master),
            "entries": [dict(e) for e in entries]
        }
    }


# =====================================================
# DELETE
# =====================================================

@router.delete("/{pressure_id}")
def delete_pressure_log_master(
    pressure_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM pressure_log_master
            WHERE pressure_id = :id
        """),
        {"id": pressure_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pressure Log Master not found")

    return {"message": "Pressure Log Master deleted successfully"}
