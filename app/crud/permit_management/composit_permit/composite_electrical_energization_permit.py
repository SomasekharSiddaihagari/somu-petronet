from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_all_composite_electrical_energization_permits(db: Session):
    query = text("""
        SELECT
            ceep.ceep_id,
            ceep.composite_work_permit_id,
            ceep.work_permit_number,
            'Energization' AS type_of_permit,
            ceep.work_clearance_time,
            ceep.work_clearance_date,
            ceep.name_of_equipment_circuit,
            ceep.department_section_area,
            ceep.equipment_number_to_be_energized,
            ceep.cross_reference_of_other_permit,
            ceep.issuer_name,
            ceep.issuer_designation,
            ceep.issuer_signature,
            cwp.status AS status,
            ceep.created_by,
            ceep.created_at,
            ceep.updated_at,

            -- ELECTRICAL certificate fields
            ceep.equipment_circuit_no,
            ceep.plant,
            ceep.work_clearance_from_time,
            ceep.work_clearance_from_date,
            ceep.energization_method,
            ceep.loto_tag_device_no,
            ceep.authorized_person_name,
            ceep.designation,
            ceep.signature,

            cwp.receiver_name,
            s.station_name
        FROM composite_electrical_energization_permit ceep
        LEFT JOIN composite_work_permit cwp ON cwp.cwp_id = ceep.composite_work_permit_id
        LEFT JOIN users u ON CAST(cwp.created_by AS INTEGER) = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        ORDER BY ceep.ceep_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


def get_composite_electrical_energization_permit_by_id(db: Session, ceep_id: int):
    query = text("""
        SELECT
            ceep.ceep_id,
            ceep.composite_work_permit_id,
            ceep.work_permit_number,
            ceep.work_clearance_time,
            ceep.work_clearance_date,
            ceep.name_of_equipment_circuit,
            ceep.department_section_area,
            ceep.equipment_number_to_be_energized,
            ceep.cross_reference_of_other_permit,
            ceep.issuer_name,
            ceep.issuer_designation,
            ceep.issuer_signature,
            cwp.status AS status,
            ceep.created_by,
            ceep.created_at,
            ceep.updated_at,

            -- ELECTRICAL certificate fields
            ceep.equipment_circuit_no,
            ceep.plant,
            ceep.work_clearance_from_time,
            ceep.work_clearance_from_date,
            ceep.energization_method,
            ceep.loto_tag_device_no,
            ceep.authorized_person_name,
            ceep.designation,
            ceep.signature,

            cwp.receiver_name,
            s.station_name
        FROM composite_electrical_energization_permit ceep
        LEFT JOIN composite_work_permit cwp ON cwp.cwp_id = ceep.composite_work_permit_id
        LEFT JOIN users u ON CAST(cwp.created_by AS INTEGER) = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        WHERE ceep.ceep_id = :ceep_id
    """)

    result = db.execute(query, {"ceep_id": ceep_id}).mappings().first()
    return result
