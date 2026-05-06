# app/crud/mfm_shutdown_detail_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_mfm_logbook.mfm_shutdown_detail_dsk_schema import (
    MFMShutdownDetailCreate,
    MFMShutdownDetailUpdate
)


def create_mfm_shutdown_detail(db: Session, payload: MFMShutdownDetailCreate):
    query = text("""
        INSERT INTO mfm_shutdown_detail_dkn (
            master_id,
            from_time, to_time, reason,
            kwh, kvah, pf,
            psd_time_from, psd_time_to, psd_cul_daily, psd_cul_monthly,
            dg_from, dg_to,
            engery_meter_reading, hours_meter,
            tank1, tank2, tank3,
            fw1, fw2, fw3, fw4, fw5,           
            remarks   ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :from_time, :to_time, :reason,
            :kwh, :kvah, :pf,
            :psd_time_from, :psd_time_to, :psd_cul_daily, :psd_cul_monthly,
            :dg_from, :dg_to,
            :engery_meter_reading, :hours_meter,
            :tank1, :tank2, :tank3,
            :fw1, :fw2, :fw3, :fw4, :fw5,
            :remarks,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING mfm_shutdown_id
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.fetchone()[0]


def update_mfm_shutdown_detail(
    db: Session,
    mfm_shutdown_id: int,
    payload: MFMShutdownDetailUpdate
):
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    data["mfm_shutdown_id"] = mfm_shutdown_id

    query = text(f"""
        UPDATE mfm_shutdown_detail_dkn
        SET {set_clause}
        WHERE mfm_shutdown_id = :mfm_shutdown_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_mfm_shutdown_detail(db: Session, mfm_shutdown_id: int):
    query = text("""
        DELETE FROM mfm_shutdown_detail_dkn
        WHERE mfm_shutdown_id = :mfm_shutdown_id
    """)
    result = db.execute(query, {"mfm_shutdown_id": mfm_shutdown_id})
    db.commit()
    return result.rowcount > 0
