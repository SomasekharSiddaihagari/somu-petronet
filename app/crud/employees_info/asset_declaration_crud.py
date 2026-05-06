from sqlalchemy.orm import Session
from sqlalchemy import text

def get_all_asset_declarations(db: Session):
    rows = db.execute(text("SELECT * FROM get_all_asset_declarations();")).fetchall()
    return [dict(r._mapping) for r in rows]

def get_asset_declaration_by_id(db: Session, asset_id: int):
    row = db.execute(
        text("SELECT * FROM get_asset_declaration_by_id(:aid);"),
        {"aid": asset_id}
    ).fetchone()

    return dict(row._mapping) if row else None

def get_asset_declaration_by_user_id(db: Session, user_id: int):
    rows = db.execute(
        text("SELECT * FROM get_asset_declaration_by_user_id(:uid);"),
        {"uid": user_id}
    ).fetchall()

    return [dict(r._mapping) for r in rows]


