from datetime import datetime
import json
import os
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "files/hse/incident_prevention"
BASE_URL = os.getenv("BackEndPath")

def build_file_url(file_path):
    if not file_path:
        return None
    return f"{BASE_URL}/{file_path}"

# ALL DB FIELDS (IMPORTANT)
FIELDS = [
    "incident_id", "category", "status", "created_by", "updated_by",
    "was_incident_avoidable",

    "avoid_better_supervision", "avoid_imparting_training",
    "avoid_work_permit_system", "avoid_better_equipment",
    "avoid_maintenance_procedure", "avoid_other_information",
    "avoid_operating_procedure", "avoid_proper_planning_time",
    "avoid_ppe", "avoid_management_control", "avoid_inspection_testing",

    "minor_allotted_engineer_id",

    # MINOR
    "minor_prepared_by_name",
    "minor_prepared_by_designation",
    "minor_recommendations",
    "minor_engineer_corrective_actions_taken",
    "minor_prepared_by_corrective_action",
    "minor_corrective_actions",
    "minor_prepared_by_remarks",
    "minor_preventive_action_taken",
    "minor_alloted_engineer_name",
    "minor_alloted_engineer_designation",
    "minor_approved_by_name",
    "minor_approved_by_station_incharge",
    "minor_approved_by_remarks",
    "minor_evidence_document_path",
    "minor_evidence_documents_multi",       # ✅ NEW

    "minor_sic_name",
    "minor_sic_updated_date",
    "minor_alloted_eng_updated_date",
    "minor_final_approve_name",
    "minor_final_approved_date",

    # MAJOR
    "major_prepared_by_name",
    "major_prepared_by_designation",
    "major_immediate_actions_taken",
    "major_recommendations",
    "major_prepared_by_remarks_si",
    "major_hse_head_remarks",
    "major_evidence_document_path",
    "major_evidence_documents_multi",       # ✅ NEW

    "major_team_leader_by",
    "major_team_leader_date",
    "major_team_acknowledged_by",
    "major_team_acknowledged_date",
    "major_report_filled_by",
    "major_report_filled_date",
    "major_investigation_ack_by",
    "major_investigation_ack_date",
    "major_safety_officer_by",
    "major_safety_officer_date",
    "major_md_review_by",
    "major_md_review_date",
    "major_hse_review_by",
    "major_hse_review_date",
    "major_capa_filled_by",
    "major_capa_filled_date",
    "major_hse_capa_review_by",
    "major_hse_capa_review_date",
    "major_closure_by",
    "major_closure_date",
]

DATE_FIELDS = [
    "minor_sic_updated_date",
    "minor_alloted_eng_updated_date",
    "minor_final_approved_date",
    "major_team_leader_date",
    "major_team_acknowledged_date",
    "major_report_filled_date",
    "major_investigation_ack_date",
    "major_safety_officer_date",
    "major_md_review_date",
    "major_hse_review_date",
    "major_capa_filled_date",
    "major_hse_capa_review_date",
    "major_closure_date",
]

def parse_date_safe(val):
    if not val:
        return None
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, str):
        val = val.strip()
        if val == "" or val.lower() == "string":
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except:
            return None
    return val

def normalize(payload: dict) -> dict:
    return {k: payload.get(k) for k in FIELDS}


def get_incident_category(db: Session, incident_id: int) -> str:
    row = db.execute(
        text("SELECT category FROM incident_report WHERE incident_id=:id"),
        {"id": incident_id}
    ).fetchone()

    if not row or not row.category:
        raise HTTPException(status_code=400, detail="Invalid incident_id")

    return row.category


def save_file(file: UploadFile) -> str:
    """Save a single file and return its path."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    path = os.path.join(UPLOAD_DIR, f"{uuid4().hex}{ext}")
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path


def save_files_multi(files: list[UploadFile]) -> str:
    """
    Save multiple files and return a JSON-encoded list of paths.
    Stored in the DB column as:  '["path/a.pdf", "path/b.jpg"]'
    Returns None if files list is empty.
    """
    if not files:
        return None
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    paths = []
    for file in files:
        ext = os.path.splitext(file.filename)[1]
        path = os.path.join(UPLOAD_DIR, f"{uuid4().hex}{ext}")
        with open(path, "wb") as f:
            f.write(file.file.read())
        paths.append(path)
    return json.dumps(paths)


def build_file_urls_multi(json_paths: str | None) -> list[str]:
    """Convert the stored JSON path list into a list of full URLs."""
    if not json_paths:
        return []
    try:
        paths = json.loads(json_paths)
        return [build_file_url(p) for p in paths if p]
    except Exception:
        return []


def filter_by_category(payload: dict, category: str) -> dict:
    if category == "Minor":
        return {k: v for k, v in payload.items() if not k.startswith("major_")}
    if category == "Major":
        return {k: v for k, v in payload.items() if not k.startswith("minor_")}
    return payload


# =========================
# CREATE
# =========================
def create_incident_prevention(
    db: Session,
    payload: dict,
    minor_file: UploadFile | None,
    major_file: UploadFile | None,
    minor_files_multi: list[UploadFile] | None = None,   # ✅ NEW
    major_files_multi: list[UploadFile] | None = None,   # ✅ NEW
):
    # =========================
    # Get category
    # =========================
    category = get_incident_category(db, payload["incident_id"])
    payload["category"] = category

    # =========================
    # File handling — single (existing, unchanged)
    # =========================
    if category == "Minor" and minor_file:
        payload["minor_evidence_document_path"] = save_file(minor_file)

    if category == "Major" and major_file:
        payload["major_evidence_document_path"] = save_file(major_file)

    # =========================
    # File handling — multiple (NEW)
    # =========================
    if category == "Minor" and minor_files_multi:
        payload["minor_evidence_documents_multi"] = save_files_multi(minor_files_multi)

    if category == "Major" and major_files_multi:
        payload["major_evidence_documents_multi"] = save_files_multi(major_files_multi)

    # =========================
    # Filter by category
    # =========================
    payload = filter_by_category(payload, category)

    # =========================
    # Normalize (only DB fields)
    # =========================
    payload = normalize(payload)

    # remove None values (important)
    payload = {k: v for k, v in payload.items() if v is not None}

    # =========================
    # INSERT
    # =========================
    columns = ", ".join(payload.keys())
    values = ", ".join([f":{k}" for k in payload.keys()])

    sql = text(f"""
        INSERT INTO incident_prevention ({columns})
        VALUES ({values})
        RETURNING ip_id
    """)

    res = db.execute(sql, payload)
    db.commit()

    ip_id = res.scalar()

    # Fetch full record
    row = db.execute(
        text("SELECT * FROM incident_prevention WHERE ip_id = :id"),
        {"id": ip_id}
    ).mappings().first()

    return dict(row)


# =========================
# UPDATE
# =========================
def update_incident_prevention(
    db: Session,
    ip_id: int,
    payload: dict,
    minor_file: UploadFile | None,
    major_file: UploadFile | None,
    minor_files_multi: list[UploadFile] | None = None,   # ✅ NEW
    major_files_multi: list[UploadFile] | None = None,   # ✅ NEW
):
    # =========================
    # category
    # =========================
    category = get_incident_category(db, payload["incident_id"])

    # =========================
    # file handling — single (existing, unchanged)
    # =========================
    if category == "Minor" and minor_file:
        payload["minor_evidence_document_path"] = save_file(minor_file)

    if category == "Major" and major_file:
        payload["major_evidence_document_path"] = save_file(major_file)

    # =========================
    # file handling — multiple (NEW)
    # =========================
    if category == "Minor" and minor_files_multi:
        payload["minor_evidence_documents_multi"] = save_files_multi(minor_files_multi)

    if category == "Major" and major_files_multi:
        payload["major_evidence_documents_multi"] = save_files_multi(major_files_multi)

    # =========================
    # convert all date fields safely
    # =========================
    for f in DATE_FIELDS:
        if f in payload:
            payload[f] = parse_date_safe(payload.get(f))

    # =========================
    # filter by category
    # =========================
    payload = filter_by_category(payload, category)

    # never update incident_id
    payload.pop("incident_id", None)

    # remove None values
    payload = {k: v for k, v in payload.items() if v is not None}

    if not payload:
        return {"message": "Nothing to update"}

    payload["ip_id"] = ip_id

    set_clause = ", ".join([f"{k}=:{k}" for k in payload if k != "ip_id"])

    print("UPDATE DATA:", payload)

    sql = text(f"""
        UPDATE incident_prevention
        SET {set_clause},
            updated_at = NOW()
        WHERE ip_id = :ip_id
        RETURNING ip_id, status
    """)

    res = db.execute(sql, payload)
    updated_row = res.fetchone()
    db.commit()

    print("UPDATED ROW:", updated_row)

    if not updated_row:
        return {"error": "Row not found", "ip_id": ip_id}

    # RETURN STATUS + CATEGORY
    return {
        "ip_id": updated_row[0],
        "status": updated_row[1],
        "category": category
    }


# =========================
# GET ALL INCIDENT PREVENTION
# =========================
def get_all_incident_prevention(db: Session):

    sql = text("""
        SELECT
            ip.ip_id,
            ip.incident_id,
            ir.incident_no_during_year,
            ir.category,
            ip.status,

            ip.created_by AS created_by_user_id,

            CONCAT(
                COALESCE(u.first_name, ''),
                ' ',
                COALESCE(u.last_name, '')
            ) AS prepared_by_name,
            u.designation AS prepared_by_designation,
            u.station AS prepared_by_station,

            -- Minor workflow
            ip.minor_sic_name,
            ip.minor_sic_updated_date,
            ip.minor_alloted_engineer_name,
            ip.minor_alloted_eng_updated_date,
            ip.minor_final_approve_name,
            ip.minor_final_approved_date,

            -- Major workflow
            ip.major_team_leader_by,
            ip.major_team_leader_date,
            ip.major_team_acknowledged_by,
            ip.major_team_acknowledged_date,
            ip.major_report_filled_by,
            ip.major_report_filled_date,
            ip.major_investigation_ack_by,
            ip.major_investigation_ack_date,
            ip.major_safety_officer_by,
            ip.major_safety_officer_date,
            ip.major_md_review_by,
            ip.major_md_review_date,
            ip.major_hse_review_by,
            ip.major_hse_review_date,
            ip.major_capa_filled_by,
            ip.major_capa_filled_date,
            ip.major_hse_capa_review_by,
            ip.major_hse_capa_review_date,
            ip.major_closure_by,
            ip.major_closure_date,

            CASE
                WHEN ir.category = 'Minor'
                THEN ip.minor_evidence_document_path
                ELSE NULL
            END AS minor_evidence_document_path,

            CASE
                WHEN ir.category = 'Major'
                THEN ip.major_evidence_document_path
                ELSE NULL
            END AS major_evidence_document_path,

            -- ✅ NEW: multi-attachment columns
            CASE
                WHEN ir.category = 'Minor'
                THEN ip.minor_evidence_documents_multi
                ELSE NULL
            END AS minor_evidence_documents_multi,

            CASE
                WHEN ir.category = 'Major'
                THEN ip.major_evidence_documents_multi
                ELSE NULL
            END AS major_evidence_documents_multi,

            ip.created_at,
            ip.updated_at

        FROM incident_prevention ip
        JOIN incident_report ir
            ON ir.incident_id = ip.incident_id

        LEFT JOIN users u
            ON u.user_id::text = ip.created_by::text

        ORDER BY ip.created_at DESC, ip.ip_id DESC
        LIMIT 100
    """)

    rows = db.execute(sql).mappings().all()

    result = []

    for row in rows:
        row_dict = dict(row)

        # Single-file URLs (existing)
        row_dict["minor_evidence_document_url"] = build_file_url(
            row_dict.get("minor_evidence_document_path")
        )
        row_dict["major_evidence_document_url"] = build_file_url(
            row_dict.get("major_evidence_document_path")
        )

        # ✅ NEW: multi-file URL lists
        row_dict["minor_evidence_documents_multi_urls"] = build_file_urls_multi(
            row_dict.get("minor_evidence_documents_multi")
        )
        row_dict["major_evidence_documents_multi_urls"] = build_file_urls_multi(
            row_dict.get("major_evidence_documents_multi")
        )

        result.append(row_dict)

    return {
        "count": len(result),
        "data": result
    }


from datetime import date

def get_incident_dashboard_counts(
    db: Session,
    user_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    station_id: int | None = None,
    days: int | None = None,
):
    params = {}

    # Build station filter
    station_filter = ""
    if station_id is not None:
        station_filter = "AND ir.station = :station_id"
        params["station_id"] = station_id

    # Build date filter
    date_filter = ""
    if from_date and to_date:
        date_filter = "AND ir.date_of_incident BETWEEN :from_date AND :to_date"
        params["from_date"] = from_date
        params["to_date"] = to_date
    elif from_date:
        date_filter = "AND ir.date_of_incident >= :from_date"
        params["from_date"] = from_date
    elif to_date:
        date_filter = "AND ir.date_of_incident <= :to_date"
        params["to_date"] = to_date
    elif days is not None:
        from_date_calc = datetime.utcnow() - timedelta(days=days)
        date_filter = "AND ir.date_of_incident >= :from_date"
        params["from_date"] = from_date_calc

    sql = text(f"""
        SELECT
            COUNT(*) AS total_reported,

            COUNT(*) FILTER (
                WHERE LOWER(COALESCE(ip.status, '')) = 'closed'
            ) AS closed_incidents,

            COUNT(*) FILTER (
                WHERE LOWER(COALESCE(ip.status, '')) != 'closed'
            ) AS open_incidents,

            COUNT(*) FILTER (
                WHERE LOWER(COALESCE(ir.category, '')) = 'major'
            ) AS major_incidents,

            COUNT(*) FILTER (
                WHERE LOWER(COALESCE(ir.category, '')) = 'minor'
            ) AS minor_incidents

        FROM incident_prevention ip
        JOIN incident_report ir
            ON ir.incident_id = ip.incident_id

        WHERE 1=1
        {station_filter}
        {date_filter}
    """)

    row = db.execute(sql, params).mappings().first()

    total = row["total_reported"] or 0
    closed = row["closed_incidents"] or 0

    resolution_rate = round((closed / total) * 100, 2) if total > 0 else 0

    return {
        "total_reported": total,
        "open_incidents": row["open_incidents"] or 0,
        "closed_incidents": closed,
        "major_incidents": row["major_incidents"] or 0,
        "minor_incidents": row["minor_incidents"] or 0,
        "resolution_rate": resolution_rate
    }


from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session




def get_incident_dashboard_by_user(
    db: Session,
    user_id: int,
    filter_station_id: int = None,
    from_date: date | None = None,
    to_date: date | None = None,
    days: int | None = None,
):
    # Get user's role + station
    role_query = text("""
        SELECT rp.role_id, u.station_id
        FROM role_permissions rp
        JOIN users u ON u.user_id = rp.user_id
        WHERE rp.user_id = :user_id
        AND rp.submenu_id = 3
        AND u.is_deleted = FALSE
    """)

    role_rows = db.execute(role_query, {"user_id": user_id}).fetchall()

    role_ids = [r.role_id for r in role_rows]
    station_id = role_rows[0].station_id if role_rows else None

    params = {}

    if filter_station_id is not None:
        where_ir = "ir.station = :filter_station_id"
        where_ip = "ir2.station = :filter_station_id"
        params["filter_station_id"] = filter_station_id
    else:
        where_ir = "1=1"
        where_ip = "1=1"

    date_condition_ir = ""
    date_condition_ip = ""

    if from_date and to_date:
        date_condition_ir = " AND ir.date_of_incident BETWEEN :from_date AND :to_date"
        date_condition_ip = " AND ir2.date_of_incident BETWEEN :from_date AND :to_date"
        params["from_date"] = from_date
        params["to_date"] = to_date
    elif from_date:
        date_condition_ir = " AND ir.date_of_incident >= :from_date"
        date_condition_ip = " AND ir2.date_of_incident >= :from_date"
        params["from_date"] = from_date
    elif to_date:
        date_condition_ir = " AND ir.date_of_incident <= :to_date"
        date_condition_ip = " AND ir2.date_of_incident <= :to_date"
        params["to_date"] = to_date
    elif days is not None:
        from_date_calc = datetime.utcnow() - timedelta(days=days)
        params["from_date"] = from_date_calc
        date_condition_ir = " AND ir.date_of_incident >= :from_date"
        date_condition_ip = " AND ir2.date_of_incident >= :from_date"

    reported_vs_closed_sql = text(f"""
        SELECT
            COUNT(*) FILTER (
                WHERE LOWER(COALESCE(ip.status,'')) = 'closed'
            ) AS closed,
            COUNT(*) FILTER (
                WHERE LOWER(COALESCE(ip.status,'')) != 'closed'
            ) AS open
        FROM incident_prevention ip
        JOIN incident_report ir2
            ON ir2.incident_id = ip.incident_id
        WHERE {where_ip} {date_condition_ip}
    """)

    rvc = db.execute(reported_vs_closed_sql, params).mappings().first()

    incidents_by_type_sql = text(f"""
        SELECT
            LOWER(TRIM(ir.incident_type)) AS category,
            COUNT(*) AS count
        FROM incident_report ir
        WHERE {where_ir} {date_condition_ir}
        AND ir.incident_type IS NOT NULL
        GROUP BY LOWER(TRIM(ir.incident_type))
        ORDER BY category
    """)

    incidents_by_type = db.execute(
        incidents_by_type_sql, params
    ).mappings().all()

    open_closed_sql = text(f"""
        SELECT
            LOWER(ir.category) AS category,
            COUNT(*) FILTER (
                WHERE LOWER(COALESCE(ip.status,'')) = 'closed'
            ) AS closed,
            COUNT(*) FILTER (
                WHERE LOWER(COALESCE(ip.status,'')) != 'closed'
            ) AS open
        FROM incident_report ir
        JOIN incident_prevention ip
            ON ip.incident_id = ir.incident_id
        WHERE {where_ir} {date_condition_ir}
        AND LOWER(ir.category) IN ('major','minor')
        GROUP BY LOWER(ir.category)
        ORDER BY category
    """)

    open_closed_by_category = db.execute(
        open_closed_sql, params
    ).mappings().all()

    yearly_trend_sql = text(f"""
        SELECT
            TO_CHAR(ir.date_of_incident, 'Mon') AS month,
            EXTRACT(MONTH FROM ir.date_of_incident) AS month_no,
            COUNT(*) FILTER (
                WHERE LOWER(ir.category) = 'major'
            ) AS major,
            COUNT(*) FILTER (
                WHERE LOWER(ir.category) = 'minor'
            ) AS minor
        FROM incident_report ir
        WHERE {where_ir} {date_condition_ir}
        AND LOWER(ir.category) IN ('major','minor')
        AND ir.date_of_incident IS NOT NULL
        GROUP BY month, month_no
        ORDER BY month_no
    """)

    yearly_trend = db.execute(
        yearly_trend_sql, params
    ).mappings().all()

    return {
        "reported_vs_closed": {
            "closed": rvc["closed"] or 0,
            "open": rvc["open"] or 0,
        },
        "incidents_by_type": incidents_by_type,
        "open_closed_by_category": open_closed_by_category,
        "yearly_trend": {
            "data": yearly_trend
        }
    }