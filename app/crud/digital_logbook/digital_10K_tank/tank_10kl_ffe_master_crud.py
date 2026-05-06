from datetime import date, datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Any, Dict

from app.schemas.digital_logbook.digital_10K_tank.tank_10kl_ffe_master_schema import (
    Tank10KLFfeCreate,
    Tank10KLFfeUpdate,
)
from app.crud.digital_logbook.digital_10K_tank.tank_10kl_ffe_entry_crud import (
    get_tank_10kl_ffe_entries_by_master_id,
)

# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------


def _clean_data(data: Dict[str, Any], extra_exclude: list = None) -> Dict[str, Any]:
    """Remove non-database fields from the payload."""
    exclude = ["tank_ffe_id", "entries"]
    if extra_exclude:
        exclude.extend(extra_exclude)
    for field in exclude:
        data.pop(field, None)
    return data


def _prepare_audit_fields(
    data: Dict[str, Any], user_id: int, is_update: bool = False
) -> Dict[str, Any]:
    """Populate audit fields like created_by, updated_by, and timestamps."""
    now = datetime.now()
    if not is_update:
        data["created_by"] = data.get("created_by") or user_id
        data["created_at"] = data.get("created_at") or now

    data["updated_by"] = data.get("updated_by") or user_id
    data["updated_at"] = data.get("updated_at") or now
    return data


def _build_insert_query(table_name: str, data: Dict[str, Any]):
    """Construct a dynamic INSERT statement."""
    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data.keys()])
    return text(
        f"INSERT INTO {table_name} ({cols}) VALUES ({vals}) RETURNING tank_ffe_id"
    )


def _build_update_query(table_name: str, data: Dict[str, Any], id_col: str):
    """Construct a dynamic UPDATE statement."""
    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    return text(f"UPDATE {table_name} SET {set_clause} WHERE {id_col} = :{id_col}")


def _log_history(
    db: Session, old_record: Dict[str, Any], action_type: str, user_id: int
):
    """Archive a snapshot of the master record into the history table."""
    history_data = {
        "tank_ffe_id": old_record.get("tank_ffe_id"),
        "station": old_record.get("station"),
        "station_in_charge": old_record.get("station_in_charge"),
        "shift": old_record.get("shift"),
        "start_time": old_record.get("start_time"),
        "logbook_date": old_record.get("logbook_date"),
        "status": old_record.get("status"),
        "ms_logbook_id": old_record.get("ms_logbook_id"),
        "technician_id": old_record.get("technician_id"),
        "sign_shift_a": old_record.get("sign_shift_a"),
        "sign_shift_b": old_record.get("sign_shift_b"),
        "sign_shift_c": old_record.get("sign_shift_c"),
        "sign_station_incharge": old_record.get("sign_station_incharge"),
        "name_shift_a": old_record.get("name_shift_a"),
        "name_shift_b": old_record.get("name_shift_b"),
        "name_shift_c": old_record.get("name_shift_c"),
        "name_station_incharge": old_record.get("name_station_incharge"),
        "created_at": old_record.get("created_at"),
        "created_by": old_record.get("created_by"),
        "updated_at": (
            datetime.now() if action_type == "DELETE" else old_record.get("updated_at")
        ),
        "updated_by": user_id if action_type == "DELETE" else old_record.get("updated_by"),
        "action_type": action_type,
    }

    history_query = text(
        """
        INSERT INTO tank_10kl_ffe_master_history (
            tank_ffe_id, station, station_in_charge, shift, start_time, logbook_date, status,
            ms_logbook_id, technician_id, sign_shift_a, sign_shift_b, sign_shift_c, sign_station_incharge,
            name_shift_a, name_shift_b, name_shift_c, name_station_incharge,
            created_at, created_by, updated_at, updated_by, action_type
        )
        VALUES (
            :tank_ffe_id, :station, :station_in_charge, :shift, :start_time, :logbook_date, :status,
            :ms_logbook_id, :technician_id, :sign_shift_a, :sign_shift_b, :sign_shift_c, :sign_station_incharge,
            :name_shift_a, :name_shift_b, :name_shift_c, :name_station_incharge,
            :created_at, :created_by, :updated_at, :updated_by, :action_type
        )
    """
    )
    db.execute(history_query, history_data)


def _process_tank_ffe_result(db: Session, result):
    """Apply business logic (shifts, times) and link nested entries."""
    if not result:
        return None

    d: dict[str, Any] = dict(result)

    # Dynamic shift calculation
    created_at = d.get("created_at") or datetime.now()
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

    t = created_at.time()
    s_a, s_b, s_c = time(7, 0), time(15, 0), time(23, 0)

    if s_a <= t < s_b:
        d["shift"] = d.get("shift") or "Shift A"
        d["start_time"] = d.get("start_time") or s_a
    elif s_b <= t < s_c:
        d["shift"] = d.get("shift") or "Shift B"
        d["start_time"] = d.get("start_time") or s_b
    else:
        d["shift"] = d.get("shift") or "Shift C"
        d["start_time"] = d.get("start_time") or s_c

    d["station_in_charge"] = (d.get("station_in_charge") or "").strip()

    if d.get("tank_ffe_id"):
        d["entries"] = get_tank_10kl_ffe_entries_by_master_id(db, d["tank_ffe_id"])
    else:
        d["entries"] = []

    return d


# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------


def get_tank_10kl_ffe_by_id(db: Session, tank_ffe_id: int):
    """Retrieve a single master record by ID with dynamic name resolution."""
    query = text(
        """
        SELECT 
            m.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.updated_by) as updated_by_name,
            COALESCE(CAST(m.technician_id AS INTEGER), 0) as technician_id, 
            COALESCE(m.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(m.created_by AS INTEGER), 0) as created_by, 
            COALESCE(m.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(m.updated_by AS INTEGER), 0) as updated_by
        FROM tank_10kl_ffe_master m
        WHERE m.tank_ffe_id = :id
    """
    )
    result = db.execute(query, {"id": tank_ffe_id}).mappings().first()
    return _process_tank_ffe_result(db, result)


def get_combined_tank_ffe_by_date(db: Session, from_date: date, to_date: date):
    """Fetch master records within a date range with dynamic name resolution."""
    query = text(
        """
        SELECT 
            m.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.updated_by) as updated_by_name,
            COALESCE(CAST(m.technician_id AS INTEGER), 0) as technician_id,
            COALESCE(m.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(m.created_by AS INTEGER), 0) as created_by, 
            COALESCE(m.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(m.updated_by AS INTEGER), 0) as updated_by
        FROM tank_10kl_ffe_master m
        WHERE CAST(m.logbook_date AS DATE) >= :from_date
          AND CAST(m.logbook_date AS DATE) <= :to_date
          AND EXISTS (
              SELECT 1 FROM tank_10kl_ffe_entry e WHERE e.master_id = m.tank_ffe_id
          )
        ORDER BY m.logbook_date DESC, m.tank_ffe_id DESC
    """
    )
    results = (
        db.execute(query, {"from_date": from_date, "to_date": to_date}).mappings().all()
    )
    return [_process_tank_ffe_result(db, row) for row in results]


def create_tank_10kl_ffe(db: Session, payload: Tank10KLFfeCreate, user_id: int):
    """Insert a new tank master record."""
    data = payload.model_dump(exclude_unset=True)
    data = _clean_data(data)
    data = _prepare_audit_fields(data, user_id)

    query = _build_insert_query("tank_10kl_ffe_master", data)
    result = db.execute(query, data)
    db.commit()
    return result.scalar()


def update_tank_10kl_ffe(
    db: Session, tank_ffe_id: int, payload: Tank10KLFfeUpdate, user_id: int
):
    """Update a master record and archive previous state to history."""
    old_record = get_tank_10kl_ffe_by_id(db, tank_ffe_id)
    if not old_record:
        return False

    _log_history(db, old_record, "UPDATE", user_id)

    data = payload.model_dump(exclude_unset=True)
    data = _clean_data(data)

    if not data:
        db.commit()
        return True

    data = _prepare_audit_fields(data, user_id, is_update=True)
    query = _build_update_query("tank_10kl_ffe_master", data, "tank_ffe_id")

    db.execute(query, {**data, "tank_ffe_id": tank_ffe_id})
    db.commit()
    return True


def delete_tank_10kl_ffe(db: Session, tank_ffe_id: int, user_id: int):
    """Remove a record from master and archive to history."""
    old_record = get_tank_10kl_ffe_by_id(db, tank_ffe_id)
    if not old_record:
        return False

    _log_history(db, old_record, "DELETE", user_id)

    query = text("DELETE FROM tank_10kl_ffe_master WHERE tank_ffe_id = :tank_ffe_id")
    result = db.execute(query, {"tank_ffe_id": tank_ffe_id})
    db.commit()

    return result.rowcount > 0
