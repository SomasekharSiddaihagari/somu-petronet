from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_all_work_at_height_toolbox_talk_participants(db: Session):
    query = text("""
        SELECT
            whttp_id,
            toolbox_talk_id,
            participant_name,
            participant_signature,
            created_at
        FROM work_at_height_toolbox_talk_participant
        ORDER BY whttp_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


def get_work_at_height_toolbox_talk_participant_by_id(
    db: Session,
    whttp_id: int
):
    query = text("""
        SELECT
            whttp_id,
            toolbox_talk_id,
            participant_name,
            participant_signature,
            created_at
        FROM work_at_height_toolbox_talk_participant
        WHERE whttp_id = :whttp_id
    """)

    result = db.execute(
        query,
        {"whttp_id": whttp_id}
    ).mappings().first()

    return result
