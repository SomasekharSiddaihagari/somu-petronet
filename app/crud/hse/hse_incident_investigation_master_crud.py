import os
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "files/hse/investigation"


# -------------------------
# FILE SAVE
# -------------------------
def save_annexure_files(files: list[UploadFile] | None) -> str | None:
    if not files:
        return None

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    paths = []

    for f in files:
        ext = os.path.splitext(f.filename)[1]
        path = os.path.join(UPLOAD_DIR, f"{uuid4().hex}{ext}")
        with open(path, "wb") as out:
            out.write(f.file.read())
        paths.append(path)

    return ",".join(paths)


# -------------------------
# INCIDENT REF FETCH
# -------------------------
def get_incident_reference_no(db: Session, incident_id: int) -> str:
    row = db.execute(
        text("""
            SELECT incident_no_during_year
            FROM incident_report
            WHERE incident_id = :id
        """),
        {"id": incident_id}
    ).mappings().first()

    if not row or not row["incident_no_during_year"]:
        raise HTTPException(
            status_code=400,
            detail="Incident reference number not generated yet"
        )

    return row["incident_no_during_year"]


# =========================
# CREATE
# =========================
def create_investigation(
    db: Session,
    payload: dict,
    annexure_files: list[UploadFile] | None
):
    payload["incident_reference_no"] = get_incident_reference_no(
        db, payload["incident_id"]
    )

    payload["annexure_files"] = save_annexure_files(annexure_files)

    sql = text("""
        INSERT INTO hse_incident_investigation_master (
            incident_id, incident_reference_no, report_number,
            incident_date, incident_time, reporting_date,
            location_details, pipeline_name_section, reported_by,

            is_leak, is_spill, is_fire, is_explosion,
            is_injury, is_near_miss, is_other,

            severity_major, severity_minor, severity_near_miss,
            severity_unsafe_act, severity_unsafe_condition,
            severity_high_potential_near_miss,

            impact_on_people, impact_on_asset,
            environmental_impact, business_interruption,

            immediate_action_taken, statutory_management_intimation,
            incident_description, site_observations_evidence,
            immediate_causes, underlying_causes, root_causes,
            rca_tool_used,

            learning_recommendations, verification_closure,
            annexure_files,

            remarks_md, remarks_hse_head, remarks_station_incharge,
            allotted_to_name, allotted_to_designation,
            created_by,status
        )
        VALUES (
            :incident_id, :incident_reference_no, :report_number,
            :incident_date, :incident_time, :reporting_date,
            :location_details, :pipeline_name_section, :reported_by,

            :is_leak, :is_spill, :is_fire, :is_explosion,
            :is_injury, :is_near_miss, :is_other,

            :severity_major, :severity_minor, :severity_near_miss,
            :severity_unsafe_act, :severity_unsafe_condition,
            :severity_high_potential_near_miss,

            :impact_on_people, :impact_on_asset,
            :environmental_impact, :business_interruption,

            :immediate_action_taken, :statutory_management_intimation,
            :incident_description, :site_observations_evidence,
            :immediate_causes, :underlying_causes, :root_causes,
            :rca_tool_used,

            :learning_recommendations, :verification_closure,
            :annexure_files,

            :remarks_md, :remarks_hse_head, :remarks_station_incharge,
            :allotted_to_name, :allotted_to_designation,
            :created_by, :status
        )
        RETURNING hiim_id
    """)

    res = db.execute(sql, payload)
    db.commit()
    return {"hiim_id": res.scalar()}


# =========================
# UPDATE (SAFE)
# =========================
def update_investigation(
    db: Session,
    hiim_id: int,
    payload: dict,
    annexure_files: list[UploadFile] | None
):
    # ❌ never allow reference change
    payload.pop("incident_reference_no", None)
    payload.pop("incident_id", None)

    if annexure_files:
        payload["annexure_files"] = save_annexure_files(annexure_files)

    if not payload:
        return False

    payload["hiim_id"] = hiim_id

    set_clause = ", ".join([f"{k}=:{k}" for k in payload if k != "hiim_id"])

    sql = text(f"""
        UPDATE hse_incident_investigation_master
        SET {set_clause},
            updated_at = NOW()
        WHERE hiim_id = :hiim_id
    """)

    db.execute(sql, payload)
    db.commit()
    return True


# =========================
# GET ALL
# =========================
def get_all_investigations(db: Session):
    rows = db.execute(
        text("""
            SELECT *
            FROM hse_incident_investigation_master
            ORDER BY created_at DESC
        """)
    ).mappings().all()

    return {"count": len(rows), "data": rows}




# =========================
# GET BY ID (MASTER + CHILD)
# =========================
# =========================
# GET BY ID (MASTER + CHILD)
# =========================
def get_investigation_by_id(db: Session, hiim_id: int):
    try:
        # -------------------------------------------------
        # 1️⃣ Fetch master + user details
        # -------------------------------------------------
        master = db.execute(
            text("""
                SELECT 
                    hiim.*,

                    -- 👇 allotted user details
                    u.user_id AS allotted_to_user_id,
                    CONCAT(
                        COALESCE(u.first_name, ''),
                        ' ',
                        COALESCE(u.last_name, '')
                    ) AS allotted_to_user_name,
                    u.designation AS allotted_to_user_designation

                FROM hse_incident_investigation_master hiim
                LEFT JOIN users u
                    ON u.user_id = hiim.allotted_to_name

                WHERE hiim.hiim_id = :hiim_id
            """),
            {"hiim_id": hiim_id}
        ).mappings().first()

        if not master:
            raise HTTPException(
                status_code=404,
                detail="Investigation record not found"
            )

        # -------------------------------------------------
        # 2️⃣ Fetch RCA 5 WHY
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
        # 3️⃣ Fetch CAPA  ✅ FIXED
        # -------------------------------------------------
        # -------------------------------------------------
# 3️⃣ Fetch CAPA Actions
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
        # 4️⃣ Final response
        # -------------------------------------------------
        return {
            "data": {
                **master,
                "rca_5why": rca_rows,
                "capa_actions": capa_rows
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

