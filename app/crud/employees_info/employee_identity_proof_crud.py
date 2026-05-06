# app/crud/identity_proof.py
from sqlalchemy.orm import Session
from sqlalchemy import text


def get_all_identity_proofs(db: Session):
    return db.execute(text("SELECT * FROM employee_identity_proof;")).fetchall()


def get_identity_proof_by_id(db: Session, eip_id: int):
    return db.execute(
        text("SELECT * FROM employee_identity_proof WHERE eip_id = :id"),
        {"id": eip_id},
    ).fetchone()


def get_identity_proof_by_user_id(db: Session, user_id: int):
    return db.execute(
        text("SELECT * FROM employee_identity_proof WHERE user_id = :uid"),
        {"uid": user_id},
    ).fetchall()
