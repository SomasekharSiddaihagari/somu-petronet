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
    prefix="/kptcl-dkn-entry",
    tags=["KPTCL DKN Entry"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class KPTCLDKNEntryCreate(BaseModel):
    master_id: Optional[int]

    reading_date: Optional[date]
    reading_time: Optional[time]

    kwh: Optional[Decimal]
    kvah: Optional[Decimal]
    pf_meter: Optional[Decimal]

    calculated_pf_day: Optional[str]
    calculated_pf_month: Optional[str]
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class KPTCLDKNEntryUpdate(KPTCLDKNEntryCreate):
    pass


# =====================================================
# POST API – CREATE ENTRY
# =====================================================

@router.post("")
def create_kptcl_dkn_entry(
    payload: KPTCLDKNEntryCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO kptcl_dkn_entry (
            master_id,
            reading_date,
            reading_time,
            kwh,
            kvah,
            pf_meter,
            calculated_pf_day,
            calculated_pf_month
                    ,created_at,created_by ,updated_at ,updated_by

        )
        VALUES (
            :master_id,
            :reading_date,
            :reading_time,
            :kwh,
            :kvah,
            :pf_meter,
            :calculated_pf_day,
            :calculated_pf_month
                 ,:created_at,:created_by ,:updated_at ,:updated_by

        )
        RETURNING kptcl_dkn_entry_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "KPTCL DKN Entry created successfully",
        "kptcl_dkn_entry_id": result.scalar()
    }

# ─────────────────────────────────────────────
# GET by date (7-hour shift window)
# ─────────────────────────────────────────────
@router.get("/kptcl-dkn")
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

    # 2️⃣ Fetch masters using 7-hour shift window via logbook_shift_master
    master_sql = text("""
        SELECT *
        FROM kptcl_dkn_master kdm
        WHERE kdm.ms_logbook_id IN (
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
            "module": "kptcl_dkn",
            "message": "No KPTCL DKN found for this date",
            "kptcl_dkn": None
        }

    # 3️⃣ Collect all kptcl_dkn_ids and fetch entries
    kptcl_dkn_ids = [m["kptcl_dkn_id"] for m in masters]

    entry_sql = text("""
        SELECT *
        FROM kptcl_dkn_entry
        WHERE master_id = ANY(:kptcl_dkn_ids)
        ORDER BY master_id, reading_date, reading_time
    """)

    entries = db.execute(
        entry_sql,
        {"kptcl_dkn_ids": kptcl_dkn_ids}
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
            "entries": entries_by_master.get(m["kptcl_dkn_id"], [])
        }
        for m in masters
    ]

    return {
        "date": str(parsed_date),
        "module": "kptcl_dkn",
        "kptcl_dkn": result
    }


# ─────────────────────────────────────────────
# GET by entry_id
# ─────────────────────────────────────────────
@router.get("/kptcl-dkn/entry/{kptcl_dkn_entry_id}")
def get_kptcl_dkn_entry(
    kptcl_dkn_entry_id: int,
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch single entry by entry_id
    entry_sql = text("""
        SELECT *
        FROM kptcl_dkn_entry
        WHERE kptcl_dkn_entry_id = :kptcl_dkn_entry_id
    """)

    entry = db.execute(
        entry_sql,
        {"kptcl_dkn_entry_id": kptcl_dkn_entry_id}
    ).mappings().first()

    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"KPTCL DKN entry with id {kptcl_dkn_entry_id} not found"
        )

    # 2️⃣ Fetch its master record
    master_sql = text("""
        SELECT *
        FROM kptcl_dkn_master
        WHERE kptcl_dkn_id = :master_id
    """)

    master = db.execute(
        master_sql,
        {"master_id": entry["master_id"]}
    ).mappings().first()

    # 3️⃣ Final response
    return {
        "module": "kptcl_dkn",
        "kptcl_dkn": {
            "master": dict(master) if master else None,
            "entry": dict(entry)
        }
    }

# =====================================================
# PUT API – UPDATE ENTRY
# =====================================================

@router.put("/{entry_id}")
def update_kptcl_dkn_entry(
    entry_id: int,
    payload: KPTCLDKNEntryUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE kptcl_dkn_entry
        SET
            master_id = :master_id,
            reading_date = :reading_date,
            reading_time = :reading_time,
            kwh = :kwh,
            kvah = :kvah,
            pf_meter = :pf_meter,
            calculated_pf_day = :calculated_pf_day,
            calculated_pf_month = :calculated_pf_month
                             ,created_at =:created_at ,created_by =:created_by ,updated_at =:updated_at ,updated_by=:updated_by

        WHERE kptcl_dkn_entry_id = :entry_id
    """)

    params = payload.dict()
    params["entry_id"] = entry_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="KPTCL DKN entry not found")

    return {"message": "KPTCL DKN Entry updated successfully"}


# =====================================================
# DELETE API – DELETE ENTRY
# =====================================================

@router.delete("/{entry_id}")
def delete_kptcl_dkn_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM kptcl_dkn_entry
        WHERE kptcl_dkn_entry_id = :entry_id
    """)

    result = db.execute(query, {"entry_id": entry_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="KPTCL DKN entry not found")

    return {"message": "KPTCL DKN Entry deleted successfully"}
