from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date

from app.schemas.digital_logbook.digital_logbook_dkn.dkn_digital_logbook_schemas import DknDigitalLogBookCreate, DknDigitalLogBookUpdate


def create_logbook(db: Session, payload: DknDigitalLogBookCreate):
    query = text("""
        INSERT INTO dkn_digital_logbook (
            station,
            station_in_charge,
            shift,
            logbook_ref_no,
            log_date,
            start_time,
            handed_over_by,
            taken_over_by,
            is_shift_closed   ,created_at,created_by ,updated_at ,updated_by,                 
            hsn, ner, mlr, svb, ip1, sv9, sv10 ,ms_logbook_id

        )
        VALUES (
            :station,
            :station_in_charge,
            :shift,
            :logbook_ref_no,
            :log_date,
            :start_time,
            :handed_over_by,
            :taken_over_by,
            :is_shift_closed,:created_at,:created_by ,:updated_at ,:updated_by,
            :hsn, :ner, :mlr, :svb, :ip1, :sv9, :sv10,:ms_logbook_id

        )
        RETURNING dkn_logbook_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()
    return result.fetchone()[0]


def update_logbook(db: Session, logbook_id: int, payload: DknDigitalLogBookUpdate):
    query = text("""
        UPDATE dkn_digital_logbook
        SET
            station = COALESCE(:station, station),
            station_in_charge = COALESCE(:station_in_charge, station_in_charge),
            shift = COALESCE(:shift, shift),
            logbook_ref_no = COALESCE(:logbook_ref_no, logbook_ref_no),
            log_date = COALESCE(:log_date, log_date),
            start_time = COALESCE(:start_time, start_time),
            handed_over_by = COALESCE(:handed_over_by, handed_over_by),
            taken_over_by = COALESCE(:taken_over_by, taken_over_by),
            is_shift_closed = COALESCE(:is_shift_closed, is_shift_closed),
                             created_at       = COALESCE(:created_at, created_at),
            created_by       = COALESCE(:created_by, created_by),
            updated_at       = COALESCE(:updated_at, updated_at),
            updated_by       = COALESCE(:updated_by, updated_by),
            hsn        = COALESCE(:hsn, hsn),
            ner        = COALESCE(:ner, ner),
            mlr        = COALESCE(:mlr, mlr),
            svb        = COALESCE(:svb, svb),
            ip1        = COALESCE(:ip1, ip1),
            sv9        = COALESCE(:sv9, sv9),
            sv10       = COALESCE(:sv10, sv10),
            ms_logbook_id       = COALESCE(:ms_logbook_id, ms_logbook_id)                 
                 
        WHERE dkn_logbook_id = :logbook_id
    """)

    params = payload.dict()
    params["logbook_id"] = logbook_id

    db.execute(query, params)
    db.commit()
    return True


def delete_logbook(db: Session, logbook_id: int):
    query = text("""
        DELETE FROM dkn_digital_logbook
        WHERE dkn_logbook_id = :logbook_id
    """)

    db.execute(query, {"logbook_id": logbook_id})
    db.commit()
    return True


# def get_logbook_by_date(db: Session, log_date: date):

#     # -------------------------------
#     # 1️⃣ GET MAX LOGBOOK ID
#     # -------------------------------
#     max_query = text("""
#         SELECT MAX(dkn_logbook_id) AS max_id
#         FROM dkn_digital_logbook
#         WHERE ms_logbook_id IN (
#             SELECT LSM.ms_logbook_id
#             FROM logbook_shift_master LSM
#                     WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
#                     AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
            
#         )
#     """)

#     max_result = db.execute(max_query, {"log_date": log_date}).mappings().first()

#     if not max_result or not max_result["max_id"]:
#         return []

#     max_id = max_result["max_id"]

#     # -------------------------------
#     # 2️⃣ GET HEADER DATA
#     # -------------------------------
#     header_query = text("""
#         SELECT *
#         FROM dkn_digital_logbook
#         WHERE dkn_logbook_id = :max_id
#     """)

#     header_row = db.execute(header_query, {"max_id": max_id}).mappings().first()

#     if not header_row:
#         return []

#     # -------------------------------
#     # 3️⃣ GET ENTRY DATA (OPTIONAL)
#     # -------------------------------
#     entry_query = text("""
#         SELECT *
#         FROM dkn_digital_logbook_entry
#         WHERE logbook_id = :max_id
#     """)

#     logdata_rows = db.execute(entry_query, {"max_id": max_id}).mappings().all()

#     # -------------------------------
#     # 4️⃣ BUILD RESPONSE
#     # -------------------------------
#     response = dict(header_row)
#     response["logData"] = [dict(row) for row in logdata_rows] if logdata_rows else []

#     return [response]

def get_logbook_by_date(db: Session, log_date: date):

    # -------------------------------
    # RESPONSE STRUCTURE
    # -------------------------------
    response = {
        "Shift A": {"dkn_digital_log": [], "handover": []},
        "Shift B": {"dkn_digital_log": [], "handover": []},
        "Shift C": {"dkn_digital_log": [], "handover": []}
    }

    # -------------------------------
    # 1️⃣ GET ALL LOGBOOKS FOR THE DAY
    # -------------------------------
    header_query = text("""
        SELECT 
            ddl.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM dkn_digital_logbook ddl

        LEFT JOIN users u1
            ON u1.user_id = ddl.created_by

        LEFT JOIN users u2
            ON u2.user_id = ddl.updated_by

        WHERE ddl.ms_logbook_id IN (
            SELECT LSM.ms_logbook_id
            FROM logbook_shift_master LSM
            WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
            AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
        )

        ORDER BY ddl.dkn_logbook_id;
    """)

    header_rows = db.execute(header_query, {"log_date": log_date}).mappings().all()

    if not header_rows:
        return response

    # -------------------------------
    # 2️⃣ LOOP THROUGH EACH LOGBOOK
    # -------------------------------
    for header in header_rows:

        shift_name = header.get("shift")

        if shift_name not in response:
            continue

        logbook_id = header["dkn_logbook_id"]

        # -------------------------------
        # GET ENTRY DATA
        # -------------------------------
        entry_query = text("""
            SELECT 
            dle.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM dkn_digital_logbook_entry dle

        LEFT JOIN users u1
            ON u1.user_id = dle.created_by

        LEFT JOIN users u2
            ON u2.user_id = dle.updated_by

        WHERE dle.logbook_id = :logbook_id
        ORDER BY dle.entry_time asc;
        """)

        log_rows = db.execute(
            entry_query,
            {"logbook_id": logbook_id}
        ).mappings().all()

        master_data = dict(header)
        master_data["logData"] = [dict(row) for row in log_rows] if log_rows else []

        response[shift_name]["dkn_digital_log"].append(master_data)

    # -------------------------------
    # 3️⃣ GET HANDOVER DATA
    # -------------------------------
    handover_query = text("""
        SELECT
            CASE
                WHEN shl.shift_id = 1 AND shl.station_id = 4 THEN 'Shift A'
                WHEN shl.shift_id = 2 AND shl.station_id = 4 THEN 'Shift B'
                WHEN shl.shift_id = 3 AND shl.station_id = 4 THEN 'Shift C'
            END AS shift,

            shl.from_user_id,
            CONCAT(u1.first_name,' ',u1.last_name) AS handover_by,

            shl.to_user_id,
            CONCAT(u2.first_name,' ',u2.last_name) AS takeover_by,

            shl.event_time

        FROM shift_handover_log shl

        LEFT JOIN users u1
            ON u1.user_id = shl.from_user_id

        LEFT JOIN users u2
            ON u2.user_id = shl.to_user_id

        WHERE shl.event_type = 'HANDOVER_ACCEPTED'
        
        AND shl.event_time >= (:log_date + INTERVAL '7 hour')
        AND shl.event_time < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')

        ORDER BY shl.shift_id, shl.event_time
    """)

    handovers = db.execute(
        handover_query,
        {"log_date": log_date}
    ).mappings().all()

    for row in handovers:

        shift_name = row.get("shift")

        if shift_name in response:
            response[shift_name]["handover"].append(dict(row))

    return response