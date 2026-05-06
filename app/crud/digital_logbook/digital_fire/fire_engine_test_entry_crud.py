from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.digital_logbook.digital_fire.fire_engine_test_entry_schemas import (
    FireEngineTestEntryCreate,
    FireEngineTestEntryUpdate
)


def create_fire_engine_test_entry(
    db: Session,
    payload: FireEngineTestEntryCreate
):
    query = text("""
        INSERT INTO fire_engine_test_entry (
            master_id,
            entry_date,
            fire_engine_no,
            time_start,
            time_stop,
            running_hours,
            battery_voltage,
            lube_oil_level,
            fuel_level_lts,
            radiator_water_level,
            lube_oil_temp,
            lube_oil_pressure,
            fwt_1,
            fwt_2,
            fwt_3,
            cooling_water_temp,
            rpm,
            mode_of_test,
            tech_sign,
            engg_sign,
            remarks   ,created_at,created_by ,updated_at ,updated_by

        ) VALUES (
            :master_id,
            :entry_date,
            :fire_engine_no,
            :time_start,
            :time_stop,
            :running_hours,
            :battery_voltage,
            :lube_oil_level,
            :fuel_level_lts,
            :radiator_water_level,
            :lube_oil_temp,
            :lube_oil_pressure,
            :fwt_1,
            :fwt_2,
            :fwt_3,
            :cooling_water_temp,
            :rpm,
            :mode_of_test,
            :tech_sign,
            :engg_sign,
            :remarks,
           :created_at
            ,:created_by ,:updated_at ,:updated_by
        )
        RETURNING *;
    """)

    result = db.execute(query, payload.dict())
    db.commit()
    return result.mappings().first()


def get_fire_engine_test_entry_by_id(
    db: Session,
    fire_entry_id: int
):
    query = text("""
        SELECT *
        FROM fire_engine_test_entry
        WHERE fire_entry_id = :fire_entry_id
    """)

    result = db.execute(
        query,
        {"fire_entry_id": fire_entry_id}
    )
    return result.mappings().first()


def get_entries_by_master_id(
    db: Session,
    master_id: int
):
    query = text("""
        SELECT *
        FROM fire_engine_test_entry
        WHERE master_id = :master_id
        ORDER BY entry_date ASC
    """)

    result = db.execute(
        query,
        {"master_id": master_id}
    )
    return result.mappings().all()


def update_fire_engine_test_entry(
    db: Session,
    fire_entry_id: int,
    payload: FireEngineTestEntryUpdate
):
    query = text("""
        UPDATE fire_engine_test_entry
        SET
            entry_date = :entry_date,
            fire_engine_no = :fire_engine_no,
            time_start = :time_start,
            time_stop = :time_stop,
            running_hours = :running_hours,
            battery_voltage = :battery_voltage,
            lube_oil_level = :lube_oil_level,
            fuel_level_lts = :fuel_level_lts,
            radiator_water_level = :radiator_water_level,
            lube_oil_temp = :lube_oil_temp,
            lube_oil_pressure = :lube_oil_pressure,
            fwt_1 = :fwt_1,
            fwt_2 = :fwt_2,
            fwt_3 = :fwt_3,
            cooling_water_temp = :cooling_water_temp,
            rpm = :rpm,
            mode_of_test = :mode_of_test,
            tech_sign = :tech_sign,
            engg_sign = :engg_sign,
            remarks = :remarks
                             ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE fire_entry_id = :fire_entry_id
        RETURNING *;
    """)

    data = payload.dict()
    data["fire_entry_id"] = fire_entry_id

    result = db.execute(query, data)
    db.commit()
    return result.mappings().first()


def delete_fire_engine_test_entry(
    db: Session,
    fire_entry_id: int
):
    query = text("""
        DELETE FROM fire_engine_test_entry
        WHERE fire_entry_id = :fire_entry_id
        RETURNING fire_entry_id;
    """)

    result = db.execute(
        query,
        {"fire_entry_id": fire_entry_id}
    )
    db.commit()
    return result.fetchone()
