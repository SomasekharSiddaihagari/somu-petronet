from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.digital_logbook.digital_fire.fire_engine_test_master_schemas import (
    FireEngineTestMasterCreate,
    FireEngineTestMasterUpdate,
    )

from app.crud.digital_logbook.digital_fire import fire_engine_test_master_crud as crud
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/fire-engine-test",
    tags=["Fire Engine Test Master"],dependencies=[Depends(validate_token)]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_fire_engine_test(
    payload: FireEngineTestMasterCreate,
    db: Session = Depends(get_db)
):
    return crud.create_fire_engine_test(db, payload)

# @router.get("/fire-engine-test/day_wise")
# def get_fire_engine_test(
#     date: str,  # format: YYYY-MM-DD
#     db: Session = Depends(get_db)
# ):
#     # 1️⃣ Parse and validate date
#     try:
#         parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
#     except ValueError:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid date format. Use YYYY-MM-DD"
#         )

#     # 2️⃣ Fetch all logbook shifts within the 7-hour shift window for that date
#     shifts = db.execute(text("""
#         SELECT * FROM logbook_shift_master
#         WHERE created_at >= DATE :date + INTERVAL '7 hour'
#           AND created_at < (DATE :date + INTERVAL '1 day' + INTERVAL '7 hour')
#     """), {"date": str(parsed_date)}).mappings().all()

#     if not shifts:
#         return {
#             "date": str(parsed_date),
#             "module": "fire_engine_test",
#             "message": "No shifts found for this date",
#             "fire_engine_test": None
#         }

#     # 3️⃣ Collect ms_logbook_ids from the shifts
#     ms_logbook_ids = [s["ms_logbook_id"] for s in shifts if s["ms_logbook_id"]]

#     if not ms_logbook_ids:
#         return {
#             "date": str(parsed_date),
#             "module": "fire_engine_test",
#             "message": "No valid logbook IDs found for this date",
#             "fire_engine_test": None
#         }

#     # 4️⃣ Fetch all fire_engine_test_masters linked via ms_logbook_id
#     masters = db.execute(text("""
#     SELECT m.*,
#            c.first_name || ' ' || c.last_name AS created_by_name,
#            u.first_name || ' ' || u.last_name AS updated_by_name
#     FROM fire_engine_test_master m
#     LEFT JOIN users c ON c.user_id = m.created_by
#     LEFT JOIN users u ON u.user_id = m.updated_by
#     WHERE m.ms_logbook_id = ANY(:ms_logbook_ids)
# """), {"ms_logbook_ids": ms_logbook_ids}).mappings().all()

#     if not masters:
#         return {
#             "date": str(parsed_date),
#             "module": "fire_engine_test",
#             "message": "Fire Engine Test not created for this date",
#             "fire_engine_test": None
#         }

#     # 5️⃣ Fetch all entries using fire_ids from the found masters
#     fire_ids = [m["fire_id"] for m in masters]

#     entries = db.execute(text("""
#     SELECT e.*,
#            c.first_name || ' ' || c.last_name AS created_by_name,
#            u.first_name || ' ' || u.last_name AS updated_by_name
#     FROM fire_engine_test_entry e
#     LEFT JOIN users c ON c.user_id = e.created_by
#     LEFT JOIN users u ON u.user_id = e.updated_by
#     WHERE e.master_id = ANY(:fire_ids)
#     ORDER BY e.master_id, e.entry_date, e.time_start
# """), {"fire_ids": fire_ids}).mappings().all()

#     # 6️⃣ Group entries under their respective master
#     from collections import defaultdict
#     entries_by_master = defaultdict(list)
#     for entry in entries:
#         entries_by_master[entry["master_id"]].append(dict(entry))

#     # 7️⃣ Final response
#     result = [
#         {
#             "master": dict(m),
#             "entries": entries_by_master.get(m["fire_id"], [])
#         }
#         for m in masters
#     ]

#     return {
#         "date": str(parsed_date),
#         "module": "fire_engine_test",
#         "fire_engine_test": result
#     }


@router.get("/fire-engine-test/day_wise")
def get_fire_engine_test(
    date: str,          
    station_id: int,    
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
            "station_id": station_id,
            "module": "fire_engine_test",
            "message": "No shifts found for this date",
            "fire_engine_test": None
        }

    # 3️⃣ Collect ms_logbook_ids from the shifts
    ms_logbook_ids = [s["ms_logbook_id"] for s in shifts if s["ms_logbook_id"]]

    if not ms_logbook_ids:
        return {
            "date": str(parsed_date),
            "station_id": station_id,
            "module": "fire_engine_test",
            "message": "No valid logbook IDs found for this date",
            "fire_engine_test": None
        }

    # 4️⃣ Fetch all fire_engine_test_masters linked via ms_logbook_id
    #    Filter by station_id: use created_by user's station_id first,
    #    fall back to updated_by user's station_id if created_by is null
    masters = db.execute(text("""
        SELECT m.*,
               c.first_name || ' ' || c.last_name AS created_by_name,
               u.first_name || ' ' || u.last_name AS updated_by_name
        FROM fire_engine_test_master m
        LEFT JOIN users c ON c.user_id = m.created_by
        LEFT JOIN users u ON u.user_id = m.updated_by
        WHERE m.ms_logbook_id = ANY(:ms_logbook_ids)
          AND COALESCE(c.station_id, u.station_id) = :station_id
    """), {
        "ms_logbook_ids": ms_logbook_ids,
        "station_id": station_id
    }).mappings().all()

    if not masters:
        return {
            "date": str(parsed_date),
            "station_id": station_id,
            "module": "fire_engine_test",
            "message": "Fire Engine Test not created for this date",
            "fire_engine_test": None
        }

    # 5️⃣ Fetch all entries using fire_ids from the found masters
    fire_ids = [m["fire_id"] for m in masters]

    entries = db.execute(text("""
        SELECT e.*,
               c.first_name || ' ' || c.last_name AS created_by_name,
               u.first_name || ' ' || u.last_name AS updated_by_name
        FROM fire_engine_test_entry e
        LEFT JOIN users c ON c.user_id = e.created_by
        LEFT JOIN users u ON u.user_id = e.updated_by
        WHERE e.master_id = ANY(:fire_ids)
        ORDER BY e.master_id, e.entry_date, e.time_start
    """), {"fire_ids": fire_ids}).mappings().all()

    # 6️⃣ Group entries under their respective master
    from collections import defaultdict
    entries_by_master = defaultdict(list)
    for entry in entries:
        entries_by_master[entry["master_id"]].append(dict(entry))

    # 7️⃣ Final response
    result = [
        {
            "master": dict(m),
            "entries": entries_by_master.get(m["fire_id"], [])
        }
        for m in masters
    ]

    return {
        "date": str(parsed_date),
        "station_id": station_id,
        "module": "fire_engine_test",
        "fire_engine_test": result
    }



@router.get("/{fire_id}")
def get_fire_engine_test(
    fire_id: int,
    db: Session = Depends(get_db)
):
    data = crud.get_fire_engine_test_by_id(db, fire_id)
    if not data:
        raise HTTPException(status_code=404, detail="Record not found")
    return data

@router.put("/{fire_id}")
def update_fire_engine_test(
    fire_id: int,
    payload: FireEngineTestMasterUpdate,
    db: Session = Depends(get_db)
):
    data = crud.update_fire_engine_test(db, fire_id, payload)
    if not data:
        raise HTTPException(status_code=404, detail="Record not found")
    return data

@router.delete("/{fire_id}")
def delete_fire_engine_test(
    fire_id: int,
    db: Session = Depends(get_db)
):
    result = crud.delete_fire_engine_test(db, fire_id)
    if not result:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"message": "Record deleted successfully"}
