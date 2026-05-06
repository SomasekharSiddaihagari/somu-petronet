from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/vibration-temperature-entry-ner",
    tags=["Vibration & Temperature Entry NER"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class VibrationTemperatureEntryNerCreate(BaseModel):
    master_id: Optional[int]

    entry_date: Optional[date]
    entry_time: Optional[time]
    mlp101_a_b_c: Optional[str]

    # -------- Pump Vibration --------
    pump_vib_de_x: Optional[float]
    pump_vib_de_y: Optional[float]
    pump_vib_nde_x: Optional[float]
    pump_vib_nde_y: Optional[float]

    # -------- Pump Thrust --------
    pump_thrust_x: Optional[float]
    pump_thrust_y: Optional[float]

    # -------- Motor Bearing Vibration --------
    motor_bearing_vib_de_x: Optional[float]
    motor_bearing_vib_de_y: Optional[float]
    motor_bearing_vib_nde_x: Optional[float]
    motor_bearing_vib_nde_y: Optional[float]

    # -------- Motor Winding Temperature (CH1–3) --------
    motor_winding_ch1: Optional[float]
    motor_winding_ch2: Optional[float]
    motor_winding_ch3: Optional[float]

    # -------- Motor Winding Temperature (CH4–6) --------
    motor_winding_ch4: Optional[float]
    motor_winding_ch5: Optional[float]
    motor_winding_ch6: Optional[float]

    # -------- Motor Bearing Temperature --------
    motor_bearing_temp_de: Optional[float]
    motor_bearing_temp_nde: Optional[float]

    # -------- Pump Body Temperature --------
    pump_body_temperature: Optional[float]

    # -------- Pump Bearing Temperature --------
    pump_bearing_temp_de_x: Optional[float]
    pump_bearing_temp_de_y: Optional[float]
    pump_bearing_temp_nde_x: Optional[float]
    pump_bearing_temp_nde_y: Optional[float]
    pump_bearing_thrust_x: Optional[float]
    pump_bearing_thrust_y: Optional[float]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class VibrationTemperatureEntryNerUpdate(VibrationTemperatureEntryNerCreate):
    pass


# =====================================================
# POST — CREATE ENTRY
# =====================================================

@router.post("")
def create_vibration_temperature_entry_ner(
    payload: VibrationTemperatureEntryNerCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO vibration_temperature_entry_ner (
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
            pump_bearing_thrust_y   ,created_at,created_by ,updated_at ,updated_by

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
            :pump_bearing_thrust_y,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING vten_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Vibration & temperature entry (NER) created successfully",
        "vten_id": result.scalar()
    }


# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================

@router.put("/{vten_id}")
def update_vibration_temperature_entry_ner(
    vten_id: int,
    payload: VibrationTemperatureEntryNerUpdate,
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = vten_id

    query = text("""
        UPDATE vibration_temperature_entry_ner
        SET
            master_id = :master_id,
            entry_date = :entry_date,
            entry_time = :entry_time,
            mlp101_a_b_c = :mlp101_a_b_c,

            pump_vib_de_x = :pump_vib_de_x,
            pump_vib_de_y = :pump_vib_de_y,
            pump_vib_nde_x = :pump_vib_nde_x,
            pump_vib_nde_y = :pump_vib_nde_y,

            pump_thrust_x = :pump_thrust_x,
            pump_thrust_y = :pump_thrust_y,

            motor_bearing_vib_de_x = :motor_bearing_vib_de_x,
            motor_bearing_vib_de_y = :motor_bearing_vib_de_y,
            motor_bearing_vib_nde_x = :motor_bearing_vib_nde_x,
            motor_bearing_vib_nde_y = :motor_bearing_vib_nde_y,

            motor_winding_ch1 = :motor_winding_ch1,
            motor_winding_ch2 = :motor_winding_ch2,
            motor_winding_ch3 = :motor_winding_ch3,

            motor_winding_ch4 = :motor_winding_ch4,
            motor_winding_ch5 = :motor_winding_ch5,
            motor_winding_ch6 = :motor_winding_ch6,

            motor_bearing_temp_de = :motor_bearing_temp_de,
            motor_bearing_temp_nde = :motor_bearing_temp_nde,

            pump_body_temperature = :pump_body_temperature,

            pump_bearing_temp_de_x = :pump_bearing_temp_de_x,
            pump_bearing_temp_de_y = :pump_bearing_temp_de_y,
            pump_bearing_temp_nde_x = :pump_bearing_temp_nde_x,
            pump_bearing_temp_nde_y = :pump_bearing_temp_nde_y,
            pump_bearing_thrust_x = :pump_bearing_thrust_x,
            pump_bearing_thrust_y = :pump_bearing_thrust_y ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE vten_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature entry (NER) not found"
        )

    return {"message": "Vibration & temperature entry (NER) updated successfully"}



@router.get("")
def get_all_vibration_temperature_entries_ner(
    db: Session = Depends(get_db)
):
    rows = db.execute(
        text("""
            SELECT *
            FROM vibration_temperature_entry_ner
            ORDER BY vten_id DESC
        """)
    ).mappings().all()

    return {
        "count": len(rows),
        "data": [dict(r) for r in rows]
    }


# =====================================================
# GET BY ID  ← ADDED
# =====================================================

@router.get("/{vten_id}")
def get_vibration_temperature_entry_ner_by_id(
    vten_id: int,
    db: Session = Depends(get_db)
):
    row = db.execute(
        text("""
            SELECT *
            FROM vibration_temperature_entry_ner
            WHERE vten_id = :vten_id
        """),
        {"vten_id": vten_id}
    ).mappings().first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature entry (NER) not found"
        )

    return {"data": dict(row)}




# =====================================================
# DELETE
# =====================================================

@router.delete("/{vten_id}")
def delete_vibration_temperature_entry_ner(
    vten_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM vibration_temperature_entry_ner
            WHERE vten_id = :id
        """),
        {"id": vten_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Vibration & temperature entry (NER) not found"
        )

    return {"message": "Vibration & temperature entry (NER) deleted successfully"}
