from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_all_composite_toolbox_talks(db: Session):
    query = text("""
        SELECT
            ctt_id,
            composite_work_permit_id,
            cross_reference_of_other_permit,
            work_clearance_time,
            work_clearance_date,
            contractor_engineer_name,
            work_installation_unit_facility_name,
            tbt_delivered_by,
            contract_supervisor_name,
            topics_issues_discussed,
            other_points_raised,
            status,
            created_by,
            created_at,
            updated_at
        FROM composite_toolbox_talk
        ORDER BY ctt_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


def get_composite_toolbox_talk_by_id(
    db: Session,
    ctt_id: int
):
    query = text("""
        SELECT
            ctt_id,
            composite_work_permit_id,
            cross_reference_of_other_permit,
            work_clearance_time,
            work_clearance_date,
            contractor_engineer_name,
            work_installation_unit_facility_name,
            tbt_delivered_by,
            contract_supervisor_name,
            topics_issues_discussed,
            other_points_raised,
            status,
            created_by,
            created_at,
            updated_at
        FROM composite_toolbox_talk
        WHERE ctt_id = :ctt_id
    """)

    result = db.execute(
        query,
        {"ctt_id": ctt_id}
    ).mappings().first()

    return result
