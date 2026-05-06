# app/crud/hse/fta_top_event_crud.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException

from app.schemas.hse.fta_top_event_schema import (
    FTATopEventCreate,
    FTATopEventUpdate
)

# =========================
# CREATE
# =========================
def create_fta_top_event(db: Session, hiim_id: int, payload: dict):

    payload["hiim_id"] = hiim_id

    sql = text("""
        INSERT INTO fta_top_event (
            hiim_id,
            event_description
        )
        VALUES (
            :hiim_id,
            :event_description
        )
        RETURNING fta_top_id
    """)

    try:
        res = db.execute(sql, payload)
        db.commit()
        return {"fta_top_id": res.scalar()}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid hiim_id or database error"
        )


# =========================
# UPDATE
# =========================
def update_fta_top_event(
    db: Session,
    fta_top_id: int,
    data: FTATopEventUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    payload["fta_top_id"] = fta_top_id

    set_clause = ", ".join([f"{k}=:{k}" for k in payload if k != "fta_top_id"])

    sql = text(f"""
        UPDATE fta_top_event
        SET {set_clause}
        WHERE fta_top_id = :fta_top_id
    """)

    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL
# =========================
def get_all_fta_top_events(db: Session):
    rows = db.execute(
        text("""
            SELECT *
            FROM fta_top_event
            ORDER BY created_at DESC
        """)
    ).mappings().all()

    return {
        "count": len(rows),
        "data": rows
    }
