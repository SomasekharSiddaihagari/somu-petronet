from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.digital_logbook.digital_fire.fire_engine_test_master_schemas import (
    FireEngineTestMasterCreate,
    FireEngineTestMasterUpdate
)


def create_fire_engine_test(db: Session, payload: FireEngineTestMasterCreate):
    query = text("""
        INSERT INTO fire_engine_test_master (
            document_number,
            station_name,
            station_incharge,
            shift,
            start_time,
            log_date,
            ms_logbook_id,
            technician_id,
            technician_name,
            technician_signature,
            engineer_name,
            engineer_signature,
            status   ,created_at,created_by ,updated_at ,updated_by

        ) VALUES (
            :document_number,
            :station_name,
            :station_incharge,
            :shift,
            :start_time,
            :log_date,
            :ms_logbook_id,
            :technician_id,
            :technician_name,
            :technician_signature,
            :engineer_name,
            :engineer_signature,
            :status,
                     
            :created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING *;
    """)

    result = db.execute(query, payload.dict())
    db.commit()
    return result.mappings().first()


def get_fire_engine_test_by_id(db: Session, fire_id: int):
    query = text("""
        SELECT *
        FROM fire_engine_test_master
        WHERE fire_id = :fire_id
    """)

    result = db.execute(query, {"fire_id": fire_id})
    return result.mappings().first()


def update_fire_engine_test(
    db: Session,
    fire_id: int,
    payload: FireEngineTestMasterUpdate
):
    query = text("""
        UPDATE fire_engine_test_master
        SET
            document_number = :document_number,
            station_name = :station_name,
            station_incharge = :station_incharge,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,
            ms_logbook_id = :ms_logbook_id,
            technician_id = :technician_id,
            technician_name = :technician_name,
            technician_signature = :technician_signature,
            engineer_name = :engineer_name,
            engineer_signature = :engineer_signature,
            status = :status,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by
        WHERE fire_id = :fire_id
        RETURNING *;
    """)

    data = payload.dict()
    data["fire_id"] = fire_id

    result = db.execute(query, data)
    db.commit()
    return result.mappings().first()


def delete_fire_engine_test(db: Session, fire_id: int):
    query = text("""
        DELETE FROM fire_engine_test_master
        WHERE fire_id = :fire_id
        RETURNING fire_id;
    """)

    result = db.execute(query, {"fire_id": fire_id})
    db.commit()
    return result.fetchone()
