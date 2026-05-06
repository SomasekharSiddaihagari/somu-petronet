from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/vibration-temperature-entry",
    tags=["Vibration & Temperature Entry MLR"],
    dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS
# =====================================================

class VibrationTemperatureEntryCreate(BaseModel):
    master_id: Optional[int] = None

    entry_date: Optional[date] = None
    entry_time: Optional[time] = None
    mlp101_a_b_c: Optional[str] = None

    pump_vib_de_x: Optional[float] = None
    pump_vib_de_y: Optional[float] = None
    pump_vib_nde_x: Optional[float] = None
    pump_vib_nde_y: Optional[float] = None

    pump_thrust_x: Optional[float] = None
    pump_thrust_y: Optional[float] = None

    motor_bearing_vib_de_x: Optional[float] = None
    motor_bearing_vib_de_y: Optional[float] = None
    motor_bearing_vib_nde_x: Optional[float] = None
    motor_bearing_vib_nde_y: Optional[float] = None

    motor_winding_ch1: Optional[float] = None
    motor_winding_ch2: Optional[float] = None
    motor_winding_ch3: Optional[float] = None

    motor_winding_ch4: Optional[float] = None
    motor_winding_ch5: Optional[float] = None
    motor_winding_ch6: Optional[float] = None

    motor_bearing_temp_de: Optional[float] = None
    motor_bearing_temp_nde: Optional[float] = None

    pump_body_temperature: Optional[float] = None

    pump_bearing_temp_de_x: Optional[float] = None
    pump_bearing_temp_de_y: Optional[float] = None
    pump_bearing_temp_nde_x: Optional[float] = None
    pump_bearing_temp_nde_y: Optional[float] = None
    pump_bearing_thrust_x: Optional[float] = None
    pump_bearing_thrust_y: Optional[float] = None

    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None


class VibrationTemperatureEntryUpdate(VibrationTemperatureEntryCreate):
    pass


# =====================================================
# POST — CREATE ENTRY
# =====================================================

@router.post("")
def create_vibration_temperature_entry(
    payload: VibrationTemperatureEntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO vibration_temperature_entry (
            master_id,
            entry_date,
            entry_time,
            mlp101_a_b_c,

            pump_vib_de_x,
            pump_vib_de_y,
            pump_vib_nde_x,
            pump_vib_nde_y,

            pump_thrust_x,
            pump_thrust_y,

            motor_bearing_vib_de_x,
            motor_bearing_vib_de_y,
            motor_bearing_vib_nde_x,
            motor_bearing_vib_nde_y,

            motor_winding_ch1,
            motor_winding_ch2,
            motor_winding_ch3,

            motor_winding_ch4,
            motor_winding_ch5,
            motor_winding_ch6,

            motor_bearing_temp_de,
            motor_bearing_temp_nde,

            pump_body_temperature,

            pump_bearing_temp_de_x,
            pump_bearing_temp_de_y,
            pump_bearing_temp_nde_x,
            pump_bearing_temp_nde_y,
            pump_bearing_thrust_x,
            pump_bearing_thrust_y,

            created_at,
            created_by,
            updated_at,
            updated_by
        )
        VALUES (
            :master_id,
            :entry_date,
            :entry_time,
            :mlp101_a_b_c,

            :pump_vib_de_x,
            :pump_vib_de_y,
            :pump_vib_nde_x,
            :pump_vib_nde_y,

            :pump_thrust_x,
            :pump_thrust_y,

            :motor_bearing_vib_de_x,
            :motor_bearing_vib_de_y,
            :motor_bearing_vib_nde_x,
            :motor_bearing_vib_nde_y,

            :motor_winding_ch1,
            :motor_winding_ch2,
            :motor_winding_ch3,

            :motor_winding_ch4,
            :motor_winding_ch5,
            :motor_winding_ch6,

            :motor_bearing_temp_de,
            :motor_bearing_temp_nde,

            :pump_body_temperature,

            :pump_bearing_temp_de_x,
            :pump_bearing_temp_de_y,
            :pump_bearing_temp_nde_x,
            :pump_bearing_temp_nde_y,
            :pump_bearing_thrust_x,
            :pump_bearing_thrust_y,

            :created_at,
            :created_by,
            :updated_at,
            :updated_by
        )
        RETURNING vte_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Vibration & temperature entry created successfully",
        "vte_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE
# =====================================================

@router.put("/{vte_id}")
def update_vibration_temperature_entry(
    vte_id: int,
    payload: VibrationTemperatureEntryUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = vte_id

    query = text("""
        UPDATE vibration_temperature_entry
        SET
            master_id               = :master_id,
            entry_date              = :entry_date,
            entry_time              = :entry_time,
            mlp101_a_b_c            = :mlp101_a_b_c,

            pump_vib_de_x           = :pump_vib_de_x,
            pump_vib_de_y           = :pump_vib_de_y,
            pump_vib_nde_x          = :pump_vib_nde_x,
            pump_vib_nde_y          = :pump_vib_nde_y,

            pump_thrust_x           = :pump_thrust_x,
            pump_thrust_y           = :pump_thrust_y,

            motor_bearing_vib_de_x  = :motor_bearing_vib_de_x,
            motor_bearing_vib_de_y  = :motor_bearing_vib_de_y,
            motor_bearing_vib_nde_x = :motor_bearing_vib_nde_x,
            motor_bearing_vib_nde_y = :motor_bearing_vib_nde_y,

            motor_winding_ch1       = :motor_winding_ch1,
            motor_winding_ch2       = :motor_winding_ch2,
            motor_winding_ch3       = :motor_winding_ch3,

            motor_winding_ch4       = :motor_winding_ch4,
            motor_winding_ch5       = :motor_winding_ch5,
            motor_winding_ch6       = :motor_winding_ch6,

            motor_bearing_temp_de   = :motor_bearing_temp_de,
            motor_bearing_temp_nde  = :motor_bearing_temp_nde,

            pump_body_temperature   = :pump_body_temperature,

            pump_bearing_temp_de_x  = :pump_bearing_temp_de_x,
            pump_bearing_temp_de_y  = :pump_bearing_temp_de_y,
            pump_bearing_temp_nde_x = :pump_bearing_temp_nde_x,
            pump_bearing_temp_nde_y = :pump_bearing_temp_nde_y,
            pump_bearing_thrust_x   = :pump_bearing_thrust_x,
            pump_bearing_thrust_y   = :pump_bearing_thrust_y,

            created_at  = :created_at,
            created_by  = :created_by,
            updated_at  = :updated_at,
            updated_by  = :updated_by

        WHERE vte_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature entry not found"
        )

    return {"message": "Vibration & temperature entry updated successfully"}


# =====================================================
# GET ALL
# =====================================================

@router.get("")
def get_all_vibration_temperature_entries(
    db: Session = Depends(get_db)
):
    rows = db.execute(
        text("""
            SELECT *
            FROM vibration_temperature_entry
            ORDER BY vte_id DESC
        """)
    ).mappings().all()

    return {
        "count": len(rows),
        "data": [dict(r) for r in rows]
    }


# =====================================================
# GET BY ID
# =====================================================

@router.get("/{vte_id}")
def get_vibration_temperature_entry_by_id(
    vte_id: int,
    db: Session = Depends(get_db)
):
    row = db.execute(
        text("""
            SELECT *
            FROM vibration_temperature_entry
            WHERE vte_id = :vte_id
        """),
        {"vte_id": vte_id}
    ).mappings().first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature entry not found"
        )

    return {"data": dict(row)}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{vte_id}")
def delete_vibration_temperature_entry(
    vte_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM vibration_temperature_entry
            WHERE vte_id = :id
        """),
        {"id": vte_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature entry not found"
        )

    return {"message": "Vibration & temperature entry deleted successfully"}