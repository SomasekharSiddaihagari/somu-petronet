from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.wah_toolbox_participant_schema import (
    WorkAtHeightToolboxTalkParticipantCreate,
    WorkAtHeightToolboxTalkParticipantUpdate
)

# =================================================
# INSERT HISTORY SNAPSHOT
# =================================================
def insert_wah_toolbox_participant_history(db: Session, whttp_id: int):
    history_sql = text("""
        INSERT INTO work_at_height_toolbox_talk_participant_history (
            whttp_id,
            toolbox_talk_id,
            participant_name,
            participant_signature,
            created_at
        )
        SELECT
            whttp_id,
            toolbox_talk_id,
            participant_name,
            participant_signature,
            created_at
        FROM work_at_height_toolbox_talk_participant
        WHERE whttp_id = :whttp_id
    """)

    db.execute(history_sql, {"whttp_id": whttp_id})


# ================================================
# CREATE PARTICIPANT (MAIN + HISTORY)
# ================================================
def create_wah_toolbox_participant(
    db: Session,
    data: WorkAtHeightToolboxTalkParticipantCreate
):
    payload = data.model_dump()

    sql = text("""
        INSERT INTO work_at_height_toolbox_talk_participant (
            toolbox_talk_id,
            participant_name,
            participant_signature
        )
        VALUES (
            :toolbox_talk_id,
            :participant_name,
            :participant_signature
        )
        RETURNING whttp_id
    """)

    result = db.execute(sql, payload)
    whttp_id = result.scalar()

    # ✅ AUTO INSERT HISTORY
    insert_wah_toolbox_participant_history(db, whttp_id)

    db.commit()

    return {"whttp_id": whttp_id}


# ================================================
# UPDATE PARTICIPANT (MAIN + HISTORY)
# ================================================
def update_wah_toolbox_participant(
    db: Session,
    whttp_id: int,
    data: WorkAtHeightToolboxTalkParticipantUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    sql = text(f"""
        UPDATE work_at_height_toolbox_talk_participant
        SET {set_clause}
        WHERE whttp_id = :whttp_id
    """)

    payload["whttp_id"] = whttp_id
    db.execute(sql, payload)

    # ✅ AUTO INSERT HISTORY ON UPDATE
    insert_wah_toolbox_participant_history(db, whttp_id)

    db.commit()

    return True
