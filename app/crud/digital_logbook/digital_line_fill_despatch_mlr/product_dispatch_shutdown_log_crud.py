import json
from datetime import datetime, date
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category import ProductDispatchCategory
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_shutdown_log_schema import ProductDispatchShutdownCreate, ProductDispatchShutdownUpdate

# --- HELPERS ---

def _to_decimal_hours(val: float) -> float:
    # Logic: HH.MM -> Decimal (e.g. 8.30 -> 8.5)
    if val is None: return 0.0
    val = float(val); hours = int(val)
    frac = round((val - hours), 2); mins = round(frac * 100)
    if mins >= 60: return round(val, 2)
    return round(hours + (mins / 60.0), 2)

def _calculate_shutdown_metrics(data: dict, pre_sd_already_decimal: bool = False):
    # Process: Shift durations, Totals, Cumulative
    for s in ["a", "b", "c"]:
        fk, tk = f"shift_{s}_from", f"shift_{s}_to"
        fv, tv = data.get(fk), data.get(tk)
        if fv is not None and tv is not None:
            fd, td = _to_decimal_hours(fv), _to_decimal_hours(tv)
            # Sync: Rounding fix for DB
            data[fk], data[tk] = fd, td
            dur = td - fd
            if dur < 0: dur += 24 # midnight logic
            data[f"shift_{s}_subtotal"] = round(dur, 2)
        elif data.get(f"shift_{s}_subtotal") is None:
            data[f"shift_{s}_subtotal"] = 0.0

    # Sum: Daily subtotal
    s_a = float(data.get("shift_a_subtotal") or 0)
    s_b = float(data.get("shift_b_subtotal") or 0)
    s_c = float(data.get("shift_c_subtotal") or 0)
    tot = round(s_a + s_b + s_c, 2)
    data["total"] = tot

    # Balance: Carry-forward + current
    ps_raw = data.get("pre_sd_hrs") or 0
    ps = round(float(ps_raw), 2) if pre_sd_already_decimal else _to_decimal_hours(ps_raw)
    data["pre_sd_hrs"] = ps
    data["cumulative"] = round(tot + ps, 2)
    return data

def _log_shutdown_history(db: Session, record: dict, action: str = "UPDATE"):
    # History: Move current record to history table
    hd = {**record}; hd["updated_at"] = datetime.now()
    for k in ["history_id", "created_by_name", "updated_by_name"]: hd.pop(k, None)
    cols = ", ".join(hd.keys()); vals = ", ".join([f":{k}" for k in hd.keys()])
    q = text(f"INSERT INTO product_dispatch_shutdown_log_history ({cols}) VALUES ({vals})")
    db.execute(q, hd)

def get_latest_cumulative_total(db: Session, station: str, search_date: date = None):
    # Query: Get latest station balance
    p = {"station": station}; df = ""
    if search_date: df = "AND e.log_date <= :sdate"; p["sdate"] = search_date
    q = text(f"SELECT e.cumulative FROM product_dispatch_shutdown_log e JOIN product_dispatch_category_master m ON e.category_master_id = m.p_category_master_id WHERE m.station = :station {df} ORDER BY e.log_date DESC, e.p_dispatch_shutdown_id DESC LIMIT 1")
    res = db.execute(q, p).fetchone()
    return float(res[0]) if res else 0.0

def get_latest_cumulative_balance_summary(db: Session, search_date: date = None):
    # Dashboard: Global latest balance
    p = {}; df = ""
    if search_date: df = "AND e.log_date <= :sdate"; p["sdate"] = search_date
    q = text(f"SELECT e.cumulative FROM product_dispatch_shutdown_log e WHERE 1=1 {df} ORDER BY e.log_date DESC, e.p_dispatch_shutdown_id DESC LIMIT 1")
    res = db.execute(q, p).fetchone()
    return float(res[0]) if res else 0.0

def get_user_name(db: Session, user_id: int):
    # Resolve: ID to Name
    if not user_id: return None
    from app.models.UserModel import User
    u = db.query(User).get(user_id)
    return f"{u.first_name or ''} {u.last_name or ''}".strip() or u.username if u else None

# --- ACTIONS ---

def create_product_dispatch_shutdown(db: Session, payload: ProductDispatchShutdownCreate):
    # Create: Auth category, Auto-Carry, Calc, Insert
    m = db.query(ProductDispatchCategory).get(payload.category_master_id)
    if not m: raise HTTPException(status_code=404, detail="Master not found")
    data = payload.model_dump(exclude_unset=True); is_dec = False
    if not data.get("pre_sd_hrs"): 
        data["pre_sd_hrs"] = get_latest_cumulative_total(db, m.station)
        is_dec = True
    _calculate_shutdown_metrics(data, pre_sd_already_decimal=is_dec)
    cols = ", ".join(data.keys()); vals = ", ".join([f":{k}" for k in data.keys()])
    q = text(f"INSERT INTO product_dispatch_shutdown_log ({cols}) VALUES ({vals}) RETURNING p_dispatch_shutdown_id")
    res = db.execute(q, data); db.commit()
    return res.fetchone()[0]

def update_product_dispatch_shutdown(db: Session, p_dispatch_shutdown_id: int, payload: ProductDispatchShutdownUpdate):
    # Update: Log History, Merge data, Recalc metrics
    old = get_shutdown_log_by_id(db, p_dispatch_shutdown_id)
    if not old: return False
    _log_shutdown_history(db, old, "UPDATE")
    md = {**old}; nd = payload.model_dump(exclude_unset=True); md.update(nd)
    _calculate_shutdown_metrics(md, pre_sd_already_decimal=True)
    # Sync: Calculated fields
    for k in ["shift_a_subtotal", "shift_b_subtotal", "shift_c_subtotal", "total", "cumulative"]:
        nd[k] = md[k]
    cl = ", ".join([f"{k} = :{k}" for k in nd.keys()]); nd["p_dispatch_shutdown_id"] = p_dispatch_shutdown_id
    q = text(f"UPDATE product_dispatch_shutdown_log SET {cl} WHERE p_dispatch_shutdown_id = :p_dispatch_shutdown_id")
    db.execute(q, nd); db.commit()
    return True

def delete_product_dispatch_shutdown(db: Session, p_dispatch_shutdown_id: int):
    # Delete: Move to audit & clear
    old = get_shutdown_log_by_id(db, p_dispatch_shutdown_id)
    if old: _log_shutdown_history(db, old, "DELETE")
    q = text("DELETE FROM product_dispatch_shutdown_log WHERE p_dispatch_shutdown_id = :p_dispatch_shutdown_id")
    res = db.execute(q, {"p_dispatch_shutdown_id": p_dispatch_shutdown_id}); db.commit()
    return res.rowcount > 0

def get_shutdown_log_by_id(db: Session, p_dispatch_shutdown_id: int):
    # Fetch: Join users for names
    q = text("SELECT e.*, TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) as created_by_name, TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) as updated_by_name FROM product_dispatch_shutdown_log e LEFT JOIN users u1 ON CAST(e.created_by AS INTEGER) = u1.user_id LEFT JOIN users u2 ON CAST(e.updated_by AS INTEGER) = u2.user_id WHERE e.p_dispatch_shutdown_id = :id")
    res = db.execute(q, {"id": p_dispatch_shutdown_id}).fetchone()
    return dict(res._mapping) if res else None

def get_shutdown_logs_by_master_id(db: Session, master_id: int):
    # Summary: All logs + Daily consolidated totals
    m = db.query(ProductDispatchCategory).get(master_id)
    if not m: return None
    md = {c.name: getattr(m, c.name) for c in m.__table__.columns}
    md["created_by_name"] = get_user_name(db, m.created_by)
    res = db.execute(text("SELECT e.* FROM product_dispatch_shutdown_log e WHERE e.category_master_id = :id ORDER BY e.p_dispatch_shutdown_id ASC"), {"id": master_id}).fetchall()
    en = [dict(r._mapping) for r in res]
    # Sum: Consolidated day totals
    sm = {
        "shift_a_total": round(sum(e.get("shift_a_subtotal") or 0 for e in en), 2),
        "shift_b_total": round(sum(e.get("shift_b_subtotal") or 0 for e in en), 2),
        "shift_c_total": round(sum(e.get("shift_c_subtotal") or 0 for e in en), 2),
        "grand_total": round(sum(e.get("total") or 0 for e in en), 2),
        "final_cumulative": round(en[-1].get("cumulative") or 0, 2) if en else 0.0
    }
    return {"master": md, "entries": en, "summary": sm}
