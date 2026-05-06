from sqlalchemy.orm import Session
from sqlalchemy import text

def get_user_basic_info(db: Session, user_id: int):
    row = db.execute(
        text("SELECT employee_code, first_name, last_name FROM users WHERE user_id = :uid"),
        {"uid": user_id}
    ).fetchone()

    return dict(row._mapping) if row else None



def get_all_form12c(db: Session):
    rows = db.execute(text("SELECT * FROM get_all_form12c();")).fetchall()
    return [dict(r._mapping) for r in rows]

def get_form12c_by_id(db: Session, form_id: int):
    row = db.execute(
        text("SELECT * FROM get_form12c_by_id(:fid);"),
        {"fid": form_id}
    ).fetchone()

    return dict(row._mapping) if row else None

def get_form12c_by_user_id(db: Session, user_id: int):
    rows = db.execute(
        text("SELECT * FROM employee_form_12c WHERE user_id = :u_id"),
        {"u_id": user_id}
    ).fetchall()

    return [dict(row._mapping) for row in rows] if rows else []


