# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.crud.digital_logbook.digital_logbook_main.logbook_shift_master_crud import create_shift_master, delete_shift_master, get_all_shift_masters, get_shift_master_by_id, update_shift_master
# from app.database import get_db
# from app.schemas.digital_logbook.digital_logbook_main.logbook_shift_master_schemas import LogbookShiftMasterCreate, LogbookShiftMasterUpdate
# from app.utils.access_service import validate_token
# from fastapi import APIRouter, Depends, Query, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import text
# from datetime import date

# router = APIRouter(
#     prefix="/logbook-shift-master",
#     tags=["Logbook Shift Master"],dependencies=[Depends(validate_token)]
# )


# @router.post("/", response_model=dict)
# def create_master(payload: LogbookShiftMasterCreate, db: Session = Depends(get_db)):
#     master_id = create_shift_master(db, payload)
#     return {
#         "message": "Shift master created successfully",
#         "ms_logbook_id": master_id
#     }





# @router.get("/", response_model=dict)
# def get_all_masters(db: Session = Depends(get_db)):
#     data = get_all_shift_masters(db)
#     return {
#         "message": "Shift master list fetched successfully",
#         "count": len(data),
#         "data": data
#     }

# @router.get("/shift-logs/view-logs")
# def get_view_logs_by_date_and_shift(
#     log_date: date = Query(..., description="Date in YYYY-MM-DD format"),
#     shift_id: int = Query(..., description="Shift ID (1=A, 2=B, 3=C)"),
#     db: Session = Depends(get_db)
# ):
#     query = """
#         SELECT
#             lsm.ms_logbook_id,
#             lsm.log_date,

#             -- Shift A
#             lsm.shift_a_start_time,
#             lsm.shift_a_end_time,
#             lsm.shift_a_status,
#             lsm.shift_a_engineer,
#             lsm.shift_a_handover_notes,

#             -- Shift B
#             lsm.shift_b_start_time,
#             lsm.shift_b_end_time,
#             lsm.shift_b_status,
#             lsm.shift_b_engineer,
#             lsm.shift_b_handover_notes,

#             -- Shift C
#             lsm.shift_c_start_time,
#             lsm.shift_c_end_time,
#             lsm.shift_c_status,
#             lsm.shift_c_engineer,
#             lsm.shift_c_handover_notes,

#             -- Current active incharge for this shift
#             ssi.user_id                     AS incharge_user_id,
#             ssi.responsibility_from,
#             ssi.responsibility_to,
#             ssi.comment_for_next_incharge,
#             ssi.handover_requested_at,
#             ssi.handover_accepted_at,
#             ssi.handover_to_user_id,

#             u.first_name || ' ' || u.last_name  AS incharge_name,

#             -- Latest handover event for this shift
#             shl.event_type                  AS latest_handover_event,
#             shl.event_time                  AS latest_handover_time,
#             shl.remarks                     AS handover_remarks,

#             uf.first_name || ' ' || uf.last_name AS from_user_name,
#             ut.first_name || ' ' || ut.last_name AS to_user_name

#         FROM logbook_shift_master lsm

#         -- Active incharge for this shift_id
#         LEFT JOIN station_shift_incharge ssi
#             ON ssi.shift_id = :shift_id
#             AND ssi.responsibility_to IS NULL

#         LEFT JOIN users u
#             ON u.user_id = ssi.user_id

#         -- Latest handover log entry for this shift
#         LEFT JOIN shift_handover_log shl
#             ON shl.id = (
#                 SELECT id FROM shift_handover_log
#                 WHERE shift_id = :shift_id
#                 ORDER BY event_time DESC
#                 LIMIT 1
#             )

#         LEFT JOIN users uf ON uf.user_id = shl.from_user_id
#         LEFT JOIN users ut ON ut.user_id = shl.to_user_id

#         WHERE lsm.log_date = :log_date
#         ORDER BY lsm.ms_logbook_id ASC
#     """

#     result = db.execute(text(query), {
#         "log_date": log_date,
#         "shift_id": shift_id
#     })
#     rows = result.mappings().all()

#     if not rows:
#         raise HTTPException(status_code=404, detail="No logs found for given date and shift")

#     response = []
#     for row in rows:
#         row = dict(row)

#         # Pick correct shift data based on shift_id
#         if shift_id == 1:
#             shift_data = {
#                 "shift": "A",
#                 "start_time": str(row["shift_a_start_time"]) if row["shift_a_start_time"] else None,
#                 "end_time": str(row["shift_a_end_time"]) if row["shift_a_end_time"] else None,
#                 "status": row["shift_a_status"],
#                 "engineer": row["shift_a_engineer"],
#                 "handover_notes": row["shift_a_handover_notes"],
#             }
#         elif shift_id == 2:
#             shift_data = {
#                 "shift": "B",
#                 "start_time": str(row["shift_b_start_time"]) if row["shift_b_start_time"] else None,
#                 "end_time": str(row["shift_b_end_time"]) if row["shift_b_end_time"] else None,
#                 "status": row["shift_b_status"],
#                 "engineer": row["shift_b_engineer"],
#                 "handover_notes": row["shift_b_handover_notes"],
#             }
#         else:
#             shift_data = {
#                 "shift": "C",
#                 "start_time": str(row["shift_c_start_time"]) if row["shift_c_start_time"] else None,
#                 "end_time": str(row["shift_c_end_time"]) if row["shift_c_end_time"] else None,
#                 "status": row["shift_c_status"],
#                 "engineer": row["shift_c_engineer"],
#                 "handover_notes": row["shift_c_handover_notes"],
#             }

#         response.append({
#             "ms_logbook_id": row["ms_logbook_id"],
#             "log_date": str(row["log_date"]),
#             "shift_info": shift_data,
#             "incharge": {
#                 "user_id": row["incharge_user_id"],
#                 "name": row["incharge_name"],
#                 "responsibility_from": str(row["responsibility_from"]) if row["responsibility_from"] else None,
#                 "responsibility_to": str(row["responsibility_to"]) if row["responsibility_to"] else None,
#                 "comment_for_next_incharge": row["comment_for_next_incharge"],
#                 "handover_requested_at": str(row["handover_requested_at"]) if row["handover_requested_at"] else None,
#                 "handover_accepted_at": str(row["handover_accepted_at"]) if row["handover_accepted_at"] else None,
#             },
#             "latest_handover": {
#                 "event_type": row["latest_handover_event"],
#                 "event_time": str(row["latest_handover_time"]) if row["latest_handover_time"] else None,
#                 "remarks": row["handover_remarks"],
#                 "from_user": row["from_user_name"],
#                 "to_user": row["to_user_name"],
#             }
#         })

#     return {
#         "log_date": str(log_date),
#         "shift_id": shift_id,
#         "total_records": len(response),
#         "data": response
#     }




# @router.put("/{master_id}", response_model=dict)
# def update_master(
#     master_id: int,
#     payload: LogbookShiftMasterUpdate,
#     db: Session = Depends(get_db)
# ):
#     update_shift_master(db, master_id, payload)
#     return {"message": "Shift master updated successfully"}


# @router.delete("/{master_id}", response_model=dict)
# def delete_master(master_id: int, db: Session = Depends(get_db)):
#     delete_shift_master(db, master_id)
#     return {"message": "Shift master deleted successfully"}




# @router.get("/{master_id}", response_model=dict)
# def get_master_by_id(master_id: int, db: Session = Depends(get_db)):
#     data = get_shift_master_by_id(db, master_id)
#     if not data:
#         raise HTTPException(status_code=404, detail="Shift master not found")

#     return {
#         "message": "Shift master fetched successfully",
#         "data": data
#     }


# @router.get("/shift-logs/{log_date}")
# def get_shift_logs_by_date(
#     log_date: date,
#     db: Session = Depends(get_db)
# ):
#     query = """
#         SELECT
#             ms_logbook_id,
#             log_date,

#             shift_a,
#             shift_a_start_time,
#             shift_a_end_time,
#             shift_a_status,
#             shift_a_engineer,
#             shift_a_handover_notes,

#             shift_b,
#             shift_b_start_time,
#             shift_b_end_time,
#             shift_b_status,
#             shift_b_engineer,
#             shift_b_handover_notes,

#             shift_c,
#             shift_c_start_time,
#             shift_c_end_time,
#             shift_c_status,
#             shift_c_engineer,
#             shift_c_handover_notes

#         FROM logbook_shift_master
#         WHERE log_date = :log_date
#     """

#     result = db.execute(text(query), {"log_date": log_date})  # no await
#     row = result.mappings().first()

#     if not row:
#         raise HTTPException(status_code=404, detail=f"No shift logs found for date: {log_date}")

#     return {
#     "ms_logbook_id": row["ms_logbook_id"],
#     "log_date": str(row["log_date"]),
#     "shift_a": {
#         "name": "Shift A",   # hardcoded, ignore DB value
#         "start_time": str(row["shift_a_start_time"]) if row["shift_a_start_time"] else None,
#         "end_time": str(row["shift_a_end_time"]) if row["shift_a_end_time"] else None,
#         "status": row["shift_a_status"],
#         "engineer": row["shift_a_engineer"],
#         "handover_notes": row["shift_a_handover_notes"],
#     },
#     "shift_b": {
#         "name": "Shift B",
#         "start_time": str(row["shift_b_start_time"]) if row["shift_b_start_time"] else None,
#         "end_time": str(row["shift_b_end_time"]) if row["shift_b_end_time"] else None,
#         "status": row["shift_b_status"],
#         "engineer": row["shift_b_engineer"],
#         "handover_notes": row["shift_b_handover_notes"],
#     },
#     "shift_c": {
#         "name": "Shift C",
#         "start_time": str(row["shift_c_start_time"]) if row["shift_c_start_time"] else None,
#         "end_time": str(row["shift_c_end_time"]) if row["shift_c_end_time"] else None,
#         "status": row["shift_c_status"],
#         "engineer": row["shift_c_engineer"],
#         "handover_notes": row["shift_c_handover_notes"],
#     },
# }

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime

from app.crud.digital_logbook.digital_logbook_main.logbook_shift_master_crud import create_shift_master, delete_shift_master, get_all_shift_masters, get_shift_master_by_id, update_shift_master
from app.database import get_db
from app.schemas.digital_logbook.digital_logbook_main.logbook_shift_master_schemas import LogbookShiftMasterCreate, LogbookShiftMasterUpdate
from app.utils.access_service import validate_token

router = APIRouter(
    prefix="/logbook-shift-master",
    tags=["Logbook Shift Master"],
    dependencies=[Depends(validate_token)]
)

# ✅ 1. POST
@router.post("/", response_model=dict)
def create_master(payload: LogbookShiftMasterCreate, db: Session = Depends(get_db)):
    master_id = create_shift_master(db, payload)
    return {"message": "Shift master created successfully", "ms_logbook_id": master_id}


#  2. GET ALL
@router.get("/", response_model=dict)
def get_all_masters(db: Session = Depends(get_db)):
    data = get_all_shift_masters(db)
    return {"message": "Shift master list fetched successfully", "count": len(data), "data": data}


#  3. STATIC routes FIRST — before any /{param} routes



@router.get("/shift-logs/view-logs")
def get_view_logs_by_date_and_shift(
    log_date: date = Query(..., description="Date in YYYY-MM-DD format"),
    shift_id: int = Query(..., description="Shift ID (1=A, 2=B, 3=C)"),
    db: Session = Depends(get_db)
):
    # query = """
    #     SELECT
    #         lsm.ms_logbook_id,
    #         lsm.log_date,
    #         lsm.shift_a_start_time, lsm.shift_a_end_time, lsm.shift_a_status, lsm.shift_a_engineer, lsm.shift_a_handover_notes,
    #         lsm.shift_b_start_time, lsm.shift_b_end_time, lsm.shift_b_status, lsm.shift_b_engineer, lsm.shift_b_handover_notes,
    #         lsm.shift_c_start_time, lsm.shift_c_end_time, lsm.shift_c_status, lsm.shift_c_engineer, lsm.shift_c_handover_notes
    #     FROM logbook_shift_master lsm
    #     WHERE lsm.log_date = :log_date
    #     ORDER BY lsm.ms_logbook_id ASC
    # """

    query = """
        WITH selected_shift AS (
            SELECT shift_id, start_time, end_time
            FROM shift
            WHERE shift_id = :shift_id   -- ✅ USE PARAM
        )

        SELECT
            lsm.ms_logbook_id,
            lsm.log_date,

            lsm.shift_a_start_time, lsm.shift_a_end_time, lsm.shift_a_status, lsm.shift_a_engineer, lsm.shift_a_handover_notes,
            lsm.shift_b_start_time, lsm.shift_b_end_time, lsm.shift_b_status, lsm.shift_b_engineer, lsm.shift_b_handover_notes,
            lsm.shift_c_start_time, lsm.shift_c_end_time, lsm.shift_c_status, lsm.shift_c_engineer, lsm.shift_c_handover_notes

        FROM logbook_shift_master lsm
        JOIN selected_shift ss
            ON (
                -- ✅ Normal shift
                (
                    ss.start_time < ss.end_time
                    AND CAST(lsm.created_at AS time) >= ss.start_time
                    AND CAST(lsm.created_at AS time) < ss.end_time
                )

                OR

                -- ✅ Overnight shift
                (
                    ss.start_time > ss.end_time
                    AND (
                        CAST(lsm.created_at AS time) >= ss.start_time
                        OR CAST(lsm.created_at AS time) < ss.end_time
                    )
                )
            )

        WHERE lsm.log_date = :log_date

        ORDER BY lsm.ms_logbook_id ASC;
    """

    # Separate query for latest handover log for this shift
    handover_query = """
        SELECT
            shl.id,
            shl.event_type,
            shl.event_time,
            shl.remarks,
            shl.is_acknowledge,
            uf.first_name || ' ' || uf.last_name AS from_user_name,
            ut.first_name || ' ' || ut.last_name AS to_user_name
        FROM shift_handover_log shl
        LEFT JOIN users uf ON uf.user_id = shl.from_user_id
        LEFT JOIN users ut ON ut.user_id = shl.to_user_id
        WHERE shl.shift_id = :shift_id
        ORDER BY shl.event_time DESC
        LIMIT 1
    """

    result = db.execute(text(query), {"log_date": log_date,"shift_id": shift_id })
    rows = result.mappings().all()

    # ✅ Allow empty result
    rows = rows or []

    # if not rows:
    #     raise HTTPException(status_code=404, detail="No logs found for given date and shift")

    handover_result = db.execute(text(handover_query), {"shift_id": shift_id})
    handover = handover_result.mappings().first()

    shift_map = {
        1: ("A", "shift_a_start_time", "shift_a_end_time", "shift_a_status", "shift_a_engineer", "shift_a_handover_notes"),
        2: ("B", "shift_b_start_time", "shift_b_end_time", "shift_b_status", "shift_b_engineer", "shift_b_handover_notes"),
        3: ("C", "shift_c_start_time", "shift_c_end_time", "shift_c_status", "shift_c_engineer", "shift_c_handover_notes"),
    }

    if shift_id not in shift_map:
        raise HTTPException(status_code=400, detail="Invalid shift_id. Use 1=A, 2=B, 3=C")

    shift_label, s_start, s_end, s_status, s_engineer, s_notes = shift_map[shift_id]

    data = []

    for row in rows:
        row = dict(row)

        data.append({
            "ms_logbook_id": row["ms_logbook_id"],
            "log_date": str(row["log_date"]),
            "shift_info": {
                "shift": shift_label,
                "start_time": str(row[s_start]) if row[s_start] else None,
                "end_time": str(row[s_end]) if row[s_end] else None,
                "status": row[s_status],
                "engineer": row[s_engineer],
                "handover_notes": row[s_notes] or "",
            }
        })


    # -------------------------------
    # 🔥 OVERALL STATUS LOGIC
    # -------------------------------
    shift_time_query = text("""
        SELECT shift_id, start_time, end_time
        FROM shift
        ORDER BY shift_id
    """)

    shift_times = db.execute(shift_time_query).mappings().all()

    today = date.today()
    current_time = datetime.now().time()


    def get_shift_status_by_time_and_date(
        shift_id,
        shift_times,
        current_time,
        log_date
    ):
        # ✅ If past date → completed
        if log_date < today:
            return "completed"

        # ✅ If future date → not started
        if log_date > today:
            return "not_started"

        # ✅ Same day → use time logic
        current_shift_id = None

        for shift in shift_times:
            start = shift["start_time"]
            end = shift["end_time"]

            # Normal shift
            if start < end:
                if start <= current_time <= end:
                    current_shift_id = shift["shift_id"]
                    break

            # Overnight shift
            else:
                if current_time >= start or current_time <= end:
                    current_shift_id = shift["shift_id"]
                    break

        if current_shift_id is None:
            return "not_started"

        if shift_id == current_shift_id:
            return "ongoing"
        elif shift_id < current_shift_id:
            return "completed"
        else:
            return "not_started"


    shift_overall_status = get_shift_status_by_time_and_date(
        shift_id,
        shift_times,
        current_time,
        log_date
    )

    return {
        "log_date": str(log_date),
        "shift_id": shift_id,
        "total_records": len(data),

        "shift_overall_status": shift_overall_status,

        # ✅ Top level — overall handover status for this shift
        "is_acknowledge": handover["is_acknowledge"] if handover else None,
        # "handover_event_type": handover["event_type"] if handover else None,
        "acknowledge_remarks": handover["remarks"] if handover else None,
        # "from_user_name": handover["from_user_name"] if handover else None,
        # "to_user_name": handover["to_user_name"] if handover else None,

        "data": data
    }



# @router.get("/shift-logs/{log_date}")
# def get_shift_logs_by_date(log_date: date, db: Session = Depends(get_db)):
#     cards_query = """
#         SELECT
#             COUNT(*) AS total_records,

#             COUNT(CASE WHEN lsm.shift_a_status IS NOT NULL AND lsm.shift_a_status != '' THEN 1 END) AS shift_a_log_count,
#             COUNT(CASE WHEN lsm.shift_a_status = 'in_progress' THEN 1 END)                          AS shift_a_pending,

#             COUNT(CASE WHEN lsm.shift_b_status IS NOT NULL AND lsm.shift_b_status != '' THEN 1 END) AS shift_b_log_count,
#             COUNT(CASE WHEN lsm.shift_b_status = 'in_progress' THEN 1 END)                          AS shift_b_pending,

#             COUNT(CASE WHEN lsm.shift_c_status IS NOT NULL AND lsm.shift_c_status != '' THEN 1 END) AS shift_c_log_count,
#             COUNT(CASE WHEN lsm.shift_c_status = 'in_progress' THEN 1 END)                          AS shift_c_pending,

#             -- ✅ Timings from shift table
#             sa.start_time AS shift_a_start_time,
#             sa.end_time   AS shift_a_end_time,
#             sb.start_time AS shift_b_start_time,
#             sb.end_time   AS shift_b_end_time,
#             sc.start_time AS shift_c_start_time,
#             sc.end_time   AS shift_c_end_time

#         FROM logbook_shift_master lsm
#         LEFT JOIN shift sa ON sa.shift_id = 1
#         LEFT JOIN shift sb ON sb.shift_id = 2
#         LEFT JOIN shift sc ON sc.shift_id = 3

#         WHERE lsm.log_date = :log_date

#         -- ✅ GROUP BY all non-aggregate columns
#         GROUP BY
#             sa.start_time, sa.end_time,
#             sb.start_time, sb.end_time,
#             sc.start_time, sc.end_time
#     """

#         # Query 2: all rows for detailed shift list
        
#     rows_query = """
#         SELECT
#             ms_logbook_id,
#             log_date,
#             shift_a_start_time, shift_a_end_time, shift_a_status, shift_a_engineer, shift_a_handover_notes,
#             shift_b_start_time, shift_b_end_time, shift_b_status, shift_b_engineer, shift_b_handover_notes,
#             shift_c_start_time, shift_c_end_time, shift_c_status, shift_c_engineer, shift_c_handover_notes
#         FROM logbook_shift_master
#         WHERE log_date = :log_date
#         ORDER BY ms_logbook_id ASC
#     """

#     cards_result = db.execute(text(cards_query), {"log_date": log_date})
#     cards_row = cards_result.mappings().first()

#     if not cards_row or cards_row["total_records"] == 0:
#         raise HTTPException(status_code=404, detail=f"No shift logs found for date: {log_date}")

#     rows_result = db.execute(text(rows_query), {"log_date": log_date})
#     rows = rows_result.mappings().all()

#     return {
#         "log_date": str(log_date),
#         "total_records": cards_row["total_records"],

#         # ✅ Cards with proper timings from shift table
#         "shift_cards": {
#             "shift_a": {
#                 "name": "Shift A",
#                 "time_range": f"{cards_row['shift_a_start_time']} - {cards_row['shift_a_end_time']}" if cards_row["shift_a_start_time"] else None,
#                 "log_count": cards_row["shift_a_log_count"],
#                 "pending": cards_row["shift_a_pending"],
#             },
#             "shift_b": {
#                 "name": "Shift B",
#                 "time_range": f"{cards_row['shift_b_start_time']} - {cards_row['shift_b_end_time']}" if cards_row["shift_b_start_time"] else None,
#                 "log_count": cards_row["shift_b_log_count"],
#                 "pending": cards_row["shift_b_pending"],
#             },
#             "shift_c": {
#                 "name": "Shift C",
#                 "time_range": f"{cards_row['shift_c_start_time']} - {cards_row['shift_c_end_time']}" if cards_row["shift_c_start_time"] else None,
#                 "log_count": cards_row["shift_c_log_count"],
#                 "pending": cards_row["shift_c_pending"],
#             },
#         },

#         # ✅ Detailed rows
#         "shift_a_logs": [
#             {
#                 "ms_logbook_id": row["ms_logbook_id"],
#                 "log_date": str(row["log_date"]),
#                 "name": "Shift A",
#                 "start_time": str(row["shift_a_start_time"]) if row["shift_a_start_time"] else None,
#                 "end_time": str(row["shift_a_end_time"]) if row["shift_a_end_time"] else None,
#                 "status": row["shift_a_status"],
#                 "engineer": row["shift_a_engineer"],
#                 "handover_notes": row["shift_a_handover_notes"] or "",
#             }
#             for row in rows if row["shift_a_status"]
#         ],
#         "shift_b_logs": [
#             {
#                 "ms_logbook_id": row["ms_logbook_id"],
#                 "log_date": str(row["log_date"]),
#                 "name": "Shift B",
#                 "start_time": str(row["shift_b_start_time"]) if row["shift_b_start_time"] else None,
#                 "end_time": str(row["shift_b_end_time"]) if row["shift_b_end_time"] else None,
#                 "status": row["shift_b_status"],
#                 "engineer": row["shift_b_engineer"],
#                 "handover_notes": row["shift_b_handover_notes"] or "",
#             }
#             for row in rows if row["shift_b_status"]
#         ],
#         "shift_c_logs": [
#             {
#                 "ms_logbook_id": row["ms_logbook_id"],
#                 "log_date": str(row["log_date"]),
#                 "name": "Shift C",
#                 "start_time": str(row["shift_c_start_time"]) if row["shift_c_start_time"] else None,
#                 "end_time": str(row["shift_c_end_time"]) if row["shift_c_end_time"] else None,
#                 "status": row["shift_c_status"],
#                 "engineer": row["shift_c_engineer"],
#                 "handover_notes": row["shift_c_handover_notes"] or "",
#             }
#             for row in rows if row["shift_c_status"]
#         ],
#     }






@router.get("/{log_date}/station/{station_id}")
def get_shift_logs_by_date_and_station(
    log_date: date,
    station_id: int,
    db: Session = Depends(get_db)
):
    cards_query = """
        SELECT
            COUNT(*) AS total_records,

            COUNT(CASE WHEN lsm.shift_a_status IS NOT NULL AND lsm.shift_a_status != '' THEN 1 END) AS shift_a_log_count,
            COUNT(CASE WHEN lsm.shift_a_status = 'in_progress' THEN 1 END)                          AS shift_a_pending,

            COUNT(CASE WHEN lsm.shift_b_status IS NOT NULL AND lsm.shift_b_status != '' THEN 1 END) AS shift_b_log_count,
            COUNT(CASE WHEN lsm.shift_b_status = 'in_progress' THEN 1 END)                          AS shift_b_pending,

            COUNT(CASE WHEN lsm.shift_c_status IS NOT NULL AND lsm.shift_c_status != '' THEN 1 END) AS shift_c_log_count,
            COUNT(CASE WHEN lsm.shift_c_status = 'in_progress' THEN 1 END)                          AS shift_c_pending,

            sa.start_time AS shift_a_start_time,
            sa.end_time   AS shift_a_end_time,
            sb.start_time AS shift_b_start_time,
            sb.end_time   AS shift_b_end_time,
            sc.start_time AS shift_c_start_time,
            sc.end_time   AS shift_c_end_time

        FROM logbook_shift_master lsm
        INNER JOIN users u ON u.user_id = lsm.created_by   -- ✅ resolve station_id
        LEFT JOIN shift sa ON sa.shift_id = 1
        LEFT JOIN shift sb ON sb.shift_id = 2
        LEFT JOIN shift sc ON sc.shift_id = 3

        WHERE lsm.log_date = :log_date
          AND u.station_id = :station_id                    -- ✅ added filter

        GROUP BY
            sa.start_time, sa.end_time,
            sb.start_time, sb.end_time,
            sc.start_time, sc.end_time
    """

    rows_query = """
        SELECT
            lsm.ms_logbook_id,
            lsm.log_date,
            lsm.shift_a_start_time, lsm.shift_a_end_time, lsm.shift_a_status, lsm.shift_a_engineer, lsm.shift_a_handover_notes,
            lsm.shift_b_start_time, lsm.shift_b_end_time, lsm.shift_b_status, lsm.shift_b_engineer, lsm.shift_b_handover_notes,
            lsm.shift_c_start_time, lsm.shift_c_end_time, lsm.shift_c_status, lsm.shift_c_engineer, lsm.shift_c_handover_notes
        FROM logbook_shift_master lsm
        INNER JOIN users u ON u.user_id = lsm.created_by
        WHERE lsm.log_date = :log_date
          AND u.station_id = :station_id
        ORDER BY lsm.ms_logbook_id ASC
    """

    cards_result = db.execute(text(cards_query), {"log_date": log_date, "station_id": station_id})
    cards_row = cards_result.mappings().first()

    if not cards_row or cards_row["total_records"] == 0:
        raise HTTPException(status_code=404, detail=f"No shift logs found for date: {log_date} and station_id: {station_id}")

    rows_result = db.execute(text(rows_query), {"log_date": log_date, "station_id": station_id})
    rows = rows_result.mappings().all()

    # -------------------------------
    # 3️⃣ 🔥 NEW: TIME-BASED SHIFT STATUS
    # -------------------------------
    shift_time_query = text("""
        SELECT shift_id, start_time, end_time
        FROM shift
        ORDER BY shift_id
    """)

    shift_times = db.execute(shift_time_query).mappings().all()
    current_time = datetime.now().time()

    def get_current_shift(shift_times, current_time):
        for shift in shift_times:
            start = shift["start_time"]
            end = shift["end_time"]

            # Normal shift
            if start < end:
                if start <= current_time <= end:
                    return shift["shift_id"]

            # Overnight shift
            else:
                if current_time >= start or current_time <= end:
                    return shift["shift_id"]

        return None

    current_shift_id = get_current_shift(shift_times, current_time)

    # Default
    shift_overall_status = {
        "shift_a": "not_started",
        "shift_b": "not_started",
        "shift_c": "not_started"
    }

    # Set ongoing
    if current_shift_id == 1:
        shift_overall_status["shift_a"] = "ongoing"
    elif current_shift_id == 2:
        shift_overall_status["shift_b"] = "ongoing"
    elif current_shift_id == 3:
        shift_overall_status["shift_c"] = "ongoing"

    # Set completed for previous shifts
    if current_shift_id:
        for i in range(1, current_shift_id):
            if i == 1:
                shift_overall_status["shift_a"] = "completed"
            elif i == 2:
                shift_overall_status["shift_b"] = "completed"

    return {
        "log_date": str(log_date),
        "station_id": station_id,                          
        "total_records": cards_row["total_records"],

        "shift_overall_status": shift_overall_status,


        "shift_cards": {
            "shift_a": {
                "name": "Shift A",
                "time_range": f"{cards_row['shift_a_start_time']} - {cards_row['shift_a_end_time']}" if cards_row["shift_a_start_time"] else None,
                "log_count": cards_row["shift_a_log_count"],
                "pending": cards_row["shift_a_pending"],
            },
            "shift_b": {
                "name": "Shift B",
                "time_range": f"{cards_row['shift_b_start_time']} - {cards_row['shift_b_end_time']}" if cards_row["shift_b_start_time"] else None,
                "log_count": cards_row["shift_b_log_count"],
                "pending": cards_row["shift_b_pending"],
            },
            "shift_c": {
                "name": "Shift C",
                "time_range": f"{cards_row['shift_c_start_time']} - {cards_row['shift_c_end_time']}" if cards_row["shift_c_start_time"] else None,
                "log_count": cards_row["shift_c_log_count"],
                "pending": cards_row["shift_c_pending"],
            },
        },

        "shift_a_logs": [
            {
                "ms_logbook_id": row["ms_logbook_id"],
                "log_date": str(row["log_date"]),
                "name": "Shift A",
                "start_time": str(row["shift_a_start_time"]) if row["shift_a_start_time"] else None,
                "end_time": str(row["shift_a_end_time"]) if row["shift_a_end_time"] else None,
                "status": row["shift_a_status"],
                "engineer": row["shift_a_engineer"],
                "handover_notes": row["shift_a_handover_notes"] or "",
            }
            for row in rows if row["shift_a_status"]
        ],
        "shift_b_logs": [
            {
                "ms_logbook_id": row["ms_logbook_id"],
                "log_date": str(row["log_date"]),
                "name": "Shift B",
                "start_time": str(row["shift_b_start_time"]) if row["shift_b_start_time"] else None,
                "end_time": str(row["shift_b_end_time"]) if row["shift_b_end_time"] else None,
                "status": row["shift_b_status"],
                "engineer": row["shift_b_engineer"],
                "handover_notes": row["shift_b_handover_notes"] or "",
            }
            for row in rows if row["shift_b_status"]
        ],
        "shift_c_logs": [
            {
                "ms_logbook_id": row["ms_logbook_id"],
                "log_date": str(row["log_date"]),
                "name": "Shift C",
                "start_time": str(row["shift_c_start_time"]) if row["shift_c_start_time"] else None,
                "end_time": str(row["shift_c_end_time"]) if row["shift_c_end_time"] else None,
                "status": row["shift_c_status"],
                "engineer": row["shift_c_engineer"],
                "handover_notes": row["shift_c_handover_notes"] or "",
            }
            for row in rows if row["shift_c_status"]
        ],
    }





#  5. PUT — dynamic /{master_id} LAST
@router.put("/{master_id}", response_model=dict)
def update_master(master_id: int, payload: LogbookShiftMasterUpdate, db: Session = Depends(get_db)):
    update_shift_master(db, master_id, payload)
    return {"message": "Shift master updated successfully"}


#  6. DELETE
@router.delete("/{master_id}", response_model=dict)
def delete_master(master_id: int, db: Session = Depends(get_db)):
    delete_shift_master(db, master_id)
    return {"message": "Shift master deleted successfully"}


#  7. GET BY ID — dynamic /{master_id} LAST
@router.get("/{master_id}", response_model=dict)
def get_master_by_id(master_id: int, db: Session = Depends(get_db)):
    data = get_shift_master_by_id(db, master_id)
    if not data:
        raise HTTPException(status_code=404, detail="Shift master not found")
    return {"message": "Shift master fetched successfully", "data": data}

