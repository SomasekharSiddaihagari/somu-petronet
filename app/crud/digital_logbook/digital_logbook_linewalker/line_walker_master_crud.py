from sqlalchemy.orm import Session
from sqlalchemy import text


def _clean(data: dict):
    return {k: v for k, v in data.items() if v is not None}


def create_line_walker_master(db: Session, payload):
    data = _clean(payload.dict())
    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data])

    query = text(f"""
        INSERT INTO line_walker_master ({cols})
        VALUES ({vals})
        RETURNING line_walker_id
    """)

    res = db.execute(query, data)
    db.commit()
    return res.fetchone()[0]


def update_line_walker_master(db: Session, line_walker_id: int, payload):
    data = _clean(payload.dict())
    if not data:
        return True

    sets = ", ".join([f"{k} = :{k}" for k in data])
    data["line_walker_id"] = line_walker_id

    query = text(f"""
        UPDATE line_walker_master
        SET {sets}
        WHERE line_walker_id = :line_walker_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_line_walker_master(db: Session, line_walker_id: int):
    db.execute(
        text("DELETE FROM line_walker_master WHERE line_walker_id = :id"),
        {"id": line_walker_id}
    )
    db.commit()
    return True
