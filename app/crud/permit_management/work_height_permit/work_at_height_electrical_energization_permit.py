# ==========================================================
# CRUD FILE
# app/crud/permit_management/work_height_permit/
# work_at_height_electrical_energization_permit.py
# ==========================================================

from sqlalchemy.orm import Session
from sqlalchemy.sql import text


# ==========================================================
# GET ALL
# ==========================================================
def get_all_work_at_height_electrical_energization_permits(
    db: Session
):
    query = text("""
        SELECT
            whpep.whpep_id,
            whpep.whp_id,
            whpep.work_permit_number,

            'Energization' AS type_of_permit,

            whpep.work_clearance_time,
            whpep.work_clearance_date,

            whpep.name_of_equipment_circuit,
            whpep.department_section_area,
            whpep.equipment_number_to_be_energized,
            whpep.cross_reference_of_other_permit,

            whpep.equipment_circuit_no,
            whpep.plant,
            whpep.work_clearance_from_time,
            whpep.work_clearance_from_date,
            whpep.loto_tag_device_no,
            whpep.authorized_person_name,
            whpep.designation,
            whpep.signature,
            whpep.energization_method,

            whpep.issuer_name,
            whpep.issuer_designation,
            whpep.issuer_signature,
            whp.status AS status,

            whpep.created_by,
            whpep.created_at,
            whpep.updated_at,

            whp.receiver_name,
            s.station_name

        FROM work_at_height_electrical_energization_permit whpep

        LEFT JOIN work_at_height_permit whp
            ON whp.whp_id = whpep.whp_id

        LEFT JOIN users u
            ON CAST(whp.created_by AS INTEGER) = u.user_id

        LEFT JOIN station s
            ON u.station_id = s.station_id

        ORDER BY whpep.whpep_id DESC
    """)

    return db.execute(query).mappings().all()


# ==========================================================
# GET BY ID
# ==========================================================
def get_work_at_height_electrical_energization_permit_by_id(
    db: Session,
    whpep_id: int
):
    query = text("""
        SELECT
            whpep.whpep_id,
            whpep.whp_id,
            whpep.work_permit_number,

            'Energization' AS type_of_permit,

            whpep.work_clearance_time,
            whpep.work_clearance_date,

            whpep.name_of_equipment_circuit,
            whpep.department_section_area,
            whpep.equipment_number_to_be_energized,
            whpep.cross_reference_of_other_permit,

            whpep.equipment_circuit_no,
            whpep.plant,
            whpep.work_clearance_from_time,
            whpep.work_clearance_from_date,
            whpep.loto_tag_device_no,
            whpep.authorized_person_name,
            whpep.designation,
            whpep.signature,
            whpep.energization_method,

            whpep.issuer_name,
            whpep.issuer_designation,
            whpep.issuer_signature,
            whp.status AS status,

            whpep.created_by,
            whpep.created_at,
            whpep.updated_at,

            whp.receiver_name,
            s.station_name

        FROM work_at_height_electrical_energization_permit whpep

        LEFT JOIN work_at_height_permit whp
            ON whp.whp_id = whpep.whp_id

        LEFT JOIN users u
            ON CAST(whp.created_by AS INTEGER) = u.user_id

        LEFT JOIN station s
            ON u.station_id = s.station_id

        WHERE whpep.whpep_id = :whpep_id
    """)

    return db.execute(
        query,
        {"whpep_id": whpep_id}
    ).mappings().first()