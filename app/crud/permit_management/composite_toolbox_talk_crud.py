from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.composite_toolbox_talk_schema import (
    CompositeToolboxTalkCreate,
    CompositeToolboxTalkUpdate
)

# =================================================
# INSERT HISTORY SNAPSHOT
# =================================================
def insert_composite_toolbox_talk_history(db: Session, ctt_id: int):
    history_sql = text("""
        INSERT INTO composite_toolbox_talk_history (
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
        )
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
            NOW()
        FROM composite_toolbox_talk
        WHERE ctt_id = :ctt_id
    """)

    db.execute(history_sql, {"ctt_id": ctt_id})


# =================================================
# CREATE (MAIN + HISTORY)
# =================================================
def create_composite_toolbox_talk(
    db: Session,
    data: CompositeToolboxTalkCreate
):
    payload = data.model_dump()

    insert_sql = text("""
        INSERT INTO composite_toolbox_talk (
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
            created_by
        )
        VALUES (
            :composite_work_permit_id,
            :cross_reference_of_other_permit,
            :work_clearance_time,
            :work_clearance_date,
            :contractor_engineer_name,
            :work_installation_unit_facility_name,
            :tbt_delivered_by,
            :contract_supervisor_name,
            :topics_issues_discussed,
            :other_points_raised,
            :status,
            :created_by
        )
        RETURNING ctt_id
    """)

    result = db.execute(insert_sql, payload)
    ctt_id = result.scalar()

    # ✅ AUTO INSERT HISTORY
    insert_composite_toolbox_talk_history(db, ctt_id)

    db.commit()

    return {"ctt_id": ctt_id}


# =================================================
# UPDATE (MAIN + HISTORY)
# =================================================
def update_composite_toolbox_talk(
    db: Session,
    ctt_id: int,
    data: CompositeToolboxTalkUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    update_sql = text(f"""
        UPDATE composite_toolbox_talk
        SET {set_clause},
            updated_at = NOW()
        WHERE ctt_id = :ctt_id
    """)

    payload["ctt_id"] = ctt_id
    db.execute(update_sql, payload)

    # ✅ AUTO INSERT HISTORY ON UPDATE
    insert_composite_toolbox_talk_history(db, ctt_id)

    db.commit()

    return True
