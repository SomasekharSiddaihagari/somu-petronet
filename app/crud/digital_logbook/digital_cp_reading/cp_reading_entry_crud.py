from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

# --- Helper Configuration & Filtering ---

STATION_FIELD_PREFIXES = {
    1: ["mlr_", "sv1_", "sv2_"],
    2: ["ner_", "sv3_", "sv4_"],
    3: ["hsn_", "sv5_", "sv6_", "sv7_"],
    4: ["dkn_", "sv8_", "ipstn_", "sv9_", "sv10_"],
}


def filter_entry_fields(entry: dict, sid: int) -> dict:
    prefixes = STATION_FIELD_PREFIXES.get(sid, [])
    common_fields = {
        "master_id",
        "sr_no",
        "entry_date",
        "entry_time",
        "remarks",
        "cp_entry_id",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "created_by_name",
        "updated_by_name",
    }
    return {
        k: v
        for k, v in entry.items()
        if k in common_fields or any(k.startswith(p) for p in prefixes)
    }


# --- Internal Helpers ---

def _log_entry_history(db: Session, record: dict):
    history_data = {k: v for k, v in record.items() if not k.endswith("_name")}
    cols = ", ".join(history_data.keys())
    vals = ", ".join([f":{k}" for k in history_data.keys()])
    db.execute(
        text(f"INSERT INTO cp_reading_entry_history ({cols}) VALUES ({vals})"),
        history_data,
    )


def _resolve_names_sql(alias: str = "e") -> str:
    return f"""
        (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
         WHERE user_id = (CASE WHEN CAST({alias}.created_by AS TEXT) ~ '^[0-9]+$' THEN CAST({alias}.created_by AS INTEGER) ELSE NULL END)) AS created_by_name,
        (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
         WHERE user_id = (CASE WHEN CAST({alias}.updated_by AS TEXT) ~ '^[0-9]+$' THEN CAST({alias}.updated_by AS INTEGER) ELSE NULL END)) AS updated_by_name
    """


def get_entry_by_id_raw(db: Session, cp_entry_id: int) -> Optional[dict]:
    """Internal version that returns raw data for history logging."""
    query = f"SELECT e.*, {_resolve_names_sql('e')} FROM cp_reading_entry e WHERE e.cp_entry_id = :id"
    row = db.execute(text(query), {"id": cp_entry_id}).mappings().first()
    return dict(row) if row else None


def get_entries_for_master(db: Session, cp_master_id: int) -> List[dict]:
    query = f"SELECT e.*, {_resolve_names_sql('e')} FROM cp_reading_entry e WHERE e.master_id = :mid ORDER BY e.created_at ASC"
    rows = db.execute(text(query), {"mid": cp_master_id}).mappings().all()
    return [dict(r) for r in rows]


# --- Main Entry CRUD ---

def get_entry_by_id(db: Session, cp_entry_id: int) -> Optional[dict]:
    """Retrieves an entry by ID (Returns unfiltered data as requested)."""
    return get_entry_by_id_raw(db, cp_entry_id)


def create_entry(db: Session, data: Dict[str, Any], uid: int) -> int:
    from .cp_reading_master_crud import get_master_by_id
    from fastapi import HTTPException

    master = get_master_by_id(db, data.get("master_id"))
    if not master:
        raise HTTPException(
            status_code=404,
            detail=f"Master ID {data.get('master_id')} not found. Cannot create entry.",
        )

    data.update(
        {
            "created_by": data.get("created_by") or uid,
            "updated_by": data.get("updated_by") or uid,
            "created_at": data.get("created_at") or datetime.now(),
            "updated_at": data.get("updated_at") or datetime.now(),
        }
    )
    cols, vals = ", ".join(data.keys()), ", ".join([f":{k}" for k in data.keys()])
    result = db.execute(
        text(
            f"INSERT INTO cp_reading_entry ({cols}) VALUES ({vals}) RETURNING cp_entry_id"
        ),
        data,
    )
    db.commit()
    return result.scalar()


def update_entry(db: Session, cp_entry_id: int, data: Dict[str, Any], uid: int) -> bool:
    from .cp_reading_master_crud import get_master_by_id
    from fastapi import HTTPException

    old_record = get_entry_by_id_raw(db, cp_entry_id)
    if not old_record:
        return False

    if "master_id" in data:
        target_master = get_master_by_id(db, data.get("master_id"))
        if not target_master:
            raise HTTPException(
                status_code=404,
                detail=f"Target Master ID {data.get('master_id')} not found.",
            )

    _log_entry_history(db, old_record)
    data.update({
        "updated_by": data.get("updated_by") or uid, 
        "updated_at": data.get("updated_at") or datetime.now()
    })
    set_clause = ", ".join([f"{k}=:{k}" for k in data.keys()])
    db.execute(
        text(f"UPDATE cp_reading_entry SET {set_clause} WHERE cp_entry_id=:id"),
        {**data, "id": cp_entry_id},
    )
    db.commit()
    return True


def delete_entry(db: Session, cp_entry_id: int) -> bool:
    old_record = get_entry_by_id_raw(db, cp_entry_id)
    if not old_record:
        return False
    _log_entry_history(db, old_record)
    db.execute(
        text("DELETE FROM cp_reading_entry WHERE cp_entry_id=:id"), {"id": cp_entry_id}
    )
    db.commit()
    return True
