from datetime import date, datetime, time, timedelta
from typing import List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

from app.schemas.digital_logbook.digital_npt.npt_report_master_schema import (
    NPTReportMasterCreate,
    NPTReportMasterUpdate,
    NPTReportMasterResponse,
)
from app.crud.digital_logbook.digital_npt.npt_report_entry_crud import (
    get_entries_by_master_id,
)

# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------

VALID_STATIONS = {1, 2, 3, 4, 5}

def validate_station_id(station_id: int):
    """Validates that the provided station_id exists in the system."""
    if station_id not in VALID_STATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid station_id: {station_id}"
        )

def _process_npt_result(db: Session, result: Any) -> Optional[dict]:
    """
    Applies shift calculation logic and fetches associated entries for a master record.
    Preserves exact original formatting and behavior.
    """
    if not result:
        return None

    d = dict(result)

    # Shift Processing Logic
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

    # Clean whitespace from station_in_charge
    if "station_in_charge" in d and d["station_in_charge"]:
        d["station_in_charge"] = d["station_in_charge"].strip()

    # Link child entries
    d["entries"] = get_entries_by_master_id(db, d["npt_id"])
    return d

def _log_npt_master_history(db: Session, record: dict, action: str, user_id: int = None):
    """
    Archives a snapshot of the NPT master record.
    SQL Query matches original logic exactly.
    """
    history_data = {
        "npt_id": record["npt_id"],
        "station": record["station"],
        "station_id": record["station_id"],
        "station_in_charge": record["station_in_charge"],
        "shift": record["shift"],
        "start_time": record["start_time"],
        "logbook_date": record["logbook_date"],
        "ms_logbook_id": record["ms_logbook_id"],
        "technician_id": record["technician_id"],
        "created_at": record["created_at"],
        "created_by": record["created_by"],
        "updated_at": datetime.now() if action == "DELETE" else record["updated_at"],
        "updated_by": user_id if action == "DELETE" else record["updated_by"],
        "action_type": action,
    }

    query = text("""
        INSERT INTO npt_report_master_history (
            npt_id, station, station_id, station_in_charge, shift, start_time, logbook_date,
            ms_logbook_id, technician_id, created_at,
            created_by, updated_at, updated_by, action_type
        )
        VALUES (
            :npt_id, :station, :station_id, :station_in_charge, :shift, :start_time, :logbook_date,
            :ms_logbook_id, :technician_id, :created_at,
            :created_by, :updated_at, :updated_by, :action_type
        )
    """)
    db.execute(query, history_data)

# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------

def get_npt_master_by_id(db: Session, npt_id: int):
    """Fetches a single NPT master record with robust name resolution matching ERV logically."""
    query = text("""
        SELECT 
            nrm.npt_id, nrm.station_id, nrm.station_in_charge, nrm.shift, nrm.start_time, nrm.logbook_date, nrm.ms_logbook_id, nrm.technician_id,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
             WHERE user_id = (CASE WHEN CAST(nrm.created_by AS TEXT) ~ '^[0-9]+$' THEN CAST(nrm.created_by AS INTEGER) ELSE NULL END)) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
             WHERE user_id = (CASE WHEN CAST(nrm.updated_by AS TEXT) ~ '^[0-9]+$' THEN CAST(nrm.updated_by AS INTEGER) ELSE NULL END)) as updated_by_name,
            COALESCE(nrm.station, (CASE 
                WHEN nrm.station_id = 1 THEN 'Mangalore'
                WHEN nrm.station_id = 2 THEN 'Neriya'
                WHEN nrm.station_id = 3 THEN 'Hassan'
                ELSE 'Devanagonthi'
            END)) as station,
            COALESCE(nrm.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(nrm.created_by AS INTEGER), 0) as created_by, 
            COALESCE(nrm.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(nrm.updated_by AS INTEGER), 0) as updated_by
        FROM npt_report_master nrm
        WHERE nrm.npt_id = :npt_id
    """)
    result = db.execute(query, {"npt_id": npt_id}).mappings().first()
    return _process_npt_result(db, result)

def get_npt_by_created_date(db: Session, search_date: date, station_id: int):
    """Fetches all NPT master records for a specific date and station with robust name resolution."""
    validate_station_id(station_id)

    start_dt = datetime.combine(search_date, time(7, 0))
    end_dt = start_dt + timedelta(days=1)

    query = text("""
        SELECT 
            nrm.npt_id, nrm.station_id, nrm.station_in_charge, nrm.shift, nrm.start_time, nrm.logbook_date, nrm.ms_logbook_id, nrm.technician_id,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
             WHERE user_id = (CASE WHEN CAST(nrm.created_by AS TEXT) ~ '^[0-9]+$' THEN CAST(nrm.created_by AS INTEGER) ELSE NULL END)) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
             WHERE user_id = (CASE WHEN CAST(nrm.updated_by AS TEXT) ~ '^[0-9]+$' THEN CAST(nrm.updated_by AS INTEGER) ELSE NULL END)) as updated_by_name,
            COALESCE(nrm.station, (CASE 
                WHEN nrm.station_id = 1 THEN 'Mangalore'
                WHEN nrm.station_id = 2 THEN 'Neriya'
                WHEN nrm.station_id = 3 THEN 'Hassan'
                ELSE 'Devanagonthi'
            END)) as station,
            COALESCE(nrm.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(nrm.created_by AS INTEGER), 0) as created_by, 
            COALESCE(nrm.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(nrm.updated_by AS INTEGER), 0) as updated_by
        FROM npt_report_master nrm
        JOIN logbook_shift_master LSM ON nrm.ms_logbook_id = LSM.ms_logbook_id
        WHERE 
            LSM.created_at >= :start_dt AND LSM.created_at < :end_dt
            AND nrm.created_at >= :start_dt AND nrm.created_at < :end_dt
            AND nrm.station_id = :station_id
        ORDER BY nrm.npt_id DESC
    """)

    results = db.execute(query, {
        "start_dt": start_dt,
        "end_dt": end_dt,
        "station_id": station_id,
    }).mappings().all()

    final_data = [_process_npt_result(db, row) for row in results]
    final_data.sort(key=lambda x: (len(x.get("entries", [])) > 0), reverse=True)
    return final_data

def create_npt_master(db: Session, payload: NPTReportMasterCreate, user_id: int):
    """Creates a new NPT master record using dynamic field insertion."""
    data = payload.model_dump(exclude_unset=True)
    validate_station_id(data.get("station_id"))

    for field in ["npt_id", "entries"]:
        data.pop(field, None)

    # Standardize audit fields
    data["created_by"] = data.get("created_by") or user_id
    data["updated_by"] = data.get("updated_by") or user_id
    data["created_at"] = data.get("created_at") or datetime.now()
    data["updated_at"] = data.get("updated_at") or datetime.now()

    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data.keys()])
    query = text(f"INSERT INTO npt_report_master ({cols}) VALUES ({vals}) RETURNING npt_id")

    result = db.execute(query, data)
    db.commit()
    return result.scalar()

def update_npt_master(db: Session, npt_id: int, payload: NPTReportMasterUpdate, user_id: int):
    """Updates an NPT master record and archives history."""
    old_record = get_npt_master_by_id(db, npt_id)
    if not old_record: return False

    _log_npt_master_history(db, old_record, "UPDATE")

    data = payload.model_dump(exclude_unset=True)
    if "station_id" in data:
        validate_station_id(data.get("station_id"))

    for field in ["npt_id", "entries"]:
        data.pop(field, None)

    if not data:
        db.commit()
        return True

    # Manual SET clause construction as per original pattern
    set_clause_parts = [f"{key} = :{key}" for key in data.keys()]
    params = {**data, "npt_id": npt_id}

    if "updated_by" not in params:
        params["updated_by"] = user_id
        set_clause_parts.append("updated_by = :updated_by")

    if "updated_at" not in params:
        set_clause_parts.append("updated_at = CURRENT_TIMESTAMP")

    query = text(f"UPDATE npt_report_master SET {', '.join(set_clause_parts)} WHERE npt_id = :npt_id")
    db.execute(query, params)
    db.commit()
    return True

def delete_npt_master(db: Session, npt_id: int, user_id: int):
    """Performs an archival delete for an NPT master record."""
    old_record = get_npt_master_by_id(db, npt_id)
    if not old_record: return False

    _log_npt_master_history(db, old_record, "DELETE", user_id=user_id)

    query = text("DELETE FROM npt_report_master WHERE npt_id = :npt_id")
    result = db.execute(query, {"npt_id": npt_id})
    db.commit()
    return result.rowcount > 0
