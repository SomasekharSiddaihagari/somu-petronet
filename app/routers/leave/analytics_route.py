import asyncio
from decimal import Decimal
from fastapi import APIRouter, BackgroundTasks, Body, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
# from app.crud.leave.analytics_crud import create_leave_balance, delete_leave_balance, get_all_leave_balances, get_leave_balance_by_id, update_leave_balance
# from app.core.leave_report_service import get_leave_analytics
from app.crud.leave.analytics_crud import (
    create_leave_balance, delete_leave_balance, get_all_leave_balances,
    get_leave_balance_by_id, update_leave_balance, get_leave_analytics
)
from app.crud.leave.leave_no_of_days import approve_reversal
from app.crud.leave.leave_notifications_crud import handle_supervisor_action
from app.database import get_db
from app.schemas.leave.analytics_shema import HRStationLeaveCount, HRStationLeaveCountResponse, LeaveBalanceCreate, LeaveBalanceResponse, LeaveBalanceUpdate, SupervisorLeaveCount, SupervisorLeaveCountResponse,  UpdateLeaveApplicationSupervisorResponse
 
router = APIRouter(
    prefix="/api/leave",
    tags=["Leave Analytics and Allocatons"]
)
 
# @router.get("/hr-station-leave-count", response_model=HRStationLeaveCountResponse)
# def get_hr_station_leave_count(db: Session = Depends(get_db)):
#     """
#     Get total approved leaves for all stations with percentage split and monthly trends.
#     """
#     query = text("""
#         SELECT public.get_hr_station_leave_count() AS result;
#     """)
 
#     row = db.execute(query).fetchone()
 
#     if not row or not row[0]:
#         raise HTTPException(status_code=404, detail="No leave data found")
 
#     # The function returns a JSON object; row[0] is already a Python dict
#     return row[0]


from typing import Optional
@router.get("/hr-station-leave-count")
def get_hr_station_leave_count(
    user_id:    Optional[int]  = Query(None, description="Filter by employee user_id"),
    station:    Optional[str]  = Query(None, description="Filter by station name"),
    leave_type: Optional[str]  = Query(None, description="Filter by leave type name"),
    year:       Optional[int]  = Query(None, description="Filter by specific year (e.g. 2025)"),
    db: Session = Depends(get_db)
):
    """
    Get dynamic leave usage trends.
    All filters are optional. When no filter is provided, returns current year data.
    """
    return get_leave_analytics(
        db=db,
        user_id=user_id,
        station=station,
        leave_type=leave_type,
        year=year
    )
 
 
# @router.get("/supervisor-leave-count", response_model=SupervisorLeaveCountResponse)
@router.get("/supervisor-leave-count")
def get_supervisor_leave_count_route(
    supervisor_id: int = Query(..., description="Supervisor ID"),
    user_id: Optional[int] = Query(None, description="Filter by employee user_id"),
    leave_type: Optional[str] = Query(None, description="Filter by leave type name"),
    year: Optional[int] = Query(None, description="Filter by specific year (e.g. 2025)"),
    db: Session = Depends(get_db)
):
    """
    Get dynamic leave usage trends for a supervisor.
    """
    return get_leave_analytics(
        db=db,
        supervisor_id=supervisor_id,
        user_id=user_id,
        leave_type=leave_type,
        year=year
    )

 
@router.get("/getaAllLeave", response_model=list[LeaveBalanceResponse])
def fetch_all(db: Session = Depends(get_db)):
    return get_all_leave_balances(db)
 
@router.get("/get_all_allocation")
def get_all_user_leave_balance(db: Session = Depends(get_db)):
    """
    Returns leave balance for ALL users grouped by readable leave type names.
    EL_E and EL_NE are clubbed and returned as 'Earned Leave'.
    """

    query = text("""
        SELECT
            lb.balance_id,
            lb.user_id,

            u.first_name,
            u.last_name,

            u.grade AS grade_name,
            st.station_name,

            lb.type_id,
            lt.code AS leave_code,
            lt.name AS leave_type_name,

            lb.allocated,
            lb.used,
            lb.balance,
            lb.is_usable,
            lb.created_date

        FROM leave_balances lb

        LEFT JOIN users u
            ON u.user_id = lb.user_id

        LEFT JOIN station st
            ON st.station_id = u.station_id

        LEFT JOIN leave_types lt
            ON lt.type_id = lb.type_id

        ORDER BY lb.user_id, lb.type_id;
    """)

    rows = db.execute(query).mappings().all()

    if not rows:
        raise HTTPException(status_code=404, detail="No leave balance data found")

    users_map = {}

    for row in rows:
        uid = row["user_id"]

        if uid not in users_map:
            users_map[uid] = {
                "user_id": uid,
                "username": f"{row['first_name']} {row['last_name']}".strip(),
                "grade_name": row["grade_name"],
                "station_name": row["station_name"],
                "leave_types": {}
            }

        # ---- CLUB EARNED LEAVE TYPES ----
        if row["leave_code"] in ("EL_E", "EL_NE"):
            leave_type_key = "Earned Leave"
        else:
            leave_type_key = row["leave_type_name"] or f"type_{row['type_id']}"

        leave_types = users_map[uid]["leave_types"]

        # ---- MERGE LOGIC ----
        if leave_type_key not in leave_types:
            leave_types[leave_type_key] = {
                "allocated": row["allocated"] or 0,
                "used": row["used"] or 0,
                "balance": row["balance"] or 0,
                "is_usable": row["is_usable"],
                "created_date": row["created_date"]
            }
        else:
            leave_types[leave_type_key]["allocated"] += row["allocated"] or 0
            leave_types[leave_type_key]["used"] += row["used"] or 0
            leave_types[leave_type_key]["balance"] += row["balance"] or 0

    return list(users_map.values())


# -----------------------------
# GET SUPERVISOR LEAVE COUNT
# -----------------------------
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime
from typing import List, Optional

logger = logging.getLogger("leave_application_debug")
logger.setLevel(logging.DEBUG)

class UpdateLeaveApplicationSupervisorRequest(BaseModel):
    leave_id: Optional[int] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    supervisor_id: Optional[int] = None
    supervisor_name: Optional[str] = None

    leave_type: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    number_of_days: Optional[Decimal] = None
    reason: Optional[str] = None

    document_path: Optional[str] = None
    contact_address: Optional[str] = None
    phone_number: Optional[str] = None

    reversal_from_date: Optional[date] = None
    reversal_to_date: Optional[date] = None
    reversal_remarks: Optional[str] = None
    leave_nature: Optional[str] = None

    status: Optional[str] = None
    comment: Optional[str] = None
    supervisor_remarks: Optional[str] = None


@router.put(
    "/update-leave-application-supervisor",
    response_model=List[UpdateLeaveApplicationSupervisorResponse]
)
def update_leave_application_supervisor(
    payload: UpdateLeaveApplicationSupervisorRequest = Body(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    ):
    params = payload.dict()

    if not params.get("leave_id"):
        raise HTTPException(status_code=400, detail="leave_id is required")

    incoming_status = (params.get("status") or "").strip().lower()

    if incoming_status == "reversal approved":

        leave_row = db.execute(text("""
            SELECT leave_id, status, reversal_from_date, reversal_to_date
            FROM hr_leave_application
            WHERE leave_id = :leave_id
        """), {"leave_id": params["leave_id"]}).fetchone()

        if not leave_row:
            raise HTTPException(status_code=404, detail="Leave application not found")

        if leave_row.status.lower() != "reversal pending":
            raise HTTPException(
                status_code=400,
                detail=f"Cannot approve reversal — current status is '{leave_row.status}', expected 'Reversal Pending'"
            )

        reversal_from = leave_row.reversal_from_date
        reversal_to   = leave_row.reversal_to_date

        if not reversal_from or not reversal_to:
            raise HTTPException(
                status_code=400,
                detail="Reversal dates are missing on the leave application"
            )

        if params.get("supervisor_remarks"):
            db.execute(text("""
                UPDATE hr_leave_application
                SET supervisor_remarks = :remarks,
                    updated_at = now()
                WHERE leave_id = :leave_id
            """), {
                "remarks": params["supervisor_remarks"],
                "leave_id": params["leave_id"]
            })

        # ✅ approve_reversal handles comp-off reset internally
        approve_reversal(db, params["leave_id"], reversal_from, reversal_to)

        updated_row = db.execute(text("""
            SELECT * FROM hr_leave_application
            WHERE leave_id = :leave_id
        """), {"leave_id": params["leave_id"]}).mappings().first()

        if not updated_row:
            raise HTTPException(status_code=404, detail="Leave application not found after update")

        background_tasks.add_task(
            handle_supervisor_action,
            db,
            updated_row,
            background_tasks
        )

        return [updated_row]

    # ─────────────────────────────────────────────────────────────
    # ALL OTHER CASES: normal generic update
    # ─────────────────────────────────────────────────────────────
    query = text("""
        UPDATE hr_leave_application
        SET
            user_id             = COALESCE(:user_id, user_id),
            user_name           = COALESCE(:user_name, user_name),
            supervisor_id       = COALESCE(:supervisor_id, supervisor_id),
            supervisor_name     = COALESCE(:supervisor_name, supervisor_name),
            leave_type          = COALESCE(:leave_type, leave_type),
            from_date           = COALESCE(CAST(:from_date AS DATE), from_date),
            to_date             = COALESCE(CAST(:to_date AS DATE), to_date),
            number_of_days      = COALESCE(:number_of_days, number_of_days),
            reason              = COALESCE(:reason, reason),
            document_path       = COALESCE(:document_path, document_path),
            contact_address     = COALESCE(:contact_address, contact_address),
            phone_number        = COALESCE(:phone_number, phone_number),
            reversal_from_date  = COALESCE(CAST(:reversal_from_date AS DATE), reversal_from_date),
            reversal_to_date    = COALESCE(CAST(:reversal_to_date AS DATE), reversal_to_date),
            reversal_remarks    = COALESCE(:reversal_remarks, reversal_remarks),
            status              = COALESCE(:status, status),
            leave_nature        = COALESCE(:leave_nature, leave_nature),
            supervisor_remarks  = COALESCE(:supervisor_remarks, supervisor_remarks),
            updated_at          = now()
        WHERE leave_id = :leave_id
        RETURNING *;
    """)

    result = db.execute(query, params)
    db.commit()

    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Leave application not found")

    # ✅ Release comp-off days if status is Rejected or Withdraw Approved
    release_statuses = {"rejected", "withdraw approved"}

    if incoming_status in release_statuses:
        db.execute(text("""
            UPDATE hr_leave_compof_day_new
            SET is_used = FALSE,
                leave_application_id = NULL
            WHERE leave_application_id = :leave_id
        """), {"leave_id": params["leave_id"]})
        db.commit()

    background_tasks.add_task(
        handle_supervisor_action,
        db,
        row,
        background_tasks
    )

    return [row]





