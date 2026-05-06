from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.digital_logbook.digital_logbook_mlr.mlr_digital_logbook_entry_schemas import MlrDigitalLogBookEntryCreate, MlrDigitalLogBookEntryUpdate

def create_mlr_entry(db: Session, payload: MlrDigitalLogBookEntryCreate):
    query = text("""
        INSERT INTO mlr_digital_logbook_entry (
            mlr_logbook_id,
            entry_time,
            location,created_at,created_by ,updated_at ,updated_by,logs
        )
        VALUES (
            :mlr_logbook_id,
            :entry_time,
            :location,:created_at,:created_by ,:updated_at ,:updated_by,:logs

        )
        RETURNING mlr_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()
    return result.fetchone()[0]


def update_mlr_entry(db: Session, entry_id: int, payload: MlrDigitalLogBookEntryUpdate):
    query = text("""
        UPDATE mlr_digital_logbook_entry
        SET
            entry_time = COALESCE(:entry_time, entry_time),
            location   = COALESCE(:location, location),created_at= COALESCE(:created_at, created_at),created_by= COALESCE(:created_by, created_by),updated_at= COALESCE(:updated_at, updated_at),updated_by= COALESCE(:updated_by, updated_by),logs= COALESCE(:logs, logs)

        WHERE mlr_entry_id = :mlr_entry_id
    """)

    params = payload.dict()
    params["mlr_entry_id"] = entry_id

    db.execute(query, params)
    db.commit()
    return True


def delete_mlr_entry(db: Session, entry_id: int):
    query = text("""
        DELETE FROM mlr_digital_logbook_entry
        WHERE mlr_entry_id = :mlr_entry_id
    """)

    db.execute(query, {"mlr_entry_id": entry_id})
    db.commit()
    return True
