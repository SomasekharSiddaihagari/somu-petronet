

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.hse.safety_committee_mintues_discussion import DiscussionCreate, DiscussionUpdate



def get_all_discussions(db: Session):
    discussions = db.execute(
        text("SELECT * FROM safety_committee_minutes_discussions ORDER BY id DESC")
    ).mappings().all()

    result = []
    for disc in discussions:
        disc_dict = dict(disc)

        children = db.execute(
            text("""
                SELECT * FROM safety_committee_minutes_discussion_child
                WHERE discussion_id = :discussion_id
                ORDER BY scmdc_id ASC
            """),
            {"discussion_id": disc_dict["id"]}
        ).mappings().all()

        disc_dict["children"] = [dict(c) for c in children]
        result.append(disc_dict)

    return result


def get_discussion_by_id(db: Session, discussion_id: int):
    discussion = db.execute(
        text("SELECT * FROM safety_committee_minutes_discussions WHERE id = :id"),
        {"id": discussion_id}
    ).mappings().first()

    if not discussion:
        return None

    children = db.execute(
        text("""
            SELECT * FROM safety_committee_minutes_discussion_child
            WHERE discussion_id = :discussion_id
            ORDER BY scmdc_id ASC
        """),
        {"discussion_id": discussion_id}
    ).mappings().all()

    return {
        **dict(discussion),
        "children": [dict(c) for c in children]
    }




def create_discussion(db: Session, data: DiscussionCreate):
    query = text("""
        INSERT INTO safety_committee_minutes_discussions
        (scmm_id, row_no, user_id, description_of_discussion, issues_discussed,
         action_taken, completed_on, action_by, target_date)
        VALUES
        (:scmm_id, :row_no, :user_id, :description_of_discussion, :issues_discussed,
         :action_taken, :completed_on, :action_by, :target_date)
        RETURNING *
    """)

    payload = data.model_dump()   # ✅ better for Pydantic v2

    print(payload)  # 🔍 DEBUG (very important)

    # ✅ Fix wrong key if coming from frontend
    if "User_id" in payload:
        payload["user_id"] = payload.pop("User_id")

    # ✅ Ensure user_id exists
    if payload.get("user_id") is None:
        raise ValueError("user_id is required")

    result = db.execute(query, payload)


    db.commit()

    return result.mappings().first()



def update_discussion(db: Session, discussion_id: int, data: DiscussionUpdate):

    # dynamic update fields
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        return {"message": "No fields to update"}

    set_clause = ", ".join([f"{k} = :{k}" for k in update_data.keys()])
    update_data["id"] = discussion_id

    query = text(f"""
        UPDATE safety_committee_minutes_discussions
        SET {set_clause}
        WHERE id = :id
        RETURNING *
    """)

    result = db.execute(query, update_data)
    db.commit()

    return result.mappings().first()