from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Any, Dict, Optional
from app.schemas.digital_logbook.digital_cp_reading.cp_reading_hsn_entry_schema import (
    CPReadingHSNEntryCreate,
    CPReadingHSNEntryUpdate,
)
from datetime import datetime


# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------


def get_hsn_entries_by_master_id(db: Session, mid: int):
    """Fetch HSN entries for a master ID with dynamic name resolution."""
    query = text(
        """
        SELECT 
            e.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.updated_by) as updated_by_name
        FROM cp_reading_hsn_entry e 
        WHERE e.master_id = :mid 
        ORDER BY e.created_at ASC
    """
    )
    return db.execute(query, {"mid": mid}).mappings().all()


def get_hsn_entry_by_id(db: Session, eid: int):
    """Retrieve a single HSN entry with dynamic name resolution."""
    query = text(
        """
        SELECT 
            e.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.updated_by) as updated_by_name
        FROM cp_reading_hsn_entry e 
        WHERE e.cp_hsn_entry_id = :id
    """
    )
    return db.execute(query, {"id": eid}).mappings().first()


def create_hsn_entry(db: Session, payload: CPReadingHSNEntryCreate, uid: int):
    data = payload.model_dump(exclude_unset=True)

    # Exclude primary key
    data.pop("cp_hsn_entry_id", None)

    # Use payload values if provided, otherwise fallback to defaults
    data["created_by"] = uid if data.get("created_by") is None else data["created_by"]
    data["updated_by"] = uid if data.get("updated_by") is None else data["updated_by"]
    data["created_at"] = data.get("created_at") or datetime.now()
    data["updated_at"] = data.get("updated_at") or datetime.now()

    # Strip signature if present
    if data.get("signature"):
        data["signature"] = data["signature"].strip()

    cols = ", ".join(data.keys())
    vals = ", ".join([f":{k}" for k in data.keys()])

    res = db.execute(
        text(
            f"INSERT INTO cp_reading_hsn_entry ({cols}) VALUES ({vals}) RETURNING cp_hsn_entry_id"
        ),
        data,
    )
    db.commit()
    return res.scalar()


def update_hsn_entry(db: Session, eid: int, payload: CPReadingHSNEntryUpdate, uid: int):
    old = get_hsn_entry_by_id(db, eid)
    if not old:
        return False

    old_dict = dict(old)

    # Standardize history audit fields
    history_data = dict(old)
    history_data.pop("created_by_name", None)
    history_data.pop("updated_by_name", None)

    # Preserving existing record metadata for UPDATE snapshot

    cols = ", ".join(history_data.keys())
    vals = ", ".join([f":{k}" for k in history_data.keys()])

    db.execute(
        text(f"INSERT INTO cp_reading_hsn_entry_history ({cols}) VALUES ({vals})"),
        history_data,
    )

    data = payload.model_dump(exclude_unset=True)

    # Exclude primary key and audit fields from dynamic update
    data.pop("cp_hsn_entry_id", None)

    if not data:
        db.commit()
        return True

    # Strip signature if present
    if data.get("signature"):
        data["signature"] = data["signature"].strip()

    set_clause_parts = [f"{k} = :{k}" for k in data.keys()]
    params = {**data, "id": eid}

    # Priority: payload value > CURRENT_TIMESTAMP/user_id
    if "updated_by" not in params:
        params["updated_by"] = uid
        set_clause_parts.append("updated_by = :updated_by")

    if "updated_at" not in params:
        set_clause_parts.append("updated_at = CURRENT_TIMESTAMP")

    set_clause = ", ".join(set_clause_parts)

    db.execute(
        text(
            f"UPDATE cp_reading_hsn_entry SET {set_clause} WHERE cp_hsn_entry_id = :id"
        ),
        params,
    )
    db.commit()
    return True


def delete_hsn_entry(db: Session, eid: int, uid: int):
    old = get_hsn_entry_by_id(db, eid)
    if not old:
        return False

    # Standardize history audit fields
    history_data = dict(old)
    history_data.pop("created_by_name", None)
    history_data.pop("updated_by_name", None)

    history_data["updated_at"] = datetime.now()
    history_data["updated_by"] = uid

    cols = ", ".join(history_data.keys())
    vals = ", ".join([f":{k}" for k in history_data.keys()])

    db.execute(
        text(f"INSERT INTO cp_reading_hsn_entry_history ({cols}) VALUES ({vals})"),
        history_data,
    )
    db.execute(
        text("DELETE FROM cp_reading_hsn_entry WHERE cp_hsn_entry_id = :eid"),
        {"eid": eid},
    )
    db.commit()
    return True
