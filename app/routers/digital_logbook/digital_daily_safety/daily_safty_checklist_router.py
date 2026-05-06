from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.crud.digital_logbook.digital_daily_safety.daily_safty_checklist_crud import create_daily_safety_checklist, delete_daily_safety_checklist, update_daily_safety_checklist
from app.database import get_db
from app.schemas.digital_logbook.digital_daily_safety.daily_safty_checklist_schemas import DailySafetyChecklistCreate, DailySafetyChecklistUpdate
from app.utils.access_service import validate_token


router = APIRouter(
    prefix="/daily-safety-checklist",
    tags=["Daily Safety Checklist"]
)


@router.post("",dependencies=[Depends(validate_token)])
def create_checklist(payload: DailySafetyChecklistCreate, db: Session = Depends(get_db)):
    dsc_id = create_daily_safety_checklist(db, payload)
    return {"message": "Checklist created", "dsc_id": dsc_id}


@router.put("/{dsc_id}",dependencies=[Depends(validate_token)])
def update_checklist(
    dsc_id: int,
    payload: DailySafetyChecklistUpdate,
    db: Session = Depends(get_db)
):
    update_daily_safety_checklist(db, dsc_id, payload)
    return {"message": "Checklist updated"}


# @router.delete("/{dsc_id}",dependencies=[Depends(validate_token)])
# def delete_checklist(dsc_id: int, db: Session = Depends(get_db)):
#     delete_daily_safety_checklist(db, dsc_id)
#     return {"message": "Checklist deleted"}


# @router.get("/{dsc_id}", dependencies=[Depends(validate_token)])
# def get_daily_safety_checklist_by_id(
#     dsc_id: int,
#     db: Session = Depends(get_db)
# ):
#     sql = text("""
#         SELECT *
#         FROM daily_safety_checklist
#         WHERE dsc_id = :dsc_id
#     """)

#     checklist = db.execute(
#         sql,
#         {"dsc_id": dsc_id}
#     ).mappings().first()

#     if not checklist:
#         raise HTTPException(
#             status_code=404,
#             detail="Daily safety checklist not found"
#         )

#     return {
#         "module": "daily_safety_checklist",
#         "safety_checklist": checklist
#     }

@router.get("/by-date-station/{date}/{station_id}", dependencies=[Depends(validate_token)])
def get_daily_safety_checklist_by_date_station(
    date: str,
    station_id: int,
    db: Session = Depends(get_db)
):

    # 1️⃣ Get station_name
    station_sql = text("""
        SELECT station_name
        FROM station
        WHERE station_id = :station_id
        AND is_deleted = false
    """)

    station = db.execute(
        station_sql,
        {"station_id": station_id}
    ).mappings().first()

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    station_name = station["station_name"]

    # 2️⃣ Fetch checklist by date + station_name
    checklist_sql = text("""
        SELECT *
        FROM daily_safety_checklist
        WHERE DATE(created_at) = :date
        AND station = :station_name
        ORDER BY created_at DESC
    """)

    result = db.execute(
        checklist_sql,
        {
            "date": date,
            "station_name": station_name
        }
    ).mappings().all()

    return {
        "date": date,
        "station_id": station_id,
        "station_name": station_name,
        "count": len(result),
        "data": result
    }
# @router.get("/by-date/{date}", dependencies=[Depends(validate_token)])
# def get_daily_safety_checklist_by_date(
#     date: str,
#     db: Session = Depends(get_db)
# ):
#     sql = text("""
#         SELECT *
#         FROM daily_safety_checklist
#         WHERE DATE(created_at) = :date
#         ORDER BY created_at DESC
#     """)

#     result = db.execute(sql, {"date": date}).mappings().all()

#     if not result:
#         return {
#             "message": "No checklist found for this date",
#             "data": []
#         }

#     return {
#         "date": date,
#         "count": len(result),
#         "data": result
#     }

# @router.get("/latest-by-date/{log_date}", dependencies=[Depends(validate_token)])
# def get_daily_safety_checklist_by_date(
#     log_date: str,
#     db: Session = Depends(get_db)
# ):
#     sql = text("""
#         SELECT d.*
#         FROM logbook_shift_master lsm
#         JOIN daily_safety_checklist d
#         ON lsm.dsc_id = d.dsc_id
#         WHERE lsm.created_at >= DATE :log_date + INTERVAL '7 hour'
#         AND lsm.created_at < (DATE :log_date + INTERVAL '1 day' + INTERVAL '7 hour')
#         LIMIT 1
#     """)

#     checklist = db.execute(
#         sql,
#         {"log_date": log_date}
#     ).mappings().first()

#     if not checklist:
#         return {
#             "module": "daily_safety_checklist",
#             "message": "No checklist found for this operational day",
#             "safety_checklist": None
#         }

#     return {
#         "module": "daily_safety_checklist",
#         "safety_checklist": checklist
#     }



# @router.get("/safety-checklist/{ms_logbook_id}")
# def get_daily_safety_checklist(
#     ms_logbook_id: int,
#     db: Session = Depends(get_db)
# ):
#     # 1️⃣ Fetch shift master
#     shift_sql = text("""
#         SELECT *
#         FROM logbook_shift_master
#         WHERE ms_logbook_id = :ms_logbook_id
#     """)

#     shift = db.execute(
#         shift_sql,
#         {"ms_logbook_id": ms_logbook_id}
#     ).mappings().first()

#     if not shift:
#         raise HTTPException(
#             status_code=404,
#             detail="Logbook shift master not found"
#         )

#     # 2️⃣ Extract dsc_id
#     dsc_id = shift["dsc_id"]

#     if not dsc_id:
#         return {
#             "ms_logbook_id": ms_logbook_id,
#             "module": "daily_safety_checklist",
#             "message": "Daily Safety Checklist not created for this shift",
#             "safety_checklist": None
#         }

#     # 3️⃣ Fetch safety checklist master
#     checklist_sql = text("""
#         SELECT *
#         FROM daily_safety_checklist
#         WHERE dsc_id = :dsc_id
#     """)

#     checklist = db.execute(
#         checklist_sql,
#         {"dsc_id": dsc_id}
#     ).mappings().first()

#     if not checklist:
#         return {
#             "ms_logbook_id": ms_logbook_id,
#             "module": "daily_safety_checklist",
#             "message": "Safety checklist record missing",
#             "safety_checklist": None
#         }

#     # 4️⃣ Final response
#     return {
#         "ms_logbook_id": ms_logbook_id,
#         "module": "daily_safety_checklist",
#         "safety_checklist": checklist
#     }
