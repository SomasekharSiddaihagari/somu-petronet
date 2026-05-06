# app/crud/hse/hse_incident_investigation_team_crud.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException

from app.schemas.hse.hse_incident_investigation_team_schema import (
    InvestigationTeamCreate,
    InvestigationTeamUpdate
)


# =========================
# CREATE
# =========================
def create_team_member(
    db: Session,
    data: InvestigationTeamCreate
):
    payload = data.model_dump()

    sql = text("""
        INSERT INTO hse_incident_investigation_team (
            incident_id,
            sl_no,
            name,
            designation,
            role,
            is_acknowledged
        )
        VALUES (
            :incident_id,
            :sl_no,
            :name,
            :designation,
            :role,
            :is_acknowledged
        )
        RETURNING invest_team_id
    """)

    res = db.execute(sql, payload)
    db.commit()
    return {"invest_team_id": res.scalar()}


# =========================
# UPDATE
# =========================
def update_team_member(
    db: Session,
    invest_team_id: int,
    data: InvestigationTeamUpdate
):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    payload["invest_team_id"] = invest_team_id

    set_clause = ", ".join([f"{k}=:{k}" for k in payload if k != "invest_team_id"])

    sql = text(f"""
        UPDATE hse_incident_investigation_team
        SET {set_clause},
            updated_at = NOW()
        WHERE invest_team_id = :invest_team_id
    """)

    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL (by investigation)
# =========================
def get_all_team_members(db: Session):
    sql = text("""
        SELECT
            invest_team_id,
            incident_id,
            sl_no,
            name,
            designation,
            role,
            is_acknowledged
        FROM hse_incident_investigation_team
        ORDER BY invest_team_id ASC
    """)

    rows = db.execute(sql).mappings().all()

    return {
        "count": len(rows),
        "data": rows
    }


from sqlalchemy import text
from sqlalchemy.orm import Session



def get_full_investigation(db: Session, incident_id: int):

    query = text("""
    
    SELECT
        ir.*,

        -- INCIDENT
        row_to_json(ir) AS incident,

        -- INVESTIGATION MASTER
        row_to_json(him) AS investigation,

        -- 🔥 NEW: leader + team ids
        iteam.leader_user_id,
        iteam.team_user_ids,

        -- TEAM DETAILS
        (
            SELECT json_agg(team_data)
            FROM (
                SELECT
                    hit.invest_team_id,
                    hit.sl_no,
                    hit.name,
                    hit.designation,
                    hit.role,
                    hit.is_acknowledged
                FROM hse_incident_investigation_team hit
                WHERE hit.incident_id = him.hiim_id
                ORDER BY hit.sl_no
            ) team_data
        ) AS investigation_team,


        -- SIC (ROLE = 2)
        (
            SELECT u.user_id
            FROM role_permissions rp
            JOIN users u
                ON u.user_id = rp.user_id
            WHERE rp.role_id = 2
            AND rp.submenu_id = 3
            AND u.station_id = ir.station
            LIMIT 1
        ) AS sic,


        -- OTHER ROLES
        (
            SELECT json_object_agg(role_name, user_ids)
            FROM (
                SELECT
                    LOWER(REPLACE(r.role_name,' ','_')) AS role_name,
                    array_agg(u.user_id) AS user_ids
                FROM role_permissions rp
                JOIN roles r
                    ON r.role_id = rp.role_id
                JOIN users u
                    ON u.user_id = rp.user_id
                WHERE rp.submenu_id = 3
                AND rp.role_id IN (4,12,10,3,1)
                AND u.station_id = ir.station
                GROUP BY r.role_name
            ) roles
        ) AS role_users

    FROM incident_report ir

    LEFT JOIN hse_incident_investigation_master him
        ON him.incident_id = ir.incident_id

    -- ✅ CORRECT JOIN: prevention table
    LEFT JOIN incident_prevention ip
        ON ip.incident_id = ir.incident_id

    -- ✅ leader + team ids
    LEFT JOIN (
        SELECT 
            prevention_id,
            MAX(CASE WHEN is_leader = TRUE THEN user_id END) AS leader_user_id,
            json_agg(user_id) FILTER (WHERE is_member = TRUE) AS team_user_ids
        FROM incident_investigation_team
        GROUP BY prevention_id
    ) iteam
        ON ip.ip_id = iteam.prevention_id

    WHERE ir.incident_id = :incident_id
    """)

    row = db.execute(query, {"incident_id": incident_id}).mappings().first()

    if not row:
        return {"message": "Incident not found"}

    response = {
        "incident": row["incident"],
        "investigation": row["investigation"],
        "investigation_team": row["investigation_team"] or [],
        "leader_user_id": row["leader_user_id"],
        "team_user_ids": row["team_user_ids"] or [],
        "sic": row["sic"]
    }

    if row["role_users"]:
        response.update(row["role_users"])

    return {"data": response}

















