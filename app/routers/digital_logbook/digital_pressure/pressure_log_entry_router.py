from pydantic import BaseModel
from datetime import date, datetime, time
from typing import Optional

from app.utils.access_service import validate_token


class PressureLogCreate(BaseModel):
    pressure_id: Optional[int] = None
    entry_date: Optional[date] = None
    entry_time: Optional[time] = None

    sv1_in: Optional[str] = None
    sv1_out: Optional[str] = None
    sv2_in: Optional[str] = None
    sv2_out: Optional[str] = None
    sv3_in: Optional[str] = None
    sv3_out: Optional[str] = None

    sv4_in: Optional[str] = None
    sv4_out: Optional[str] = None
    sv5_in: Optional[str] = None
    sv5_out: Optional[str] = None

    sv6_in: Optional[str] = None
    sv6_out: Optional[str] = None
    sv7_in: Optional[str] = None
    sv7_out: Optional[str] = None
    sv8_in: Optional[str] = None
    sv8_out: Optional[str] = None

    sv9_in: Optional[str] = None
    sv9_out: Optional[str] = None
    sv10_in: Optional[str] = None
    sv10_out: Optional[str] = None

    mangalore_1: Optional[str] = None
    mangalore_2: Optional[str] = None

    neriya_1: Optional[str] = None
    neriya_2: Optional[str] = None
    neriya_3: Optional[str] = None

    hassan_1: Optional[str] = None
    hassan_2: Optional[str] = None

    ip_1: Optional[str] = None
    ip_2: Optional[str] = None

    devangonthi_1: Optional[str] = None
    devangonthi_2: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
class PressureLogUpdate(PressureLogCreate):
    pass
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.database import get_db

from fastapi import HTTPException


router = APIRouter(prefix="/pressure-log", tags=["Pressure Log"],dependencies=[Depends(validate_token)])



@router.post("", response_model=dict)
def create_pressure_log(
    payload: PressureLogCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO pressure_log_entry (
            pressure_id, entry_date, entry_time,

            sv1_in, sv1_out, sv2_in, sv2_out, sv3_in, sv3_out,
            sv4_in, sv4_out, sv5_in, sv5_out,
            sv6_in, sv6_out, sv7_in, sv7_out, sv8_in, sv8_out,
            sv9_in, sv9_out, sv10_in, sv10_out,

            mangalore_1, mangalore_2,
            neriya_1, neriya_2, neriya_3,
            hassan_1, hassan_2,
            ip_1, ip_2,
            devangonthi_1, devangonthi_2   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :pressure_id, :entry_date, :entry_time,

            :sv1_in, :sv1_out, :sv2_in, :sv2_out, :sv3_in, :sv3_out,
            :sv4_in, :sv4_out, :sv5_in, :sv5_out,
            :sv6_in, :sv6_out, :sv7_in, :sv7_out, :sv8_in, :sv8_out,
            :sv9_in, :sv9_out, :sv10_in, :sv10_out,

            :mangalore_1, :mangalore_2,
            :neriya_1, :neriya_2, :neriya_3,
            :hassan_1, :hassan_2,
            :ip_1, :ip_2,
            :devangonthi_1, :devangonthi_2,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING pressure_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Pressure log created successfully",
        "pressure_entry_id": result.scalar()
    }



@router.put("/{pressure_entry_id}", response_model=dict)
def update_pressure_log(
    pressure_entry_id: int,
    payload: PressureLogUpdate,
    db: Session = Depends(get_db)
):
    data = payload.dict(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No fields provided")

    # ← REMOVE updated_at and created_at to avoid duplicate column error
    data.pop("updated_at", None)
    data.pop("created_at", None)

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])

    query = text(f"""
        UPDATE pressure_log_entry
        SET {set_clause},
            updated_at = NOW()
        WHERE pressure_entry_id = :pressure_entry_id
    """)

    data["pressure_entry_id"] = pressure_entry_id

    result = db.execute(query, data)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pressure log not found")

    return {"message": "Pressure log updated successfully"}


@router.get("/{pressure_entry_id}")
def get_pressure_log_by_id(
    pressure_entry_id: int,
    db: Session = Depends(get_db)
):
    entry = db.execute(
        text("""
            SELECT
                e.*,
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) AS created_by_name
            FROM pressure_log_entry e
            LEFT JOIN users u
                ON u.user_id = e.created_by
                AND u.is_deleted = FALSE
            WHERE e.pressure_entry_id = :pressure_entry_id
        """),
        {"pressure_entry_id": pressure_entry_id}
    ).mappings().first()

    if not entry:
        raise HTTPException(status_code=404, detail="Pressure log entry not found")

    return {"data": dict(entry)}
# =====================================================
# DELETE
# =====================================================
@router.delete("/{pressure_entry_id}")
def delete_pressure_log(
    pressure_entry_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM pressure_log_entry
        WHERE pressure_entry_id = :pressure_entry_id
    """)

    result = db.execute(query, {"pressure_entry_id": pressure_entry_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Entry not found")

    return {
        "status": "success",
        "message": "Pressure log deleted"
    }
