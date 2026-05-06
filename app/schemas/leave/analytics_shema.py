from decimal import Decimal
from pydantic import BaseModel
 
class HRStationLeaveCount(BaseModel):
    station_name: str
    total_leaves: float
 
 
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
 
class LeaveBalanceBase(BaseModel):
    user_id: Optional[int] = None
    type_id: Optional[int] = None
    allocated: Optional[float] = None
    used: Optional[float] = 0
    balance: Optional[float] = None
    is_usable: Optional[bool] = True
 
class LeaveBalanceCreate(LeaveBalanceBase):
    pass
 
class LeaveBalanceUpdate(LeaveBalanceBase):
    pass
 
class LeaveBalanceResponse(LeaveBalanceBase):
    balance_id: int
    created_date: Optional[datetime]
 
    class Config:
        orm_mode = True
class UpdateLeaveApplicationSupervisorRequest(BaseModel):
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    supervisor_id: Optional[int] = None
    supervisor_name: Optional[str] = None

    leave_type: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    number_of_days: Optional[Decimal] = None
    reason: Optional[str] = None

    contact_address: Optional[str] = None
    phone_number: Optional[str] = None

    reversal_from_date: Optional[date] = None
    reversal_to_date: Optional[date] = None
    reversal_remarks: Optional[str] = None

    status: Optional[str] = None
    comment: Optional[str] = None
    supervisor_remarks: Optional[str] = None

 
class UpdateLeaveApplicationSupervisorResponse(BaseModel):
    leave_id: int
    user_id: int
    supervisor_id: int
    supervisor_name: str
    status: str
    user_name: str
    reversal_from_date: Optional[date]
    reversal_to_date: Optional[date]
    reversal_remarks: Optional[str]
    supervisor_remarks: Optional[str]  # NEW FIELD
    reason: Optional[str]
    updated_at: datetime


class HRStationLeaveCount(BaseModel):
    station_id: int
    station_name: str
    total_leaves: float
 
class EmployeeSummary(BaseModel):
    first_name: str
    last_name: str
    supervisor_name: str
    total_leaves: int
    percentage_split: float
 
class MonthlyTrend(BaseModel):
    first_name: str
    last_name: str
    supervisor_name: str
    month: Optional[str]
    total_leaves: int
  
class StationSummary(BaseModel):
    station_id: int
    station_name: str
    total_leaves: float
    percentage_split: float
 
class MonthlyTrend(BaseModel):
    station_id: int
    station_name: str
    month: Optional[str]
    total_leaves: float
 
class HRStationLeaveCountResponse(BaseModel):
    station_summary: List[StationSummary]
    monthly_trends: List[MonthlyTrend]
class SupervisorLeaveCountResponse(BaseModel):
    employee_summary: List[EmployeeSummary]
    monthly_trends: List[MonthlyTrend]
 
class EmployeeSummary(BaseModel):
    first_name: str
    last_name: str
    supervisor_name: str
    total_leaves: int
    percentage_split: float
 
class MonthlyTrend(BaseModel):
    first_name: str
    last_name: str
    supervisor_name: str
    month: Optional[str]
    total_leaves: int
 
class SupervisorLeaveCountResponse(BaseModel):
    employee_summary: List[EmployeeSummary]
    monthly_trends: List[MonthlyTrend]

class SupervisorLeaveCount(BaseModel):
    user_name: str
    supervisor_name: str
    total_leaves: int
 
    class Config:
        orm_mode = True