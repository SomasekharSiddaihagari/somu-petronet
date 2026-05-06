# app/crud/ner_digital_logbook_entry_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_logbook_ner.ner_digital_logbook_entry_schema import (
    NerDigitalLogBookEntryCreate,
    NerDigitalLogBookEntryUpdate
)


def create_ner_digital_logbook_entry(
    db: Session,
    payload: NerDigitalLogBookEntryCreate
):
    query = text("""
        INSERT INTO ner_digital_logbook_entry (
            ner_logbook_id,
            entry_time,
            location,created_at,created_by ,updated_at ,updated_by,logs

        )
        VALUES (
            :ner_logbook_id,
            :entry_time,
            :location,:created_at,:created_by ,:updated_at ,:updated_by,:logs

        )
        RETURNING ner_entry_id
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.fetchone()[0]


def update_ner_digital_logbook_entry(
    db: Session,
    ner_entry_id: int,
    payload: NerDigitalLogBookEntryUpdate
):
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return False

    set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
    data["ner_entry_id"] = ner_entry_id

    query = text(f"""
        UPDATE ner_digital_logbook_entry
        SET {set_clause}
        WHERE ner_entry_id = :ner_entry_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_ner_digital_logbook_entry(db: Session, ner_entry_id: int):
    query = text("""
        DELETE FROM ner_digital_logbook_entry
        WHERE ner_entry_id = :ner_entry_id
    """)
    result = db.execute(query, {"ner_entry_id": ner_entry_id})
    db.commit()
    return result.rowcount > 0
