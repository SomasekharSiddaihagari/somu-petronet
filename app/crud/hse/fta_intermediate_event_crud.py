# app/crud/hse/fta_intermediate_event_crud.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException

from app.schemas.hse.fta_intermediate_event_schema import (
    FTAIntermediateEventCreate,
    FTAIntermediateEventUpdate
)

# =========================
# CREATE
# =========================
def create_intermediate_event(
    db: Session,
    data: FTAIntermediateEventCreate
):
    payload = data.model_dump()

    sql = text("""
        INSERT INTO fta_intermediate_event (
            top_event_id,
            intermediate_e1,
            intermediate_e2
        )
        VALUES (
            :top_event_id,
            :intermediate_e1,
            :intermediate_e2
        )
        RETURNING intermediate_event_id
    """)

    res = db.execute(sql, payload)
    db.commit()

    return {"intermediate_event_id": res.scalar()}


# =========================
# UPDATE
# =========================
def update_intermediate_event(
    db: Session,
    intermediate_event_id: int,
    data: FTAIntermediateEventUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    payload["intermediate_event_id"] = intermediate_event_id

    set_clause = ", ".join(
        [f"{k}=:{k}" for k in payload if k != "intermediate_event_id"]
    )

    sql = text(f"""
        UPDATE fta_intermediate_event
        SET {set_clause}
        WHERE intermediate_event_id = :intermediate_event_id
    """)

    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL
# =========================
def get_all_intermediate_events(
    db: Session,
    top_event_id: int | None = None
):
    if top_event_id:
        sql = text("""
            SELECT *
            FROM fta_intermediate_event
            WHERE top_event_id = :top_event_id
            ORDER BY intermediate_event_id
        """)
        rows = db.execute(sql, {"top_event_id": top_event_id}).mappings().all()
    else:
        sql = text("""
            SELECT *
            FROM fta_intermediate_event
            ORDER BY intermediate_event_id DESC
        """)
        rows = db.execute(sql).mappings().all()

    return {
        "count": len(rows),
        "data": rows
    }
