from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.wah_toolbox_talk_schema import (
    WorkAtHeightToolboxTalkCreate,
    WorkAtHeightToolboxTalkUpdate
)

# =================================================
# INSERT HISTORY SNAPSHOT
# =================================================
def insert_wah_toolbox_talk_history(db: Session, whtt_id: int):
    history_sql = text("""
        INSERT INTO work_at_height_toolbox_talk_history (
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
        )
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
            NOW()
        FROM work_at_height_toolbox_talk
        WHERE whtt_id = :whtt_id
    """)

    db.execute(history_sql, {"whtt_id": whtt_id})


# -------------------------------------------------
# CREATE TOOLBOX TALK (MAIN + HISTORY)
# -------------------------------------------------
def create_wah_toolbox_talk(
    db: Session,
    data: WorkAtHeightToolboxTalkCreate
):
    payload = data.model_dump()

    insert_sql = text("""
        INSERT INTO work_at_height_toolbox_talk (
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
            created_by
        )
        VALUES (
            :work_at_height_permit_id,
            :cross_reference_of_other_permit,
            :work_clearance_time,
            :work_clearance_date,
            :contractor_engineer_name,
            :work_installation_unit_facility_name,
            :tbt_delivered_by,
            :contract_supervisor_name,
            :topics_issues_discussed,
            :other_points_raised,
            :created_by
        )
        RETURNING whtt_id
    """)

    result = db.execute(insert_sql, payload)
    whtt_id = result.scalar()

    # ✅ AUTO INSERT HISTORY
    insert_wah_toolbox_talk_history(db, whtt_id)

    db.commit()

    return {"whtt_id": whtt_id}


# -------------------------------------------------
# UPDATE TOOLBOX TALK (MAIN + HISTORY)
# -------------------------------------------------
def update_wah_toolbox_talk(
    db: Session,
    whtt_id: int,
    data: WorkAtHeightToolboxTalkUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    update_sql = text(f"""
        UPDATE work_at_height_toolbox_talk
        SET {set_clause},
            updated_at = NOW()
        WHERE whtt_id = :whtt_id
    """)

    payload["whtt_id"] = whtt_id
    db.execute(update_sql, payload)

    # ✅ AUTO INSERT HISTORY ON UPDATE
    insert_wah_toolbox_talk_history(db, whtt_id)

    db.commit()

    return True
