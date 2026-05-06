from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
 
 
# =========================
# CREATE
# =========================
def create_rca_5why(db: Session, payload: dict):
    try:
        sql = text("""
            INSERT INTO hse_incident_rca_5why (
                hiim_id, 
                why1,
                why2,
                why3,
                why4,
                why5_root_cause,
                problem_statement   
            )
            VALUES (
                :hiim_id,  
                :why1,
                :why2,
                :why3,
                :why4,
                :why5_root_cause,
                :problem_statement
            )
            RETURNING
                rca_id,
                hiim_id,
                why1,
                why2,
                why3,
                why4,
                why5_root_cause,
                problem_statement   
        """)
 
        res = db.execute(sql, payload).mappings().first()
        db.commit()
        return res
 
    except SQLAlchemyError:
        db.rollback()
        raise
 
 
# =========================
# UPDATE
# =========================
def update_rca_5why(db: Session, rca_id: int, payload: dict):
    try:
        allowed_fields = {
            "why1", "why2", "why3", "why4", "why5_root_cause","problem_statement"
        }
 
        update_data = {
            k: v for k, v in payload.items()
            if k in allowed_fields and v is not None
        }
 
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
 
        update_data["rca_id"] = rca_id
 
        set_clause = ", ".join(
            f"{k} = :{k}" for k in update_data if k != "rca_id"
        )
 
        sql = text(f"""
            UPDATE hse_incident_rca_5why
            SET {set_clause}
            WHERE rca_id = :rca_id
        """)
 
        result = db.execute(sql, update_data)
 
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="RCA record not found")
 
        db.commit()
        return True
 
    except SQLAlchemyError:
        db.rollback()
        raise
 
 
# =========================
# GET ALL (OPTIONAL FILTER)
# =========================
def get_all_rca_5why(db: Session, hiim_id: int | None = None):
    sql = """
        SELECT
            rca_id,
            hiim_id,
            why1,
            why2,
            why3,
            why4,
            why5_root_cause,
            problem_statement
        FROM hse_incident_rca_5why
    """
 
    params = {}
 
    if hiim_id:
        sql += " WHERE hiim_id = :hiim_id"
        params["hiim_id"] = hiim_id
 
    sql += " ORDER BY rca_id ASC"
 
    rows = db.execute(text(sql), params).mappings().all()
 
    return {
        "count": len(rows),
        "data": rows
    }
 
 
 
 