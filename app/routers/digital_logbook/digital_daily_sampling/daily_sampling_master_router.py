from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime, time

from app.database import get_db
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/daily-sampling-master",
    tags=["Daily Sampling Master"],dependencies=[Depends(validate_token)]
)

# =====================================================
# SCHEMAS (Inside router as requested)
# =====================================================

class DailySamplingMasterCreate(BaseModel):
    document_number: Optional[str]
    station: Optional[str]
    station_in_charge: Optional[str]
    shift: Optional[str]
    start_time: Optional[time]
    log_date: Optional[date]
    status: Optional[str]
    created_at : Optional[datetime] = None
    ms_logbook_id:Optional[int] = None
    technician_id: Optional[int] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    temperature: Optional[str] = None

class DailySamplingMasterUpdate(DailySamplingMasterCreate):
    pass


# =====================================================
# POST API – CREATE MASTER
# =====================================================

@router.post("")
def create_daily_sampling_master(
    payload: DailySamplingMasterCreate,
    db: Session = Depends(get_db)
    ):
    query = text("""
        INSERT INTO daily_sampling_master (
            document_number,
            station,
            station_in_charge,
            shift,
            start_time,
            log_date,
            status,
            technician_id,
            created_at,
            ms_logbook_id,
            created_by ,
            updated_at ,
            updated_by,
            temperature

        )
        VALUES (
            :document_number,
            :station,
            :station_in_charge,
            :shift,
            :start_time,
            :log_date,
            :status,
            :technician_id,
            :created_at,
            :ms_logbook_id,
            :created_by ,
            :updated_at ,
            :updated_by,
            :temperature
        )
        RETURNING sampling_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Daily Sampling Master created successfully",
        "sampling_id": result.scalar()
    }

# @router.get("/day_wise")
# def get_daily_sampling(
#     date: str,  # format: YYYY-MM-DD
#     db: Session = Depends(get_db)
#     ):
#     # 1️⃣ Parse and validate date
#     try:
#         parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
#     except ValueError:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid date format. Use YYYY-MM-DD"
#         )

#     # 2️⃣ Fetch sampling masters where ms_logbook_id falls within the 7-hour shift window
#     # daily_sampling_master.ms_logbook_id → logbook_shift_master.ms_logbook_id (filtered by created_at window)
#     master_sql = text("""
#         SELECT *
#         FROM daily_sampling_master dsm
#         WHERE dsm.ms_logbook_id IN (
#             SELECT LSM.ms_logbook_id
#             FROM logbook_shift_master LSM
#             WHERE LSM.created_at >= DATE :date + INTERVAL '7 hour'
#               AND LSM.created_at < (DATE :date + INTERVAL '1 day' + INTERVAL '7 hour')
#         )
#     """)

#     masters = db.execute(
#         master_sql,
#         {"date": str(parsed_date)}
#     ).mappings().all()

#     if not masters:
#         return {
#             "date": str(parsed_date),
#             "module": "daily_sampling",
#             "message": "No Daily Sampling found for this date",
#             "daily_sampling": None
#         }

#     # 3️⃣ Collect all sampling_ids and fetch entries
#     sampling_ids = [m["sampling_id"] for m in masters]

#     entry_sql = text("""
#         SELECT *
#         FROM daily_sampling_entry
#         WHERE master_id = ANY(:sampling_ids)
#         ORDER BY master_id, sr_no, date, sample_time
#     """)

#     entries = db.execute(
#         entry_sql,
#         {"sampling_ids": sampling_ids}
#     ).mappings().all()

#     # 4️⃣ Group entries under their respective master
#     from collections import defaultdict
#     entries_by_master = defaultdict(list)
#     for entry in entries:
#         entries_by_master[entry["master_id"]].append(dict(entry))

#     # 5️⃣ Final response
#     result = [
#         {
#             "master": dict(m),
#             "entries": entries_by_master.get(m["sampling_id"], [])
#         }
#         for m in masters
#     ]

#     return {
#         "date": str(parsed_date),
#         "module": "daily_sampling",
#         "daily_sampling": result
#     }

@router.get("/day_wise")
def get_daily_sampling(
    date: str,
    db: Session = Depends(get_db)
    ):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

    # 2️⃣ Fetch masters with creator/updater names
    master_sql = text("""
        SELECT 
            dsm.*,
            CONCAT(uc.first_name, ' ', uc.last_name) AS created_by_name,
            CONCAT(uu.first_name, ' ', uu.last_name) AS updated_by_name
        FROM daily_sampling_master dsm
        LEFT JOIN users uc ON uc.user_id = dsm.created_by
        LEFT JOIN users uu ON uu.user_id = dsm.updated_by
        WHERE dsm.ms_logbook_id IN (
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
            "module": "daily_sampling",
            "message": "No Daily Sampling found for this date",
            "daily_sampling": None
        }

    sampling_ids = [m["sampling_id"] for m in masters]

    # 3️⃣ Fetch entries with creator/updater names
    entry_sql = text("""
        SELECT 
            dse.*,
            CONCAT(uc.first_name, ' ', uc.last_name) AS created_by_name,
            CONCAT(uu.first_name, ' ', uu.last_name) AS updated_by_name
        FROM daily_sampling_entry dse
        LEFT JOIN users uc ON uc.user_id = dse.created_by
        LEFT JOIN users uu ON uu.user_id = dse.updated_by
        WHERE dse.master_id = ANY(:sampling_ids)
        ORDER BY dse.master_id, dse.sr_no, dse.date, dse.sample_time
    """)

    entries = db.execute(
        entry_sql,
        {"sampling_ids": sampling_ids}
    ).mappings().all()

    from collections import defaultdict
    entries_by_master = defaultdict(list)
    for entry in entries:
        entries_by_master[entry["master_id"]].append(dict(entry))

    result = [
        {
            "master": dict(m),
            "entries": entries_by_master.get(m["sampling_id"], [])
        }
        for m in masters
    ]

    return {
        "date": str(parsed_date),
        "module": "daily_sampling",
        "daily_sampling": result
    }


@router.get("/{sampling_id}")
def get_daily_sampling_by_master(
    sampling_id: int,
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch master by sampling_id
    master_sql = text("""
        SELECT *
        FROM daily_sampling_master
        WHERE sampling_id = :sampling_id
    """)
    master = db.execute(master_sql, {"sampling_id": sampling_id}).mappings().first()

    if not master:
        raise HTTPException(status_code=404, detail=f"Daily Sampling master with id {sampling_id} not found")

    # 2️⃣ Fetch all entries for this master
    entry_sql = text("""
        SELECT *
        FROM daily_sampling_entry
        WHERE master_id = :sampling_id
        ORDER BY sr_no, date, sample_time
    """)
    entries = db.execute(entry_sql, {"sampling_id": sampling_id}).mappings().all()

    return {
        "module": "daily_sampling",
        "daily_sampling": {
            "master": dict(master),
            "entries": [dict(e) for e in entries]
        }
    }



# =====================================================
# PUT API – UPDATE MASTER
# =====================================================

@router.put("/{sampling_id}")
def update_daily_sampling_master(
    sampling_id: int,
    payload: DailySamplingMasterUpdate,
    db: Session = Depends(get_db)
):
    query = text("""
        UPDATE daily_sampling_master
        SET
            document_number = :document_number,
            station = :station,
            station_in_charge = :station_in_charge,
            shift = :shift,
            start_time = :start_time,
            log_date = :log_date,
            status = :status,
            technician_id=:technician_id,
            created_at =:created_at,
            ms_logbook_id=:ms_logbook_id,
            created_by =:created_by ,
            updated_at =:updated_at ,
            updated_by=:updated_by,
            temperature=:temperature

        WHERE sampling_id = :sampling_id
    """)

    params = payload.dict()
    params["sampling_id"] = sampling_id

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Daily sampling master not found")

    return {"message": "Daily Sampling Master updated successfully"}


# =====================================================
# DELETE API – DELETE MASTER
# =====================================================

@router.delete("/{sampling_id}")
def delete_daily_sampling_master(
    sampling_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM daily_sampling_master
        WHERE sampling_id = :sampling_id
    """)

    result = db.execute(query, {"sampling_id": sampling_id})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Daily sampling master not found")

    return {"message": "Daily Sampling Master deleted successfully"}
