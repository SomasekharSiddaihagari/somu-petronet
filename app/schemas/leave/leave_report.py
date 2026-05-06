from datetime import date
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel


class LeaveTypeSummary(BaseModel):
    code: str
    name: str
    available: Decimal
    availed: Decimal
    encashed: Decimal = Decimal("0.00")
    auto_encashed: Decimal = Decimal(0) 

class UserLeaveReport(BaseModel):
    emp_id: int                
    emp_code: str                
    emp_name: str
    station: Optional[str]
    station_id: Optional[int]
    leave_types: List[LeaveTypeSummary]
    total_leaves_availed: Decimal


class LeaveReportResponse(BaseModel):
    from_date: date
    to_date: date
    station: Optional[str]
    total_employees: int
    leave_type_meta: List[dict]               # [{"code": "CL", "name": "Casual Leave"}, ...]
    records: List[UserLeaveReport]


class LeaveDateDetail(BaseModel):
    leave_date: date
    day_type: str  # 'full' or 'half'
    leave_type_code: str  # leave type code (e.g., CL, EL_E)
    leave_type_name: str  # leave type full name
    status: str
    leave_application_id: int
    
    class Config:
        from_attributes = True

class UserLeaveDatesReport(BaseModel):
    emp_id: int
    emp_code: str
    emp_name: str
    station: Optional[str] = None
    station_id: Optional[int] = None
    leave_dates: List[LeaveDateDetail]
    total_days: Decimal

class LeaveDatesResponse(BaseModel):
    from_date: date
    to_date: date
    station: Optional[str] = None
    total_employees: int
    records: List[UserLeaveDatesReport]
    