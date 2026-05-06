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
    prefix="/kptcl-hsn-entry",
    tags=["KPTCL HSN Entry"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class KPTCLHSNEntryCreate(BaseModel):
    master_id: Optional[int]

    reading_date: Optional[date]
    reading_time: Optional[time]

    t1c_kwh: Optional[Decimal]
    t1c_kvah: Optional[Decimal]

    calculated_pf: Optional[Decimal]
    t1pr_pf: Optional[Decimal]
    t1pr_kva: Optional[Decimal]

    initial_final_kwh: Optional[Decimal]
    initial_final_kvah: Optional[Decimal]
    kwh_kvah: Optional[Decimal]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class KPTCLHSNEntryUpdate(KPTCLHSNEntryCreate):
    pass


# =====================================================
# POST API – CREATE ENTRY
# =====================================================

@router.post("")
def create_kptcl_hsn_entry(
    payload: KPTCLHSNEntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO kptcl_hsn_entry (
            master_id,
            reading_date,
            reading_time,

            t1c_kwh,
            t1c_kvah,

            calculated_pf,
            t1pr_pf,
            t1pr_kva,

            initial_final_kwh,
            initial_final_kvah,
            kwh_kvah
                    ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :reading_date,
            :reading_time,

            :t1c_kwh,
            :t1c_kvah,

            :calculated_pf,
            :t1pr_pf,
            :t1pr_kva,

            :initial_final_kwh,
            :initial_final_kvah,
            :kwh_kvah,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING kptcl_hsn_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "KPTCL HSN Entry created successfully",
        "kptcl_hsn_entry_id": result.scalar()
    }

# ─────────────────────────────────────────────
# GET by date (7-hour shift window)
# ─────────────────────────────────────────────
@router.get("/kptcl-hsn")
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

    # 2️⃣ Fetch masters using 7-hour shift window via logbook_shift_master
    master_sql = text("""
        SELECT *
        FROM kptcl_hsn_master khm
        WHERE khm.ms_logbook_id IN (
            SELECT LSM.ms_logbook_id
            FROM logbook_shift_master LSM
            WHERE LSM.created_at >= DATE :date + INTERVAL '7 hour'
              AND LSM.created_at < (DATE :date + INTERVAL '1 day' + INTERVAL '7 hour')
        )
    """)

    masters = db.execute(
        master_sql,
        {"date": str(parsed_date)}
    ).mappings().all()

    if not masters:
        return {
            "date": str(parsed_date),
            "module": "kptcl_hsn",
            "message": "No KPTCL HSN found for this date",
            "kptcl_hsn": None
        }

    # 3️⃣ Collect all kptcl_hsn_ids and fetch entries
    kptcl_hsn_ids = [m["kptcl_hsn_id"] for m in masters]

    entry_sql = text("""
        SELECT *
        FROM kptcl_hsn_entry
        WHERE master_id = ANY(:kptcl_hsn_ids)
        ORDER BY master_id, reading_date, reading_time
    """)

    entries = db.execute(
        entry_sql,
        {"kptcl_hsn_ids": kptcl_hsn_ids}
    ).mappings().all()

    # 4️⃣ Group entries under their respective master
    from collections import defaultdict
    entries_by_master = defaultdict(list)
    for entry in entries:
        entries_by_master[entry["master_id"]].append(dict(entry))

    # 5️⃣ Final response
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


# ─────────────────────────────────────────────
# GET by entry_id
# ─────────────────────────────────────────────
@router.get("/kptcl-hsn/entry/{kptcl_hsn_entry_id}")
def get_kptcl_hsn_entry(
    kptcl_hsn_entry_id: int,
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch single entry by entry_id
    entry_sql = text("""
        SELECT *
        FROM kptcl_hsn_entry
        WHERE kptcl_hsn_entry_id = :kptcl_hsn_entry_id
    """)

    entry = db.execute(
        entry_sql,
        {"kptcl_hsn_entry_id": kptcl_hsn_entry_id}
    ).mappings().first()

    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"KPTCL HSN entry with id {kptcl_hsn_entry_id} not found"
        )

    # 2️⃣ Fetch its master record
    master_sql = text("""
        SELECT *
        FROM kptcl_hsn_master
        WHERE kptcl_hsn_id = :master_id
    """)

    master = db.execute(
        master_sql,
        {"master_id": entry["master_id"]}
    ).mappings().first()

    # 3️⃣ Final response
    return {
        "module": "kptcl_hsn",
        "kptcl_hsn": {
            "master": dict(master) if master else None,
            "entry": dict(entry)
        }
    }

# =====================================================
# PUT API – UPDATE ENTRY
# =====================================================

@router.put("/{entry_id}")
def update_kptcl_hsn_entry(
    entry_id: int,
    payload: KPTCLHSNEntryUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE kptcl_hsn_entry
        SET
            master_id = :master_id,
            reading_date = :reading_date,
            reading_time = :reading_time,

            t1c_kwh = :t1c_kwh,
            t1c_kvah = :t1c_kvah,

            calculated_pf = :calculated_pf,
            t1pr_pf = :t1pr_pf,
            t1pr_kva = :t1pr_kva,

            initial_final_kwh = :initial_final_kwh,
            initial_final_kvah = :initial_final_kvah,
            kwh_kvah = :kwh_kvah
                             ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE kptcl_hsn_entry_id = :entry_id
    """)

    params = payload.dict()
    params["entry_id"] = entry_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="KPTCL HSN entry not found")

    return {"message": "KPTCL HSN Entry updated successfully"}


# =====================================================
# DELETE API – DELETE ENTRY
# =====================================================

@router.delete("/{entry_id}")
def delete_kptcl_hsn_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM kptcl_hsn_entry
        WHERE kptcl_hsn_entry_id = :entry_id
    """)

    result = db.execute(query, {"entry_id": entry_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="KPTCL HSN entry not found")

    return {"message": "KPTCL HSN Entry deleted successfully"}
