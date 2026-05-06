import json
from typing import Optional
from datetime import datetime, date, timedelta
from sqlalchemy import text, func, or_, and_
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category import ProductDispatchCategory
from app.models.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_log import ProductDispatchShiftLog
from app.models.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_log_entry import ProductDispatchLogEntry
from app.models.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_log_history import ProductDispatchShiftLogHistory
from app.models.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_log_entry_history import ProductDispatchLogEntryHistory
from app.models.digital_logbook.geo_fencing.geo_shift import Shift
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shift_log_schema import (
    ProductDispatchShiftLogCreate,
    ProductDispatchShiftLogUpdate,
)

# --- HELPERS ---

def _calculate_pump_metrics(data: dict):
    # Logic: Round inputs & calc totals
    pump_keys = ["bp_101a", "bp_101b", "mp_102a", "mp_102b", "mp_102c", "sump_pump", "ci_pump_101a", "ci_pump_101b", "dra"]
    total_current = 0.0
    for key in pump_keys:
        prev = round(float(data.get(f"{key}_previous_hrs") or 0), 2)
        curr = round(float(data.get(f"{key}_current_hrs") or 0), 2)
        
        # Save-back: Rounding fix for DB
        data[f"{key}_previous_hrs"] = prev
        data[f"{key}_current_hrs"] = curr
        data[f"{key}_cumulative_hrs"] = round(prev + curr, 2)
        total_current += curr
    
    data["total_pump_hrs"] = round(total_current, 2)
    return data

def _get_previous_shift_log(db: Session, category_master_id: int, current_shift_id: int, current_date: date):
    # Query: Find latest record backwards
    return db.query(ProductDispatchShiftLog).filter(
        ProductDispatchShiftLog.category_master_id == category_master_id,
        or_(
            ProductDispatchShiftLog.log_date < current_date,
            and_(
                ProductDispatchShiftLog.log_date == current_date,
                ProductDispatchShiftLog.shift_id < current_shift_id
            )
        )
    ).order_by(
        ProductDispatchShiftLog.log_date.desc(),
        ProductDispatchShiftLog.shift_id.desc()
    ).first()

def _apply_previous_shift_data(db: Session, data: dict, prev_log: ProductDispatchShiftLog):
    # Carry-Forward: Map prev cum to curr start
    pump_keys = ["bp_101a", "bp_101b", "mp_102a", "mp_102b", "mp_102c", "sump_pump", "ci_pump_101a", "ci_pump_101b", "dra"]
    for key in pump_keys:
        attr_prev_hrs = f"{key}_previous_hrs"
        attr_cum_hrs = f"{key}_cumulative_hrs"
        if data.get(attr_prev_hrs) in [None, 0.0]:
            data[attr_prev_hrs] = getattr(prev_log, attr_cum_hrs) or 0.0
    return data

def _validate_json_entries(data: dict):
    # Validation: Check negative values
    for list_key in ["suction_movements", "line_fill_entries", "section_capacity_summary"]:
        if list_key in data and isinstance(data[list_key], list):
            for item in data[list_key]:
                for num_field in ["quantity_kl", "section_capacity", "section_current_fill"]:
                    if item.get(num_field) is not None and item[num_field] < 0:
                        raise HTTPException(status_code=400, detail=f"{num_field} negative")

def _save_sub_entries(db: Session, shift_log_id: int, payload: dict):
    # Children: Re-insert list items
    db.query(ProductDispatchLogEntry).filter(ProductDispatchLogEntry.shift_log_id == shift_log_id).delete()
    entries_to_save = []
    mapping = {"suction_movements": "SUCTION", "line_fill_entries": "LINE_FILL", "section_capacity_summary": "CAPACITY"}
    for key, entry_type in mapping.items():
        items = payload.get(key) or []
        for item in items:
            entry = ProductDispatchLogEntry(
                shift_log_id=shift_log_id,
                entry_type=entry_type,
                section_name=item.get("section_name"),
                product=item.get("product"),
                pmhbl_batch_no=item.get("pmhbl_batch_no"),
                mrpl_batch_no=item.get("mrpl_batch_no"),
                quantity_kl=item.get("quantity_kl"),
                section_capacity=item.get("section_capacity"),
                section_current_fill=item.get("section_current_fill"),
            )
            entries_to_save.append(entry)
    if entries_to_save: db.add_all(entries_to_save)

def _log_to_history(db: Session, db_record: ProductDispatchShiftLog):
    # History: Snapshot parent & children
    try:
        parent_data = {c.name: getattr(db_record, c.name) for c in db_record.__table__.columns}
        history_parent = ProductDispatchShiftLogHistory(**parent_data)
        db.add(history_parent)
        for entry in db_record.sub_entries:
            entry_data = {c.name: getattr(entry, c.name) for c in entry.__table__.columns}
            history_entry = ProductDispatchLogEntryHistory(**entry_data)
            db.add(history_entry)
    except Exception as e:
        db.rollback()
        raise e

# --- ACTIONS ---

def create_shift_log(db: Session, payload: ProductDispatchShiftLogCreate):
    # Create: Auth, Carry-Forward, Calc, Save
    master = db.query(ProductDispatchCategory).filter(ProductDispatchCategory.p_category_master_id == payload.category_master_id).first()
    if not master: raise HTTPException(status_code=404, detail="Master ID not found")
    
    data = payload.model_dump(exclude_unset=True)
    current_date = data.get("log_date") or date.today()
    
    # Logic: Auto-Carry
    prev_log = _get_previous_shift_log(db, payload.category_master_id, payload.shift_id, current_date)
    if prev_log: data = _apply_previous_shift_data(db, data, prev_log)
    
    _validate_json_entries(data)
    _calculate_pump_metrics(data)
    
    suction = data.pop("suction_movements", [])
    line_fill = data.pop("line_fill_entries", [])
    capacity = data.pop("section_capacity_summary", [])
    
    new_log = ProductDispatchShiftLog(**data)
    new_log.created_at = new_log.updated_at = datetime.now()
    if new_log.updated_by is None: new_log.updated_by = new_log.created_by
    
    db.add(new_log)
    db.flush()
    _save_sub_entries(db, new_log.shift_log_id, {"suction_movements": suction, "line_fill_entries": line_fill, "section_capacity_summary": capacity})
    db.commit()
    return new_log.shift_log_id

def update_shift_log(db: Session, shift_log_id: int, payload: ProductDispatchShiftLogUpdate):
    # Update: Move to History, Patch data, Recalc
    db_record = db.query(ProductDispatchShiftLog).filter(ProductDispatchShiftLog.shift_log_id == shift_log_id).first()
    if not db_record: return False
    
    new_data = payload.model_dump(exclude_unset=True)
    _validate_json_entries(new_data)
    _log_to_history(db, db_record)
    
    curr_state = {c.name: getattr(db_record, c.name) for c in db_record.__table__.columns}
    curr_state.update(new_data)
    _calculate_pump_metrics(curr_state)
    
    for key, value in new_data.items():
        if key not in ["suction_movements", "line_fill_entries", "section_capacity_summary"]:
            setattr(db_record, key, value)
    
    db_record.updated_at = datetime.now()
    # Sync: Calc fields
    f_list = ["total_pump_hrs"] + [f"{k}_cumulative_hrs" for k in ["bp_101a", "bp_101b", "mp_102a", "mp_102b", "mp_102c", "sump_pump", "ci_pump_101a", "ci_pump_101b", "dra"]]
    for f in f_list: setattr(db_record, f, curr_state[f])
    
    if any(k in new_data for k in ["suction_movements", "line_fill_entries", "section_capacity_summary"]):
        _save_sub_entries(db, shift_log_id, new_data)
    db.commit()
    return True

def get_shift_log_by_id(db: Session, shift_log_id: int):
    # Fetch: Get Parent (User names) & Children
    query = text("""
        SELECT e.*, 
        TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) as created_by_name,
        TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) as updated_by_name
        FROM product_dispatch_shift_log e
        LEFT JOIN users u1 ON CAST(e.created_by AS INTEGER) = u1.user_id
        LEFT JOIN users u2 ON CAST(e.updated_by AS INTEGER) = u2.user_id
        WHERE e.shift_log_id = :id
    """)
    result = db.execute(query, {"id": shift_log_id}).fetchone()
    if not result: return None
        
    data = dict(result._mapping)
    obj = db.query(ProductDispatchShiftLog).get(shift_log_id)
    # Map: Sub lists
    data["suction_movements"] = [{"product": e.product, "pmhbl_batch_no": e.pmhbl_batch_no, "mrpl_batch_no": e.mrpl_batch_no, "quantity_kl": e.quantity_kl} for e in obj.sub_entries if e.entry_type == "SUCTION"]
    data["line_fill_entries"] = [{"section_name": e.section_name, "product": e.product, "pmhbl_batch_no": e.pmhbl_batch_no, "mrpl_batch_no": e.mrpl_batch_no, "quantity_kl": e.quantity_kl} for e in obj.sub_entries if e.entry_type == "LINE_FILL"]
    data["section_capacity_summary"] = [{"section_name": e.section_name, "section_capacity": e.section_capacity, "section_current_fill": e.section_current_fill} for e in obj.sub_entries if e.entry_type == "CAPACITY"]
    return data

def get_shift_logs_by_filter(db: Session, filter_date: date = None, shift_id: int = None):
    # List: Filter by date/shift
    query = db.query(ProductDispatchShiftLog)
    if filter_date: query = query.filter(func.date(ProductDispatchShiftLog.created_at) == filter_date)
    if shift_id: query = query.filter(ProductDispatchShiftLog.shift_id == shift_id)
    return [get_shift_log_by_id(db, l.shift_log_id) for l in query.all()]

def delete_shift_log(db: Session, shift_log_id: int):
    # Delete: Move to history & clear
    log = db.query(ProductDispatchShiftLog).filter(ProductDispatchShiftLog.shift_log_id == shift_log_id).first()
    if not log: return False
    _log_to_history(db, log)
    db.delete(log)
    db.commit()
    return True

def get_cumulative_carry_forward(db: Session, log_date: date, shift_id: int, category_master_id: Optional[int] = None):
    # Preview: Fetch prev logs for frontend
    if not category_master_id:
        lm = db.query(ProductDispatchCategory).order_by(ProductDispatchCategory.p_category_master_id.desc()).first()
        category_master_id = lm.p_category_master_id if lm else 0
    prev = _get_previous_shift_log(db, category_master_id, shift_id - 1, log_date)
    pump_keys = ["bp_101a", "bp_101b", "mp_102a", "mp_102b", "mp_102c", "sump_pump", "ci_pump_101a", "ci_pump_101b", "dra"]
    res = {f"{k}_cumulative_hrs": (getattr(prev, f"{k}_cumulative_hrs") or 0.0 if prev else 0.0) for k in pump_keys}
    return res
