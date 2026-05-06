from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.hse.safety_committee_minutes_schema import SafetyCommitteeMinutesCreate, SafetyCommitteeMinutesUpdate
from datetime import date
from sqlalchemy.sql import text


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

def create_minutes(db: Session, data: SafetyCommitteeMinutesCreate):
    payload = data.model_dump()

    payload["updated_by"] = payload.get("created_by")

    # 🔥 AUTO GENERATE MEETING NUMBER
    meeting_no = generate_meeting_no(db, payload["created_by"])
    payload["meeting_no"] = meeting_no

    # 🔥 REQUIRED (fix for error)
    payload["is_active"] = True

    sql = text("""
        INSERT INTO safety_committee_minutes (
            meeting_no, location, frequency, meeting_date,
            next_meeting,
            station_id,
            created_by, updated_by
        ) VALUES (
            :meeting_no, :location, :frequency, :meeting_date,
            :next_meeting,
            :station_id,
            :created_by, :updated_by
        ) RETURNING scmm_id, meeting_no
    """)

    result = db.execute(sql, payload).fetchone()
    db.commit()

    return {
        "status": "success",
        "scmm_id": result.scmm_id,
        "meeting_no": result.meeting_no,
        "station_id": payload.get("station_id"),
        "message": "Minutes created successfully"
    }


# def get_minutes_by_id(db: Session, scmm_id: int):
#     sql = text("""
#         SELECT * FROM safety_committee_minutes WHERE scmm_id = :scmm_id
#     """)
#     result = db.execute(sql, {"scmm_id": scmm_id}).mappings().first()
#     return result

def get_all_minutes(db: Session):
    sql = text("""
        SELECT * FROM safety_committee_minutes ORDER BY created_at DESC
    """)
    result = db.execute(sql).mappings().all()
    return result

def update_minutes(db: Session, scmm_id: int, data: SafetyCommitteeMinutesUpdate):
    payload = data.model_dump(exclude_unset=True)
    if not payload:
        return {"message": "No fields to update"}

    set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])
    sql = text(f"""
        UPDATE safety_committee_minutes
        SET {set_clause}, updated_at = NOW()
        WHERE scmm_id = :scmm_id
    """)
    
    payload["scmm_id"] = scmm_id
    db.execute(sql, payload)
    db.commit()
    
    return {"message": "Minutes updated successfully"}

def delete_minutes(db: Session, scmm_id: int):
    sql = text("DELETE FROM safety_committee_minutes WHERE scmm_id = :scmm_id")
    db.execute(sql, {"scmm_id": scmm_id})
    db.commit()
    return {"message": "Minutes deleted successfully"}



# =========================
# GET BY ID (FULL FORM)
# =========================

# def get_minutes_by_id(db: Session, scmm_id: int):
#     # =====================================================
#     # 1️⃣ MASTER
#     # =====================================================
#     master = db.execute(
#         text("""
#             SELECT
#                 scmm_id,
#                 meeting_no,
#                 location,
#                 frequency,
#                 meeting_date,
#                 next_meeting,
#                 created_by,
#                 updated_by,
#                 created_at,
#                 updated_at
#             FROM safety_committee_minutes
#             WHERE scmm_id = :scmm_id
#         """),
#         {"scmm_id": scmm_id},
#     ).mappings().first()

#     if not master:
#         return {
#             "status": "error",
#             "message": "Minutes not found"
#         }

#     # =====================================================
#     # 2️⃣ MEMBERS  ✅ FIXED FK
#     # IMPORTANT: members.minutes_id → master.scmm_id
#     # =====================================================
#     members = db.execute(
#         text("""
#             SELECT
#                 scmm_id,
#                 minutes_id,
#                 member_name,
#                 created_by,
#                 updated_by,
#                 created_at,
#                 updated_at
#             FROM safety_committee_minutes_members
#             WHERE minutes_id = :minutes_id
#             ORDER BY scmm_id
#         """),
#         {"minutes_id": scmm_id},
#     ).mappings().all()

#     # =====================================================
#     # 3️⃣ DISCUSSIONS (FETCH EXISTING)
#     # =====================================================
#     discussion_rows = db.execute(
#         text("""
#             SELECT
#                 id,
#                 scmm_id,
#                 row_no,
#                 description_of_discussion,
#                 issues_discussed,
#                 action_taken,
#                 completed_on,
#                 action_by,
#                 target_date
#             FROM safety_committee_minutes_discussions
#             WHERE scmm_id = :scmm_id
#             ORDER BY row_no
#         """),
#         {"scmm_id": scmm_id},
#     ).mappings().all()

#     # =====================================================
#     # 4️⃣ BUILD FIXED 1–10 ROWS
#     # =====================================================
#     discussion_map = {row["row_no"]: row for row in discussion_rows}

#     discussions = []
#     for i in range(1, 11):
#         if i in discussion_map:
#             discussions.append(discussion_map[i])
#         else:
#             discussions.append({
#                 "id": None,
#                 "scmm_id": scmm_id,
#                 "row_no": i,
#                 "description_of_discussion": None,
#                 "issues_discussed": None,
#                 "action_taken": None,
#                 "completed_on": None,
#                 "action_by": None,
#                 "target_date": None,
#             })

#     # =====================================================
#     # ✅ FINAL RESPONSE
#     # =====================================================
#     return {
#         "status": "success",
#         "data": {
#             **master,
#             "members": members or [],  # 🔥 safe empty
#             "discussions": discussions,
#         }
#     }




def get_minutes_by_id(db: Session, scmm_id: int):
    # =====================================================
    # 1️⃣ MASTER
    # =====================================================
    master = db.execute(
        text("""
            SELECT
                scmm_id,
                meeting_no,
                location,
                frequency,
                meeting_date,
                next_meeting,
                station_id,
                created_by,
                updated_by,
                created_at,
                updated_at
            FROM safety_committee_minutes
            WHERE scmm_id = :scmm_id
        """),
        {"scmm_id": scmm_id},
    ).mappings().first()

    if not master:
        return {
            "status": "error",
            "message": "Minutes not found"
        }

    # =====================================================
    # 2️⃣ MEMBERS
    # =====================================================
    members = db.execute(
        text("""
            SELECT
                scmm_id,
                minutes_id,
                member_name,
                created_by,
                updated_by,
                created_at,
                updated_at
            FROM safety_committee_minutes_members
            WHERE minutes_id = :minutes_id
            ORDER BY scmm_id
        """),
        {"minutes_id": scmm_id},
    ).mappings().all()

    # =====================================================
    # 3️⃣ DISCUSSIONS (FETCH EXISTING)
    # =====================================================
    discussion_rows = db.execute(
        text("""
            SELECT
                id,
                scmm_id,
                row_no,
                description_of_discussion,
                issues_discussed,
                action_taken,
                completed_on,
                action_by,
                target_date
            FROM safety_committee_minutes_discussions
            WHERE scmm_id = :scmm_id
            ORDER BY row_no
        """),
        {"scmm_id": scmm_id},
    ).mappings().all()

    # =====================================================
    # 4️⃣ BUILD FIXED 1–10 ROWS
    # =====================================================
    discussion_map = {row["row_no"]: row for row in discussion_rows}

    discussions = []
    for i in range(1, 11):
        if i in discussion_map:
            discussions.append(discussion_map[i])
        else:
            discussions.append({
                "id": None,
                "scmm_id": scmm_id,
                "row_no": i,
                "description_of_discussion": None,
                "issues_discussed": None,
                "action_taken": None,
                "completed_on": None,
                "action_by": None,
                "target_date": None,
            })

    # =====================================================
    # 5️⃣ INCIDENT REPORTS BY STATION (ONLY "Open" STATUS)
    # =====================================================
    station_id = master["station_id"]

    incident_reports = []
    if station_id is not None:
        incident_reports = db.execute(
            text("""
                SELECT ir.*
                FROM incident_report ir
                INNER JOIN incident_prevention ip
                    ON ir.incident_id = ip.incident_id
                WHERE ir.station = :station_id
                  AND ip.status = 'Open'
            """),
            {"station_id": station_id},
        ).mappings().all()

    # =====================================================
    # ✅ FINAL RESPONSE
    # =====================================================
    return {
        "status": "success",
        "data": {
            **master,
            "members": members or [],
            "discussions": discussions,
            "incident_reports": [dict(row) for row in incident_reports],
        }
    }





