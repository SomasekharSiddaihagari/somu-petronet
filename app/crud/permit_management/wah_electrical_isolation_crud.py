# ================================
# CRUD FILE
# wah_electrical_isolation_crud.py
# ================================

from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.wah_electrical_isolation_schema import (
    WorkAtHeightElectricalIsolationCreate,
    WorkAtHeightElectricalIsolationUpdate
)


# ==========================================
# SERIAL NUMBER
# ==========================================
def generate_eip_serial_number(db: Session, user_id: int, table_name: str) -> str:
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
        raise HTTPException(status_code=400, detail="Station not found")

    station_code = station["station_code"]

    today = date.today()

    if today.month >= 4:
        fy = f"{today.year}-{str(today.year + 1)[-2:]}"
    else:
        fy = f"{today.year - 1}-{str(today.year)[-2:]}"

    count_query = text(f"""
        SELECT COUNT(*) cnt
        FROM {table_name}
        WHERE work_permit_number LIKE :pattern
    """)

    result = db.execute(
        count_query,
        {"pattern": f"EIP/{station_code}/{fy}/%"}
    ).mappings().first()

    next_seq = (result["cnt"] or 0) + 1

    return f"EIP/{station_code}/{fy}/{str(next_seq).zfill(3)}"


# ==========================================
# HISTORY
# ==========================================
def insert_wah_electrical_isolation_history(
    db: Session,
    whpis_id: int
):
    sql = text("""
        INSERT INTO work_at_height_electrical_isolation_permit_history (
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            cross_reference_of_other_permit,
            department_section_area,
            equipment_number_to_be_isolated,
            name_of_equipment_circuit,
            description_of_work,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            isolation_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by,
            created_at,
            updated_at
        )
        SELECT
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            cross_reference_of_other_permit,
            department_section_area,
            equipment_number_to_be_isolated,
            name_of_equipment_circuit,
            description_of_work,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            isolation_method,

            issuer_name,
            issuer_designation,
            issuer_signature,
            created_by,
            created_at,
            NOW()
        FROM work_at_height_electrical_isolation_permit
        WHERE whpis_id = :whpis_id
    """)

    db.execute(sql, {"whpis_id": whpis_id})


# ==========================================
# CREATE
# ==========================================
def create_wah_electrical_isolation(
    db: Session,
    data: WorkAtHeightElectricalIsolationCreate
):
    payload = data.model_dump()

    payload["work_permit_number"] = generate_eip_serial_number(
        db,
        payload["created_by"],
        "work_at_height_electrical_isolation_permit"
    )

    sql = text("""
        INSERT INTO work_at_height_electrical_isolation_permit (
            whp_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            cross_reference_of_other_permit,
            department_section_area,
            equipment_number_to_be_isolated,
            name_of_equipment_circuit,
            description_of_work,

            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            isolation_method,

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
            :cross_reference_of_other_permit,
            :department_section_area,
            :equipment_number_to_be_isolated,
            :name_of_equipment_circuit,
            :description_of_work,

            :equipment_circuit_no,
            :plant,
            :work_clearance_from_time,
            :work_clearance_from_date,
            :loto_tag_device_no,
            :authorized_person_name,
            :designation,
            :signature,
            :isolation_method,

            :issuer_name,
            :issuer_designation,
            :issuer_signature,
            :created_by
        )
        RETURNING whpis_id
    """)

    result = db.execute(sql, payload)
    whpis_id = result.scalar()

    insert_wah_electrical_isolation_history(db, whpis_id)

    db.commit()

    return {
        "whpis_id": whpis_id,
        "work_permit_number": payload["work_permit_number"]
    }


# ==========================================
# UPDATE
# ==========================================
def update_wah_electrical_isolation(
    db: Session,
    whpis_id: int,
    data: WorkAtHeightElectricalIsolationUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join(
        [f"{k}=:{k}" for k in payload.keys()]
    )

    sql = text(f"""
        UPDATE work_at_height_electrical_isolation_permit
        SET {set_clause},
            updated_at = NOW()
        WHERE whpis_id = :whpis_id
    """)

    payload["whpis_id"] = whpis_id

    db.execute(sql, payload)

    insert_wah_electrical_isolation_history(db, whpis_id)

    db.commit()

    return True