from typing import Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date

from app.schemas.digital_logbook.digital_logbook_mlr.mlr_digital_logbook_schemas import MlrDigitalLogBookCreate, MlrDigitalLogBookUpdate


def create_mlr_logbook(db: Session, payload: MlrDigitalLogBookCreate):
    query = text("""
        INSERT INTO mlr_digital_logbook (
            logbook_ref_no,
            station,
            station_in_charge,
            shift,
            log_date,
            start_time,
            handed_over_by,
            taken_over_by,
            is_shift_closed   ,created_at,created_by ,updated_at ,updated_by,
            dkn,
            hsn,
            ner,
            sv1,
            sv2,
            ms_logbook_id

        )
        VALUES (
            :logbook_ref_no,
            :station,
            :station_in_charge,
            :shift,
            :log_date,
            :start_time,
            :handed_over_by,
            :taken_over_by,
            :is_shift_closed,:created_at,:created_by ,:updated_at ,:updated_by,
            :dkn,
            :hsn,
            :ner,
            :sv1,
            :sv2,
            :ms_logbook_id

        )
        RETURNING mlr_logbook_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()
    return result.fetchone()[0]


def update_mlr_logbook(db: Session, logbook_id: int, payload: MlrDigitalLogBookUpdate):
    query = text("""
        UPDATE mlr_digital_logbook
        SET
            logbook_ref_no    = COALESCE(:logbook_ref_no, logbook_ref_no),
            station           = COALESCE(:station, station),
            station_in_charge = COALESCE(:station_in_charge, station_in_charge),
            shift             = COALESCE(:shift, shift),
            log_date          = COALESCE(:log_date, log_date),
            start_time        = COALESCE(:start_time, start_time),
            handed_over_by    = COALESCE(:handed_over_by, handed_over_by),
            taken_over_by     = COALESCE(:taken_over_by, taken_over_by),
            is_shift_closed   = COALESCE(:is_shift_closed, is_shift_closed),
            created_at= COALESCE(:created_at, created_at),
            created_by= COALESCE(:created_by, created_by),
            updated_at= COALESCE(:updated_at, updated_at),
            updated_by= COALESCE(:updated_by, updated_by),
            dkn        = COALESCE(:dkn, dkn),
            hsn        = COALESCE(:hsn, hsn),
            ner        = COALESCE(:ner, ner),
            sv1        = COALESCE(:sv1, sv1),
            sv2        = COALESCE(:sv2, sv2),
            ms_logbook_id = COALESCE(:ms_logbook_id, ms_logbook_id)

        WHERE mlr_logbook_id = :mlr_logbook_id
    """)

    params = payload.dict()
    params["mlr_logbook_id"] = logbook_id

    db.execute(query, params)
    db.commit()
    return True


def delete_mlr_logbook(db: Session, logbook_id: int):
    query = text("""
        DELETE FROM mlr_digital_logbook
        WHERE mlr_logbook_id = :mlr_logbook_id
    """)

    db.execute(query, {"mlr_logbook_id": logbook_id})
    db.commit()
    return True


# def get_logbook_by_date(db: Session, log_date: date):

#     # -------------------------------
#     # 1️⃣ GET MAX LOGBOOK ID
#     # -------------------------------
#     max_query = text("""
#         SELECT MAX(mlr_logbook_id) AS max_id
#         FROM mlr_digital_logbook
#         WHERE ms_logbook_id IN (
#             SELECT LSM.ms_logbook_id
#             FROM logbook_shift_master LSM
#             WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
#             AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
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
#         FROM mlr_digital_logbook
#         WHERE mlr_logbook_id = :max_id
#     """)

#     header_row = db.execute(header_query, {"max_id": max_id}).mappings().first()

#     if not header_row:
#         return []

#     # -------------------------------
#     # 3️⃣ GET ENTRY DATA (LEFT JOIN NOT REQUIRED NOW)
#     # -------------------------------
#     entry_query = text("""
#         SELECT *
#         FROM mlr_digital_logbook_entry
#         WHERE mlr_logbook_id = :max_id
#     """)

#     logdata_rows = db.execute(entry_query, {"max_id": max_id}).mappings().all()

#     # -------------------------------
#     # 4️⃣ BUILD RESPONSE
#     # -------------------------------
#     response = dict(header_row)
#     response["logData"] = [dict(row) for row in logdata_rows] if logdata_rows else []

#     return [response]



# ------------------------------------------------------
# Without technician
# ------------------------------------------------------
def get_logbook_by_date(db: Session, log_date: date):

    # -------------------------------
    # RESPONSE STRUCTURE
    # -------------------------------
    response = {
        "Shift A": {"mlr_digital_log": [], "handover": []},
        "Shift B": {"mlr_digital_log": [], "handover": []},
        "Shift C": {"mlr_digital_log": [], "handover": []}
    }

    # -------------------------------
    # 1️⃣ GET ALL LOGBOOKS FOR THE DAY
    # -------------------------------
    header_query = text("""
        SELECT 
            mdl.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM mlr_digital_logbook mdl

        LEFT JOIN users u1
            ON u1.user_id = mdl.created_by

        LEFT JOIN users u2
            ON u2.user_id = mdl.updated_by

        WHERE mdl.ms_logbook_id IN (
            SELECT LSM.ms_logbook_id
            FROM logbook_shift_master LSM
            WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
            AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
        )

        ORDER BY mdl.mlr_logbook_id;
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

        mlr_id = header["mlr_logbook_id"]

        # -------------------------------
        # GET ENTRY DATA
        # -------------------------------
        entry_query = text("""
            SELECT 
            mle.*,

            -- Created By Name
            CONCAT(u1.first_name, ' ', u1.last_name) AS created_by_name,

            -- Updated By Name
            CONCAT(u2.first_name, ' ', u2.last_name) AS updated_by_name

        FROM mlr_digital_logbook_entry mle

        LEFT JOIN users u1
            ON u1.user_id = mle.created_by

        LEFT JOIN users u2
            ON u2.user_id = mle.updated_by

        WHERE mle.mlr_logbook_id = :mlr_id
        ORDER BY mle.entry_time asc;
        """)

        log_rows = db.execute(
            entry_query,
            {"mlr_id": mlr_id}
        ).mappings().all()

        master_data = dict(header)
        master_data["logData"] = [dict(row) for row in log_rows] if log_rows else []

        response[shift_name]["mlr_digital_log"].append(master_data)

    # -------------------------------
    # 3️⃣ GET HANDOVER DATA
    # -------------------------------
    handover_query = text("""
        SELECT
            CASE
                WHEN shl.shift_id = 1 AND shl.station_id = 1  THEN 'Shift A'
                WHEN shl.shift_id = 2 AND shl.station_id = 1  THEN 'Shift B'
                WHEN shl.shift_id = 3 AND shl.station_id = 1  THEN 'Shift C'
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

        ORDER BY shl.shift_id, shl.event_time;
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


# ------------------------------------------------------
# With technician (JSONB based timeline)
# ------------------------------------------------------
def get_logbook_by_date_api_with_technicians(db: Session, log_date: date):

    # -------------------------------
    # RESPONSE STRUCTURE
    # -------------------------------
    response: Dict[str, Any] = {
        "Shift A": {"mlr_digital_log": [], "handover": [], "technicians": []},
        "Shift B": {"mlr_digital_log": [], "handover": [], "technicians": []},
        "Shift C": {"mlr_digital_log": [], "handover": [], "technicians": []}
    }

    # -------------------------------
    # 1️⃣ GET ALL LOGBOOKS
    # -------------------------------
    header_query = text("""
        SELECT 
            mdl.*,
            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name
        FROM mlr_digital_logbook mdl
        LEFT JOIN users u1 ON u1.user_id = mdl.created_by
        LEFT JOIN users u2 ON u2.user_id = mdl.updated_by
        WHERE mdl.ms_logbook_id IN (
            SELECT LSM.ms_logbook_id
            FROM logbook_shift_master LSM
            WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
            AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
        )
        ORDER BY mdl.mlr_logbook_id;
    """)

    header_rows = db.execute(header_query, {"log_date": log_date}).mappings().all()

    if not header_rows:
        return response

    # -------------------------------
    # 2️⃣ LOG DATA
    # -------------------------------
    for header in header_rows:

        shift_name = header.get("shift")
        if shift_name not in response:
            continue

        mlr_id = header["mlr_logbook_id"]

        entry_query = text("""
            SELECT 
                mle.*,
                CONCAT(u1.first_name, ' ', u1.last_name) AS created_by_name,
                CONCAT(u2.first_name, ' ', u2.last_name) AS updated_by_name
            FROM mlr_digital_logbook_entry mle
            LEFT JOIN users u1 ON u1.user_id = mle.created_by
            LEFT JOIN users u2 ON u2.user_id = mle.updated_by
            WHERE mle.mlr_logbook_id = :mlr_id;
        """)

        log_rows = db.execute(entry_query, {"mlr_id": mlr_id}).mappings().all()

        master_data = dict(header)
        master_data["logData"] = [dict(row) for row in log_rows]

        response[shift_name]["mlr_digital_log"].append(master_data)

    # -------------------------------
    # 3️⃣ HANDOVER DATA
    # -------------------------------
    handover_query = text("""
        SELECT
            CASE
                WHEN shl.shift_id = 1 AND shl.station_id = 1 THEN 'Shift A'
                WHEN shl.shift_id = 2 AND shl.station_id = 1 THEN 'Shift B'
                WHEN shl.shift_id = 3 AND shl.station_id = 1 THEN 'Shift C'
            END AS shift,

            shl.from_user_id,
            CONCAT(u1.first_name,' ',u1.last_name) AS handover_by,

            shl.to_user_id,
            CONCAT(u2.first_name,' ',u2.last_name) AS takeover_by,

            shl.event_time

        FROM shift_handover_log shl
        LEFT JOIN users u1 ON u1.user_id = shl.from_user_id
        LEFT JOIN users u2 ON u2.user_id = shl.to_user_id
        WHERE shl.event_type = 'HANDOVER_ACCEPTED'
        AND shl.event_time >= (:log_date + INTERVAL '7 hour')
        AND shl.event_time < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
        ORDER BY shl.shift_id, shl.event_time;
    """)

    handovers = db.execute(handover_query, {"log_date": log_date}).mappings().all()

    for row in handovers:
        shift_name = row.get("shift")
        if shift_name in response:
            response[shift_name]["handover"].append(dict(row))

    # -------------------------------
    # 4️⃣ TECHNICIAN TIMELINE (AFTER HANDOVER)
    # -------------------------------
    technician_query = text("""
        SELECT 
            mdl.shift,
            mdl.ms_logbook_id,

            (tech.value->>'technician_id')::int AS technician_id,
            CONCAT(u.first_name, ' ', u.last_name) AS technician_name,

            (tech.value->>'from_date')::timestamp AS from_date,
            (tech.value->>'to_date')::timestamp AS to_date,
            (tech.value->>'created_by')::int AS created_by

        FROM mlr_digital_logbook mdl

        JOIN logbook_shift_master LSM
            ON LSM.ms_logbook_id = mdl.ms_logbook_id

        LEFT JOIN LATERAL jsonb_array_elements(
            COALESCE(LSM.all_technicians, '[]'::jsonb)
        ) AS tech(value)
            ON TRUE

        LEFT JOIN users u
            ON u.user_id = (tech.value->>'technician_id')::int

        WHERE LSM.created_at >= (:log_date + INTERVAL '7 hour')
        AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')

        -- 🔥 FIX: remove empty rows
        AND tech.value IS NOT NULL
        AND (tech.value->>'technician_id') IS NOT NULL

        ORDER BY mdl.shift, from_date
    """)

    technician_rows = db.execute(
        technician_query,
        {"log_date": log_date}
    ).mappings().all()

    # 🔥 assign after handover
    for row in technician_rows:

        shift_name = row.get("shift")

        if shift_name in response:
            response[shift_name]["technicians"].append({
                "technician_id": row["technician_id"],
                "technician_name": row["technician_name"],
                "from_date": row["from_date"],
                "to_date": row["to_date"],
                "created_by": row["created_by"],
                "ms_logbook_id": row["ms_logbook_id"]
            })

    return response