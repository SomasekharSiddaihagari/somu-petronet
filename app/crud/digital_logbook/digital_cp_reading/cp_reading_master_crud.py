from datetime import date, datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from .cp_reading_entry_crud import get_entries_for_master

# --- Helper Configuration & Filtering ---

STATION_NAMES = {1: "Mangalore", 2: "Neriya", 3: "Hassan", 4: "Devanagonthi"}

STATION_FIELD_PREFIXES = {
    1: ["mlr_", "sv1_", "sv2_"],
    2: ["ner_", "sv3_", "sv4_"],
    3: ["hsn_", "sv5_", "sv6_", "sv7_"],
    4: ["dkn_", "sv8_", "ipstn_", "sv9_", "sv10_"],
}


def filter_entry_fields_by_station(entry: dict, sid: int) -> dict:
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

def validate_station_id(sid: int):
    if sid not in STATION_NAMES:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400, detail=f"Invalid station_id: {sid}. Must be 1-4."
        )


def _log_master_history(db: Session, record: dict):
    history_data = {
        k: v for k, v in record.items() if not k.endswith("_name") and k != "entries"
    }
    cols = ", ".join(history_data.keys())
    vals = ", ".join([f":{k}" for k in history_data.keys()])
    db.execute(
        text(f"INSERT INTO cp_reading_master_history ({cols}) VALUES ({vals})"),
        history_data,
    )


def _resolve_names_sql(alias: str = "m") -> str:
    return f"""
        (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
         WHERE user_id = (CASE WHEN CAST({alias}.created_by AS TEXT) ~ '^[0-9]+$' THEN CAST({alias}.created_by AS INTEGER) ELSE NULL END)) AS created_by_name,
        (SELECT TRIM(CONCAT(first_name, ' ', last_name)) FROM users 
         WHERE user_id = (CASE WHEN CAST({alias}.updated_by AS TEXT) ~ '^[0-9]+$' THEN CAST({alias}.updated_by AS INTEGER) ELSE NULL END)) AS updated_by_name
    """


# --- Main Master CRUD ---

def get_master_by_id(db: Session, cp_master_id: int) -> Optional[dict]:
    query = f"SELECT m.*, {_resolve_names_sql('m')} FROM cp_reading_master m WHERE m.cp_master_id = :id"
    row = db.execute(text(query), {"id": cp_master_id}).mappings().first()
    if not row:
        return None
    d = dict(row)
    sid = d.get("station_id")
    entries = get_entries_for_master(db, cp_master_id)
    d["entries"] = [filter_entry_fields_by_station(e, sid) for e in entries]
    return d


def get_masters_by_date(
    db: Session, sid: int, search_date: date
) -> List[dict]:
    validate_station_id(sid)
    query = f"""
        SELECT m.*, {_resolve_names_sql('m')} FROM cp_reading_master m 
        WHERE m.station_id = :sid AND m.log_date = :sd
        AND EXISTS (SELECT 1 FROM cp_reading_entry e WHERE e.master_id = m.cp_master_id)
        ORDER BY m.log_date DESC, m.cp_master_id DESC
    """
    rows = (
        db.execute(text(query), {"sid": sid, "sd": search_date})
        .mappings()
        .all()
    )
    
    results = []
    for r in rows:
        d = dict(r)
        entries = get_entries_for_master(db, d["cp_master_id"])
        d["entries"] = [filter_entry_fields_by_station(e, sid) for e in entries]
        results.append(d)
        
    return results


def create_master(db: Session, data: Dict[str, Any], uid: int) -> int:
    sid = data.get("station_id")
    validate_station_id(sid)
    data.update(
        {
            "station": data.get("station") or STATION_NAMES.get(sid, ""),
            "created_by": data.get("created_by") or uid,
            "updated_by": data.get("updated_by") or uid,
            "created_at": data.get("created_at") or datetime.now(),
            "updated_at": data.get("updated_at") or datetime.now(),
        }
    )
    cols, vals = ", ".join(data.keys()), ", ".join([f":{k}" for k in data.keys()])
    result = db.execute(
        text(
            f"INSERT INTO cp_reading_master ({cols}) VALUES ({vals}) RETURNING cp_master_id"
        ),
        data,
    )
    db.commit()
    return result.scalar()


def update_master(
    db: Session, cp_master_id: int, data: Dict[str, Any], uid: int
) -> bool:
    old_record = get_master_by_id(db, cp_master_id)
    if not old_record:
        return False
    _log_master_history(db, old_record)
    data.update({
        "updated_by": data.get("updated_by") or uid, 
        "updated_at": data.get("updated_at") or datetime.now()
    })
    set_clause = ", ".join([f"{k}=:{k}" for k in data.keys()])
    db.execute(
        text(f"UPDATE cp_reading_master SET {set_clause} WHERE cp_master_id=:id"),
        {**data, "id": cp_master_id},
    )
    db.commit()
    return True


def delete_master(db: Session, cp_master_id: int) -> bool:
    old_record = get_master_by_id(db, cp_master_id)
    if not old_record:
        return False
    _log_master_history(db, old_record)
    db.execute(
        text("DELETE FROM cp_reading_master WHERE cp_master_id=:id"),
        {"id": cp_master_id},
    )
    db.commit()
    return True
