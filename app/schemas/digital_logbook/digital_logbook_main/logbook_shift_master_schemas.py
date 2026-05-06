from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime


class LogbookShiftMasterCreate(BaseModel):
    mlr_logbook_id: Optional[int] = None
    hsn_logbook_id: Optional[int] = None
    dkn_logbook_id: Optional[int] = None

    shift_a: Optional[str] = None
    shift_b: Optional[str] = None
    shift_c: Optional[str] = None

    shift_a_start_time: Optional[time] = None
    shift_b_start_time: Optional[time] = None
    shift_c_start_time: Optional[time] = None

    shift_a_end_time: Optional[time] = None
    shift_b_end_time: Optional[time] = None
    shift_c_end_time: Optional[time] = None

    log_date: Optional[date] = None

    shift_a_status: Optional[str] = None
    shift_b_status: Optional[str] = None
    shift_c_status: Optional[str] = None

    shift_a_handover_notes: Optional[str] = None
    shift_b_handover_notes: Optional[str] = None
    shift_c_handover_notes: Optional[str] = None

    shift_a_engineer: Optional[str] = None
    shift_b_engineer: Optional[str] = None
    shift_c_engineer: Optional[str] = None

    tank_ffe_id: Optional[int] = None
    cp_dkn_id: Optional[int] = None
    cp_hsn_id: Optional[int] = None
    cp_mlr_id: Optional[int] = None
    cp_ner_id: Optional[int] = None

    dsc_id: Optional[int] = None
    sampling_id: Optional[int] = None
    dg_id: Optional[int] = None
    erv_id: Optional[int] = None
    fire_id: Optional[int] = None

    kptcl_dkn_id: Optional[int] = None
    kptcl_hsn_id: Optional[int] = None
    kptcl_ner_id: Optional[int] = None
    line_id: Optional[int] = None

    vtmn_id: Optional[int] = None
    vtm_id: Optional[int] = None
    tank_id: Optional[int] = None
    pressure_id: Optional[int] = None
    npt_id: Optional[int] = None

    mfm_log_dkn_id: Optional[int] = None
    mfm_log_ner_id: Optional[int] = None
    mfm_acc_hsn_id: Optional[int] = None
    mfm_acc_dkn_id: Optional[int] = None

    security_guard_id: Optional[int] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    assigned_to: Optional[int] = None

class LogbookShiftMasterUpdate(BaseModel):
    shift_a: Optional[str] = None
    shift_b: Optional[str] = None
    shift_c: Optional[str] = None

    shift_a_start_time: Optional[time] = None
    shift_b_start_time: Optional[time] = None
    shift_c_start_time: Optional[time] = None

    shift_a_end_time: Optional[time] = None
    shift_b_end_time: Optional[time] = None
    shift_c_end_time: Optional[time] = None

    log_date: Optional[date] = None

    shift_a_status: Optional[str] = None
    shift_b_status: Optional[str] = None
    shift_c_status: Optional[str] = None

    shift_a_handover_notes: Optional[str] = None
    shift_b_handover_notes: Optional[str] = None
    shift_c_handover_notes: Optional[str] = None

    shift_a_engineer: Optional[str] = None
    shift_b_engineer: Optional[str] = None
    shift_c_engineer: Optional[str] = None

    tank_ffe_id: Optional[int] = None
    cp_dkn_id: Optional[int] = None
    cp_hsn_id: Optional[int] = None
    cp_mlr_id: Optional[int] = None
    cp_ner_id: Optional[int] = None
    line_id: Optional[int] = None

    dsc_id: Optional[int] = None
    sampling_id: Optional[int] = None
    dg_id: Optional[int] = None
    erv_id: Optional[int] = None
    fire_id: Optional[int] = None

    kptcl_dkn_id: Optional[int] = None
    kptcl_hsn_id: Optional[int] = None
    kptcl_ner_id: Optional[int] = None

    vtmn_id: Optional[int] = None
    vtm_id: Optional[int] = None
    tank_id: Optional[int] = None
    pressure_id: Optional[int] = None
    npt_id: Optional[int] = None

    mfm_log_dkn_id: Optional[int] = None
    mfm_log_ner_id: Optional[int] = None
    mfm_acc_hsn_id: Optional[int] = None
    mfm_acc_dkn_id: Optional[int] = None

    security_guard_id: Optional[int] = None
    closed_at: Optional[datetime] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None