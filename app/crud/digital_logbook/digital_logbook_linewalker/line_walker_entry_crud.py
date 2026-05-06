from sqlalchemy.orm import Session
from sqlalchemy import text


def _clean(data: dict):
    return {k: v for k, v in data.items() if v is not None}


def create_line_walker_entry(db: Session, payload):
    data = _clean(payload.dict())
    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data])

    query = text(f"""
        INSERT INTO line_walker_entry ({cols})
        VALUES ({vals})
        RETURNING line_entry_id
    """)

    res = db.execute(query, data)
    db.commit()
    return res.fetchone()[0]


def update_line_walker_entry(db: Session, line_entry_id: int, payload):
    data = _clean(payload.dict())
    if not data:
        return True

    sets = ", ".join([f"{k} = :{k}" for k in data])
    data["line_entry_id"] = line_entry_id

    query = text(f"""
        UPDATE line_walker_entry
        SET {sets}
        WHERE line_entry_id = :line_entry_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_line_walker_entry(db: Session, line_entry_id: int):
    db.execute(
        text("DELETE FROM line_walker_entry WHERE line_entry_id = :id"),
        {"id": line_entry_id}
    )
    db.commit()
    return True
