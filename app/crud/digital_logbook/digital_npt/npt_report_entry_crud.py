from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from app.schemas.digital_logbook.digital_npt.npt_report_entry_schema import (
    NPTReportEntryCreate,
    NPTReportEntryUpdate,
)

# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------


def _log_npt_entry_history(db: Session, record: dict, action: str, user_id: int = None):
    """
    Archives a snapshot of the NPT entry record.
    SQL Query matches original logic exactly.
    """
    history_data = dict(record)

    # Remove dynamic name resolution fields not current in history table schema
    history_data.pop("created_by_name", None)
    history_data.pop("updated_by_name", None)

    if "npt_master_id" in history_data:
        history_data["master_id"] = history_data.pop("npt_master_id")

    history_data["action_type"] = action
    
    # Track who triggered this history entry and when for DELETE actions
    # For UPDATE, we preserve the record's existing metadata for the snapshot
    if action == "DELETE":
        history_data["updated_at"] = datetime.now()
        history_data["updated_by"] = user_id if user_id else history_data.get("updated_by")

    cols = ", ".join(history_data.keys())
    vals = ", ".join([f":{k}" for k in history_data.keys()])

    history_query = text(
        f"INSERT INTO npt_report_entry_history ({cols}) VALUES ({vals})"
    )
    db.execute(history_query, history_data)


def _clean_npt_entry_params(params: dict) -> dict:
    """Standardizes dictionary keys and cleans signature whitespace."""
    if "npt_master_id" in params:
        params["master_id"] = params.pop("npt_master_id")

    params.pop("npe_id", None)

    if params.get("engg_sign"):
        params["engg_sign"] = params["engg_sign"].strip()

    return params


# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------


def get_entries_by_master_id(db: Session, master_id: int):
    """Fetch all entries belonging to a specific NPT Master record with robust name resolution."""
    query = text("""
        SELECT 
            npe.npe_id, npe.master_id as npt_master_id, npe.patrol_date, npe.start_time, npe.start_point, npe.end_time, npe.end_point, npe.team_member, npe.report_time, npe.point_at_reporting_time, npe.engg_sign, npe.remarks,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
             WHERE user_id = (CASE WHEN CAST(npe.created_by AS TEXT) ~ '^[0-9]+$' THEN CAST(npe.created_by AS INTEGER) ELSE NULL END)) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
             WHERE user_id = (CASE WHEN CAST(npe.updated_by AS TEXT) ~ '^[0-9]+$' THEN CAST(npe.updated_by AS INTEGER) ELSE NULL END)) as updated_by_name,
            COALESCE(npe.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(npe.created_by AS INTEGER), 0) as created_by, 
            COALESCE(npe.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(npe.updated_by AS INTEGER), 0) as updated_by
        FROM npt_report_entry npe
        WHERE npe.master_id = :mid 
        ORDER BY npe.report_time ASC
    """)
    return db.execute(query, {"mid": master_id}).mappings().all()


def get_npt_entry_by_id(db: Session, npe_id: int):
    """Fetch a single NPT entry by ID with robust name resolution."""
    query = text("""
        SELECT 
            npe.npe_id, npe.master_id as npt_master_id, npe.patrol_date, npe.start_time, npe.start_point, npe.end_time, npe.end_point, npe.team_member, npe.report_time, npe.point_at_reporting_time, npe.engg_sign, npe.remarks,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
             WHERE user_id = (CASE WHEN CAST(npe.created_by AS TEXT) ~ '^[0-9]+$' THEN CAST(npe.created_by AS INTEGER) ELSE NULL END)) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
             WHERE user_id = (CASE WHEN CAST(npe.updated_by AS TEXT) ~ '^[0-9]+$' THEN CAST(npe.updated_by AS INTEGER) ELSE NULL END)) as updated_by_name,
            COALESCE(npe.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(npe.created_by AS INTEGER), 0) as created_by, 
            COALESCE(npe.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(npe.updated_by AS INTEGER), 0) as updated_by
        FROM npt_report_entry npe
        WHERE npe.npe_id = :id
    """)
    return db.execute(query, {"id": npe_id}).mappings().first()


def create_npt_entry(db: Session, payload: NPTReportEntryCreate, user_id: int):
    """Create a new NPT report entry and return its ID."""
    data = payload.model_dump(exclude_unset=True)
    data = _clean_npt_entry_params(data)

    # Standardize audit fields
    data["created_by"] = data.get("created_by") or user_id
    data["updated_by"] = data.get("updated_by") or user_id
    data["created_at"] = data.get("created_at") or datetime.now()
    data["updated_at"] = data.get("updated_at") or datetime.now()

    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data.keys()])
    query = text(
        f"INSERT INTO npt_report_entry ({cols}) VALUES ({vals}) RETURNING npe_id"
    )

    result = db.execute(query, data)
    db.commit()
    return result.scalar()


def update_npt_entry(
    db: Session, npe_id: int, payload: NPTReportEntryUpdate, user_id: int
):
    """Update an NPT report entry and log history."""
    old_record = get_npt_entry_by_id(db, npe_id)
    if not old_record:
        return False

    _log_npt_entry_history(db, dict(old_record), "UPDATE", user_id=user_id)

    params = payload.model_dump(exclude_unset=True)
    params = _clean_npt_entry_params(params)

    if not params:
        db.commit()
        return True

    set_clause_parts = [f"{k} = :{k}" for k in params.keys()]
    update_params = {**params, "id": npe_id}

    if "updated_by" not in update_params:
        update_params["updated_by"] = user_id
        set_clause_parts.append("updated_by = :updated_by")

    if "updated_at" not in update_params:
        set_clause_parts.append("updated_at = CURRENT_TIMESTAMP")

    query = text(
        f"UPDATE npt_report_entry SET {', '.join(set_clause_parts)} WHERE npe_id = :id"
    )
    db.execute(query, update_params)
    db.commit()
    return True


def delete_npt_entry(db: Session, npe_id: int, user_id: int):
    """Delete an NPT report entry and archive to history."""
    old_record = get_npt_entry_by_id(db, npe_id)
    if not old_record:
        return False

    _log_npt_entry_history(db, dict(old_record), "DELETE", user_id=user_id)

    query = text("DELETE FROM npt_report_entry WHERE npe_id = :id")
    db.execute(query, {"id": npe_id})
    db.commit()
    return True
