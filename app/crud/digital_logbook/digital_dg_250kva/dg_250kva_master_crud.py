# app/crud/dg_250kva_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_dg_250kva.dg_250kva_master_schema import (
    DG250KVACreate,
    DG250KVAUpdate
)


def create_dg_250kva(db: Session, payload: DG250KVACreate):
    query = text("""
        INSERT INTO dg_250kva_master (
            station,
            station_in_charge,
            shift,
            start_time,
            entry_date,
            status,
            document_number,
            ms_logbook_id,
            technician_id,
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
            :entry_date,
            :status,
            :document_number,
            :ms_logbook_id,
            :technician_id,
            :created_at,
            :created_by,
            :updated_at,
            :updated_by
        )
        RETURNING dg_id
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.fetchone()[0]


def update_dg_250kva(
    db: Session,
    dg_id: int,
    payload: DG250KVAUpdate
):
    data = payload.model_dump(exclude_unset=True)

    if not data:
        return False

    set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
    data["dg_id"] = dg_id

    query = text(f"""
        UPDATE dg_250kva_master
        SET {set_clause}
        WHERE dg_id = :dg_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_dg_250kva(db: Session, dg_id: int):
    query = text("""
        DELETE FROM dg_250kva_master
        WHERE dg_id = :dg_id
    """)
    result = db.execute(query, {"dg_id": dg_id})
    db.commit()
    return result.rowcount > 0
