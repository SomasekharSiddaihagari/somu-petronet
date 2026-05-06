from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.hse.incident_investigation_team_schema import (
    IncidentInvestigationTeamCreate,
    IncidentInvestigationTeamUpdate
)


# =========================
# CREATE
# =========================
def create_investigation_team(db: Session, data):
    try:
        payload = data.model_dump()
        print("PAYLOAD:", payload)

        sql = text("""
            INSERT INTO incident_investigation_team (
                prevention_id,
                sl_no,
                member_name,
                designation,
                station,
                role,
                is_leader,
                is_member,
                leader_acknowledged,
                member_acknowledged,
                user_id,
                created_at,
                updated_at
            )
            VALUES (
                :prevention_id,
                :sl_no,
                :member_name,
                :designation,
                :station,
                :role,
                :is_leader,
                :is_member,
                :leader_acknowledged,
                :member_acknowledged,
                :user_id,
                NOW(),
                NOW()
            )
            RETURNING iit_id
        """)

        result = db.execute(sql, payload)
        new_id = result.scalar()

        db.commit()
        print("INSERTED ID:", new_id)

        return {"iit_id": new_id, "user_id": payload["user_id"]}

    except Exception as e:
        db.rollback()
        print("ERROR:", str(e))
        raise

# =========================
# UPDATE
# =========================
def update_investigation_team(db, iit_id: int, data):
    try:
        payload = data.model_dump(exclude_unset=True)
        print("UPDATE PAYLOAD:", payload)

        if not payload:
            return {"message": "No fields to update"}

        # auto role logic (recommended)
        if "role" in payload:
            if payload["role"] == "Leader":
                payload["is_leader"] = True
                payload["is_member"] = False
            elif payload["role"] == "Member":
                payload["is_leader"] = False
                payload["is_member"] = True

        set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

        sql = text(f"""
            UPDATE incident_investigation_team
            SET {set_clause},
                updated_at = NOW()
            WHERE iit_id = :iit_id
            RETURNING iit_id
        """)

        payload["iit_id"] = iit_id

        result = db.execute(sql, payload)
        updated_id = result.scalar()

        db.commit()

        if not updated_id:
            raise HTTPException(status_code=404, detail="Record not found")

        return {
            "message": "Updated successfully",
            "iit_id": updated_id
        }

    except Exception as e:
        db.rollback()
        print("PUT ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
# =========================
# LIST
# =========================
def get_all_investigation_teams(db: Session):
    sql = text("""
        SELECT *
        FROM incident_investigation_team
        ORDER BY created_at DESC
    """)
    rows = db.execute(sql).mappings().all()
    return {"count": len(rows), "data": rows}


# =========================
# GET BY PREVENTION
# =========================
def get_investigation_team_by_prevention_id(db: Session, prevention_id: int):
    sql = text("""
        SELECT *
        FROM incident_investigation_team
        WHERE prevention_id = :prevention_id
        ORDER BY sl_no
    """)
    rows = db.execute(sql, {"prevention_id": prevention_id}).mappings().all()
    return {"count": len(rows), "data": rows}


# =========================
# GET BY ID
# =========================
def get_investigation_team_by_id(db: Session, iit_id: int):
    sql = text("""
        SELECT *
        FROM incident_investigation_team
        WHERE iit_id = :iit_id
    """)
    return db.execute(sql, {"iit_id": iit_id}).mappings().first()
