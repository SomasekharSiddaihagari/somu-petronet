# app/crud/ner_digital_logbook_crud.py
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import text
from app.schemas.digital_logbook.digital_logbook_ner.ner_digital_logbook_schema import (
    NerDigitalLogBookCreate,
    NerDigitalLogBookUpdate
)


def create_ner_digital_logbook(db: Session, payload: NerDigitalLogBookCreate):
    query = text("""
        INSERT INTO ner_digital_logbook (
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
            mlr,
            sv3,
            sv4,
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
            :mlr,
            :sv3,
            :sv4,
            :ms_logbook_id

        )
        RETURNING ner_logbook_id
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.fetchone()[0]


def update_ner_digital_logbook(
    db: Session,
    ner_logbook_id: int,
    payload: NerDigitalLogBookUpdate
):
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return False

    set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
    data["ner_logbook_id"] = ner_logbook_id

    query = text(f"""
        UPDATE ner_digital_logbook
        SET {set_clause}
        WHERE ner_logbook_id = :ner_logbook_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_ner_digital_logbook(db: Session, ner_logbook_id: int):
    query = text("""
        DELETE FROM ner_digital_logbook
        WHERE ner_logbook_id = :ner_logbook_id
    """)
    result = db.execute(query, {"ner_logbook_id": ner_logbook_id})
    db.commit()
    return result.rowcount > 0

# def get_logbook_by_date(db: Session, log_date: date):
#     main_query  = text("""
#          SELECT *
#         FROM ner_digital_logbook DL
#         JOIN ner_digital_logbook_entry DLE 
#         ON DLE.ner_logbook_id = DL.ner_logbook_id
#         WHERE DL.ms_logbook_id IN (
#             SELECT LSM.ms_logbook_id
#             FROM logbook_shift_master LSM
#             WHERE DATE(LSM.created_at) = :log_date
#         );
#     """)
#     logdata_rows = db.execute(main_query, {"log_date": log_date}).mappings().all()
#     if not logdata_rows:
#         return []
    
#      # -------------------------------
#     # 2️⃣ GET MAX LOGBOOK ID
#     # -------------------------------
#     max_query = text("""
#         SELECT MAX(ner_logbook_id) AS max_id
#         FROM ner_digital_logbook
#         WHERE ms_logbook_id IN (
#             SELECT LSM.ms_logbook_id
#             FROM logbook_shift_master LSM
#             WHERE DATE(LSM.created_at) = :log_date
#         )
#     """)

#     max_result = db.execute(max_query, {"log_date": log_date}).mappings().first()
#     max_id = max_result["max_id"]

#     # -------------------------------
#     # 3️⃣ GET HEADER DATA (ONLY MAX ID ROW)
#     # -------------------------------
#     header_query = text("""
#         SELECT *
#         FROM ner_digital_logbook
#         WHERE ner_logbook_id = :max_id
#     """)

#     header_row = db.execute(header_query, {"max_id": max_id}).mappings().first()

#     if not header_row:
#         return []

#     # -------------------------------
#     # 4️⃣ BUILD FINAL RESPONSE
#     # -------------------------------
#     response = dict(header_row)  # all max-id data dynamically

#     response["logData"] = [dict(row) for row in logdata_rows]

#     return [response]

def get_logbook_by_date(db: Session, log_date: date):

    # -------------------------------
    # RESPONSE STRUCTURE
    # -------------------------------
    response = {
        "Shift A": {"ner_digital_log": [], "handover": []},
        "Shift B": {"ner_digital_log": [], "handover": []},
        "Shift C": {"ner_digital_log": [], "handover": []}
    }

    # -------------------------------
    # 1️⃣ GET ALL LOGBOOKS FOR THE DAY
    # -------------------------------
    header_query = text("""
        SELECT 
            ndl.*,

            -- Created By Name
            TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,

            -- Updated By Name
            TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

        FROM ner_digital_logbook ndl

        LEFT JOIN users u1
            ON u1.user_id = ndl.created_by

        LEFT JOIN users u2
            ON u2.user_id = ndl.updated_by

        WHERE ndl.ms_logbook_id IN (
            SELECT LSM.ms_logbook_id
            FROM logbook_shift_master LSM
            WHERE LSM.created_at >= :log_date + INTERVAL '7 hour'
            AND LSM.created_at < (:log_date + INTERVAL '1 day' + INTERVAL '7 hour')
        )

        ORDER BY ndl.ner_logbook_id;
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

        logbook_id = header["ner_logbook_id"]

        # -------------------------------
        # GET ENTRY DATA
        # -------------------------------
        entry_query = text("""
            SELECT 
                nle.*,

                -- Created By Name
                TRIM(CONCAT(COALESCE(u1.first_name,''),' ',COALESCE(u1.last_name,''))) AS created_by_name,

                -- Updated By Name
                TRIM(CONCAT(COALESCE(u2.first_name,''),' ',COALESCE(u2.last_name,''))) AS updated_by_name

            FROM ner_digital_logbook_entry nle

            LEFT JOIN users u1
                ON u1.user_id = nle.created_by

            LEFT JOIN users u2
                ON u2.user_id = nle.updated_by

            WHERE nle.ner_logbook_id = :logbook_id
            ORDER BY nle.entry_time asc;
        """)

        log_rows = db.execute(
            entry_query,
            {"logbook_id": logbook_id}
        ).mappings().all()

        master_data = dict(header)
        master_data["logData"] = [dict(row) for row in log_rows] if log_rows else []

        response[shift_name]["ner_digital_log"].append(master_data)

    # -------------------------------
    # 3️⃣ GET HANDOVER DATA
    # -------------------------------
    handover_query = text("""
        SELECT
            CASE
                WHEN shl.shift_id = 1 AND shl.station_id = 2 THEN 'Shift A'
                WHEN shl.shift_id = 2 AND shl.station_id = 2 THEN 'Shift B'
                WHEN shl.shift_id = 3 AND shl.station_id = 2 THEN 'Shift C'
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