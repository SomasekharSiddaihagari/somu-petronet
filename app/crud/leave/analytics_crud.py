from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.leave.leave_balance import LeaveBalance
from app.schemas.leave.analytics_shema import LeaveBalanceCreate, LeaveBalanceUpdate

from typing import Optional, List 
from datetime import date, timedelta

def get_leave_analytics(
    db: Session,
    user_id:   Optional[int]  = None,
    station:   Optional[str]  = None,
    leave_type: Optional[str] = None,
    supervisor_id: Optional[int] = None,
    year: Optional[int] = None
) -> List[dict]:
    # ── Build dynamic internal filters ───────────────────────────────────────────
    filter_clauses = ["LOWER(hla.status) IN ('approved', 'reversal approved', 'withdraw approved', 'reversal pending', 'withdraw pending', 'withdraw rejected')"]

    params: dict = {}
    
    # Calculate Year and Date Range
    current_date = date.today()
    target_year = year if year else current_date.year
    
    series_start = f"{target_year}-01-01"
    series_end = f"{target_year}-12-01"

    params["target_year"] = target_year
    params["series_start"] = series_start
    params["series_end"] = series_end

    filter_clauses.append("EXTRACT(YEAR FROM hla.from_date) = :target_year")

    if user_id:
        filter_clauses.append("hla.user_id = :user_id")
        params["user_id"] = user_id
 
    if station:
        filter_clauses.append("LOWER(s.station_name) = LOWER(:station)")
        params["station"] = station
 
    if leave_type:
        filter_clauses.append("LOWER(hla.leave_type) = LOWER(:leave_type)")
        params["leave_type"] = leave_type

    if supervisor_id:
        filter_clauses.append("hla.supervisor_id = :supervisor_id")
        params["supervisor_id"] = supervisor_id
 
    filter_sql = " AND ".join(filter_clauses)
 
    # ── Single Query for Dynamic Trends ────────────────────────────────────
    query_sql = f"""
        WITH months AS (
            SELECT date_trunc('month', d) as m
            FROM generate_series(
                CAST(:series_start AS DATE),
                CAST(:series_end AS DATE),
                interval '1 month'
            ) d
        ),
        leave_data AS (
            SELECT
                date_trunc('month', hla.from_date) as month_date,
                SUM(CASE WHEN LOWER(hla.status) = 'withdraw approved' THEN 0 ELSE hla.number_of_days END) as monthly_total
            FROM hr_leave_application hla
            LEFT JOIN users u ON u.user_id = hla.user_id
            LEFT JOIN station s ON s.station_id = u.station_id
            WHERE {filter_sql}
            GROUP BY 1
        )
        SELECT
            TO_CHAR(months.m, 'FMMonth YYYY') as month_label,
            COALESCE(ld.monthly_total, 0) as total_leaves
        FROM months
        LEFT JOIN leave_data ld ON ld.month_date = months.m
        ORDER BY months.m DESC;
    """
 
    res = db.execute(text(query_sql), params).mappings().all()
 
    return [
        {
            "month": r["month_label"],
            "total_leaves": float(r["total_leaves"]),
        }
        for r in res
    ]


def get_all_leave_balances(db: Session):
    return db.query(LeaveBalance).all()
 
def get_leave_balance_by_id(db: Session, balance_id: int):
    return db.query(LeaveBalance).filter(LeaveBalance.balance_id == balance_id).first()
 
def create_leave_balance(db: Session, data: LeaveBalanceCreate):
    obj = LeaveBalance(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
 
def update_leave_balance(db: Session, balance_id: int, data: LeaveBalanceUpdate):
    obj = db.query(LeaveBalance).filter(LeaveBalance.balance_id == balance_id).first()
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj
 
def delete_leave_balance(db: Session, balance_id: int):
    obj = db.query(LeaveBalance).filter(LeaveBalance.balance_id == balance_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False