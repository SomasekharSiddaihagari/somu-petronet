from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_all_work_at_height_toolbox_talks(db: Session):
    query = text("""
        SELECT
            whtt_id,
            work_at_height_permit_id,
            cross_reference_of_other_permit,
            work_clearance_time,
            work_clearance_date,
            contractor_engineer_name,
            work_installation_unit_facility_name,
            tbt_delivered_by,
            contract_supervisor_name,
            topics_issues_discussed,
            other_points_raised,
            created_by,
            created_at,
            updated_at
        FROM work_at_height_toolbox_talk
        ORDER BY whtt_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


def get_work_at_height_toolbox_talk_by_id(
    db: Session,
    whtt_id: int
):
    query = text("""
        SELECT
            whtt_id,
            work_at_height_permit_id,
            cross_reference_of_other_permit,
            work_clearance_time,
            work_clearance_date,
            contractor_engineer_name,
            work_installation_unit_facility_name,
            tbt_delivered_by,
            contract_supervisor_name,
            topics_issues_discussed,
            other_points_raised,
            created_by,
            created_at,
            updated_at
        FROM work_at_height_toolbox_talk
        WHERE whtt_id = :whtt_id
    """)

    result = db.execute(
        query,
        {"whtt_id": whtt_id}
    ).mappings().first()

    return result
