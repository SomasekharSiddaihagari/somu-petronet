# app/crud/digital_logbook/digital_cp_reading/cp_reading_ner_master_crud.py
from datetime import date, datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_ner_master_schema import (
    CPReadingNERMasterCreate,
    CPReadingNERMasterUpdate,
)
from app.crud.digital_logbook.digital_cp_reading.cp_reading_ner_entry_crud import (
    get_ner_entries_by_master_id,
)
from app.models.digital_logbook.digital_cp_reading.cp_reading_ner_master_history import (
    CPReadingNERMasterHistory,
)


def _process_ner_result(db: Session, result):
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
        get_ner_entries_by_master_id(db, d["cp_ner_id"]) if d.get("cp_ner_id") else []
    )
    return d


def _log_cp_ner_master_history(db: Session, record: dict, user_id: int):
    """Safely logs a snapshot of the NER Master record to history by filtering allowed columns."""
    history_columns = CPReadingNERMasterHistory.__table__.columns.keys()

    # Filter only keys that exist in the History Model
    safe_data = {
        k: v for k, v in record.items() if k in history_columns and k not in ["entries"]
    }

    # Update with current info
    safe_data["updated_by"] = user_id
    safe_data["updated_at"] = datetime.now()
    safe_data.pop("history_id", None)
    
    # Ensure resolved names don't fail history insert if they aren't in columns
    safe_data.pop("created_by_name", None)
    safe_data.pop("updated_by_name", None)

    cols = ", ".join(safe_data.keys())
    vals = ", ".join([f":{k}" for k in safe_data.keys()])
    query = text(f"INSERT INTO cp_reading_ner_master_history ({cols}) VALUES ({vals})")
    db.execute(query, safe_data)


def get_ner_master_by_id(db: Session, ner_id: int):
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
            COALESCE(m.station, 'Neriya') as station
        FROM cp_reading_ner_master m
        WHERE m.cp_ner_id = :id
    """
    )
    result = db.execute(query, {"id": ner_id}).mappings().first()
    return _process_ner_result(db, result)


def create_ner_master(db: Session, payload: CPReadingNERMasterCreate, user_id: int):
    data = payload.model_dump(exclude_unset=True)
    for field in ["cp_ner_id", "entries"]:
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
        f"INSERT INTO cp_reading_ner_master ({cols}) VALUES ({vals}) RETURNING cp_ner_id"
    )
    result = db.execute(query, data)
    db.commit()
    return result.scalar()


def update_ner_master(
    db: Session, ner_id: int, payload: CPReadingNERMasterUpdate, user_id: int
):
    old = get_ner_master_by_id(db, ner_id)
    if not old:
        return False

    # Log to history before update
    _log_cp_ner_master_history(db, dict(old), user_id)

    data = payload.model_dump(exclude_unset=True)
    for field in ["cp_ner_id", "entries"]:
        data.pop(field, None)
    if not data:
        db.commit()
        return True

    set_clause_parts = [f"{k} = :{k}" for k in data.keys()]
    params = {**data, "id": ner_id}

    if "updated_by" not in params:
        params["updated_by"] = user_id
        set_clause_parts.append("updated_by = :updated_by")

    if "updated_at" not in params:
        set_clause_parts.append("updated_at = CURRENT_TIMESTAMP")

    set_clause = ", ".join(set_clause_parts)

    db.execute(
        text(f"UPDATE cp_reading_ner_master SET {set_clause} WHERE cp_ner_id = :id"),
        params,
    )
    db.commit()
    return True


def delete_ner_master(db: Session, ner_id: int, user_id: int):
    old = get_ner_master_by_id(db, ner_id)
    if not old:
        return False

    # Log to history before delete
    _log_cp_ner_master_history(db, dict(old), user_id)

    db.execute(
        text("DELETE FROM cp_reading_ner_master WHERE cp_ner_id = :id"), {"id": ner_id}
    )
    db.commit()
    return True


def get_ner_masters_by_date_range(db: Session, from_date: date, to_date: date):
    query = text(
        """
        SELECT m.*,
               (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.created_by) as created_by_name,
               (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = m.updated_by) as updated_by_name,
               COALESCE(m.created_at, CURRENT_TIMESTAMP) as created_at,
               COALESCE(CAST(m.created_by AS INTEGER), 0) as created_by,
               COALESCE(m.updated_at, CURRENT_TIMESTAMP) as updated_at,
               COALESCE(CAST(m.updated_by AS INTEGER), 0) as updated_by,
               COALESCE(m.station, 'Neriya') as station
        FROM cp_reading_ner_master m
        WHERE m.log_date >= :from_date
          AND m.log_date <= :to_date
          AND EXISTS (SELECT 1 FROM cp_reading_ner_entry e WHERE e.master_id = m.cp_ner_id)
        ORDER BY m.log_date DESC, m.cp_ner_id DESC
    """
    )
    results = (
        db.execute(query, {"from_date": from_date, "to_date": to_date}).mappings().all()
    )
    return [_process_ner_result(db, row) for row in results]
