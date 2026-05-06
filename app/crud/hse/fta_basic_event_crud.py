# app/crud/hse/fta_basic_event_crud.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException

from app.schemas.hse.fta_basic_event_schema import (
    FTABasicEventCreate,
    FTABasicEventUpdate
)


# =========================
# CREATE
# =========================
def create_basic_event(db: Session, data: FTABasicEventCreate):
    payload = data.model_dump()

    sql = text("""
        INSERT INTO fta_basic_event (
            intermediate_event_id,
            e1_b1,
            e1_b2,
            e2_b1,
            e2_b2
        )
        VALUES (
            :intermediate_event_id,
            :e1_b1,
            :e1_b2,
            :e2_b1,
            :e2_b2
        )
        RETURNING fte_basic_id
    """)

    res = db.execute(sql, payload)
    db.commit()
    return {"fte_basic_id": res.scalar()}


# =========================
# UPDATE
# =========================
def update_basic_event(
    db: Session,
    fte_basic_id: int,
    data: FTABasicEventUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        raise HTTPException(status_code=400, detail="No fields to update")

    payload["fte_basic_id"] = fte_basic_id

    set_clause = ", ".join(
        [f"{k}=:{k}" for k in payload if k != "fte_basic_id"]
    )

    sql = text(f"""
        UPDATE fta_basic_event
        SET {set_clause}
        WHERE fte_basic_id = :fte_basic_id
    """)

    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL
# =========================
def get_all_basic_events(db: Session):
    rows = db.execute(
        text("""
            SELECT *
            FROM fta_basic_event
            ORDER BY fte_basic_id DESC
        """)
    ).mappings().all()

    return {
        "count": len(rows),
        "data": rows
    }
