from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_all_composite_toolbox_talk_participants(db: Session):
    query = text("""
        SELECT
            cttp_id,
            toolbox_talk_id,
            participant_name,
            participant_signature,
            created_at
        FROM composite_toolbox_talk_participant
        ORDER BY cttp_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


def get_composite_toolbox_talk_participant_by_id(
    db: Session,
    cttp_id: int
):
    query = text("""
        SELECT
            cttp_id,
            toolbox_talk_id,
            participant_name,
            participant_signature,
            created_at
        FROM composite_toolbox_talk_participant
        WHERE cttp_id = :cttp_id
    """)

    result = db.execute(
        query,
        {"cttp_id": cttp_id}
    ).mappings().first()

    return result
