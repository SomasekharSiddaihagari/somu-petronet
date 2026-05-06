from datetime import datetime, date, time, timedelta
from typing import Any, List
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.UserModel import User

from app.models.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category import (
    ProductDispatchCategory,
)
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category_schema import (
    ProductDispatchCategoryCreate,
    ProductDispatchCategoryUpdate,
)

# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------


def _process_dispatch_result(
    db: Session, result: Any, entry_table: str, shift_id: int = None
) -> dict:
    """Attach child entries and resolve names"""
    if not result:
        return {}

    d = dict(result)
    master_id = d.get("p_category_master_id") or d.get("category_master_id")

    if not master_id:
        return d

    # Fetch child entries with audit names using LEFT JOINs
    order_by = "ORDER BY e.created_at ASC"
    if entry_table == "product_dispatch_hourly_log":
        order_by = "ORDER BY e.log_time ASC"

    # Apply shift filter if entry table is shift log
    shift_filter = ""
    params = {"id": master_id}
    if entry_table == "product_dispatch_shift_log" and shift_id is not None:
        shift_filter = "AND e.shift_id = :sid"
        params["sid"] = shift_id

    query = text(
        f"""
        SELECT 
            e.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) as created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) as updated_by_name
        FROM {entry_table} e
        LEFT JOIN users u1 ON CAST(e.created_by AS INTEGER) = u1.user_id
        LEFT JOIN users u2 ON CAST(e.updated_by AS INTEGER) = u2.user_id
        WHERE e.category_master_id = :id 
        {shift_filter}
        {order_by}
    """
    )

    entries_raw = db.execute(query, params).mappings().all()
    entries = [dict(e) for e in entries_raw]

    if entry_table == "product_dispatch_shift_log":
        # For unified shift log, we need to fetch and group its raw sub-entries
        for entry in entries:
            shift_log_id = entry.get("shift_log_id")
            sub_query = text(
                """
                SELECT * FROM product_dispatch_log_entry 
                WHERE shift_log_id = :sid 
                ORDER BY entry_id ASC
            """
            )
            sub_results = db.execute(sub_query, {"sid": shift_log_id}).mappings().all()

            # Map raw rows into specific grouped lists for the frontend
            entry["suction_movements"] = [
                dict(r) for r in sub_results if r["entry_type"] == "SUCTION"
            ]
            entry["line_fill_entries"] = [
                dict(r) for r in sub_results if r["entry_type"] == "LINE_FILL"
            ]
            entry["section_capacity_summary"] = [
                dict(r) for r in sub_results if r["entry_type"] == "CAPACITY"
            ]

    elif entry_table == "product_dispatch_shutdown_log":
        # Calculate daily totals for the summary row in Figma
        d["summary"] = {
            "shift_a_total": round(sum(e.get("shift_a_subtotal") or 0 for e in entries), 2),
            "shift_b_total": round(sum(e.get("shift_b_subtotal") or 0 for e in entries), 2),
            "shift_c_total": round(sum(e.get("shift_c_subtotal") or 0 for e in entries), 2),
            "grand_total": round(sum(e.get("total") or 0 for e in entries), 2),
            "final_cumulative": round(entries[-1].get("cumulative") or 0, 2) if entries else 0.0
        }

    d["entries"] = entries
    return d


def _log_category_history(db: Session, record: dict, action: str = "UPDATE"):
    """Snapshot for master history"""
    history_data = {**record}

    # Add audit info
    history_data["updated_at"] = datetime.now()

    # Exclude redundant PK and virtual fields
    history_data.pop("history_id", None)
    history_data.pop("created_by_name", None)
    history_data.pop("updated_by_name", None)

    columns = ", ".join(history_data.keys())
    values = ", ".join([f":{k}" for k in history_data.keys()])

    query = text(
        f"""
        INSERT INTO product_dispatch_category_master_history ({columns})
        VALUES ({values})
    """
    )
    db.execute(query, history_data)


def get_user_name(db: Session, user_id: int):
    """Resolve IDs to names"""
    if not user_id:
        return None

    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        return (
            f"{user.first_name or ''} {user.last_name or ''}"
        ).strip() or user.username
    return None


# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------


def get_product_dispatch_category_by_id(db: Session, p_category_master_id: int):
    """Fetch category by ID"""
    query = text(
        "SELECT * FROM product_dispatch_category_master WHERE p_category_master_id = :id"
    )
    result = db.execute(query, {"id": p_category_master_id}).fetchone()
    return dict(result._mapping) if result else None


def create_product_dispatch_category(
    db: Session, payload: ProductDispatchCategoryCreate
):
    """Create new category master"""
    data = payload.model_dump(exclude_unset=True)
    columns = ", ".join(data.keys())
    values = ", ".join([f":{k}" for k in data.keys()])

    query = text(
        f"""
        INSERT INTO product_dispatch_category_master ({columns})
        VALUES ({values})
        RETURNING p_category_master_id
    """
    )

    result = db.execute(query, data)
    db.commit()
    return result.fetchone()[0]


def update_product_dispatch_category(
    db: Session, p_category_master_id: int, payload: ProductDispatchCategoryUpdate
):
    """Update category master"""
    old_record = get_product_dispatch_category_by_id(db, p_category_master_id)
    if not old_record:
        return False

    _log_category_history(db, old_record, "UPDATE")

    data = payload.model_dump(exclude_unset=True)
    if not data:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    data["p_category_master_id"] = p_category_master_id

    query = text(
        f"""
        UPDATE product_dispatch_category_master
        SET {set_clause}
        WHERE p_category_master_id = :p_category_master_id
    """
    )

    db.execute(query, data)
    db.commit()
    return True


def delete_product_dispatch_category(db: Session, p_category_master_id: int):
    """Delete master and cascade to logs"""
    # 1. Check if record exists
    old_record = get_product_dispatch_category_by_id(db, p_category_master_id)
    if not old_record:
        return False

    # 2. Archive before deletion
    _log_category_history(db, old_record, "DELETE")

    # 3. Clean up linked entries (Cascade Delete)
    log_tables = [
        "product_dispatch_hourly_log",
        "product_dispatch_shift_log",
        "product_dispatch_shutdown_log",
    ]

    for table in log_tables:
        db.execute(
            text(f"DELETE FROM {table} WHERE category_master_id = :id"),
            {"id": p_category_master_id},
        )

    # 4. Finally delete the Master record
    query = text(
        """
        DELETE FROM product_dispatch_category_master
        WHERE p_category_master_id = :p_category_master_id
    """
    )
    result = db.execute(query, {"p_category_master_id": p_category_master_id})
    db.commit()
    return result.rowcount > 0


def get_product_dispatch_category_with_names(db: Session, p_category_master_id: int):
    """Fetch record with resolved names"""
    master = (
        db.query(ProductDispatchCategory)
        .filter(ProductDispatchCategory.p_category_master_id == p_category_master_id)
        .first()
    )
    if not master:
        return None

    master_data = {c.name: getattr(master, c.name) for c in master.__table__.columns}
    master_data["created_by_name"] = get_user_name(db, master.created_by)
    master_data["updated_by_name"] = get_user_name(db, master.updated_by)

    return master_data


def get_common_dispatch_by_date(
    db: Session, search_date: date, entry_table: str, shift_id: int = None
):
    """Generic fetcher for 7AM-7AM window"""
    start_dt = datetime.combine(search_date, time(7, 0))
    end_dt = start_dt + timedelta(days=1)

    query = text(
        """
        SELECT 
            m.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) as created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) as updated_by_name,
            COALESCE(m.technician_id, 0) as technician_id,
            COALESCE(m.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(m.created_by AS INTEGER), 0) as created_by, 
            COALESCE(m.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(m.updated_by AS INTEGER), 0) as updated_by
        FROM product_dispatch_category_master m
        JOIN logbook_shift_master LSM ON m.ms_logbook_id = LSM.ms_logbook_id
        LEFT JOIN users u1 ON CAST(m.created_by AS INTEGER) = u1.user_id
        LEFT JOIN users u2 ON CAST(m.updated_by AS INTEGER) = u2.user_id
        WHERE LSM.created_at >= :start_dt AND LSM.created_at < :end_dt
          AND m.created_at >= :start_dt AND m.created_at < :end_dt
        ORDER BY m.p_category_master_id DESC
    """
    )

    results = (
        db.execute(query, {"start_dt": start_dt, "end_dt": end_dt}).mappings().all()
    )

    # Fetch and attach entries
    processed_data = [
        _process_dispatch_result(db, row, entry_table, shift_id) for row in results
    ]

    # Filter: Only include masters that have at least one sub-entry
    final_data = [d for d in processed_data if len(d.get("entries", [])) > 0]

    # Sort: Newest master record first
    final_data.sort(key=lambda x: str(x.get("created_at")), reverse=True)

    return final_data


def get_shift_log_dispatch_by_date(
    db: Session, search_date: date, shift_id: int
):
    """Specific fetcher for Shift Log with 1-3 ID validation"""
    if shift_id not in [1, 2, 3]:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid Shift ID {shift_id}. Only 1 (A), 2 (B), or 3 (C) are allowed."
        )

    start_dt = datetime.combine(search_date, time(7, 0))
    end_dt = start_dt + timedelta(days=1)

    query = text(
        """
        SELECT 
            m.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) as created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) as updated_by_name,
            COALESCE(m.technician_id, 0) as technician_id,
            COALESCE(m.created_at, CURRENT_TIMESTAMP) as created_at, 
            COALESCE(CAST(m.created_by AS INTEGER), 0) as created_by, 
            COALESCE(m.updated_at, CURRENT_TIMESTAMP) as updated_at, 
            COALESCE(CAST(m.updated_by AS INTEGER), 0) as updated_by
        FROM product_dispatch_category_master m
        JOIN logbook_shift_master LSM ON m.ms_logbook_id = LSM.ms_logbook_id
        LEFT JOIN users u1 ON CAST(m.created_by AS INTEGER) = u1.user_id
        LEFT JOIN users u2 ON CAST(m.updated_by AS INTEGER) = u2.user_id
        WHERE LSM.created_at >= :start_dt AND LSM.created_at < :end_dt
          AND m.created_at >= :start_dt AND m.created_at < :end_dt
        ORDER BY m.p_category_master_id DESC
    """
    )

    results = db.execute(query, {"start_dt": start_dt, "end_dt": end_dt}).mappings().all()

    processed_data = [
        _process_dispatch_result(db, row, "product_dispatch_shift_log", shift_id) for row in results
    ]

    # Only include results that have matching shift entries
    final_data = [d for d in processed_data if len(d.get("entries", [])) > 0]
    final_data.sort(key=lambda x: str(x.get("created_at")), reverse=True)

    return final_data


def get_combined_hourly_by_date(db: Session, search_date: date):
    return get_common_dispatch_by_date(db, search_date, "product_dispatch_hourly_log")


def get_combined_shutdown_by_date(db: Session, search_date: date):
    return get_common_dispatch_by_date(db, search_date, "product_dispatch_shutdown_log")


def get_combined_shift_log_by_date(db: Session, search_date: date, shift_id: int):
    return get_shift_log_dispatch_by_date(db, search_date, shift_id)


def get_shift_log_by_master_id(db: Session, master_id: int, shift_id: int = None):
    master = get_product_dispatch_category_with_names(db, master_id)
    if not master:
        return None

    # Process the result to attach entries (with optional shift filter)
    result = _process_dispatch_result(
        db, master, "product_dispatch_shift_log", shift_id
    )

    # If a shift_id is provided, only return data if entries for that shift exist
    if shift_id is not None and not result.get("entries"):
        return None

    return {"master": master, "entries": result.get("entries", [])}


def get_category_master_by_date(db: Session, search_date: date):
    """Fetch only master records for a specific logbook date with resolved audit names."""
    query = text("""
        SELECT 
            m.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) as created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) as updated_by_name
        FROM product_dispatch_category_master m
        LEFT JOIN users u1 ON CAST(m.created_by AS INTEGER) = u1.user_id
        LEFT JOIN users u2 ON CAST(m.updated_by AS INTEGER) = u2.user_id
        WHERE m.logbook_date = :search_date 
        ORDER BY m.p_category_master_id DESC
    """)
    results = db.execute(query, {"search_date": search_date}).mappings().all()
    return [dict(row) for row in results]
