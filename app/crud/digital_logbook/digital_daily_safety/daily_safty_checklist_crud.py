from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.digital_logbook.digital_daily_safety.daily_safty_checklist_schemas import DailySafetyChecklistCreate, DailySafetyChecklistUpdate



def _clean(data: dict):
    return {k: v for k, v in data.items() if v is not None}


def create_daily_safety_checklist(db: Session, payload: DailySafetyChecklistCreate):
    data = _clean(payload.dict(exclude={"dsc_id"}))

    columns = ", ".join(data.keys())
    values = ", ".join([f":{k}" for k in data.keys()])

    query = text(f"""
        INSERT INTO daily_safety_checklist ({columns})
        VALUES ({values})
        RETURNING dsc_id
    """)

    result = db.execute(query, data)
    db.commit()
    return result.fetchone()[0]


def update_daily_safety_checklist(
    db: Session,
    dsc_id: int,
    payload: DailySafetyChecklistUpdate
):
    data = _clean(payload.dict(exclude={"dsc_id"}))
    if not data:
        return True

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    data["dsc_id"] = dsc_id

    query = text(f"""
        UPDATE daily_safety_checklist
        SET {set_clause},
            updated_at = NOW()
        WHERE dsc_id = :dsc_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_daily_safety_checklist(db: Session, dsc_id: int):
    query = text("""
        DELETE FROM daily_safety_checklist
        WHERE dsc_id = :dsc_id
    """)
    db.execute(query, {"dsc_id": dsc_id})
    db.commit()
    return True
