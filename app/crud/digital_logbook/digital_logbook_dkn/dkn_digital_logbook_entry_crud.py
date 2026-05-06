from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.digital_logbook.digital_logbook_dkn.dkn_digital_logbook_entry_schemas import DknDigitalLogBookEntryCreate, DknDigitalLogBookEntryUpdate



def create_entry(db: Session, payload: DknDigitalLogBookEntryCreate):
    query = text("""
        INSERT INTO dkn_digital_logbook_entry (
            logbook_id, entry_time, location,created_at,created_by ,updated_at ,updated_by,logs

        )
        VALUES (
            :logbook_id, :entry_time, :location,:created_at,:created_by ,:updated_at ,:updated_by,:logs

        )
        RETURNING dkn_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()
    return result.fetchone()[0]


def update_entry(db: Session, entry_id: int, payload: DknDigitalLogBookEntryUpdate):
    query = text("""
        UPDATE dkn_digital_logbook_entry
        SET
            entry_time = COALESCE(:entry_time, entry_time),
            location   = COALESCE(:location, location),
            created_at       = COALESCE(:created_at, created_at),
            created_by       = COALESCE(:created_by, created_by),
            updated_at       = COALESCE(:updated_at, updated_at),
            updated_by       = COALESCE(:updated_by, updated_by),
            logs             = COALESCE(:logs, logs) 

        WHERE dkn_entry_id = :entry_id
    """)

    params = payload.dict()
    params["entry_id"] = entry_id

    db.execute(query, params)
    db.commit()
    return True


def delete_entry(db: Session, entry_id: int):
    query = text("""
        DELETE FROM dkn_digital_logbook_entry
        WHERE dkn_entry_id = :entry_id
    """)

    db.execute(query, {"entry_id": entry_id})
    db.commit()
    return True
