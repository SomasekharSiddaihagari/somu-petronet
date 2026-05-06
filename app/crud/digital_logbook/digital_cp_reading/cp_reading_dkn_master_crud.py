# app/crud/digital_logbook/digital_cp_reading/cp_reading_dkn_master_crud.py
from datetime import date, datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Any, Dict, Optional

from app.schemas.digital_logbook.digital_cp_reading.cp_reading_dkn_master_schema import (
    CPReadingDKNMasterCreate,
    CPReadingDKNMasterUpdate,
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_dkn_entry_crud import (
    get_dkn_entries_by_master_id,
)


# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------


def _clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove non-database fields from the payload."""
    exclude = ["cp_dkn_id", "entries"]
    for field in exclude:
        data.pop(field, None)
    return data


def _prepare_audit_fields(
    data: Dict[str, Any], user_id: int, is_update: bool = False
) -> Dict[str, Any]:
    """Maintain consistent audit fields across CRUD operations."""
    now = datetime.now()
    if not is_update:
        data["created_by"] = data.get("created_by") or user_id
        data["created_at"] = data.get("created_at") or now

    data["updated_by"] = data.get("updated_by") or user_id
    data["updated_at"] = data.get("updated_at") or now
    return data


def _log_history(db: Session, record: Dict[str, Any], action: str, user_id: int = None):
    """Archive a snapshot of the DKN master record."""
    history_data = dict(record)
    
    # Remove dynamic name fields and nested entries
    history_data.pop("created_by_name", None)
    history_data.pop("updated_by_name", None)
    history_data.pop("entries", None)

    if action == "DELETE":
        history_data["updated_at"] = datetime.now()
        history_data["updated_by"] = user_id if user_id else history_data.get("updated_by")

    cols = ", ".join(history_data.keys())
    vals = ", ".join([f":{k}" for k in history_data.keys()])

    query = text(f"INSERT INTO cp_reading_dkn_master_history ({cols}) VALUES ({vals})")
    db.execute(query, history_data)


def _process_dkn_result(db: Session, result):
    if not result:
        return None
    d = dict(result)

    created_at = d.get("created_at") or datetime.now()
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    t = created_at.time()

    s_a = time(7, 0)
    s_b = time(15, 0)
    s_c = time(23, 0)

    if s_a <= t < s_b:
        d["shift"] = d.get("shift") or "Shift A"
        d["station_in_charge"] = (d.get("station_in_charge") or "").strip()
        d["start_time"] = d.get("start_time") or s_a
    elif s_b <= t < s_c:
        d["shift"] = d.get("shift") or "Shift B"
        d["station_in_charge"] = (d.get("station_in_charge") or "").strip()
        d["start_time"] = d.get("start_time") or s_b
    else:
        d["shift"] = d.get("shift") or "Shift C"
        d["station_in_charge"] = (d.get("station_in_charge") or "").strip()
        d["start_time"] = d.get("start_time") or s_c

    d["entries"] = (
        get_dkn_entries_by_master_id(db, d["cp_dkn_id"]) if d.get("cp_dkn_id") else []
    )
    return d


# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------


def get_dkn_master_by_id(db: Session, dkn_id: int):
    """Retrieve a DKN master record with dynamic name resolution."""
    query = text(
        """
        SELECT 
            m.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.updated_by) as updated_by_name,
            COALESCE(m.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(m.created_by AS INTEGER), 0) as created_by, 
            COALESCE(m.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(m.updated_by AS INTEGER), 0) as updated_by,
            COALESCE(m.station, 'Devanagonthi') as station
        FROM cp_reading_dkn_master m
        WHERE m.cp_dkn_id = :id
    """
    )
    result = db.execute(query, {"id": dkn_id}).mappings().first()
    return _process_dkn_result(db, result)


def create_dkn_master(db: Session, payload: CPReadingDKNMasterCreate, user_id: int):
    data = payload.model_dump(exclude_unset=True)
    for field in ["cp_dkn_id", "entries"]:
        data.pop(field, None)

    # Use payload values if provided, otherwise fallback to defaults
    data["created_by"] = (
        user_id if data.get("created_by") is None else data["created_by"]
    )
    data["updated_by"] = (
        user_id if data.get("updated_by") is None else data["updated_by"]
    )
    data["created_at"] = data.get("created_at") or datetime.now()
    data["updated_at"] = data.get("updated_at") or datetime.now()

    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data.keys()])

    query = text(
        f"INSERT INTO cp_reading_dkn_master ({cols}) VALUES ({vals}) RETURNING cp_dkn_id"
    )
    result = db.execute(query, data)
    db.commit()
    return result.scalar()


def update_dkn_master(
    db: Session, dkn_id: int, payload: CPReadingDKNMasterUpdate, user_id: int
):
    """Update a DKN master record and log history snapshot."""
    old_record = get_dkn_master_by_id(db, dkn_id)
    if not old_record:
        return False
    
    _log_history(db, old_record, "UPDATE", user_id)

    data = payload.model_dump(exclude_unset=True)
    data = _clean_data(data)
    if not data:
        db.commit()
        return True

    data = _prepare_audit_fields(data, user_id, is_update=True)
    set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])

    query = text(f"UPDATE cp_reading_dkn_master SET {set_clause} WHERE cp_dkn_id = :id")
    db.execute(query, {**data, "id": dkn_id})
    db.commit()
    return True


def delete_dkn_master(db: Session, dkn_id: int, user_id: int):
    """Perform archival deletion of a DKN master record."""
    old_record = get_dkn_master_by_id(db, dkn_id)
    if not old_record:
        return False

    _log_history(db, old_record, "DELETE", user_id)

    db.execute(text("DELETE FROM cp_reading_dkn_master WHERE cp_dkn_id = :id"), {"id": dkn_id})
    db.commit()
    return True


def get_dkn_masters_by_date_range(db: Session, from_date: date, to_date: date):
    """Retrieve DKN master records within a date range with dynamic name resolution."""
    query = text(
        """
        SELECT m.*,
               (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.created_by) as created_by_name,
               (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.updated_by) as updated_by_name,
               COALESCE(m.created_at, CURRENT_TIMESTAMP) as created_at,
               COALESCE(CAST(m.created_by AS INTEGER), 0) as created_by,
               COALESCE(m.updated_at, CURRENT_TIMESTAMP) as updated_at,
               COALESCE(CAST(m.updated_by AS INTEGER), 0) as updated_by,
               COALESCE(m.station, 'Devanagonthi') as station
        FROM cp_reading_dkn_master m
        WHERE m.log_date >= :from_date
          AND m.log_date <= :to_date
          AND EXISTS (SELECT 1 FROM cp_reading_dkn_entry e WHERE e.master_id = m.cp_dkn_id)
        ORDER BY m.log_date DESC, m.cp_dkn_id DESC
    """
    )
    results = (
        db.execute(query, {"from_date": from_date, "to_date": to_date}).mappings().all()
    )
    return [_process_dkn_result(db, row) for row in results]
