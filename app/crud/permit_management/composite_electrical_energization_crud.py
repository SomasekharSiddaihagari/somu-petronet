from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.composite_electrical_energization_schema import (
    CompositeElectricalEnergizationPermitCreate,
    CompositeElectricalEnergizationPermitUpdate,
)


# =================================================
# AUTO SERIAL NUMBER GENERATOR
# =================================================
def generate_composite_eep_serial_number(db: Session, user_id: int) -> str:

    station_query = text(
        """
        SELECT s.station_code
        FROM users u
        JOIN station s ON s.station_id = u.station_id
        WHERE u.user_id = :user_id
          AND u.is_deleted = FALSE
    """
    )
    station = db.execute(station_query, {"user_id": user_id}).mappings().first()

    if not station:
        raise HTTPException(status_code=400, detail="Station not found for this user")

    station_code = station["station_code"]

    today = date.today()
    if today.month >= 4:
        fy = f"{today.year}-{str(today.year + 1)[-2:]}"
    else:
        fy = f"{today.year - 1}-{str(today.year)[-2:]}"

    count_query = text(
        """
        SELECT COUNT(*) as cnt
        FROM composite_electrical_energization_permit
        WHERE work_permit_number LIKE :pattern
    """
    )
    result = (
        db.execute(count_query, {"pattern": f"EEP/{station_code}/{fy}/%"})
        .mappings()
        .first()
    )

    next_seq = (result["cnt"] or 0) + 1
    sequence = str(next_seq).zfill(3)

    return f"EEP/{station_code}/{fy}/{sequence}"


# =================================================
# INSERT HISTORY SNAPSHOT
# =================================================
def insert_composite_electrical_energization_history(db: Session, ceep_id: int):
    history_sql = text(
        """
        INSERT INTO composite_electrical_energization_permit_history (
            ceep_id,
            composite_work_permit_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,
            issuer_name,
            issuer_designation,
            issuer_signature,
            status,
            created_by,
            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            energization_method,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            created_at,
            updated_at
        )
        SELECT
            ceep_id,
            composite_work_permit_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,
            issuer_name,
            issuer_designation,
            issuer_signature,
            status,
            created_by,
            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            energization_method,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            created_at,
            NOW()
        FROM composite_electrical_energization_permit
        WHERE ceep_id = :ceep_id
    """
    )
    db.execute(history_sql, {"ceep_id": ceep_id})


# =================================================
# CREATE (MAIN + HISTORY)
# =================================================
def create_electrical_energization(
    db: Session, data: CompositeElectricalEnergizationPermitCreate
):
    payload = data.model_dump()

    # ✅ Auto generate work_permit_number
    payload["work_permit_number"] = generate_composite_eep_serial_number(
        db, payload["created_by"]
    )

    insert_sql = text(
        """
        INSERT INTO composite_electrical_energization_permit (
            composite_work_permit_id,
            work_permit_number,
            work_clearance_time,
            work_clearance_date,
            name_of_equipment_circuit,
            department_section_area,
            equipment_number_to_be_energized,
            cross_reference_of_other_permit,
            issuer_name,
            issuer_designation,
            issuer_signature,
            status,
            created_by,
            equipment_circuit_no,
            plant,
            work_clearance_from_time,
            work_clearance_from_date,
            energization_method,
            loto_tag_device_no,
            authorized_person_name,
            designation,
            signature,
            created_at,
            updated_at
        )
        VALUES (
            :composite_work_permit_id,
            :work_permit_number,
            :work_clearance_time,
            :work_clearance_date,
            :name_of_equipment_circuit,
            :department_section_area,
            :equipment_number_to_be_energized,
            :cross_reference_of_other_permit,
            :issuer_name,
            :issuer_designation,
            :issuer_signature,
            :status,
            :created_by,
            :equipment_circuit_no,
            :plant,
            :work_clearance_from_time,
            :work_clearance_from_date,
            :energization_method,
            :loto_tag_device_no,
            :authorized_person_name,
            :designation,
            :signature,
            NOW(),
            NOW()
        )
        RETURNING ceep_id
    """
    )

    result = db.execute(insert_sql, payload)
    ceep_id = result.scalar()

    insert_composite_electrical_energization_history(db, ceep_id)

    db.commit()

    return {"ceep_id": ceep_id, "work_permit_number": payload["work_permit_number"]}


# =================================================
# UPDATE (MAIN + HISTORY)
# =================================================
def update_electrical_energization(
    db: Session, ceep_id: int, data: CompositeElectricalEnergizationPermitUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    update_sql = text(
        f"""
        UPDATE composite_electrical_energization_permit
        SET {set_clause},
            updated_at = NOW()
        WHERE ceep_id = :ceep_id
    """
    )

    payload["ceep_id"] = ceep_id
    db.execute(update_sql, payload)

    insert_composite_electrical_energization_history(db, ceep_id)

    db.commit()

    return True
