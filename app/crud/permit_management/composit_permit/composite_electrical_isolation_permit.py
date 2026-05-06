from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_all_composite_electrical_isolation_permits(db: Session):
    query = text("""
        SELECT
            ceip.ceip_id,
            ceip.composite_work_permit_id,
            ceip.work_permit_number,
            'Electrical Isolation' AS type_of_permit,
            ceip.work_clearance_time,
            ceip.work_clearance_date,
            ceip.cross_reference_of_other_permit,
            ceip.department_section_area,
            ceip.equipment_number_to_be_isolated,
            ceip.name_of_equipment_circuit,
            ceip.description_of_work,
            ceip.issuer_name,
            ceip.issuer_designation,
            ceip.issuer_signature,
            cwp.status AS status,
            ceip.created_by,
            ceip.created_at,
            ceip.updated_at,

            -- ELECTRICAL certificate fields
            ceip.equipment_circuit_no,
            ceip.plant,
            ceip.work_clearance_from_time,
            ceip.work_clearance_from_date,
            ceip.isolation_method,
            ceip.loto_tag_device_no,
            ceip.authorized_person_name,
            ceip.designation,
            ceip.signature,

            cwp.receiver_name,
            s.station_name
        FROM composite_electrical_isolation_permit ceip
        LEFT JOIN composite_work_permit cwp ON cwp.cwp_id = ceip.composite_work_permit_id
        LEFT JOIN users u ON CAST(cwp.created_by AS INTEGER) = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        ORDER BY ceip.ceip_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


def get_composite_electrical_isolation_permit_by_id(db: Session, ceip_id: int):
    query = text("""
        SELECT
            ceip.ceip_id,
            ceip.composite_work_permit_id,
            ceip.work_permit_number,
            ceip.work_clearance_time,
            ceip.work_clearance_date,
            ceip.cross_reference_of_other_permit,
            ceip.department_section_area,
            ceip.equipment_number_to_be_isolated,
            ceip.name_of_equipment_circuit,
            ceip.description_of_work,
            ceip.issuer_name,
            ceip.issuer_designation,
            ceip.issuer_signature,
            cwp.status AS status,
            ceip.created_by,
            ceip.created_at,
            ceip.updated_at,

            -- ELECTRICAL certificate fields
            ceip.equipment_circuit_no,
            ceip.plant,
            ceip.work_clearance_from_time,
            ceip.work_clearance_from_date,
            ceip.isolation_method,
            ceip.loto_tag_device_no,
            ceip.authorized_person_name,
            ceip.designation,
            ceip.signature,

            cwp.receiver_name,
            s.station_name
        FROM composite_electrical_isolation_permit ceip
        LEFT JOIN composite_work_permit cwp ON cwp.cwp_id = ceip.composite_work_permit_id
        LEFT JOIN users u ON CAST(cwp.created_by AS INTEGER) = u.user_id
        LEFT JOIN station s ON u.station_id = s.station_id
        WHERE ceip.ceip_id = :ceip_id
    """)

    result = db.execute(query, {"ceip_id": ceip_id}).mappings().first()
    return result
