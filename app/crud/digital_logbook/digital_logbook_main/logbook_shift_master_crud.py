from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.digital_logbook.digital_logbook_main.logbook_shift_master_schemas import LogbookShiftMasterCreate, LogbookShiftMasterUpdate

def create_shift_master(db: Session, payload: LogbookShiftMasterCreate):
    query = text("""
        INSERT INTO logbook_shift_master (
            mlr_logbook_id, hsn_logbook_id, dkn_logbook_id,
            shift_a, shift_b, shift_c,
            shift_a_start_time, shift_b_start_time, shift_c_start_time,
            shift_a_end_time, shift_b_end_time, shift_c_end_time,
            log_date,
            shift_a_status, shift_b_status, shift_c_status,
            shift_a_handover_notes, shift_b_handover_notes, shift_c_handover_notes,
            shift_a_engineer, shift_b_engineer, shift_c_engineer,
            tank_ffe_id, cp_dkn_id, cp_hsn_id, cp_mlr_id, cp_ner_id,
            dsc_id, sampling_id, dg_id, erv_id, fire_id,
            kptcl_dkn_id, kptcl_hsn_id, kptcl_ner_id,
            vtmn_id, vtm_id, tank_id, pressure_id, npt_id,
            mfm_log_dkn_id, mfm_log_ner_id, mfm_acc_hsn_id, mfm_acc_dkn_id,
            security_guard_id   ,created_at,created_by ,updated_at ,updated_by,assigned_to

        )
        VALUES (
            :mlr_logbook_id, :hsn_logbook_id, :dkn_logbook_id,
            :shift_a, :shift_b, :shift_c,
            :shift_a_start_time, :shift_b_start_time, :shift_c_start_time,
            :shift_a_end_time, :shift_b_end_time, :shift_c_end_time,
            :log_date,
            :shift_a_status, :shift_b_status, :shift_c_status,
            :shift_a_handover_notes, :shift_b_handover_notes, :shift_c_handover_notes,
            :shift_a_engineer, :shift_b_engineer, :shift_c_engineer,
            :tank_ffe_id, :cp_dkn_id, :cp_hsn_id, :cp_mlr_id, :cp_ner_id,
            :dsc_id, :sampling_id, :dg_id, :erv_id, :fire_id,
            :kptcl_dkn_id, :kptcl_hsn_id, :kptcl_ner_id,
            :vtmn_id, :vtm_id, :tank_id, :pressure_id, :npt_id,
            :mfm_log_dkn_id, :mfm_log_ner_id, :mfm_acc_hsn_id, :mfm_acc_dkn_id,
            :security_guard_id,:created_at,:created_by ,:updated_at ,:updated_by,:assigned_to

        )
        RETURNING ms_logbook_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()
    return result.fetchone()[0]



def update_shift_master(db: Session, master_id: int, payload: LogbookShiftMasterUpdate):
    query = text("""
        UPDATE logbook_shift_master SET
            shift_a = COALESCE(:shift_a, shift_a),
            shift_b = COALESCE(:shift_b, shift_b),
            shift_c = COALESCE(:shift_c, shift_c),

            shift_a_start_time = COALESCE(:shift_a_start_time, shift_a_start_time),
            shift_b_start_time = COALESCE(:shift_b_start_time, shift_b_start_time),
            shift_c_start_time = COALESCE(:shift_c_start_time, shift_c_start_time),

            shift_a_end_time = COALESCE(:shift_a_end_time, shift_a_end_time),
            shift_b_end_time = COALESCE(:shift_b_end_time, shift_b_end_time),
            shift_c_end_time = COALESCE(:shift_c_end_time, shift_c_end_time),

            log_date = COALESCE(:log_date, log_date),

            shift_a_status = COALESCE(:shift_a_status, shift_a_status),
            shift_b_status = COALESCE(:shift_b_status, shift_b_status),
            shift_c_status = COALESCE(:shift_c_status, shift_c_status),

            shift_a_handover_notes = COALESCE(:shift_a_handover_notes, shift_a_handover_notes),
            shift_b_handover_notes = COALESCE(:shift_b_handover_notes, shift_b_handover_notes),
            shift_c_handover_notes = COALESCE(:shift_c_handover_notes, shift_c_handover_notes),

            shift_a_engineer = COALESCE(:shift_a_engineer, shift_a_engineer),
            shift_b_engineer = COALESCE(:shift_b_engineer, shift_b_engineer),
            shift_c_engineer = COALESCE(:shift_c_engineer, shift_c_engineer),

            tank_ffe_id = COALESCE(:tank_ffe_id, tank_ffe_id),
            cp_dkn_id = COALESCE(:cp_dkn_id, cp_dkn_id),
            cp_hsn_id = COALESCE(:cp_hsn_id, cp_hsn_id),
            cp_mlr_id = COALESCE(:cp_mlr_id, cp_mlr_id),
            cp_ner_id = COALESCE(:cp_ner_id, cp_ner_id),

            dsc_id = COALESCE(:dsc_id, dsc_id),
            sampling_id = COALESCE(:sampling_id, sampling_id),
            dg_id = COALESCE(:dg_id, dg_id),
            erv_id = COALESCE(:erv_id, erv_id),
            fire_id = COALESCE(:fire_id, fire_id),

            kptcl_dkn_id = COALESCE(:kptcl_dkn_id, kptcl_dkn_id),
            kptcl_hsn_id = COALESCE(:kptcl_hsn_id, kptcl_hsn_id),
            kptcl_ner_id = COALESCE(:kptcl_ner_id, kptcl_ner_id),

            vtmn_id = COALESCE(:vtmn_id, vtmn_id),
            vtm_id = COALESCE(:vtm_id, vtm_id),
            tank_id = COALESCE(:tank_id, tank_id),
            pressure_id = COALESCE(:pressure_id, pressure_id),
            npt_id = COALESCE(:npt_id, npt_id),

            mfm_log_dkn_id = COALESCE(:mfm_log_dkn_id, mfm_log_dkn_id),
            mfm_log_ner_id = COALESCE(:mfm_log_ner_id, mfm_log_ner_id),
            mfm_acc_hsn_id = COALESCE(:mfm_acc_hsn_id, mfm_acc_hsn_id),
            mfm_acc_dkn_id = COALESCE(:mfm_acc_dkn_id, mfm_acc_dkn_id),

            security_guard_id = COALESCE(:security_guard_id, security_guard_id)
,created_at= COALESCE(:created_at, created_at),created_by= COALESCE(:created_by, created_by),updated_at= COALESCE(:updated_at, updated_at),updated_by= COALESCE(:updated_by, updated_by)


        WHERE ms_logbook_id = :ms_logbook_id
    """)

    params = payload.dict()
    params["ms_logbook_id"] = master_id

    db.execute(query, params)
    db.commit()
    return True

def delete_shift_master(db: Session, master_id: int):
    query = text("""
        DELETE FROM logbook_shift_master
        WHERE ms_logbook_id = :ms_logbook_id
    """)

    db.execute(query, {"ms_logbook_id": master_id})
    db.commit()
    return True



def get_shift_master_by_id(db: Session, master_id: int):
    query = text("""
        SELECT *
        FROM logbook_shift_master
        WHERE ms_logbook_id = :ms_logbook_id
    """)

    result = db.execute(query, {"ms_logbook_id": master_id}).mappings().first()
    return dict(result) if result else None


def get_all_shift_masters(db: Session):
    query = text("""
        SELECT *
        FROM logbook_shift_master
        ORDER BY ms_logbook_id DESC
    """)

    result = db.execute(query).mappings().all()
    return [dict(row) for row in result]
