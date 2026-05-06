from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.hse.safety_committee_schema import SafetyCommitteeMemberCreate, SafetyCommitteeMemberUpdate

def generate_team_sl_no(db: Session):
    sql = text("""
        SELECT COALESCE(MAX(sl_no), 0) + 1 AS new_sl_no
        FROM safety_committee_members
    """)
    result = db.execute(sql).fetchone()
    return result.new_sl_no

def create_safety_committee_member(db: Session, data):

    payload = data.model_dump()
    created_by = payload.get("created_by")
    members = payload.get("members")

    # take station from first member
    station_id = members[0].get("station") if members else None

    # =========================================
    # make old teams inactive for that station
    # =========================================
    if station_id:
        deactivate_sql = text("""
            UPDATE safety_committee_members
            SET is_active = false
            WHERE station = :station_id
        """)
        db.execute(deactivate_sql, {"station_id": station_id})

    # =========================================
    # generate new team id
    # =========================================
    team_sql = text("""
        SELECT COALESCE(MAX(sl_no),0)+1 AS new_sl_no
        FROM safety_committee_members
    """)
    team_id = db.execute(team_sql).fetchone().new_sl_no

    # =========================================
    # insert new team members (active)
    # =========================================
    insert_sql = text("""
        INSERT INTO safety_committee_members
        (sl_no, name, designation, station, is_active, created_by, updated_by,user_id)
        VALUES
        (:sl_no, :name, :designation, :station, true, :created_by, :updated_by, :user_id)
    """)

    for m in members:
        db.execute(insert_sql, {
            "sl_no": team_id,
            "name": m.get("name"),
            "designation": m.get("designation"),
            "station": m.get("station"),
            "created_by": created_by,
            "updated_by": created_by,
            "user_id": m.get("user_id")
        })

    db.commit()

    return {
        "status": "success",
        "team_id": team_id,
        "message": "New team created & old team deactivated"
    }

# ============================================
# GET TEAM BY TEAM ID
# ============================================
def get_team_by_station(db: Session, station_id: int):

    # 🔹 latest active team for station
    team_sql = text("""
        SELECT sl_no
        FROM safety_committee_members
        WHERE station = :station_id
        AND is_active = true
        ORDER BY sl_no DESC
        LIMIT 1
    """)

    team_row = db.execute(team_sql, {"station_id": station_id}).fetchone()

    if not team_row:
        return {
            "station_id": station_id,
            "active_team": [],
            "message": "No active team"
        }

    team_id = team_row.sl_no

    # 🔹 fetch members of that team
    member_sql = text("""
        SELECT scm_id, sl_no AS team_id, name, designation, station
        FROM safety_committee_members
        WHERE sl_no = :team_id
        AND is_active = true
        ORDER BY scm_id
    """)

    members = db.execute(member_sql, {"team_id": team_id}).mappings().all()

    return {
        "station_id": station_id,
        "team_id": team_id,
        "active_team": members
    }


def delete_safety_committee_member(db: Session, scm_id: int):
    sql = text("""
        DELETE FROM safety_committee_members
        WHERE scm_id = :scm_id
    """)
    db.execute(sql, {"scm_id": scm_id})
    db.commit()


def get_safety_committee_member_by_id(db: Session, scm_id: int):
    sql = text("""
        SELECT * FROM safety_committee_members WHERE scm_id = :scm_id
    """)
    result = db.execute(sql, {"scm_id": scm_id}).mappings().first()
    return result

def get_all_safety_committee_members(db: Session):
    sql = text("""
        SELECT * FROM safety_committee_members ORDER BY created_at DESC
    """)
    result = db.execute(sql).mappings().all()
    return result

def update_safety_committee_member(db: Session, scm_id: int, data: SafetyCommitteeMemberUpdate):
    payload = data.model_dump(exclude_unset=True)
    if not payload:
        return {"message": "No fields to update"}

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])
    sql = text(f"""
        UPDATE safety_committee_members
        SET {set_clause}, updated_at = NOW()
        WHERE scm_id = :scm_id
    """)
    
    payload["scm_id"] = scm_id
    db.execute(sql, payload)
    db.commit()
    
    return {"message": "Safety Committee Member updated successfully"}

def delete_safety_committee_member(db: Session, scm_id: int):
    sql = text("DELETE FROM safety_committee_members WHERE scm_id = :scm_id")
    db.execute(sql, {"scm_id": scm_id})
    db.commit()
    return {"message": "Safety Committee Member deleted successfully"}


    
