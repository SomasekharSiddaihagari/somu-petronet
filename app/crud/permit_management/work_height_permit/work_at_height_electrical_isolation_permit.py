# ==========================================================
# CRUD FILE
# app/crud/permit_management/work_height_permit/
# work_at_height_electrical_isolation_permit.py
# ==========================================================

from sqlalchemy.orm import Session
from sqlalchemy.sql import text


# ==========================================================
# GET ALL
# ==========================================================
def get_all_work_at_height_electrical_isolation_permits(
    db: Session
):
    query = text("""
        SELECT
            whpis.whpis_id,
            whpis.whp_id,
            whpis.work_permit_number,

            'Electrical Isolation' AS type_of_permit,

            whpis.work_clearance_time,
            whpis.work_clearance_date,
            whpis.cross_reference_of_other_permit,
            whpis.department_section_area,
            whpis.equipment_number_to_be_isolated,
            whpis.name_of_equipment_circuit,
            whpis.description_of_work,

            whpis.equipment_circuit_no,
            whpis.plant,
            whpis.work_clearance_from_time,
            whpis.work_clearance_from_date,
            whpis.loto_tag_device_no,
            whpis.authorized_person_name,
            whpis.designation,
            whpis.signature,
            whpis.isolation_method,

            whpis.issuer_name,
            whpis.issuer_designation,
            whpis.issuer_signature,
            whp.status AS status,

            whpis.created_by,
            whpis.created_at,
            whpis.updated_at,

            whp.receiver_name,
            s.station_name

        FROM work_at_height_electrical_isolation_permit whpis

        LEFT JOIN work_at_height_permit whp
            ON whp.whp_id = whpis.whp_id

        LEFT JOIN users u
            ON CAST(whp.created_by AS INTEGER) = u.user_id

        LEFT JOIN station s
            ON u.station_id = s.station_id

        ORDER BY whpis.whpis_id DESC
    """)

    return db.execute(query).mappings().all()


# ==========================================================
# GET BY ID
# ==========================================================
def get_work_at_height_electrical_isolation_permit_by_id(
    db: Session,
    whpis_id: int
):
    query = text("""
        SELECT
            whpis.whpis_id,
            whpis.whp_id,
            whpis.work_permit_number,

            'Electrical Isolation' AS type_of_permit,

            whpis.work_clearance_time,
            whpis.work_clearance_date,
            whpis.cross_reference_of_other_permit,
            whpis.department_section_area,
            whpis.equipment_number_to_be_isolated,
            whpis.name_of_equipment_circuit,
            whpis.description_of_work,

            whpis.equipment_circuit_no,
            whpis.plant,
            whpis.work_clearance_from_time,
            whpis.work_clearance_from_date,
            whpis.loto_tag_device_no,
            whpis.authorized_person_name,
            whpis.designation,
            whpis.signature,
            whpis.isolation_method,

            whpis.issuer_name,
            whpis.issuer_designation,
            whpis.issuer_signature,
            whp.status AS status,

            whpis.created_by,
            whpis.created_at,
            whpis.updated_at,

            whp.receiver_name,
            s.station_name

        FROM work_at_height_electrical_isolation_permit whpis

        LEFT JOIN work_at_height_permit whp
            ON whp.whp_id = whpis.whp_id

        LEFT JOIN users u
            ON CAST(whp.created_by AS INTEGER) = u.user_id

        LEFT JOIN station s
            ON u.station_id = s.station_id

        WHERE whpis.whpis_id = :whpis_id
    """)

    return db.execute(
        query,
        {"whpis_id": whpis_id}
    ).mappings().first()