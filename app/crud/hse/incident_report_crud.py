import os

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import date
from fastapi import HTTPException

from app.schemas.hse.incident_report_schema import (
    IncidentReportCreate,
    IncidentReportUpdate
)

# 🔒 FIXED ORGANISATION
FIXED_ORGANISATION = "Petronet"
BASE_URL = os.getenv("BackEndPath")

def build_file_url(file_path):
    if not file_path:
        return None
    return f"{BASE_URL}/{file_path}"

# =========================
# CREATE INCIDENT REPORT
# =========================
def get_financial_year(today=None):
    today = today or date.today()
    if today.month >= 4:
        return f"{today.year}-{str(today.year+1)[-2:]}"
    return f"{today.year-1}-{str(today.year)[-2:]}"


# ----------------------------
# Station Code via User
# ----------------------------
def get_station_code(db: Session, user_id: int):
    sql = text("""
        SELECT s.station_code
        FROM users u
        JOIN station s ON s.station_id = u.station_id
        WHERE u.user_id = :uid
    """)
    row = db.execute(sql, {"uid": user_id}).fetchone()
    if not row:
        raise HTTPException(400, "User station not found")
    return row.station_code


# ----------------------------
# Generate Incident Number
# ----------------------------
def generate_incident_no(db: Session, category: str, station_code: str):
    fy = get_financial_year()
    cat = "MIN" if category == "Minor" else "MAJ"

    sql = text("""
        SELECT
            COALESCE(
                MAX(
                    CAST(SPLIT_PART(incident_no_during_year,'/',5) AS INTEGER)
                ), 0
            ) AS last_no
        FROM incident_report
        WHERE incident_no_during_year LIKE :pat
    """)

    pattern = f"IR/{cat}/{station_code}/{fy}/%"

    row = db.execute(sql, {"pat": pattern}).fetchone()

    next_no = row.last_no + 1

    return f"IR/{cat}/{station_code}/{fy}/{str(next_no).zfill(3)}"



# =========================
# CREATE
# =========================
def create_incident_report(db: Session, data):
    payload = data.model_dump()

    payload["organisation"] = FIXED_ORGANISATION
    user_id = int(payload["created_by"])

    station_code = get_station_code(db, user_id)
    ref_no = generate_incident_no(db, payload["category"], station_code)

    payload["incident_no_during_year"] = ref_no

    sql = text("""
        INSERT INTO incident_report (
            organisation, category, sector, location,
            incident_no_during_year,
            date_of_incident, time_of_incident,
            incident_type, fire_incident,
            report_type, duration_of_fire,
            loss_of_life_injury, electrocution, slip_trip,
            fire, fall_from_height, leak_spill, explosion,
            inhalation_of_gas, blowout, driving,
            others, others_text, station,
            incident_location_detail, plant_shutdown,
            status, created_by,

            -- ===== MINOR WORKFLOW =====
            minor_sic_name,
            minor_sic_updated_date,
            minor_alloted_engineer_name,
            minor_alloted_eng_updated_date,
            minor_final_approve_name,
            minor_final_approved_date,

            -- ===== MAJOR WORKFLOW =====
            major_team_leader_by,
            major_team_leader_date,
            major_team_acknowledged_by,
            major_team_acknowledged_date,
            major_report_filled_by,
            major_report_filled_date,
            major_investigation_ack_by,
            major_investigation_ack_date,
            major_safety_officer_by,
            major_safety_officer_date,
            major_md_review_by,
            major_md_review_date,
            major_hse_review_by,
            major_hse_review_date,
            major_capa_filled_by,
            major_capa_filled_date,
            major_hse_capa_review_by,
            major_hse_capa_review_date,
            major_closure_by,
            major_closure_date
        )
        VALUES (
            :organisation, :category, :sector, :location,
            :incident_no_during_year,
            :date_of_incident, :time_of_incident,
            :incident_type, :fire_incident,
            :report_type, :duration_of_fire,
            :loss_of_life_injury, :electrocution, :slip_trip,
            :fire, :fall_from_height, :leak_spill, :explosion,
            :inhalation_of_gas, :blowout, :driving,
            :others, :others_text, :station,
            :incident_location_detail, :plant_shutdown,
            :status, :created_by,

            -- ===== MINOR =====
            :minor_sic_name,
            :minor_sic_updated_date,
            :minor_alloted_engineer_name,
            :minor_alloted_eng_updated_date,
            :minor_final_approve_name,
            :minor_final_approved_date,

            -- ===== MAJOR =====
            :major_team_leader_by,
            :major_team_leader_date,
            :major_team_acknowledged_by,
            :major_team_acknowledged_date,
            :major_report_filled_by,
            :major_report_filled_date,
            :major_investigation_ack_by,
            :major_investigation_ack_date,
            :major_safety_officer_by,
            :major_safety_officer_date,
            :major_md_review_by,
            :major_md_review_date,
            :major_hse_review_by,
            :major_hse_review_date,
            :major_capa_filled_by,
            :major_capa_filled_date,
            :major_hse_capa_review_by,
            :major_hse_capa_review_date,
            :major_closure_by,
            :major_closure_date
        )
        RETURNING incident_id
    """)

    res = db.execute(sql, payload)
    db.commit()

    return {
        "incident_id": res.scalar(),
        "incident_no": ref_no
    }



# =========================
# UPDATE INCIDENT REPORT
# =========================

def update_incident_report(
    db: Session,
    incident_id: int,
    data: IncidentReportUpdate
    ):
    payload = data.model_dump(exclude_unset=True)

    # 🔒 Prevent organisation manipulation
    payload.pop("organisation", None)

    if not payload:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])

    sql = text(f"""
        UPDATE incident_report
        SET {set_clause},
            updated_at = NOW()
        WHERE incident_id = :incident_id
    """)

    payload["incident_id"] = incident_id
    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL INCIDENT REPORTS
# =========================

def get_all_incident_reports(db: Session):

    sql = text("""
        SELECT
            ir.*,

            -- station name
            st.station_name,

            -- 🔥 created by name
            u.first_name AS created_by_first_name,
            u.last_name AS created_by_last_name,

            -- CHILD TABLES
            row_to_json(ia) AS impact_assessment,
            row_to_json(ca) AS cause_analysis,
            row_to_json(ip) AS incident_prevention,

            -- 🔥 TEAM DATA (ADDED ONLY)
            iteam.leader_user_id,
            iteam.team_user_ids

        FROM incident_report ir

        LEFT JOIN station st
            ON ir.station = st.station_id
            AND st.is_deleted = FALSE

        -- 🔥 JOIN USERS TABLE
        LEFT JOIN users u
            ON ir.created_by = u.user_id
            AND u.is_deleted = FALSE

        LEFT JOIN incident_impact_assessment ia
            ON ir.incident_id = ia.incident_id

        LEFT JOIN incident_cause_analysis ca
            ON ir.incident_id = ca.incident_id

        LEFT JOIN incident_prevention ip
            ON ir.incident_id = ip.incident_id

        -- 🔥 TEAM JOIN (ADDED ONLY)
        LEFT JOIN (
            SELECT 
                prevention_id,

                -- leader user id
                MAX(CASE WHEN is_leader = TRUE THEN user_id END) AS leader_user_id,

                -- team members array
                json_agg(user_id) FILTER (WHERE is_member = TRUE) AS team_user_ids

            FROM incident_investigation_team
            GROUP BY prevention_id
        ) iteam
            ON ip.ip_id = iteam.prevention_id

        ORDER BY ir.created_at DESC, ir.incident_id DESC
    """)

    rows = db.execute(sql).mappings().all()

    incidents = []

    for row in rows:
        incident = dict(row)

        incident["impact_assessment"] = row["impact_assessment"]
        incident["cause_analysis"] = row["cause_analysis"]
        incident["incident_prevention"] = row["incident_prevention"]

        # 🔥 created by full name
        incident["created_by_name"] = (
            (row["created_by_first_name"] or "") + " " +
            (row["created_by_last_name"] or "")
        ).strip()

        # 🔥 TEAM DATA ADDED
        incident["leader_user_id"] = row["leader_user_id"]
        incident["team_user_ids"] = row["team_user_ids"] or []

        incidents.append(incident)

    return {
        "count": len(incidents),
        "data": incidents
    }

def get_investigation_team_with_user(db: Session):

    sql = text("""
        SELECT 
            iit.iit_id,
            iit.prevention_id,
            iit.member_name,
            iit.role,
            iit.is_leader,
            iit.is_member,
            iit.designation,
            iit.station,

            COALESCE(
                json_agg(
                    json_build_object(
                        'user_id', u.user_id,
                        'first_name', u.first_name,
                        'last_name', u.last_name,
                        'full_name', CONCAT(u.first_name,' ',u.last_name)
                    )
                ) FILTER (WHERE u.user_id IS NOT NULL),
                '[]'
            ) AS matched_users

        FROM incident_investigation_team iit

        LEFT JOIN users u
            ON u.is_deleted = FALSE
            AND (
                LOWER(u.first_name || ' ' || u.last_name) = LOWER(iit.member_name)
                OR LOWER(u.first_name) = LOWER(iit.member_name)
                OR LOWER(u.last_name) = LOWER(iit.member_name)
            )

        GROUP BY 
            iit.iit_id,
            iit.prevention_id,
            iit.member_name,
            iit.role,
            iit.is_leader,
            iit.is_member,
            iit.designation,
            iit.station

        ORDER BY iit.prevention_id, iit.is_leader DESC, iit.iit_id
    """)

    rows = db.execute(sql).mappings().all()

    result = [dict(r) for r in rows]

    return {
        "count": len(result),
        "data": result
    }

# def get_incidents_by_user(db: Session, user_id: int):

#     # ---------------- INCIDENT QUERY ----------------
#     incident_query = text("""
#         SELECT 
#             ir.*,

#             json_build_object(
#                 'station_id', st.station_id,
#                 'station_name', st.station_name
#             ) AS station,

#             row_to_json(ia) AS impact_assessment,
#             row_to_json(ca) AS cause_analysis,
#             row_to_json(ip) AS incident_prevention

#         FROM incident_report ir

#         LEFT JOIN station st
#             ON ir.station = st.station_id
#             AND st.is_deleted = FALSE

#         LEFT JOIN incident_impact_assessment ia
#             ON ir.incident_id = ia.incident_id

#         LEFT JOIN incident_cause_analysis ca
#             ON ir.incident_id = ca.incident_id

#         LEFT JOIN incident_prevention ip
#             ON ir.incident_id = ip.incident_id

#         WHERE ir.created_by = :user_id
#         ORDER BY ir.created_at DESC
#     """)

#     incident_rows = db.execute(incident_query, {"user_id": user_id}).mappings().all()

#     incidents = [dict(row) for row in incident_rows]


#     # ---------------- USERS QUERY ----------------
#     users_query = text("""
#     SELECT DISTINCT
#         r.role_id,
#         r.role_name
#     FROM role_permissions rp
#     JOIN roles r
#         ON r.role_id = rp.role_id
#     WHERE rp.submenu_id = 3
#     AND rp.role_id IN (4,12,10,2,3,1)
#     """)

#     roles = db.execute(users_query).mappings().all()


#     return {
#         "incidents": incidents,
#         "role_based_users": [dict(role) for role in roles]
#     }




# def get_incidents_by_user(db: Session, user_id: int):

#     incident_query = text("""
#         SELECT 
#             ir.*,

#             json_build_object(
#                 'station_id', st.station_id,
#                 'station_name', st.station_name
#             ) AS station,

#             row_to_json(ia) AS impact_assessment,
#             row_to_json(ca) AS cause_analysis,
#             row_to_json(ip) AS incident_prevention,


#             -- ✅ SIC FROM ROLE_PERMISSION
#             (
#                 SELECT u.user_id
#                 FROM role_permissions rp
#                 JOIN users u
#                     ON u.user_id = rp.user_id

#                 WHERE rp.role_id = 2
#                 AND rp.submenu_id = 3
#                 AND u.station_id = st.station_id
#                 AND u.is_deleted = FALSE

#                 LIMIT 1
#             ) AS sic,


#             -- OTHER ROLES
#             role_map.role_users


#         FROM incident_report ir

#         LEFT JOIN station st
#             ON ir.station = st.station_id
#             AND st.is_deleted = FALSE

#         LEFT JOIN incident_impact_assessment ia
#             ON ir.incident_id = ia.incident_id

#         LEFT JOIN incident_cause_analysis ca
#             ON ir.incident_id = ca.incident_id

#         LEFT JOIN incident_prevention ip
#             ON ir.incident_id = ip.incident_id


#         LEFT JOIN LATERAL (

#             SELECT json_object_agg(
#                 LOWER(REPLACE(t.role_name,' ','_')),
#                 t.user_ids
#             ) AS role_users

#             FROM (
#                 SELECT 
#                     r.role_name,
#                     array_agg(u.user_id) AS user_ids
#                 FROM role_permissions rp
#                 JOIN roles r 
#                     ON r.role_id = rp.role_id
#                 JOIN users u 
#                     ON u.user_id = rp.user_id

#                 WHERE rp.submenu_id = 3
#                 AND rp.role_id IN (4,12,10,3,1)
#                 AND u.station_id = st.station_id

#                 GROUP BY r.role_name
#             ) t

#         ) role_map ON TRUE


#         WHERE ir.created_by = :user_id
#         ORDER BY ir.created_at DESC
#     """)

#     rows = db.execute(incident_query, {"user_id": user_id}).mappings().all()

#     incidents = []

#     for row in rows:
#         incident = dict(row)

#         incident["station"] = row["station"]
#         incident["impact_assessment"] = row["impact_assessment"]
#         incident["cause_analysis"] = row["cause_analysis"]
#         incident["incident_prevention"] = row["incident_prevention"]

#         incident["sic"] = row["sic"]

#         if row["role_users"]:
#             incident.update(row["role_users"])

#         incident.pop("role_users", None)

#         incidents.append(incident)

#     return {"data": incidents}

from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_incidents_by_user(db: Session, user_id: int):

    # ✅ Get user's role + station (kept for role_users/sic population)
    role_query = text("""
        SELECT rp.role_id, u.station_id
        FROM role_permissions rp
        JOIN users u
            ON u.user_id = rp.user_id
        WHERE rp.user_id = :user_id
        AND rp.submenu_id = 3
        AND u.is_deleted = FALSE
    """)

    role_rows = db.execute(role_query, {"user_id": user_id}).fetchall()

    role_ids = [r.role_id for r in role_rows]
    station_id = role_rows[0].station_id if role_rows else None

    # ✅ ALL users can see ALL reports — no restriction
    where_condition = "1=1"
    params = {}

    # =========================================================
    # MAIN QUERY
    # =========================================================
    incident_query = text(f"""
        SELECT 
            ir.*,

            TRIM(
                CONCAT(
                    COALESCE(u_creator.first_name, ''),
                    ' ',
                    COALESCE(u_creator.last_name, '')
                )
            ) AS reported_by_name,

            json_build_object(
                'station_id', st.station_id,
                'station_name', st.station_name
            ) AS station,

            row_to_json(ia) AS impact_assessment,
            row_to_json(ca) AS cause_analysis,
            row_to_json(ip) AS incident_prevention,

            iteam.leader_user_id,
            iteam.team_user_ids,

            (
                SELECT u.user_id
                FROM role_permissions rp
                JOIN users u
                    ON u.user_id = rp.user_id
                WHERE rp.role_id = 2
                AND rp.submenu_id = 3
                AND u.station_id = st.station_id
                AND u.is_deleted = FALSE
                LIMIT 1
            ) AS sic,

            role_map.role_users

        FROM incident_report ir

        LEFT JOIN users u_creator
            ON u_creator.user_id = ir.created_by
            AND u_creator.is_deleted = FALSE

        LEFT JOIN station st
            ON ir.station = st.station_id
            AND st.is_deleted = FALSE

        LEFT JOIN incident_impact_assessment ia
            ON ir.incident_id = ia.incident_id

        LEFT JOIN incident_cause_analysis ca
            ON ir.incident_id = ca.incident_id

        LEFT JOIN incident_prevention ip
            ON ir.incident_id = ip.incident_id

        LEFT JOIN (
            SELECT 
                prevention_id,
                MAX(CASE WHEN is_leader = TRUE THEN user_id END) AS leader_user_id,
                json_agg(user_id) FILTER (WHERE is_member = TRUE) AS team_user_ids
            FROM incident_investigation_team
            GROUP BY prevention_id
        ) iteam
            ON ip.ip_id = iteam.prevention_id

        LEFT JOIN LATERAL (
            SELECT json_object_agg(
                LOWER(REPLACE(t.role_name,' ','_')),
                t.user_ids
            ) AS role_users
            FROM (
                SELECT 
                    r.role_name,
                    array_agg(u.user_id) AS user_ids
                FROM role_permissions rp
                JOIN roles r ON r.role_id = rp.role_id
                JOIN users u ON u.user_id = rp.user_id
                WHERE rp.submenu_id = 3
                AND rp.role_id IN (4,12,10,3,1,2)
                AND u.station_id = st.station_id
                GROUP BY r.role_name
            ) t
        ) role_map ON TRUE

        WHERE {where_condition}
        ORDER BY ir.created_at DESC, ir.incident_id DESC
    """)

    rows = db.execute(incident_query, params).mappings().all()

    # =========================================================
    # RESPONSE BUILD
    # =========================================================
    incidents = []

    for row in rows:
        incident = dict(row)
        incident_id = incident["incident_id"]

        incident["reported_by_name"] = row["reported_by_name"]

        # -----------------------------------------------------
        # Prevention URL fix
        # -----------------------------------------------------
        incident_prevention = row["incident_prevention"]

        if incident_prevention:
            incident_prevention = dict(incident_prevention)

            if incident_prevention.get("minor_evidence_document_path"):
                incident_prevention["minor_evidence_document_url"] = build_file_url(
                    incident_prevention.get("minor_evidence_document_path")
                )

            if incident_prevention.get("major_evidence_document_path"):
                incident_prevention["major_evidence_document_url"] = build_file_url(
                    incident_prevention.get("major_evidence_document_path")
                )

        incident["incident_prevention"] = incident_prevention

        # =====================================================
        # INVESTIGATION BLOCK
        # =====================================================
        investigation = db.execute(
            text("""
                SELECT 
                    hiim.*,
                    u.user_id AS allotted_to_user_id,
                    TRIM(CONCAT(
                        COALESCE(u.first_name,''),' ',
                        COALESCE(u.last_name,'')
                    )) AS allotted_to_user_name,
                    u.designation AS allotted_to_user_designation
                FROM hse_incident_investigation_master hiim
                LEFT JOIN users u
                    ON u.user_id = hiim.allotted_to_name
                    AND u.is_deleted = FALSE
                WHERE hiim.incident_id = :incident_id
            """),
            {"incident_id": incident_id}
        ).mappings().first()

        if investigation:
            investigation = dict(investigation)

            if investigation.get("annexure_files"):
                investigation["annexure_files_url"] = build_file_url(
                    investigation.get("annexure_files")
                )

            hiim_id = investigation["hiim_id"]

            rca_rows = db.execute(
                text("""
                    SELECT *
                    FROM hse_incident_rca_5why
                    WHERE hiim_id = :hiim_id
                    ORDER BY rca_id ASC
                """),
                {"hiim_id": hiim_id}
            ).mappings().all()

            capa_rows = db.execute(
                text("""
                    SELECT *
                    FROM hse_incident_capa_actions
                    WHERE incident_id = :hiim_id
                    ORDER BY capa_id ASC
                """),
                {"hiim_id": hiim_id}
            ).mappings().all()

            # CAPA REPORT
            capa_report = db.execute(
                text("""
                    SELECT *
                    FROM capa_report
                    WHERE incident_id = :incident_id
                    ORDER BY capa_report_id DESC
                    LIMIT 1
                """),
                {"incident_id": incident_id}
            ).mappings().first()

            capa_report_data = None

            if capa_report:
                capa_report_id = capa_report["capa_report_id"]

                doc_changes = db.execute(
                    text("""
                        SELECT *
                        FROM capa_document_change
                        WHERE capa_id = :capa_report_id
                        ORDER BY capa_doc_id ASC
                    """),
                    {"capa_report_id": capa_report_id}
                ).mappings().all()

                for d in doc_changes:
                    if d.get("document_path"):
                        d["document_url"] = build_file_url(d.get("document_path"))

                capa_report_data = {
                    **capa_report,
                    "document_changes": doc_changes
                }

            # =====================================================
            # FTA STRUCTURE
            # =====================================================
            fta_top_rows = db.execute(
                text("""
                    SELECT *
                    FROM fta_top_event
                    WHERE hiim_id = :hiim_id
                    ORDER BY fta_top_id ASC
                """),
                {"hiim_id": hiim_id}
            ).mappings().all()

            fta_top_list = []

            for top in fta_top_rows:
                top_dict = dict(top)
                top_event_id = top_dict["fta_top_id"]

                intermediate_rows = db.execute(
                    text("""
                        SELECT *
                        FROM fta_intermediate_event
                        WHERE top_event_id = :top_event_id
                        ORDER BY intermediate_event_id ASC
                    """),
                    {"top_event_id": top_event_id}
                ).mappings().all()

                intermediate_list = []

                for inter in intermediate_rows:
                    inter_dict = dict(inter)
                    intermediate_event_id = inter_dict["intermediate_event_id"]

                    basic_rows = db.execute(
                        text("""
                            SELECT *
                            FROM fta_basic_event
                            WHERE intermediate_event_id = :intermediate_event_id
                            ORDER BY fte_basic_id ASC
                        """),
                        {"intermediate_event_id": intermediate_event_id}
                    ).mappings().all()

                    inter_dict["basic_events"] = [dict(b) for b in basic_rows]
                    intermediate_list.append(inter_dict)

                top_dict["intermediate_events"] = intermediate_list
                fta_top_list.append(top_dict)

            investigation["rca_5why"] = rca_rows
            investigation["capa_actions"] = capa_rows
            investigation["capa_report"] = capa_report_data
            investigation["fta_structure"] = fta_top_list

            incident["investigation"] = investigation
        else:
            incident["investigation"] = None

        # -----------------------------------------------------
        # Other fields
        # -----------------------------------------------------
        incident["leader_user_id"] = row["leader_user_id"]
        incident["team_user_ids"] = row["team_user_ids"]
        incident["sic"] = row["sic"]

        if row["role_users"]:
            incident.update(row["role_users"])

        incident.pop("role_users", None)

        incidents.append(incident)

    return {"data": incidents}




from sqlalchemy import text
from sqlalchemy.orm import Session


# def get_incident_by_id(db: Session, incident_id: int):

#     query = text("""
#         SELECT 
#             ir.*,

#             json_build_object(
#                 'station_id', st.station_id,
#                 'station_name', st.station_name
#             ) AS station,

#             row_to_json(ia) AS impact_assessment,
#             row_to_json(ca) AS cause_analysis,
#             row_to_json(ip) AS incident_prevention,


#             -- ✅ SIC FROM ROLE_PERMISSION
#             (
#                 SELECT u.user_id
#                 FROM role_permissions rp
#                 JOIN users u
#                     ON u.user_id = rp.user_id

#                 WHERE rp.role_id = 2
#                 AND rp.submenu_id = 3
#                 AND u.station_id = st.station_id
#                 AND u.is_deleted = FALSE

#                 LIMIT 1
#             ) AS sic,


#             -- ✅ OTHER ROLES
#             role_map.role_users


#         FROM incident_report ir

#         LEFT JOIN station st
#             ON ir.station = st.station_id
#             AND st.is_deleted = FALSE

#         LEFT JOIN incident_impact_assessment ia
#             ON ir.incident_id = ia.incident_id

#         LEFT JOIN incident_cause_analysis ca
#             ON ir.incident_id = ca.incident_id

#         LEFT JOIN incident_prevention ip
#             ON ir.incident_id = ip.incident_id


#         LEFT JOIN LATERAL (

#             SELECT json_object_agg(
#                 LOWER(REPLACE(t.role_name,' ','_')),
#                 t.user_ids
#             ) AS role_users

#             FROM (
#                 SELECT 
#                     r.role_name,
#                     array_agg(u.user_id) AS user_ids
#                 FROM role_permissions rp
#                 JOIN roles r 
#                     ON r.role_id = rp.role_id
#                 JOIN users u 
#                     ON u.user_id = rp.user_id

#                 WHERE rp.submenu_id = 3
#                 AND rp.role_id IN (4,12,10,3,1)
#                 AND u.station_id = st.station_id

#                 GROUP BY r.role_name
#             ) t

#         ) role_map ON TRUE


#         WHERE ir.incident_id = :incident_id
#     """)

#     row = db.execute(query, {"incident_id": incident_id}).mappings().first()

#     if not row:
#         return {"message": "Incident not found"}

#     incident = dict(row)

#     incident["station"] = row["station"]
#     incident["impact_assessment"] = row["impact_assessment"]
#     incident["cause_analysis"] = row["cause_analysis"]
#     incident["incident_prevention"] = row["incident_prevention"]

#     incident["sic"] = row["sic"]

#     if row["role_users"]:
#         incident.update(row["role_users"])

#     incident.pop("role_users", None)

#     return {
#         "data": incident
#     }
def get_incident_by_id(db: Session, incident_id: int):

    # -------------------------------------------------
    # 1️⃣ INCIDENT MAIN QUERY
    # -------------------------------------------------
    query = text("""
        SELECT 
            ir.*,

            TRIM(
                CONCAT(
                    COALESCE(u_creator.first_name, ''),
                    ' ',
                    COALESCE(u_creator.last_name, '')
                )
            ) AS created_by_name,

            json_build_object(
                'station_id', st.station_id,
                'station_name', st.station_name
            ) AS station,

            row_to_json(ia) AS impact_assessment,
            row_to_json(ca) AS cause_analysis,
            row_to_json(ip) AS incident_prevention,

            (
                SELECT array_agg(u.user_id)
                FROM role_permissions rp
                JOIN users u
                    ON u.user_id = rp.user_id
                WHERE rp.role_id = 2
                AND rp.submenu_id = 3
                AND u.station_id = ir.station
                AND u.is_deleted = FALSE
            ) AS sic,

            (
                SELECT array_agg(u.user_id)
                FROM role_permissions rp
                JOIN users u
                    ON u.user_id = rp.user_id
                WHERE rp.role_id = 13
                AND u.station_id = ir.station
                AND u.is_deleted = FALSE
            ) AS safety_officer,

            iteam.leader_user_id,
            iteam.team_user_ids,

            role_map.role_users

        FROM incident_report ir

        LEFT JOIN station st
            ON ir.station = st.station_id
            AND st.is_deleted = FALSE

        LEFT JOIN users u_creator
            ON u_creator.user_id = ir.created_by
            AND u_creator.is_deleted = FALSE

        LEFT JOIN incident_impact_assessment ia
            ON ir.incident_id = ia.incident_id

        LEFT JOIN incident_cause_analysis ca
            ON ir.incident_id = ca.incident_id

        LEFT JOIN incident_prevention ip
            ON ir.incident_id = ip.incident_id

        LEFT JOIN (
            SELECT 
                prevention_id,
                MAX(CASE WHEN is_leader = TRUE THEN user_id END) AS leader_user_id,
                json_agg(user_id) FILTER (WHERE is_member = TRUE) AS team_user_ids
            FROM incident_investigation_team
            GROUP BY prevention_id
        ) iteam
            ON ip.ip_id = iteam.prevention_id

        LEFT JOIN LATERAL (
            SELECT json_object_agg(
                LOWER(REPLACE(t.role_name,' ','_')),
                t.user_ids
            ) AS role_users
            FROM (
                SELECT 
                    r.role_name,
                    array_agg(u.user_id) AS user_ids
                FROM role_permissions rp
                JOIN roles r ON r.role_id = rp.role_id
                JOIN users u ON u.user_id = rp.user_id
                WHERE rp.submenu_id = 3
                AND rp.role_id IN (4,12,10,3,1)
                AND u.station_id = ir.station
                GROUP BY r.role_name
            ) t
        ) role_map ON TRUE

        WHERE ir.incident_id = :incident_id
    """)

    row = db.execute(query, {"incident_id": incident_id}).mappings().first()

    if not row:
        return {"message": "Incident not found"}

    incident = dict(row)

    incident["station"] = row["station"]
    incident["impact_assessment"] = row["impact_assessment"]
    incident["cause_analysis"] = row["cause_analysis"]

    # 🔥 INCIDENT PREVENTION URL FIX
    incident_prevention = row["incident_prevention"]

    if incident_prevention:
        incident_prevention = dict(incident_prevention)

        if incident_prevention.get("minor_evidence_document_path"):
            incident_prevention["minor_evidence_document_url"] = build_file_url(
                incident_prevention.get("minor_evidence_document_path")
            )

        if incident_prevention.get("major_evidence_document_path"):
            incident_prevention["major_evidence_document_url"] = build_file_url(
                incident_prevention.get("major_evidence_document_path")
            )

    incident["incident_prevention"] = incident_prevention

    incident["sic"] = row["sic"] or []
    incident["safety_officer"] = row["safety_officer"] or []
    incident["leader_user_id"] = row["leader_user_id"]
    incident["team_user_ids"] = row["team_user_ids"] or []
    incident["created_by_name"] = row["created_by_name"]

    if row["role_users"]:
        incident.update(row["role_users"])

    incident.pop("role_users", None)

    # -------------------------------------------------
    # 2️⃣ RESOLVE LEADER + TEAM USER NAMES
    # -------------------------------------------------
    leader_id = incident.get("leader_user_id")
    team_ids = incident.get("team_user_ids") or []

    all_user_ids = []
    if leader_id:
        all_user_ids.append(leader_id)
    all_user_ids.extend(team_ids)

    if all_user_ids:
        user_rows = db.execute(
            text("""
                SELECT 
                    user_id,
                    TRIM(CONCAT(
                        COALESCE(first_name, ''),
                        ' ',
                        COALESCE(last_name, '')
                    )) AS full_name,
                    designation
                FROM users
                WHERE user_id = ANY(:user_ids)
                AND is_deleted = FALSE
            """),
            {"user_ids": all_user_ids}
        ).mappings().all()

        user_map = {row["user_id"]: dict(row) for row in user_rows}

        incident["leader_user"] = user_map.get(leader_id) if leader_id else None
        incident["team_users"] = [
            user_map[uid] for uid in team_ids if uid in user_map
        ]
    else:
        incident["leader_user"] = None
        incident["team_users"] = []

    # -------------------------------------------------
    # 3️⃣ FETCH INVESTIGATION MASTER
    # -------------------------------------------------
    investigation = db.execute(
        text("""
            SELECT 
                hiim.*,

                u.user_id AS allotted_to_user_id,
                TRIM(
                    CONCAT(
                        COALESCE(u.first_name, ''),
                        ' ',
                        COALESCE(u.last_name, '')
                    )
                ) AS allotted_to_user_name,
                u.designation AS allotted_to_user_designation

            FROM hse_incident_investigation_master hiim
            LEFT JOIN users u
                ON u.user_id = hiim.allotted_to_name
                AND u.is_deleted = FALSE

            WHERE hiim.incident_id = :incident_id
        """),
        {"incident_id": incident_id}
    ).mappings().first()

    if investigation:

        investigation = dict(investigation)

        if investigation.get("annexure_files"):
            investigation["annexure_files_url"] = build_file_url(
                investigation.get("annexure_files")
            )

        hiim_id = investigation["hiim_id"]

        # -------------------------------------------------
        # 4️⃣ RCA
        # -------------------------------------------------
        rca_rows = db.execute(
            text("""
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
                WHERE hiim_id = :hiim_id
                ORDER BY rca_id ASC
            """),
            {"hiim_id": hiim_id}
        ).mappings().all()

        # -------------------------------------------------
        # 5️⃣ CAPA ACTIONS
        # -------------------------------------------------
        capa_rows = db.execute(
            text("""
                SELECT
                    capa_id,
                    incident_id,
                    action,
                    action_type,
                    target_date
                FROM hse_incident_capa_actions
                WHERE incident_id = :hiim_id
                ORDER BY capa_id ASC
            """),
            {"hiim_id": hiim_id}
        ).mappings().all()

        # -------------------------------------------------
        # 6️⃣ CAPA REPORT
        # -------------------------------------------------
        capa_report = db.execute(
            text("""
                SELECT *
                FROM capa_report
                WHERE incident_id = :incident_id
                ORDER BY capa_report_id DESC
                LIMIT 1
            """),
            {"incident_id": incident_id}
        ).mappings().first()

        capa_report_data = None

        if capa_report:
            capa_report_id = capa_report["capa_report_id"]

            doc_changes = db.execute(
                text("""
                    SELECT *
                    FROM capa_document_change
                    WHERE capa_id = :capa_report_id
                    ORDER BY capa_doc_id ASC
                """),
                {"capa_report_id": capa_report_id}
            ).mappings().all()

            for d in doc_changes:
                if d.get("document_path"):
                    d["document_url"] = build_file_url(d.get("document_path"))

            capa_report_data = {
                **capa_report,
                "document_changes": doc_changes
            }

        # =====================================================
        # 7️⃣ FTA STRUCTURE
        # =====================================================
        fta_top_rows = db.execute(
            text("""
                SELECT *
                FROM fta_top_event
                WHERE hiim_id = :hiim_id
                ORDER BY fta_top_id ASC
            """),
            {"hiim_id": hiim_id}
        ).mappings().all()

        fta_top_list = []

        for top in fta_top_rows:
            top_dict = dict(top)
            top_event_id = top_dict["fta_top_id"]

            intermediate_rows = db.execute(
                text("""
                    SELECT *
                    FROM fta_intermediate_event
                    WHERE top_event_id = :top_event_id
                    ORDER BY intermediate_event_id ASC
                """),
                {"top_event_id": top_event_id}
            ).mappings().all()

            intermediate_list = []

            for inter in intermediate_rows:
                inter_dict = dict(inter)
                intermediate_event_id = inter_dict["intermediate_event_id"]

                basic_rows = db.execute(
                    text("""
                        SELECT *
                        FROM fta_basic_event
                        WHERE intermediate_event_id = :intermediate_event_id
                        ORDER BY fte_basic_id ASC
                    """),
                    {"intermediate_event_id": intermediate_event_id}
                ).mappings().all()

                inter_dict["basic_events"] = [dict(b) for b in basic_rows]
                intermediate_list.append(inter_dict)

            top_dict["intermediate_events"] = intermediate_list
            fta_top_list.append(top_dict)

        # -------------------------------------------------
        # FINAL INVESTIGATION BLOCK
        # -------------------------------------------------
        incident["investigation"] = {
            **investigation,
            "rca_5why": rca_rows,
            "capa_actions": capa_rows,
            "capa_report": capa_report_data,
            "fta_structure": fta_top_list
        }

    else:
        incident["investigation"] = None

    # -------------------------------------------------
    # FINAL RESPONSE
    # -------------------------------------------------
    return {
        "data": incident
    }

