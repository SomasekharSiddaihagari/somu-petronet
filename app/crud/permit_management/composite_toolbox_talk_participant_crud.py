from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.schemas.permit_management.composite_toolbox_talk_participant_schema import (
    CompositeToolboxTalkParticipantCreate,
    CompositeToolboxTalkParticipantUpdate
)

# =================================================
# INSERT HISTORY SNAPSHOT
# =================================================
def insert_composite_toolbox_talk_participant_history(db: Session, cttp_id: int):
    history_sql = text("""
        INSERT INTO composite_toolbox_talk_participant_history (
            cttp_id,
            toolbox_talk_id,
            participant_name,
            participant_signature,
            created_at
        )
        SELECT
            cttp_id,
            toolbox_talk_id,
            participant_name,
            participant_signature,
            NOW()
        FROM composite_toolbox_talk_participant
        WHERE cttp_id = :cttp_id
    """)

    db.execute(history_sql, {"cttp_id": cttp_id})


# =================================================
# CREATE (MAIN + HISTORY)
# =================================================
def create_toolbox_talk_participant(
    db: Session,
    data: CompositeToolboxTalkParticipantCreate
):
    payload = data.model_dump()

    insert_sql = text("""
        INSERT INTO composite_toolbox_talk_participant (
            toolbox_talk_id,
            participant_name,
            participant_signature
        )
        VALUES (
            :toolbox_talk_id,
            :participant_name,
            :participant_signature
        )
        RETURNING cttp_id
    """)

    result = db.execute(insert_sql, payload)
    cttp_id = result.scalar()

    # ✅ AUTO INSERT HISTORY
    insert_composite_toolbox_talk_participant_history(db, cttp_id)

    db.commit()

    return {"cttp_id": cttp_id}


# =================================================
# UPDATE (MAIN + HISTORY)
# =================================================
def update_toolbox_talk_participant(
    db: Session,
    cttp_id: int,
    data: CompositeToolboxTalkParticipantUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    update_sql = text(f"""
        UPDATE composite_toolbox_talk_participant
        SET {set_clause}
        WHERE cttp_id = :cttp_id
    """)

    payload["cttp_id"] = cttp_id
    db.execute(update_sql, payload)

    # ✅ AUTO INSERT HISTORY ON UPDATE
    insert_composite_toolbox_talk_participant_history(db, cttp_id)

    db.commit()

    return True
