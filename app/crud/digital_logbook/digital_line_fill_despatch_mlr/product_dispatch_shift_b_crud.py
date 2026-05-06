# app/crud/erv_b_shift_log_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_b_schema import (
    ERVBShiftLogCreate,
    ERVBShiftLogUpdate
)


def create_erv_b_shift_log(db: Session, payload: ERVBShiftLogCreate):
    query = text("""
        INSERT INTO b_shift_log (
            category_master_id,
            log_date, shift_name, shift_start_time, lpe_frl_at,
            suction_line, mlr,
            fire_pump_auto, fire_pump_manual, availability_auto, availability_manual,
            sku, hsd, ms, dkn, batch, qty,
            sump_level_percent, ci_pumped_percent,
            net_qty_of_shift, gross_qty_of_shift, atg_qty_of_shift,
            bp_101a_previous_hrs, bp_101a_current_hrs, bp_101a_cumulative_hrs,
            bp_101a_availability, bp_101a_product,
            bp_101b_previous_hrs, bp_101b_current_hrs, bp_101b_cumulative_hrs,
            bp_101b_availability, bp_101b_product,
            bp_102a_previous_hrs, bp_102a_current_hrs, bp_102a_cumulative_hrs,
            bp_102a_availability, bp_102a_product,
            bp_102b_previous_hrs, bp_102b_current_hrs, bp_102b_cumulative_hrs,
            bp_102b_availability, bp_102b_product,
            bp_102c_previous_hrs, bp_102c_current_hrs, bp_102c_cumulative_hrs,
            bp_102c_availability, bp_102c_product,
            sump_pump_previous_hrs, sump_pump_current_hrs, sump_pump_cumulative_hrs,
            sump_pump_availability, sump_pump_product,
            ci_pump_101a_previous_hrs, ci_pump_101a_current_hrs, ci_pump_101a_cumulative_hrs,
            ci_pump_101a_availability, ci_pump_101a_product,
            ci_pump_101b_previous_hrs, ci_pump_101b_current_hrs, ci_pump_101b_cumulative_hrs,
            ci_pump_101b_availability, ci_pump_101b_product,
            maintenance_details, shift_engineer_name, signature
          ,created_at,created_by ,updated_at ,updated_by

                  )
        VALUES (
            :category_master_id,
            :log_date, :shift_name, :shift_start_time, :lpe_frl_at,
            :suction_line, :mlr,
            :fire_pump_auto, :fire_pump_manual, :availability_auto, :availability_manual,
            :sku, :hsd, :ms, :dkn, :batch, :qty,
            :sump_level_percent, :ci_pumped_percent,
            :net_qty_of_shift, :gross_qty_of_shift, :atg_qty_of_shift,
            :bp_101a_previous_hrs, :bp_101a_current_hrs, :bp_101a_cumulative_hrs,
            :bp_101a_availability, :bp_101a_product,
            :bp_101b_previous_hrs, :bp_101b_current_hrs, :bp_101b_cumulative_hrs,
            :bp_101b_availability, :bp_101b_product,
            :bp_102a_previous_hrs, :bp_102a_current_hrs, :bp_102a_cumulative_hrs,
            :bp_102a_availability, :bp_102a_product,
            :bp_102b_previous_hrs, :bp_102b_current_hrs, :bp_102b_cumulative_hrs,
            :bp_102b_availability, :bp_102b_product,
            :bp_102c_previous_hrs, :bp_102c_current_hrs, :bp_102c_cumulative_hrs,
            :bp_102c_availability, :bp_102c_product,
            :sump_pump_previous_hrs, :sump_pump_current_hrs, :sump_pump_cumulative_hrs,
            :sump_pump_availability, :sump_pump_product,
            :ci_pump_101a_previous_hrs, :ci_pump_101a_current_hrs, :ci_pump_101a_cumulative_hrs,
            :ci_pump_101a_availability, :ci_pump_101a_product,
            :ci_pump_101b_previous_hrs, :ci_pump_101b_current_hrs, :ci_pump_101b_cumulative_hrs,
            :ci_pump_101b_availability, :ci_pump_101b_product,
            :maintenance_details, :shift_engineer_name, :signature
       ,:created_at,:created_by ,:updated_at ,:updated_by

                  )
        RETURNING b_shift_log_id
    """)

    result = db.execute(query, payload.model_dump())
    db.commit()
    return result.fetchone()[0]


def update_erv_b_shift_log(
    db: Session,
    b_shift_log_id: int,
    payload: ERVBShiftLogUpdate
):
    data = payload.model_dump(exclude_unset=True)

    if not data:
        return False

    set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
    data["b_shift_log_id"] = b_shift_log_id

    query = text(f"""
        UPDATE b_shift_log
        SET {set_clause}
        WHERE b_shift_log_id = :b_shift_log_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_erv_b_shift_log(db: Session, b_shift_log_id: int):
    query = text("""
        DELETE FROM b_shift_log
        WHERE b_shift_log_id = :b_shift_log_id
    """)
    result = db.execute(query, {"b_shift_log_id": b_shift_log_id})
    db.commit()
    return result.rowcount > 0
