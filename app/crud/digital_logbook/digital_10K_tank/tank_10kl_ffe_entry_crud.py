# app/crud/digital_logbook/digital_10K_tank/tank_10kl_ffe_entry_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_10K_tank.tank_10kl_ffe_entry_schema import (
    Tank10KLFfeEntryCreate,
    Tank10KLFfeEntryUpdate,
)
from datetime import datetime


# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------


def get_tank_10kl_ffe_entries_by_master_id(db: Session, master_id: int):
    """Fetch all entries for a master ID with dynamic name resolution."""
    query = text(
        """
        SELECT 
            e.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.updated_by) as updated_by_name
        FROM tank_10kl_ffe_entry e 
        WHERE e.master_id = :mid 
        ORDER BY e.created_at ASC
        """
    )
    return db.execute(query, {"mid": master_id}).mappings().all()


def get_tank_10kl_ffe_entry_by_id(db: Session, tank_ffe_entry_id: int):
    """Fetch a single entry by ID with dynamic name resolution."""
    query = text(
        """
        SELECT 
            e.*,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.created_by) as created_by_name,
            (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users WHERE user_id = e.updated_by) as updated_by_name
        FROM tank_10kl_ffe_entry e 
        WHERE e.tank_ffe_entry_id = :id
    """
    )
    return db.execute(query, {"id": tank_ffe_entry_id}).mappings().first()


def create_tank_10kl_ffe_entry(
    db: Session, payload: Tank10KLFfeEntryCreate, user_id: int
):
    d = payload.model_dump(exclude_unset=True)

    # If entry_date is not provided, try to fetch it from the master record
    if not d.get("entry_date") and d.get("master_id"):
        master = (
            db.execute(
                text(
                    "SELECT logbook_date FROM tank_10kl_ffe_master WHERE tank_ffe_id = :mid"
                ),
                {"mid": d["master_id"]},
            )
            .mappings()
            .first()
        )
        if master and master.get("logbook_date"):
            d["entry_date"] = master["logbook_date"]

    # Use payload values if provided, otherwise fallback to defaults
    d["created_by"] = d.get("created_by") or user_id
    d["updated_by"] = d.get("updated_by") or user_id
    d["created_at"] = d.get("created_at") or datetime.now()
    d["updated_at"] = d.get("updated_at") or datetime.now()

    cols = ", ".join(d.keys())
    vals = ", ".join([f":{k}" for k in d.keys()])

    query = text(
        f"INSERT INTO tank_10kl_ffe_entry ({cols}) VALUES ({vals}) RETURNING tank_ffe_entry_id"
    )

    result = db.execute(query, d)
    db.commit()
    return result.scalar()


def update_tank_10kl_ffe_entry(
    db: Session, tank_ffe_entry_id: int, payload: Tank10KLFfeEntryUpdate, user_id: int
):
    old_data = get_tank_10kl_ffe_entry_by_id(db, tank_ffe_entry_id)
    if not old_data:
        return False

    # Standardize history audit fields
    history_data = dict(old_data)
    history_data.pop("created_by_name", None)
    history_data.pop("updated_by_name", None)

    history_data["action_type"] = "UPDATE"
    # Preserve original metadata for UPDATE snapshot

    cols = ", ".join(history_data.keys())
    vals = ", ".join([f":{k}" for k in history_data.keys()])

    hist_query = text(
        f"INSERT INTO tank_10kl_ffe_entry_history ({cols}) VALUES ({vals})"
    )
    db.execute(hist_query, history_data)

    data = payload.model_dump(exclude_unset=True)
    if data:
        # Exclude primary key from dynamic update
        data.pop("tank_ffe_entry_id", None)

        if not data:
            db.commit()
            return True

        set_clause_parts = [f"{k} = :{k}" for k in data.keys()]
        params = {**data, "eid": tank_ffe_entry_id}

        # Priority: payload value > CURRENT_TIMESTAMP/user_id
        if "updated_by" not in params:
            params["updated_by"] = user_id
            set_clause_parts.append("updated_by = :updated_by")

        if "updated_at" not in params:
            set_clause_parts.append("updated_at = CURRENT_TIMESTAMP")

        set_clause = ", ".join(set_clause_parts)

        query = text(
            f"UPDATE tank_10kl_ffe_entry SET {set_clause} WHERE tank_ffe_entry_id = :eid"
        )
        db.execute(query, params)
        db.commit()
    return True


def delete_tank_10kl_ffe_entry(db: Session, tank_ffe_entry_id: int, user_id: int):
    old_data = get_tank_10kl_ffe_entry_by_id(db, tank_ffe_entry_id)
    if not old_data:
        return False

    # Standardize history audit fields
    history_data = dict(old_data)
    history_data.pop("created_by_name", None)
    history_data.pop("updated_by_name", None)

    history_data["action_type"] = "DELETE"
    history_data["updated_at"] = datetime.now()
    history_data["updated_by"] = user_id

    cols = ", ".join(history_data.keys())
    vals = ", ".join([f":{k}" for k in history_data.keys()])

    hist_query = text(
        f"INSERT INTO tank_10kl_ffe_entry_history ({cols}) VALUES ({vals})"
    )
    db.execute(hist_query, history_data)

    query = text("DELETE FROM tank_10kl_ffe_entry WHERE tank_ffe_entry_id = :eid")
    db.execute(query, {"eid": tank_ffe_entry_id})
    db.commit()
    return True
