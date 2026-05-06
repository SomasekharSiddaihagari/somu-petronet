# app/crud/dg_250kva_entry_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_dg_250kva.dg_250kva_entry_schema import (
    DG250KVAEntryCreate,
    DG250KVAEntryUpdate
)


def create_dg_250kva_entry(db: Session, payload: DG250KVAEntryCreate):
    query = text("""
        INSERT INTO dg_250kva_entry (
            master_id,
            log_date,
            start_time, stop_time, run_time,
            cumulative, hmr, battery_voltage, lube_oil_pressure,
            rpm, electrical_hmr, water_temperature,
            voltage_load, voltage_ry, voltage_yb, voltage_br,
            current_r, current_y, current_b,
            kwh_initial, kwh_final, kwh_consumed, kwh_cumulative,
            diesel_initial, diesel_final, diesel_consumed, diesel_total,
            remarks, signature   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :log_date,
            :start_time, :stop_time, :run_time,
            :cumulative, :hmr, :battery_voltage, :lube_oil_pressure,
            :rpm, :electrical_hmr, :water_temperature,
            :voltage_load, :voltage_ry, :voltage_yb, :voltage_br,
            :current_r, :current_y, :current_b,
            :kwh_initial, :kwh_final, :kwh_consumed, :kwh_cumulative,
            :diesel_initial, :diesel_final, :diesel_consumed, :diesel_total,
            :remarks, :signature,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING dg_entry_id
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.fetchone()[0]


def update_dg_250kva_entry(
    db: Session,
    dg_entry_id: int,
    payload: DG250KVAEntryUpdate
):
    data = payload.model_dump(exclude_unset=True)

    if not data:
        return False

    set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
    data["dg_entry_id"] = dg_entry_id

    query = text(f"""
        UPDATE dg_250kva_entry
        SET {set_clause}
        WHERE dg_entry_id = :dg_entry_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_dg_250kva_entry(db: Session, dg_entry_id: int):
    query = text("""
        DELETE FROM dg_250kva_entry
        WHERE dg_entry_id = :dg_entry_id
    """)
    result = db.execute(query, {"dg_entry_id": dg_entry_id})
    db.commit()
    return result.rowcount > 0
