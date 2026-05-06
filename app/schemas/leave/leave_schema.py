from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from datetime import date
 
class LeaveApplicationCreate(BaseModel):
    user_id: int
 
    supervisor_id: Optional[int] = None
    supervisor_name: Optional[str] = None
    user_name: Optional[str] = None
    supervisor_remarks: Optional[str] = None
 
    leave_type: Optional[str] = None
 
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    number_of_days: Optional[float] = None
 
    reason: Optional[str] = None
    document_path: Optional[str] = None
 
    contact_address: Optional[str] = None
    phone_number: Optional[str] = None
 
    reversal_from_date: Optional[date] = None
    reversal_to_date: Optional[date] = None
    reversal_remarks: Optional[str] = None
 
    status: Optional[str] = None
 
 
class LeaveApplicationDayCreate(BaseModel):
    leave_application_id: int
    leave_date: Optional[date] = None
    day_type: Optional[str] = None
    half_session: Optional[str] = None


class LeaveSummaryResponse(BaseModel):
    leave_type_id: int
    leave_type_name: str
    encashable: bool
    allocated: float
    applied: float
    balance: float

class LeaveBalanceUpdate(BaseModel):
    allocated: Optional[Decimal] = None
    used: Optional[Decimal] = None
    balance: Optional[Decimal] = None
    is_usable: Optional[bool] = None