# ==========================================================
# CRUD FILE
# app/crud/permit_management/wah_electrical_energization_crud.py
# ==========================================================

from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.wah_electrical_energization_schema import (
    WorkAtHeightElectricalEnergizationCreate,
    WorkAtHeightElectricalEnergizationUpdate
)


# =================================================
# SERIAL NUMBER
# =================================================
def generate_wah_eep_serial_number(
    db: Session,
    user_id: int
):
    station_query = text("""
        SELECT s.station_code
        FROM users u
        JOIN station s ON s.station_id = u.station_id
        WHERE u.user_id = :user_id
          AND u.is_deleted = FALSE
    """)

    station = db.execute(
        station_query,
        {"user_id": user_id}
    ).mappings().first()

    if not station:
        raise HTTPException(
            status_code=400,
            detail="Station not found"
        )

    station_code = station["station_code"]

    today = date.today()

    if today.month >= 4:
        fy = f"{today.year}-{str(today.year + 1)[-2:]}"
    else:
        fy = f"{today.year - 1}-{str(today.year)[-2:]}"

    count_query = text("""
        SELECT COUNT(*) cnt
        FROM work_at_height_electrical_energization_permit
        WHERE work_permit_number LIKE :pattern
    """)

    result = db.execute(
        count_query,
        {"pattern": f"EEP/{station_code}/{fy}/%"}
    ).mappings().first()

    next_seq = (result["cnt"] or 0) + 1

    return f"EEP/{station_code}/{fy}/{str(next_seq).zfill(3)}"


# =================================================
# HISTORY INSERT
# =================================================
def insert_wah_electrical_energization_history(
    db: Session,
    whpep_id: int
):
    sql = text("""
        INSERT INTO work_at_height_electrical_energization_permit_history (
            whpep_id,
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            energization_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by,
            created_at,
            updated_at
        )
        SELECT
            whpep_id,
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            energization_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by,
            created_at,
            NOW()
        FROM work_at_height_electrical_energization_permit
        WHERE whpep_id = :whpep_id
    """)

    db.execute(sql, {"whpep_id": whpep_id})


# =================================================
# CREATE
# =================================================
def create_wah_electrical_energization(
    db: Session,
    data: WorkAtHeightElectricalEnergizationCreate
):
    payload = data.model_dump()

    payload["work_permit_number"] = generate_wah_eep_serial_number(
        db,
        payload["created_by"]
    )

    sql = text("""
        INSERT INTO work_at_height_electrical_energization_permit (
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            energization_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by
        )
        VALUES (
            :whp_id,
            :work_permit_number,
            :work_clearance_time,
            :work_clearance_date,
            :name_of_equipment_circuit,
            :department_section_area,
            :equipment_number_to_be_energized,
            :cross_reference_of_other_permit,

            :equipment_circuit_no,
            :plant,
            :work_clearance_from_time,
            :work_clearance_from_date,
            :loto_tag_device_no,
            :authorized_person_name,
            :designation,
            :signature,
            :energization_method,

            :issuer_name,
            :issuer_designation,
            :issuer_signature,
            :created_by
        )
        RETURNING whpep_id
    """)

    result = db.execute(sql, payload)
    whpep_id = result.scalar()

    insert_wah_electrical_energization_history(db, whpep_id)

    db.commit()

    return {
        "whpep_id": whpep_id,
        "work_permit_number": payload["work_permit_number"]
    }


# =================================================
# UPDATE
# =================================================
def update_wah_electrical_energization(
    db: Session,
    whpep_id: int,
    data: WorkAtHeightElectricalEnergizationUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join(
        [f"{k}=:{k}" for k in payload.keys()]
    )

    sql = text(f"""
        UPDATE work_at_height_electrical_energization_permit
        SET {set_clause},
            updated_at = NOW()
        WHERE whpep_id = :whpep_id
    """)

    payload["whpep_id"] = whpep_id

    db.execute(sql, payload)

    insert_wah_electrical_energization_history(db, whpep_id)

    db.commit()

    return True