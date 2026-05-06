from sqlalchemy.orm import Session
from sqlalchemy import text


def _clean(data: dict):
    return {k: v for k, v in data.items() if v is not None}


def create_supervisor_entry(db: Session, payload):
    data = _clean(payload.dict())
    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data])
    print(cols)
    print(vals)

    query = text(f"""
        INSERT INTO supervisor_entry ({cols})
        VALUES ({vals})
        RETURNING sup_entry_id
    """)

    res = db.execute(query, data)
    db.commit()
    return res.fetchone()[0]


def update_supervisor_entry(db: Session, sup_entry_id: int, payload):
    data = _clean(payload.dict())
    if not data:
        return True

    sets = ", ".join([f"{k} = :{k}" for k in data])
    data["sup_entry_id"] = sup_entry_id

    query = text(f"""
        UPDATE supervisor_entry
        SET {sets}
        WHERE sup_entry_id = :sup_entry_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_supervisor_entry(db: Session, sup_entry_id: int):
    db.execute(
        text("DELETE FROM supervisor_entry WHERE sup_entry_id = :id"),
        {"id": sup_entry_id}
    )
    db.commit()
    return True
