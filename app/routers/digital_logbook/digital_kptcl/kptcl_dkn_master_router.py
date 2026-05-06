from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/kptcl-dkn-master",
    tags=["KPTCL DKN Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class KPTCLDKNMasterCreate(BaseModel):
    station_name: Optional[str]
    station_incharge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]
    document_number: Optional[str]
    status: Optional[str]
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class KPTCLDKNMasterUpdate(KPTCLDKNMasterCreate):
    pass





@router.post("")
def create_kptcl_dkn_master(
    payload: KPTCLDKNMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO kptcl_dkn_master (
            station_name,
            station_incharge,
            shift,
            start_time,
            log_date,
            document_number,
            status,
            ms_logbook_id,
            technician_id,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :station_name,
            :station_incharge,
            :shift,
            :start_time,
            :log_date,
            :document_number,
            :status,
            :ms_logbook_id,
            :technician_id ,
            :created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING kptcl_dkn_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "KPTCL DKN Master created successfully",
        "kptcl_dkn_id": result.scalar()
    }







@router.get("/day_wise")
def get_kptcl_dkn(
    date: str,  # format: YYYY-MM-DD
    db: Session = Depends(get_db)
):
    # 1️⃣ Parse and validate date
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

    # 2️⃣ Fetch all logbook shifts within the 7-hour shift window for that date
    shifts = db.execute(text("""
        SELECT * FROM logbook_shift_master
        WHERE created_at >= DATE :date + INTERVAL '7 hour'
          AND created_at < (DATE :date + INTERVAL '1 day' + INTERVAL '7 hour')
    """), {"date": str(parsed_date)}).mappings().all()

    if not shifts:
        return {
            "date": str(parsed_date),
            "module": "kptcl_dkn",
            "message": "No shifts found for this date",
            "data": None
        }

    # 3️⃣ Collect ms_logbook_ids from the shifts
    ms_logbook_ids = [s["ms_logbook_id"] for s in shifts if s["ms_logbook_id"]]

    if not ms_logbook_ids:
        return {
            "date": str(parsed_date),
            "module": "kptcl_dkn",
            "message": "No valid logbook IDs found for this date",
            "data": None
        }

    # 4️⃣ Fetch all kptcl_dkn_masters linked via ms_logbook_id
    masters = db.execute(text("""
        SELECT m.*,
            c.first_name || ' ' || c.last_name AS created_by_name,
            u.first_name || ' ' || u.last_name AS updated_by_name
        FROM kptcl_dkn_master m
        LEFT JOIN users c ON c.user_id = m.created_by
        LEFT JOIN users u ON u.user_id = m.updated_by
        WHERE m.ms_logbook_id = ANY(:ms_logbook_ids)
    """), {"ms_logbook_ids": ms_logbook_ids}).mappings().all()

    if not masters:
        return {
            "date": str(parsed_date),
            "module": "kptcl_dkn",
            "message": "KPTCL DKN not created for this date",
            "data": None
        }

    # 5️⃣ Fetch all entries using kptcl_dkn_ids from the found masters
    kptcl_ids = [m["kptcl_dkn_id"] for m in masters]

    entries = db.execute(text("""
    SELECT e.*,
           c.first_name || ' ' || c.last_name AS created_by_name,
           u.first_name || ' ' || u.last_name AS updated_by_name
    FROM kptcl_dkn_entry e
    LEFT JOIN users c ON c.user_id = e.created_by
    LEFT JOIN users u ON u.user_id = e.updated_by
    WHERE e.master_id = ANY(:kptcl_ids)
    ORDER BY e.master_id, e.reading_date, e.reading_time
"""), {"kptcl_ids": kptcl_ids}).mappings().all()

    # 6️⃣ Group entries under their respective master
    from collections import defaultdict
    entries_by_master = defaultdict(list)
    for entry in entries:
        entries_by_master[entry["master_id"]].append(dict(entry))

    # 7️⃣ Final response
    result = [
        {
            "master": dict(m),
            "entries": entries_by_master.get(m["kptcl_dkn_id"], [])
        }
        for m in masters
    ]

    return {
        "date": str(parsed_date),
        "module": "kptcl_dkn",
        "kptcl_dkn": result
    }





@router.get("/kptcl-dkn/entry/{kptcl_dkn_id}")
def get_kptcl_dkn_by_master(
    kptcl_dkn_id: int,
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch master by kptcl_dkn_id
    master_sql = text("""
        SELECT *
        FROM kptcl_dkn_master
        WHERE kptcl_dkn_id = :kptcl_dkn_id
    """)
    master = db.execute(master_sql, {"kptcl_dkn_id": kptcl_dkn_id}).mappings().first()

    if not master:
        raise HTTPException(status_code=404, detail=f"KPTCL DKN master with id {kptcl_dkn_id} not found")

    # 2️⃣ Fetch all entries for this master
    entry_sql = text("""
        SELECT *
        FROM kptcl_dkn_entry
        WHERE master_id = :kptcl_dkn_id
        ORDER BY reading_date, reading_time
    """)
    entries = db.execute(entry_sql, {"kptcl_dkn_id": kptcl_dkn_id}).mappings().all()

    return {
        "module": "kptcl_dkn",
        "kptcl_dkn": {
            "master": dict(master),
            "entries": [dict(e) for e in entries]
        }
    }



@router.put("/{kptcl_dkn_id}")
def update_kptcl_dkn_master(
    kptcl_dkn_id: int,
    payload: KPTCLDKNMasterUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE kptcl_dkn_master
        SET
            station_name = :station_name,
            station_incharge = :station_incharge,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,
            document_number = :document_number,
            status = :status,
            ms_logbook_id = :ms_logbook_id,
            technician_id=:technician_id,
            created_at =:created_at ,
            created_by =:created_by ,
            updated_at =:updated_at ,
            updated_by=:updated_by
        WHERE kptcl_dkn_id = :kptcl_dkn_id
    """)

    params = payload.dict()
    params["kptcl_dkn_id"] = kptcl_dkn_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="KPTCL DKN master record not found")

    return {"message": "KPTCL DKN Master updated successfully"}


# =====================================================
# DELETE API – DELETE MASTER
# ================================================
# =====

@router.delete("/{kptcl_dkn_id}")
def delete_kptcl_dkn_master(
    kptcl_dkn_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM kptcl_dkn_master
        WHERE kptcl_dkn_id = :kptcl_dkn_id
    """)

    result = db.execute(query, {"kptcl_dkn_id": kptcl_dkn_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="KPTCL DKN master record not found")

    return {"message": "KPTCL DKN Master deleted successfully"}
