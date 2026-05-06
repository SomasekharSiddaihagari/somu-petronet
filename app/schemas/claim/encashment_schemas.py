from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


# =================================================
# ENCASHMENT MAIN
# =================================================
class EncashmentMainBase(BaseModel):
    encashment_ref_id: Optional[str] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    station: Optional[str] = None
    grade: Optional[str] = None
    claim_module: Optional[str] = None
    status: Optional[str] = None
    amount_claimed: Optional[Decimal] = None


    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    updated_by_supervisor: Optional[date] = None
    updated_by_supervisor_name: Optional[str] = None
    updated_by_hr: Optional[date] = None
    updated_by_hr_name: Optional[str] = None
    updated_by_finance: Optional[date] = None
    updated_by_finance_name: Optional[str] = None


class EncashmentMainCreate(EncashmentMainBase):
    pass


class EncashmentMainUpdate(EncashmentMainBase):
    pass


class EncashmentMainResponse(EncashmentMainBase):
    encashment_main_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# =================================================
# LEAVE ENCASHMENT SUBMISSION
# =================================================

class LeaveEncashmentBase(BaseModel):
    encashment_ref_id: Optional[str] = None
    encashment_main_id: Optional[int] = None

    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    designation: Optional[str] = None
    station: Optional[str] = None

    encashment_date: Optional[date] = None
    leave_type: Optional[str] = None
    encashment_opening: Optional[Decimal] = None
    non_encashment_opening: Optional[Decimal] = None
    total_encashment_opening: Optional[Decimal] = None
    el_encashable: Optional[Decimal] = None
    encash_el: Optional[Decimal] = None
    balance_as_on_date: Optional[Decimal] = None
    amount_claimed: Optional[Decimal] = None
    no_days_approved:Optional[Decimal] = None
    request_text: Optional[str] = None
    declaration_accepted: Optional[bool] = None

    status: Optional[str] = None

    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    updated_by_supervisor: Optional[date] = None
    updated_by_supervisor_name: Optional[str] = None
    supervisor_comment: Optional[str] = None

    updated_by_hr: Optional[date] = None
    updated_by_hr_name: Optional[str] = None
    hr_comment: Optional[str] = None

    updated_by_finance: Optional[date] = None
    updated_by_finance_name: Optional[str] = None
    finance_comment: Optional[str] = None


class LeaveEncashmentCreate(LeaveEncashmentBase):
    pass


class LeaveEncashmentUpdate(LeaveEncashmentBase):
    pass


class LeaveEncashmentResponse(LeaveEncashmentBase):
    leave_encashment_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
