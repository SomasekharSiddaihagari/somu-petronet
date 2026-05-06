from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from decimal import Decimal


class LeaveTypeSummary(BaseModel):
    available: Optional[Decimal] = Decimal("0.00")
    availed: Optional[Decimal] = Decimal("0.00")


class UserLeaveReport(BaseModel):
    emp_id: int
    emp_name: str
    station: Optional[str] = None
    casual_leave: LeaveTypeSummary
    earned_leave: LeaveTypeSummary
    half_pay_leave: LeaveTypeSummary
    total_leaves_availed: Decimal


class LeaveReportResponse(BaseModel):
    from_date: date
    to_date: date
    station: Optional[str] = None
    total_employees: int
    records: List[UserLeaveReport]