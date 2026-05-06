from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from decimal import Decimal

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/kptcl-hsn-master",
    tags=["KPTCL HSN Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class KPTCLHSNMasterCreate(BaseModel):
    station_name: Optional[str]
    station_incharge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]
    document_number: Optional[str]
    status: Optional[str]
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None
    billing_kwh_rdg: Optional[Decimal]
    billing_kvah_rdg: Optional[Decimal]
    monthly_avg_pf: Optional[Decimal]
    monthly_avg_kva: Optional[Decimal]


    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class KPTCLHSNMasterUpdate(KPTCLHSNMasterCreate):
    pass



@router.post("")
def create_kptcl_hsn_master(
    payload: KPTCLHSNMasterCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO kptcl_hsn_master (
            station_name,
            station_incharge,
            shift,
            start_time,
            log_date,
            document_number,
            status,

            billing_kwh_rdg,
            billing_kvah_rdg,
            monthly_avg_pf,
            monthly_avg_kva,
                ms_logbook_id,
               technician_id,
                 created_at,
                 created_by ,
                 updated_at,
                 updated_by

        )
        VALUES (
            :station_name,
            :station_incharge,
            :shift,
            :start_time,
            :log_date,
            :document_number,
            :status,
            :billing_kwh_rdg,
            :billing_kvah_rdg,
            :monthly_avg_pf,
            :monthly_avg_kva,
            :ms_logbook_id,
            :technician_id,
            :created_at,
            :created_by ,
            :updated_at ,
            :updated_by
        )
        RETURNING kptcl_hsn_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "KPTCL HSN Master created successfully",
        "kptcl_hsn_id": result.scalar()
    }






@router.get("/logbook/kptcl/hsn/day_wise")
def get_kptcl_hsn(
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
            "module": "kptcl_hsn",
            "message": "No shifts found for this date",
            "data": None
        }

    # 3️⃣ Collect ms_logbook_ids from the shifts
    ms_logbook_ids = [s["ms_logbook_id"] for s in shifts if s["ms_logbook_id"]]

    if not ms_logbook_ids:
        return {
            "date": str(parsed_date),
            "module": "kptcl_hsn",
            "message": "No valid logbook IDs found for this date",
            "data": None
        }

    # 4️⃣ Fetch all kptcl_hsn_masters linked via ms_logbook_id
    masters = db.execute(text("""
    SELECT m.*,
           c.first_name || ' ' || c.last_name AS created_by_name,
           u.first_name || ' ' || u.last_name AS updated_by_name
    FROM kptcl_hsn_master m
    LEFT JOIN users c ON c.user_id = m.created_by
    LEFT JOIN users u ON u.user_id = m.updated_by
    WHERE m.ms_logbook_id = ANY(:ms_logbook_ids)
"""), {"ms_logbook_ids": ms_logbook_ids}).mappings().all()

    if not masters:
        return {
            "date": str(parsed_date),
            "module": "kptcl_hsn",
            "message": "KPTCL HSN not created for this date",
            "data": None
        }

    # 5️⃣ Fetch all entries using kptcl_hsn_ids from the found masters
    kptcl_ids = [m["kptcl_hsn_id"] for m in masters]

    entries = db.execute(text("""
    SELECT e.*,
           c.first_name || ' ' || c.last_name AS created_by_name,
           u.first_name || ' ' || u.last_name AS updated_by_name
    FROM kptcl_hsn_entry e
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
            "entries": entries_by_master.get(m["kptcl_hsn_id"], [])
        }
        for m in masters
    ]

    return {
        "date": str(parsed_date),
        "module": "kptcl_hsn",
        "kptcl_hsn": result
    }

@router.get("/kptcl-hsn/entry/{kptcl_hsn_id}")
def get_kptcl_hsn_by_master(
    kptcl_hsn_id: int,
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch master by kptcl_hsn_id
    master_sql = text("""
        SELECT *
        FROM kptcl_hsn_master
        WHERE kptcl_hsn_id = :kptcl_hsn_id
    """)
    master = db.execute(master_sql, {"kptcl_hsn_id": kptcl_hsn_id}).mappings().first()

    if not master:
        raise HTTPException(status_code=404, detail=f"KPTCL HSN master with id {kptcl_hsn_id} not found")

    # 2️⃣ Fetch all entries for this master
    entry_sql = text("""
        SELECT *
        FROM kptcl_hsn_entry
        WHERE master_id = :kptcl_hsn_id
        ORDER BY reading_date, reading_time
    """)
    entries = db.execute(entry_sql, {"kptcl_hsn_id": kptcl_hsn_id}).mappings().all()

    return {
        "module": "kptcl_hsn",
        "kptcl_hsn": {
            "master": dict(master),
            "entries": [dict(e) for e in entries]
        }
    }


# =====================================================
# POST API – CREATE MASTER
# =====================================================





# =====================================================
# PUT API – UPDATE MASTER
# =====================================================

@router.put("/{kptcl_hsn_id}")
def update_kptcl_hsn_master(
    kptcl_hsn_id: int,
    payload: KPTCLHSNMasterUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE kptcl_hsn_master
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
            billing_kwh_rdg = :billing_kwh_rdg,
            billing_kvah_rdg = :billing_kvah_rdg,
            monthly_avg_pf = :monthly_avg_pf,
            monthly_avg_kva = :monthly_avg_kva

            ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by
        WHERE kptcl_hsn_id = :kptcl_hsn_id
    """)

    params = payload.dict()
    params["kptcl_hsn_id"] = kptcl_hsn_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="KPTCL HSN master record not found")

    return {"message": "KPTCL HSN Master updated successfully"}


# =====================================================
# DELETE API – DELETE MASTER
# =====================================================

@router.delete("/{kptcl_hsn_id}")
def delete_kptcl_hsn_master(
    kptcl_hsn_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM kptcl_hsn_master
        WHERE kptcl_hsn_id = :kptcl_hsn_id
    """)

    result = db.execute(query, {"kptcl_hsn_id": kptcl_hsn_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="KPTCL HSN master record not found")

    return {"message": "KPTCL HSN Master deleted successfully"}
