"""
Leave Report Router
===================

Endpoints
---------
GET /api/admin/leave-report
    Returns leave summary JSON for all users (or one user) in a date range.

GET /api/admin/leave-report/download
    Streams the same data as a formatted .xlsx file.

Query Parameters
----------------
from_date   : date (YYYY-MM-DD) – start of reporting period          [required]
to_date     : date (YYYY-MM-DD) – end of reporting period            [required]
user_id     : int               – filter to a single employee         [optional]
station     : str               – filter / label by station           [optional]

Permissions
-----------
Decorated with `require_admin` dependency – swap with your own auth guard.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session                  # ← sync Session
import io

from app.core.generate_leave_report import generate_leave_report_excel
from app.core.leave_report_service import get_leave_dates_report, get_leave_report
from app.database import get_db
from app.schemas.leave.leave_report import LeaveDatesResponse, LeaveReportResponse                     # adjust to your db dep
# from app.auth.dependencies import require_admin   # uncomment your auth guard




router = APIRouter(
    prefix="/api/admin/leave-report",
    tags=["Leave Report"],
    # dependencies=[Depends(require_admin)],        # uncomment to protect routes
)


def _validate_dates(from_date: date, to_date: date) -> None:
    if from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="`from_date` must be before or equal to `to_date`.",
        )


# ── JSON endpoint ─────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=LeaveReportResponse,
    summary="Get leave report (JSON)",
    description=(
        "Returns leave availed and available balance for all employees "
        "(or a single employee when `user_id` is supplied) within the given date range."
    ),
)
def get_leave_report_json(
    from_date: date = Query(..., description="Start of reporting period (YYYY-MM-DD)"),
    to_date:   date = Query(..., description="End of reporting period (YYYY-MM-DD)"),
    user_id:   Optional[int] = Query(None, description="Filter by specific employee ID"),
    station:   Optional[str] = Query(None, description="Filter / label by station name"),
    db: Session = Depends(get_db),
) -> LeaveReportResponse:
    _validate_dates(from_date, to_date)
    return get_leave_report(
        db=db,
        from_date=from_date,
        to_date=to_date,
        user_id=user_id,
        station=station,
    )   

@router.get(
    "/dates",
    response_model=LeaveDatesResponse,
    summary="Get leave dates detail report (JSON)",
    description=(
        "Returns detailed leave dates for employees within the given date range. "
        "Shows exact dates, leave types, and day types (full/half). "
        "Can filter by user_id, station, or leave_type."
    ),
)

def get_leave_dates_report_json(
    from_date: date = Query(..., description="Start of reporting period (YYYY-MM-DD)"),
    to_date: date = Query(..., description="End of reporting period (YYYY-MM-DD)"),
    user_id: Optional[int] = Query(None, description="Filter by specific employee ID"),
    station: Optional[str] = Query(None, description="Filter by station name"),
    leave_type: Optional[str] = Query(None, description="Filter by leave type code (e.g., CL, EL_E, HPL)"),
    db: Session = Depends(get_db),
    ) -> LeaveDatesResponse:
    _validate_dates(from_date, to_date)
    return get_leave_dates_report(
        db=db,
        from_date=from_date,
        to_date=to_date,
        user_id=user_id,
        station=station,
        leave_type=leave_type,
    )

# ── Excel download endpoint ───────────────────────────────────────────────────

@router.get(
    "/download",
    summary="Download leave report (.xlsx)",
    description=(
        "Generates and streams a formatted Excel leave report for the given date range. "
        "Pass `user_id` to download a report for a single employee."
    ),
    response_class=StreamingResponse,
    )
def download_leave_report_excel(
    from_date: date = Query(..., description="Start of reporting period (YYYY-MM-DD)"),
    to_date:   date = Query(..., description="End of reporting period (YYYY-MM-DD)"),
    user_id:   Optional[int] = Query(None, description="Filter by specific employee ID"),
    station:   Optional[str] = Query(None, description="Filter / label by station"),
    db: Session = Depends(get_db),
    ) -> StreamingResponse:
    _validate_dates(from_date, to_date)

    report = get_leave_report(
        db=db,
        from_date=from_date,
        to_date=to_date,
        user_id=user_id,
        station=station,
    )

    excel_bytes = generate_leave_report_excel(report)

    filename = (
        f"leave_report_{from_date}_{to_date}"
        + (f"_user{user_id}" if user_id else "")
        + ".xlsx"
    )

    return StreamingResponse(
        content=io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

from fastapi import APIRouter, Query
from datetime import date, timedelta
from typing import List, Dict, Any
from sqlalchemy import text


@router.get("/team-availability")
def get_team_availability(
    supervisor_id: int = Query(..., description="Supervisor ID"),
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db),
):
    # 1. Employees
    employees_sql = text("""
        SELECT 
            u.user_id,
            COALESCE(CONCAT(u.first_name, ' ', u.last_name), u.username) AS name,
            s.station_name AS station
        FROM users u
        LEFT JOIN station s ON s.station_id = u.station_id
        WHERE u.supervisor_id = :supervisor_id 
        AND u.is_deleted = false
        ORDER BY u.first_name, u.last_name
    """)
    employees = db.execute(employees_sql, {"supervisor_id": supervisor_id}).mappings().all()

    if not employees:
        return {"employees": [], "dates": [], "data": {}, "team_availability": []}

    employee_ids = [emp["user_id"] for emp in employees]

    # 2. Date range
    dates: List[date] = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)

    # 3. Leave days — LOWER() to avoid PostgreSQL case-sensitivity issues
    #    Fetch reversal_from_date / reversal_to_date for partial reversal handling
        leave_days_sql = text("""
        SELECT 
            la.user_id,
            lad.leave_date,
            la.status,
            la.reversal_from_date::date AS reversal_from_date,
            la.reversal_to_date::date   AS reversal_to_date
        FROM hr_leave_application_day lad
        JOIN hr_leave_application la ON la.leave_id = lad.leave_application_id
        WHERE la.supervisor_id = :supervisor_id
        AND la.user_id = ANY(:employee_ids)
        AND lad.leave_date BETWEEN :start_date AND :end_date
        AND LOWER(la.status) IN (
            'approved',
            'pending',
            'withdraw rejected',
            'withdraw pending',
            'reversal pending',
            'reversal rejected',
            'reversal approved'          -- <-- add this line
        )
    """)
    raw_leave_days = db.execute(leave_days_sql, {
        "supervisor_id": supervisor_id,
        "employee_ids": employee_ids,
        "start_date": start_date,
        "end_date": end_date,
    }).mappings().all()

    def _status_to_label_and_priority(
        status: str,
        leave_date: date = None,
        reversal_from: date = None,
        reversal_to: date = None,
    ):
        """
        Priority levels:
          3 - Reversal Approved AND leave_date is within reversal range → Working
          2 - On Leave (Approved / Withdraw Rejected / Withdraw Pending /
                        Reversal Pending / Reversal Rejected /
                        Reversal Approved but date outside reversal range)
          1 - Pending  (exact 'pending' only — NOT 'reversal pending')
          0 - Unknown / ignore
        """
        s = status.lower().strip()

        if s == "reversal approved":
            if leave_date and reversal_from and reversal_to:
                if reversal_from <= leave_date <= reversal_to:
                    return "Reversal Approved", 3   # this day was reversed → Working
            # Date outside reversal range → leave still stands
            return "On Leave", 2

        if s in ("approved", "withdraw rejected", "withdraw pending",
                 "reversal pending", "reversal rejected"):
            return "On Leave", 2

        if s == "pending":   # exact match only
            return "Pending", 1

        return None, 0

    # {user_id: {leave_date: "On Leave" | "Pending" | "Reversal Approved"}}
    leave_days_by_user: Dict[int, Dict[date, str]] = {}

    for ld in raw_leave_days:
        uid           = ld["user_id"]
        d             = ld["leave_date"]
        reversal_from = ld["reversal_from_date"]
        reversal_to   = ld["reversal_to_date"]

        new_label, new_pri = _status_to_label_and_priority(
            ld["status"],
            leave_date=d,
            reversal_from=reversal_from,
            reversal_to=reversal_to,
        )
        if new_label is None:
            continue

        leave_days_by_user.setdefault(uid, {})
        current_label = leave_days_by_user[uid].get(d)
        _, cur_pri = _status_to_label_and_priority(current_label) if current_label else (None, 0)

        if new_pri > cur_pri:
            leave_days_by_user[uid][d] = new_label

    # 4. Public holidays
    holidays_sql = text("""
        SELECT holiday_date, holiday_type 
        FROM hr_public_holiday 
        WHERE holiday_date BETWEEN :start_date AND :end_date 
          AND status = 'Active'
    """)
    raw_holidays = db.execute(holidays_sql, {
        "start_date": start_date,
        "end_date": end_date,
    }).mappings().all()
    holiday_map: Dict[date, str] = {h["holiday_date"]: h["holiday_type"] for h in raw_holidays}

    # 5. Per-employee week offs
    week_offs_sql = text("""
        SELECT user_id, week_off_day, effective_from, effective_to
        FROM employee_weekly_off
        WHERE user_id = ANY(:employee_ids)
          AND is_active = true
          AND effective_from <= :end_date
          AND (effective_to IS NULL OR effective_to >= :start_date)
    """)
    raw_week_offs = db.execute(week_offs_sql, {
        "employee_ids": employee_ids,
        "start_date": start_date,
        "end_date": end_date,
    }).mappings().all()

    week_offs_by_user: Dict[int, List[Dict]] = {}
    for wo in raw_week_offs:
        uid = wo["user_id"]
        iso_days = {int(x.strip()) for x in wo["week_off_day"].split(",") if x.strip()}
        week_offs_by_user.setdefault(uid, []).append({
            "days": iso_days,
            "from": wo["effective_from"],
            "to": wo["effective_to"],
        })

    def is_week_off(uid: int, d: date) -> bool:
        iso_day = d.isoweekday()
        for wo in week_offs_by_user.get(uid, []):
            if wo["from"] <= d and (wo["to"] is None or d <= wo["to"]):
                if iso_day in wo["days"]:
                    return True
        return False

    # 6. Build matrix
    matrix: Dict[int, List[str]] = {}
    working_counts = [0] * len(dates)

    for emp in employees:
        uid = emp["user_id"]
        row: List[str] = []
        user_leave_days = leave_days_by_user.get(uid, {})

        for i, d in enumerate(dates):
            if d in holiday_map:
                cell = "Week Off" if holiday_map[d] == "RESTRICTED" else "Public Holiday"
            elif is_week_off(uid, d):
                cell = "Week Off"
            elif d in user_leave_days:
                label = user_leave_days[d]
                cell = "Working" if label == "Reversal Approved" else label
            else:
                cell = "Working"

            row.append(cell)
            if cell == "Working":
                working_counts[i] += 1

        matrix[uid] = row

    # 7. Team availability %
    total_emp = len(employees)
    team_availability = [
        f"{round((count / total_emp) * 100)}%" if total_emp > 0 else "0%"
        for count in working_counts
    ]

    return {
        "employees": [
            {"id": emp["user_id"], "name": emp["name"], "station": emp["station"] or "Station Not Found"}
            for emp in employees
        ],
        "dates": [d.isoformat() for d in dates],
        "data": matrix,
        "team_availability": team_availability,
    }




@router.get("/hr-team-availability")
def get_hr_team_availability(
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db),
):
    # 1. All Employees
    employees_sql = text("""
        SELECT 
            u.user_id,
            COALESCE(CONCAT(u.first_name, ' ', u.last_name), u.username) AS name,
            s.station_name AS station
        FROM users u
        LEFT JOIN station s ON s.station_id = u.station_id
        WHERE u.is_deleted = false
          AND u.is_employee = true
        ORDER BY u.first_name, u.last_name
    """)
    employees = db.execute(employees_sql, {}).mappings().all()

    if not employees:
        return {"employees": [], "dates": [], "data": {}, "team_availability": []}

    employee_ids = [emp["user_id"] for emp in employees]

    # 2. Dates
    dates: List[date] = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)

    # 3. Leave days – now with explicit ::date casting (same as supervisor endpoint)
    leave_days_sql = text("""
        SELECT 
            lad.leave_date,
            la.user_id,
            la.status,
            la.reversal_from_date::date AS reversal_from_date,
            la.reversal_to_date::date   AS reversal_to_date
        FROM hr_leave_application_day lad
        JOIN hr_leave_application la ON lad.leave_application_id = la.leave_id
        WHERE la.user_id = ANY(:employee_ids)
          AND lad.leave_date BETWEEN :start_date AND :end_date
          AND LOWER(la.status) IN (
              'approved',
              'pending',
              'withdraw rejected',
              'withdraw pending',
              'reversal pending',
              'reversal rejected',
              'reversal approved'
          )
    """)
    raw_leave_days = db.execute(leave_days_sql, {
        "employee_ids": employee_ids,
        "start_date": start_date,
        "end_date": end_date,
    }).mappings().all()

    def _status_to_label_and_priority(
        status: str,
        leave_date: date = None,
        reversal_from: date = None,
        reversal_to: date = None,
    ):
        """
        Priority levels:
          3 - Reversal Approved AND leave_date is within reversal range → Working
          2 - On Leave (Approved, Withdraw Rejected, Withdraw Pending,
                        Reversal Pending, Reversal Rejected,
                        OR Reversal Approved but date outside reversal range)
          1 - Pending (exact 'pending' only)
          0 - Unknown / ignore
        """
        s = status.lower().strip()

        if s == "reversal approved":
            if leave_date and reversal_from and reversal_to:
                if reversal_from <= leave_date <= reversal_to:
                    return "Reversal Approved", 3   # Working
            return "On Leave", 2

        if s in ("approved", "withdraw rejected", "withdraw pending",
                 "reversal pending", "reversal rejected"):
            return "On Leave", 2

        if s == "pending":
            return "Pending", 1

        return None, 0

    # {user_id: {leave_date: "On Leave" | "Pending" | "Reversal Approved"}}
    leave_map: Dict[int, Dict[date, str]] = {}

    for row in raw_leave_days:
        uid = row["user_id"]
        d = row["leave_date"]
        reversal_from = row["reversal_from_date"]  # now a date or None
        reversal_to = row["reversal_to_date"]      # now a date or None

        new_label, new_pri = _status_to_label_and_priority(
            row["status"],
            leave_date=d,
            reversal_from=reversal_from,
            reversal_to=reversal_to,
        )
        if new_label is None:
            continue

        leave_map.setdefault(uid, {})
        current_label = leave_map[uid].get(d)
        _, cur_pri = _status_to_label_and_priority(current_label) if current_label else (None, 0)

        if new_pri > cur_pri:
            leave_map[uid][d] = new_label

    # 4. Public holidays (unchanged)
    holidays_sql = text("""
        SELECT holiday_date, holiday_type 
        FROM hr_public_holiday 
        WHERE holiday_date BETWEEN :start_date AND :end_date 
          AND status = 'Active'
    """)
    raw_holidays = db.execute(holidays_sql, {
        "start_date": start_date,
        "end_date": end_date,
    }).mappings().all()
    holiday_map: Dict[date, str] = {h["holiday_date"]: h["holiday_type"] for h in raw_holidays}

    # 5. Per-employee week offs (unchanged)
    week_offs_sql = text("""
        SELECT user_id, week_off_day, effective_from, effective_to
        FROM employee_weekly_off
        WHERE user_id = ANY(:employee_ids)
          AND is_active = true
          AND effective_from <= :end_date
          AND (effective_to IS NULL OR effective_to >= :start_date)
    """)
    raw_week_offs = db.execute(week_offs_sql, {
        "employee_ids": employee_ids,
        "start_date": start_date,
        "end_date": end_date,
    }).mappings().all()

    week_offs_by_user: Dict[int, List[Dict]] = {}
    for wo in raw_week_offs:
        uid = wo["user_id"]
        iso_days = {int(x.strip()) for x in wo["week_off_day"].split(",") if x.strip()}
        week_offs_by_user.setdefault(uid, []).append({
            "days": iso_days,
            "from": wo["effective_from"],
            "to": wo["effective_to"],
        })

    def is_week_off(uid: int, d: date) -> bool:
        iso_day = d.isoweekday()
        for wo in week_offs_by_user.get(uid, []):
            if wo["from"] <= d and (wo["to"] is None or d <= wo["to"]):
                if iso_day in wo["days"]:
                    return True
        return False

    # 6. Build matrix
    matrix: Dict[int, List[str]] = {}
    working_counts = [0] * len(dates)

    for emp in employees:
        uid = emp["user_id"]
        row: List[str] = []
        user_leaves = leave_map.get(uid, {})

        for i, d in enumerate(dates):
            if d in holiday_map:
                cell = "Week Off" if holiday_map[d] == "RESTRICTED" else "Public Holiday"
            elif is_week_off(uid, d):
                cell = "Week Off"
            elif d in user_leaves:
                label = user_leaves[d]
                cell = "Working" if label == "Reversal Approved" else label
            else:
                cell = "Working"

            row.append(cell)
            if cell == "Working":
                working_counts[i] += 1

        matrix[uid] = row

    # 7. Team availability
    total_emp = len(employees)
    team_availability = [
        f"{round((count / total_emp) * 100)}%" if total_emp > 0 else "0%"
        for count in working_counts
    ]

    return {
        "employees": [
            {"id": emp["user_id"], "name": emp["name"], "station": emp["station"] or "Station Not Found"}
            for emp in employees
        ],
        "dates": [d.isoformat() for d in dates],
        "data": matrix,
        "team_availability": team_availability,
    }