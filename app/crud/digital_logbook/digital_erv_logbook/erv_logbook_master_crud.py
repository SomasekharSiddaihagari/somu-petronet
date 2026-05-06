from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, date, time, timedelta
from typing import List, Optional, Any
from app.schemas.digital_logbook.digital_erv_logbook.erv_logbook_master_schema import (
    ErvLogbookCreate,
    ErvLogbookUpdate,
)
from app.crud.digital_logbook.digital_erv_logbook.erv_vehicle_inspection_entry_crud import (
    get_erv_vehicle_entries_by_master_id,
)

# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------

def _process_erv_result(db: Session, result: Any) -> Optional[dict]:
    """
    Applies shift calculation logic and fetches associated entries for a master record.
    Behaves EXACTLY like the original process logic.
    """
    if not result:
        return None

    d: dict[str, Any] = dict(result)
    
    # Extract creation time for shift assignment
    created_at = d.get("created_at") or datetime.now()
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    t = created_at.time()

    # Fixed shift time intervals (Original Logic)
    s_a, s_b, s_c = time(7, 0), time(15, 0), time(23, 0)

    # Assign shift and default charge name based on time
    if s_a <= t < s_b:
        d["shift"] = d.get("shift") or "Shift A"
        d["station_in_charge"] = d.get("station_in_charge") or "STATION IN-CHARGE A"
        d["start_time"] = d.get("start_time") or s_a
    elif s_b <= t < s_c:
        d["shift"] = d.get("shift") or "Shift B"
        d["station_in_charge"] = d.get("station_in_charge") or "STATION IN-CHARGE B"
        d["start_time"] = d.get("start_time") or s_b
    else:
        d["shift"] = d.get("shift") or "Shift C"
        d["station_in_charge"] = d.get("station_in_charge") or "STATION IN-CHARGE C"
        d["start_time"] = d.get("start_time") or s_c

    # Attach child entries from the vehicle inspection table
    if d.get("erv_id"):
        d["entries"] = get_erv_vehicle_entries_by_master_id(db, d["erv_id"])
    else:
        d["entries"] = []

    return d

def _log_erv_master_history(db: Session, record: dict, action: str, user_id: Optional[int] = None):
    """
    Archives a snapshot of the ERV master record. 
    SQL Query remains identical to original logic.
    """
    history_data = {
        "erv_id": record["erv_id"],
        "station": record["station"],
        "shift_in_charge": record.get("shift_in_charge") or record.get("station_in_charge"),
        "shift": record["shift"],
        "start_time": record["start_time"],
        "logbook_date": record["logbook_date"],
        "ms_logbook_id": record["ms_logbook_id"],
        "technician_id": record["technician_id"],
        "created_at": record["created_at"],
        "created_by": record["created_by"],
        "updated_at": datetime.now() if action == "DELETE" else record["updated_at"],
        "updated_by": user_id if user_id else record["updated_by"],
        "action_type": action,
    }

    # Strict adherence to original manual SQL
    query = text("""
        INSERT INTO erv_logbook_master_history (
            erv_id, station, shift_in_charge, shift, start_time, logbook_date,
            ms_logbook_id, technician_id,  created_at,
            created_by, updated_at, updated_by, action_type
        )
        VALUES (
            :erv_id, :station, :shift_in_charge, :shift, :start_time, :logbook_date,
            :ms_logbook_id, :technician_id, :created_at,
            :created_by, :updated_at, :updated_by, :action_type
        )
    """)
    db.execute(query, history_data)

# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------

def get_all_erv_logbooks(db: Session):
    """Fetch all ERV logbook master records with original COALESCE logic."""
    query = text("""
        SELECT 
            e.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.updated_by) as updated_by_name,
            COALESCE(e.technician_id, 0) as technician_id,
            COALESCE(e.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(e.created_by AS INTEGER), 0) as created_by, 
            COALESCE(e.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(e.updated_by AS INTEGER), 0) as updated_by
        FROM erv_logbook_master e
        ORDER BY e.created_at DESC
    """)
    results = db.execute(query).mappings().all()
    return [_process_erv_result(db, row) for row in results]

def get_erv_logbook_by_id(db: Session, erv_id: int):
    """Fetches a single ERV record with original COALESCE logic."""
    query = text("""
        SELECT 
            e.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.updated_by) as updated_by_name,
            COALESCE(e.technician_id, 0) as technician_id,
            COALESCE(e.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(e.created_by AS INTEGER), 0) as created_by, 
            COALESCE(e.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(e.updated_by AS INTEGER), 0) as updated_by
        FROM erv_logbook_master e
        WHERE e.erv_id = :erv_id
    """)
    result = db.execute(query, {"erv_id": erv_id}).mappings().first()
    return _process_erv_result(db, result)

def get_combined_erv_by_date(db: Session, search_date: date):
    """Fetches all ERV logs for a specific shift date window."""
    start_dt = datetime.combine(search_date, time(7, 0))
    end_dt = start_dt + timedelta(days=1)

    query = text("""
        SELECT 
            e.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.updated_by) as updated_by_name,
            COALESCE(e.technician_id, 0) as technician_id,
            COALESCE(e.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(e.created_by AS INTEGER), 0) as created_by, 
            COALESCE(e.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(e.updated_by AS INTEGER), 0) as updated_by
        FROM erv_logbook_master e
        JOIN logbook_shift_master LSM ON e.ms_logbook_id = LSM.ms_logbook_id
        WHERE LSM.created_at >= :start_dt AND LSM.created_at < :end_dt
          AND e.created_at >= :start_dt AND e.created_at < :end_dt
        ORDER BY e.erv_id DESC
    """)

    results = db.execute(query, {"start_dt": start_dt, "end_dt": end_dt}).mappings().all()
    final_data = [_process_erv_result(db, row) for row in results]
    
    # Maintenance of original sort order
    final_data.sort(key=lambda x: (len(x.get("entries", [])) > 0, str(x.get("created_at"))), reverse=True)
    return final_data

def create_erv_logbook(db: Session, payload: ErvLogbookCreate, user_id: int):
    """Inserts record using original hardcoded insertion logic."""
    data = payload.model_dump(exclude_unset=True)
    for field in ["erv_id", "entries"]: 
        data.pop(field, None)

    # Manual audit field population (Original Logic)
    data["created_by"] = data.get("created_by") or user_id
    data["updated_by"] = data.get("updated_by") or user_id
    data["created_at"] = data.get("created_at") or datetime.now()
    data["updated_at"] = data.get("updated_at") or datetime.now()

    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data.keys()])
    query = text(f"INSERT INTO erv_logbook_master ({cols}) VALUES ({vals}) RETURNING erv_id")
    
    result = db.execute(query, data)
    db.commit()
    return result.scalar()

def update_erv_logbook(db: Session, erv_id: int, payload: ErvLogbookUpdate, user_id: int):
    """Updates record while preserving history tracking logic."""
    old_record = get_erv_logbook_by_id(db, erv_id)
    if not old_record: return False

    _log_erv_master_history(db, old_record, "UPDATE")

    data = payload.model_dump(exclude_unset=True)
    for field in ["erv_id", "entries"]: 
        data.pop(field, None)

    if not data:
        db.commit()
        return True

    # Manual SET clause construction as per original pattern
    set_clause_parts = [f"{key} = :{key}" for key in data.keys()]
    params = {**data, "erv_id": erv_id}

    if "updated_by" not in params:
        params["updated_by"] = user_id
        set_clause_parts.append("updated_by = :updated_by")

    if "updated_at" not in params:
        set_clause_parts.append("updated_at = CURRENT_TIMESTAMP")

    query = text(f"UPDATE erv_logbook_master SET {', '.join(set_clause_parts)} WHERE erv_id = :erv_id")
    db.execute(query, params)
    db.commit()
    return True

def delete_erv_logbook(db: Session, erv_id: int, user_id: int):
    """Performs an archival delete."""
    old_record = get_erv_logbook_by_id(db, erv_id)
    if not old_record: return False

    _log_erv_master_history(db, old_record, "DELETE", user_id=user_id)

    query = text("DELETE FROM erv_logbook_master WHERE erv_id = :erv_id")
    result = db.execute(query, {"erv_id": erv_id})
    db.commit()
    return result.rowcount > 0
