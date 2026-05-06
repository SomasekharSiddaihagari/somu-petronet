from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from typing import List

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/vibration-temperature-master",
    tags=["Vibration & Temperature Master MLR"],
    dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS
# =====================================================

class VibrationTemperatureMasterCreate(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[time] = None
    logbook_date: Optional[date] = None
    ms_logbook_id: Optional[int] = None

    shift_engineer_a_name: Optional[str] = None
    shift_engineer_a_signature: Optional[str] = None

    shift_engineer_b_name: Optional[str] = None
    shift_engineer_b_signature: Optional[str] = None

    shift_engineer_c_name: Optional[str] = None        # ← ADDED
    shift_engineer_c_signature: Optional[str] = None   # ← ADDED
      
    technician_a_id: Optional[int] = None              # ← ADDED


    technician_b_id: Optional[int] = None              # ← ADDED

 
    technician_c_signature: Optional[str] = None
    technician_c_id: Optional[int] = None              # ← ADDED

    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None


class VibrationTemperatureMasterUpdate(VibrationTemperatureMasterCreate):
    pass


# =====================================================
# POST — CREATE MASTER
# =====================================================

@router.post("")
def create_vibration_temperature_master(
    payload: VibrationTemperatureMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO vibration_temperature_master_mlr (
            station,
            station_in_charge,
            shift,
            start_time,
            logbook_date,
            ms_logbook_id,

            shift_engineer_a_name,
            shift_engineer_a_signature,

            shift_engineer_b_name,
            shift_engineer_b_signature,

            shift_engineer_c_name,
            shift_engineer_c_signature,

     
            technician_a_id,

       
            technician_b_id,

          
            technician_c_signature,
            technician_c_id,

            created_at,
            created_by,
            updated_at,
            updated_by
        )
        VALUES (
            :station,
            :station_in_charge,
            :shift,
            :start_time,
            :logbook_date,
            :ms_logbook_id,

            :shift_engineer_a_name,
            :shift_engineer_a_signature,

            :shift_engineer_b_name,
            :shift_engineer_b_signature,

            :shift_engineer_c_name,
            :shift_engineer_c_signature,

         
            :technician_a_id,

       
            :technician_b_id,

         
            :technician_c_signature,
            :technician_c_id,

            :created_at,
            :created_by,
            :updated_at,
            :updated_by
        )
        RETURNING vtm_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Vibration & temperature master created successfully",
        "vtm_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE
# =====================================================

@router.put("/{vtm_id}")
def update_vibration_temperature_master(
    vtm_id: int,
    payload: VibrationTemperatureMasterUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = vtm_id

    query = text("""
        UPDATE vibration_temperature_master_mlr
        SET
            station                    = :station,
            station_in_charge          = :station_in_charge,
            shift                      = :shift,
            start_time                 = :start_time,
            logbook_date               = :logbook_date,
            ms_logbook_id              = :ms_logbook_id,

            shift_engineer_a_name      = :shift_engineer_a_name,
            shift_engineer_a_signature = :shift_engineer_a_signature,

            shift_engineer_b_name      = :shift_engineer_b_name,
            shift_engineer_b_signature = :shift_engineer_b_signature,

            shift_engineer_c_name      = :shift_engineer_c_name,
            shift_engineer_c_signature = :shift_engineer_c_signature,

        
            technician_a_id            = :technician_a_id,

        
            technician_b_id            = :technician_b_id,

       
            technician_c_signature     = :technician_c_signature,
            technician_c_id            = :technician_c_id,

            created_at  = :created_at,
            created_by  = :created_by,
            updated_at  = :updated_at,
            updated_by  = :updated_by

        WHERE vtm_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature master not found"
        )

    return {"message": "Vibration & temperature master updated successfully"}


# =====================================================
# GET BY DATE
# =====================================================

@router.get("/by-date")
def get_vibration_temperature_master_by_date(
    log_date: date,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            vtm.*,
            TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,

            TRIM(CONCAT(COALESCE(ta.first_name, ''), ' ', COALESCE(ta.last_name, ''))) AS technician_a_full_name,
            TRIM(CONCAT(COALESCE(tb.first_name, ''), ' ', COALESCE(tb.last_name, ''))) AS technician_b_full_name,
            TRIM(CONCAT(COALESCE(tc.first_name, ''), ' ', COALESCE(tc.last_name, ''))) AS technician_c_full_name,

            CASE
                WHEN EXTRACT(HOUR FROM LSM.created_at) < 7
                THEN DATE(LSM.created_at - INTERVAL '1 day')
                ELSE DATE(LSM.created_at)
            END AS logbook_date

        FROM vibration_temperature_master_mlr vtm

        LEFT JOIN users u
            ON u.user_id = vtm.created_by::int
            AND u.is_deleted = FALSE

        LEFT JOIN users ta
            ON ta.user_id = vtm.technician_a_id
            AND ta.is_deleted = FALSE

        LEFT JOIN users tb
            ON tb.user_id = vtm.technician_b_id
            AND tb.is_deleted = FALSE

        LEFT JOIN users tc
            ON tc.user_id = vtm.technician_c_id
            AND tc.is_deleted = FALSE

        JOIN logbook_shift_master LSM
            ON LSM.ms_logbook_id = vtm.ms_logbook_id

        WHERE
            CASE
                WHEN EXTRACT(HOUR FROM LSM.created_at) < 7
                THEN DATE(LSM.created_at - INTERVAL '1 day')
                ELSE DATE(LSM.created_at)
            END = :log_date
    """)

    rows = db.execute(query, {"log_date": log_date}).mappings().all()

    if not rows:
        return {"count": 0, "data": []}

    result = []
    for row in rows:
        master_dict = dict(row)
        vtm_id = master_dict["vtm_id"]

        entries = db.execute(
            text("""
                SELECT
                    vte.*,
                    TRIM(CONCAT(COALESCE(uc.first_name, ''), ' ', COALESCE(uc.last_name, ''))) AS created_by_name,
                    TRIM(CONCAT(COALESCE(uu.first_name, ''), ' ', COALESCE(uu.last_name, ''))) AS updated_by_name
                FROM vibration_temperature_entry vte
                LEFT JOIN users uc
                    ON uc.user_id = vte.created_by::int
                    AND uc.is_deleted = FALSE
                LEFT JOIN users uu
                    ON uu.user_id = vte.updated_by::int
                    AND uu.is_deleted = FALSE
                WHERE vte.master_id = :vtm_id
                ORDER BY vte.vte_id ASC
            """),
            {"vtm_id": vtm_id}
        ).mappings().all()

        master_dict["entries"] = [dict(e) for e in entries]
        result.append(master_dict)

    return {"count": len(result), "data": result}


# =====================================================
# GET ALL
# =====================================================

@router.get("")
def get_all_vibration_temperature_masters(
    db: Session = Depends(get_db)
):
    rows = db.execute(
        text("""
            SELECT *
            FROM vibration_temperature_master_mlr
            ORDER BY vtm_id DESC
        """)
    ).mappings().all()

    return {
        "count": len(rows),
        "data": [dict(r) for r in rows]
    }


# =====================================================
# GET BY ID (MASTER + ENTRIES)
# =====================================================

@router.get("/{vtm_id}")
def get_vibration_temperature_master_by_id(
    vtm_id: int,
    db: Session = Depends(get_db)
):
    master = db.execute(
        text("""
            SELECT 
                vtm.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name,

                -- Technician A name from users
                TRIM(CONCAT(COALESCE(ta.first_name, ''), ' ', COALESCE(ta.last_name, ''))) AS technician_a_full_name,

                -- Technician B name from users
                TRIM(CONCAT(COALESCE(tb.first_name, ''), ' ', COALESCE(tb.last_name, ''))) AS technician_b_full_name,

                -- Technician C name from users
                TRIM(CONCAT(COALESCE(tc.first_name, ''), ' ', COALESCE(tc.last_name, ''))) AS technician_c_full_name

            FROM vibration_temperature_master_mlr vtm

            LEFT JOIN users u
                ON u.user_id = vtm.created_by::int
                AND u.is_deleted = FALSE

            LEFT JOIN users ta
                ON ta.user_id = vtm.technician_a_id
                AND ta.is_deleted = FALSE

            LEFT JOIN users tb
                ON tb.user_id = vtm.technician_b_id
                AND tb.is_deleted = FALSE

            LEFT JOIN users tc
                ON tc.user_id = vtm.technician_c_id
                AND tc.is_deleted = FALSE

            WHERE vtm.vtm_id = :vtm_id
        """),
        {"vtm_id": vtm_id}
    ).mappings().first()

    if not master:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature master not found"
        )

    entries = db.execute(
        text("""
            SELECT
                e.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name
            FROM vibration_temperature_entry e
            LEFT JOIN users u
                ON u.user_id = e.created_by::int
                AND u.is_deleted = FALSE
            WHERE e.master_id = :vtm_id
            ORDER BY e.vte_id ASC
        """),
        {"vtm_id": vtm_id}
    ).mappings().all()

    data = dict(master)
    data["entries"] = [dict(e) for e in entries]

    return {"data": data}



# =====================================================
# DELETE
# =====================================================

@router.delete("/{vtm_id}")
def delete_vibration_temperature_master(
    vtm_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM vibration_temperature_master_mlr
            WHERE vtm_id = :id
        """),
        {"id": vtm_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature master not found"
        )

    return {"message": "Vibration & temperature master deleted successfully"}