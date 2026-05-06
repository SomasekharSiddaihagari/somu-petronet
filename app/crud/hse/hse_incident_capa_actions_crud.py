# app/crud/hse/hse_incident_capa_actions_crud.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException

from app.schemas.hse.hse_incident_capa_actions_schema import (
    IncidentCAPACreate,
    IncidentCAPAUpdate
)


# =========================
# CREATE
# =========================
def create_capa_action(db: Session, data: IncidentCAPACreate):
    payload = data.model_dump()

    sql = text("""
        INSERT INTO hse_incident_capa_actions (
            incident_id,
            action,
            action_type,
            target_date
        )
        VALUES (
            :incident_id,
            :action,
            :action_type,
            :target_date
        )
        RETURNING capa_id
    """)

    res = db.execute(sql, payload)
    db.commit()
    return {"capa_id": res.scalar()}


# =========================
# UPDATE
# =========================
def update_capa_action(
    db: Session,
    capa_id: int,
    data: IncidentCAPAUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    payload["capa_id"] = capa_id

    set_clause = ", ".join(
        [f"{k}=:{k}" for k in payload if k != "capa_id"]
    )

    sql = text(f"""
        UPDATE hse_incident_capa_actions
        SET {set_clause}
        WHERE capa_id = :capa_id
    """)

    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL
# =========================
def get_all_capa_actions(db: Session):
    rows = db.execute(
        text("""
            SELECT *
            FROM hse_incident_capa_actions
            ORDER BY capa_id DESC
        """)
    ).mappings().all()

    return {
        "count": len(rows),
        "data": rows
    }
