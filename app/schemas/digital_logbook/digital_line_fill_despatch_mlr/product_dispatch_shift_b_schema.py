# app/schemas/erv_b_shift_log_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time


class ERVBShiftLogBase(BaseModel):
    category_master_id: Optional[int] = None

    # BASIC
    log_date: Optional[date] = None
    shift_name: Optional[str] = None
    shift_start_time: Optional[time] = None
    lpe_frl_at: Optional[str] = None

    # SUCTION / MLR
    suction_line: Optional[str] = None
    mlr: Optional[str] = None

    # FIRE SYSTEM
    fire_pump_auto: Optional[bool] = None
    fire_pump_manual: Optional[bool] = None
    availability_auto: Optional[bool] = None
    availability_manual: Optional[bool] = None

    # PRODUCT QUANTITIES
    sku: Optional[float] = None
    hsd: Optional[float] = None
    ms: Optional[float] = None
    dkn: Optional[float] = None
    batch: Optional[str] = None
    qty: Optional[float] = None

    # SHIFT TOTALS
    sump_level_percent: Optional[float] = None
    ci_pumped_percent: Optional[float] = None
    net_qty_of_shift: Optional[float] = None
    gross_qty_of_shift: Optional[float] = None
    atg_qty_of_shift: Optional[float] = None

    # PUMP RUNNING HOURS
    bp_101a_previous_hrs: Optional[float] = None
    bp_101a_current_hrs: Optional[float] = None
    bp_101a_cumulative_hrs: Optional[float] = None
    bp_101a_availability: Optional[str] = None
    bp_101a_product: Optional[str] = None

    bp_101b_previous_hrs: Optional[float] = None
    bp_101b_current_hrs: Optional[float] = None
    bp_101b_cumulative_hrs: Optional[float] = None
    bp_101b_availability: Optional[str] = None
    bp_101b_product: Optional[str] = None

    bp_102a_previous_hrs: Optional[float] = None
    bp_102a_current_hrs: Optional[float] = None
    bp_102a_cumulative_hrs: Optional[float] = None
    bp_102a_availability: Optional[str] = None
    bp_102a_product: Optional[str] = None

    bp_102b_previous_hrs: Optional[float] = None
    bp_102b_current_hrs: Optional[float] = None
    bp_102b_cumulative_hrs: Optional[float] = None
    bp_102b_availability: Optional[str] = None
    bp_102b_product: Optional[str] = None

    bp_102c_previous_hrs: Optional[float] = None
    bp_102c_current_hrs: Optional[float] = None
    bp_102c_cumulative_hrs: Optional[float] = None
    bp_102c_availability: Optional[str] = None
    bp_102c_product: Optional[str] = None

    sump_pump_previous_hrs: Optional[float] = None
    sump_pump_current_hrs: Optional[float] = None
    sump_pump_cumulative_hrs: Optional[float] = None
    sump_pump_availability: Optional[str] = None
    sump_pump_product: Optional[str] = None

    ci_pump_101a_previous_hrs: Optional[float] = None
    ci_pump_101a_current_hrs: Optional[float] = None
    ci_pump_101a_cumulative_hrs: Optional[float] = None
    ci_pump_101a_availability: Optional[str] = None
    ci_pump_101a_product: Optional[str] = None

    ci_pump_101b_previous_hrs: Optional[float] = None
    ci_pump_101b_current_hrs: Optional[float] = None
    ci_pump_101b_cumulative_hrs: Optional[float] = None
    ci_pump_101b_availability: Optional[str] = None
    ci_pump_101b_product: Optional[str] = None

    # MAINTENANCE
    maintenance_details: Optional[str] = None
    shift_engineer_name: Optional[str] = None
    signature: Optional[str] = None

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class ERVBShiftLogCreate(ERVBShiftLogBase):
    pass


class ERVBShiftLogUpdate(ERVBShiftLogBase):
    pass
