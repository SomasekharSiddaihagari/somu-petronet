from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.hse.safety_committee_meeting_schema import SafetyCommitteeMeetingCreate, SafetyCommitteeMeetingUpdate
def generate_meeting_no(db, user_id: int):
    from datetime import date

    # station code
    station_sql = text("""
        SELECT st.station_code
        FROM station st
        JOIN users u ON u.station_id = st.station_id
        WHERE u.user_id = :user_id
        LIMIT 1
    """)
    station_code = db.execute(station_sql, {"user_id": user_id}).scalar()

    if not station_code:
        raise Exception("Station not found")

    today = date.today()

    if today.month >= 4:
        year_part = f"{today.year}-{str(today.year+1)[-2:]}"
    else:
        year_part = f"{today.year-1}-{str(today.year)[-2:]}"

    seq_sql = text("""
        SELECT COALESCE(
            MAX(CAST(regexp_replace(meeting_no, '^.*/([0-9]{3})$', '\\1') AS INTEGER)),0
        ) + 1
        FROM safety_committee_minutes
        WHERE meeting_no LIKE :pattern
    """)

    pattern = f"SCM/{station_code}/{year_part}/%"
    seq = db.execute(seq_sql, {"pattern": pattern}).scalar()

    seq_str = str(seq).zfill(3)

    return f"SCM/{station_code}/{year_part}/{seq_str}"

def create_meeting(db: Session, data: SafetyCommitteeMeetingCreate):
    payload = data.model_dump()
    payload["updated_by"] = payload.get("created_by")

    sql = text("""
        INSERT INTO safety_committee_quarterly_meetings (
            location,
            meeting_date,
            meeting_time,
            is_active,
            created_by,
            updated_by
        ) VALUES (
            :location,
            :meeting_date,
            :meeting_time,
            :is_active,
            :created_by,
            :updated_by
        ) RETURNING scm_id
    """)

    result = db.execute(sql, payload)
    db.commit()

    new_id = result.scalar()

    return {
        "status": "success",
        "scm_id": new_id,
        "message": "Quarterly Meeting created successfully"
    }

def get_meeting_by_id(db: Session, scm_id: int):
    sql = text("""
        SELECT * FROM safety_committee_quarterly_meetings WHERE scm_id = :scm_id
    """)
    result = db.execute(sql, {"scm_id": scm_id}).mappings().first()
    return result

def get_all_meetings(db: Session):
    sql = text("""
        SELECT * FROM safety_committee_quarterly_meetings ORDER BY created_at DESC
    """)
    result = db.execute(sql).mappings().all()
    return result

def update_meeting(db: Session, scm_id: int, data: SafetyCommitteeMeetingUpdate):
    payload = data.model_dump(exclude_unset=True)
    payload["updated_by"] = payload.get("created_by")
    if not payload:
        return {"message": "No fields to update"}

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])
    sql = text(f"""
        UPDATE safety_committee_quarterly_meetings
        SET {set_clause}, updated_at = NOW()
        WHERE scm_id = :scm_id
    """)
    
    payload["scm_id"] = scm_id
    db.execute(sql, payload)
    db.commit()
    
    return {"message": "Quarterly Meeting updated successfully"}

def delete_meeting(db: Session, scm_id: int):
    sql = text("DELETE FROM safety_committee_quarterly_meetings WHERE scm_id = :scm_id")
    db.execute(sql, {"scm_id": scm_id})
    db.commit()
    return {"message": "Quarterly Meeting deleted successfully"}
