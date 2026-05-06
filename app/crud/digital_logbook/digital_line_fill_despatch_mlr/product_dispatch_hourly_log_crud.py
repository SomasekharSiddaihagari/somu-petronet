from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_category import ProductDispatchCategory
from app.schemas.digital_logbook.digital_line_fill_despatch_mlr.product_dispatch_hourly_log_schema import ProductDispatchHourlyCreate, ProductDispatchHourlyUpdate

# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------

def _log_hourly_history(db: Session, record: dict, action: str = "UPDATE"):
    """Snapshot for history table"""
    history_data = {**record}
    
    # Add audit info
    history_data["updated_at"] = datetime.now()
    
    # Exclude fields not in the database model
    history_data.pop("history_id", None)
    history_data.pop("created_by_name", None)
    history_data.pop("updated_by_name", None)

    columns = ", ".join(history_data.keys())
    values = ", ".join([f":{k}" for k in history_data.keys()])
    
    query = text(f"""
        INSERT INTO product_dispatch_hourly_log_history ({columns})
        VALUES ({values})
    """)
    db.execute(query, history_data)


def get_user_name(db: Session, user_id: int):
    """Resolve IDs to names"""
    if not user_id:
        return None
    from app.models.UserModel import User
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        return f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username
    return None


# ------------------------------------------------------------------------------
# MAIN CRUD OPERATIONS
# ------------------------------------------------------------------------------

def create_product_dispatch_hourly(db: Session, payload: ProductDispatchHourlyCreate):
    """Create new hour entry"""
    # Validate Master ID
    master = db.query(ProductDispatchCategory).filter(
        ProductDispatchCategory.p_category_master_id == payload.category_master_id
    ).first()
    if not master:
        raise HTTPException(status_code=404, detail=f"Master record with ID {payload.category_master_id} not found")

    data = payload.model_dump(exclude_unset=True)
    columns = ", ".join(data.keys())
    values = ", ".join([f":{k}" for k in data.keys()])
    
    query = text(f"""
        INSERT INTO product_dispatch_hourly_log ({columns})
        VALUES ({values})
        RETURNING p_dispatch_hour_id
    """)

    result = db.execute(query, data)
    db.commit()
    return result.fetchone()[0]


def update_product_dispatch_hourly(db: Session, p_dispatch_hour_id: int, payload: ProductDispatchHourlyUpdate):
    """Update hour entry"""
    old_record = get_hourly_log_by_id(db, p_dispatch_hour_id)
    if not old_record:
        return False
    
    # Validate Master ID if being updated
    if payload.category_master_id is not None:
        master = db.query(ProductDispatchCategory).filter(
            ProductDispatchCategory.p_category_master_id == payload.category_master_id
        ).first()
        if not master:
            raise HTTPException(status_code=404, detail=f"Master record with ID {payload.category_master_id} not found")
            
    _log_hourly_history(db, old_record, "UPDATE")

    data = payload.model_dump(exclude_unset=True)
    if not data:
        return False

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    data["p_dispatch_hour_id"] = p_dispatch_hour_id

    query = text(f"""
        UPDATE product_dispatch_hourly_log
        SET {set_clause}
        WHERE p_dispatch_hour_id = :p_dispatch_hour_id
    """)

    db.execute(query, data)
    db.commit()
    return True


def delete_product_dispatch_hourly(db: Session, p_dispatch_hour_id: int):
    """Delete entry"""
    old_record = get_hourly_log_by_id(db, p_dispatch_hour_id)
    if old_record:
        _log_hourly_history(db, old_record, "DELETE")

    query = text("""
        DELETE FROM product_dispatch_hourly_log
        WHERE p_dispatch_hour_id = :p_dispatch_hour_id
    """)
    result = db.execute(query, {"p_dispatch_hour_id": p_dispatch_hour_id})
    db.commit()
    return result.rowcount > 0


def get_hourly_log_by_id(db: Session, p_dispatch_hour_id: int):
    """Fetch log by ID"""
    query = text("""
        SELECT 
            e.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) as created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) as updated_by_name
        FROM product_dispatch_hourly_log e
        LEFT JOIN users u1 ON CAST(e.created_by AS INTEGER) = u1.user_id
        LEFT JOIN users u2 ON CAST(e.updated_by AS INTEGER) = u2.user_id
        WHERE e.p_dispatch_hour_id = :id
    """)
    result = db.execute(query, {"id": p_dispatch_hour_id}).fetchone()
    if not result:
        return None
        
    return dict(result._mapping)


def get_hourly_logs_by_master_id(db: Session, master_id: int):
    """Fetch all entries for master"""
    master = db.query(ProductDispatchCategory).filter(
        ProductDispatchCategory.p_category_master_id == master_id
    ).first()
    if not master:
        return None
    
    master_data = {c.name: getattr(master, c.name) for c in master.__table__.columns}
    master_data["created_by_name"] = get_user_name(db, master.created_by)
    master_data["updated_by_name"] = get_user_name(db, master.updated_by)

    query = text("""
        SELECT 
            e.*,
            TRIM(CONCAT(COALESCE(u1.first_name, ''), ' ', COALESCE(u1.last_name, ''))) as created_by_name,
            TRIM(CONCAT(COALESCE(u2.first_name, ''), ' ', COALESCE(u2.last_name, ''))) as updated_by_name
        FROM product_dispatch_hourly_log e
        LEFT JOIN users u1 ON CAST(e.created_by AS INTEGER) = u1.user_id
        LEFT JOIN users u2 ON CAST(e.updated_by AS INTEGER) = u2.user_id
        WHERE e.category_master_id = :id
    """)
    result = db.execute(query, {"id": master_id}).fetchall()
    
    return {
        "master": master_data,
        "entries": [dict(r._mapping) for r in result]
    }
