from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.hse.safety_committee_minutes_members_schema import SafetyCommitteeMinutesMemberCreate, SafetyCommitteeMinutesMemberUpdate

def create_minutes_member(db: Session, data: SafetyCommitteeMinutesMemberCreate):
    payload = data.model_dump()
    payload["updated_by"] = payload.get("created_by")
    
    # Model defines PK as scmm_id (same as minutes table??)
    # This might be tricky if they are 1-to-1 or just bad naming. 
    # Assuming it is an auto-increment PK for this table.
    sql = text("""
        INSERT INTO safety_committee_minutes_members (
            minutes_id, member_name,user_id, created_by, updated_by
        ) VALUES (
            :minutes_id, :member_name,:user_id, :created_by, :updated_by
        ) RETURNING scmm_id
    """)
    
    result = db.execute(sql, payload)
    db.commit()
    
    new_id = result.scalar()
    return {
        "status": "success",
        "scmm_id": new_id,
        "message": "Minutes Member created successfully"
    }

def get_minutes_member_by_id(db: Session, scmm_id: int):
    sql = text("""
        SELECT * FROM safety_committee_minutes_members WHERE scmm_id = :scmm_id
    """)
    result = db.execute(sql, {"scmm_id": scmm_id}).mappings().first()
    return result

def get_all_minutes_members(db: Session):
    sql = text("""
        SELECT * FROM safety_committee_minutes_members ORDER BY created_at DESC
    """)
    result = db.execute(sql).mappings().all()
    return result

def update_minutes_member(db: Session, scmm_id: int, data: SafetyCommitteeMinutesMemberUpdate):
    payload = data.model_dump(exclude_unset=True)
    if not payload:
        return {"message": "No fields to update"}

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])
    sql = text(f"""
        UPDATE safety_committee_minutes_members
        SET {set_clause}, updated_at = NOW()
        WHERE scmm_id = :scmm_id
    """)
    
    payload["scmm_id"] = scmm_id
    db.execute(sql, payload)
    db.commit()
    
    return {"message": "Minutes Member updated successfully"}

def delete_minutes_member(db: Session, scmm_id: int):
    sql = text("DELETE FROM safety_committee_minutes_members WHERE scmm_id = :scmm_id")
    db.execute(sql, {"scmm_id": scmm_id})
    db.commit()
    return {"message": "Minutes Member deleted successfully"}
