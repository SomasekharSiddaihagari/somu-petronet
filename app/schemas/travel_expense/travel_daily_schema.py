from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class DailyAllowanceSheetBase(BaseModel):
    user_id: Optional[int] = None

    employee_name: Optional[str] = None
    employee_number: Optional[str] = None
    designation: Optional[str] = None
    grade: Optional[str] = None
    station: Optional[str] = None
    department: Optional[str] = None

    updated_by_supervisor: Optional[date] = None
    updated_by_supervisor_name: Optional[str] = None

    updated_by_hr: Optional[date] = None
    updated_by_hr_name: Optional[str] = None

    updated_by_md: Optional[date] = None
    updated_by_md_name: Optional[str] = None

    updated_by_finance: Optional[date] = None
    updated_by_finance_name: Optional[str] = None

    supervisor_comments: Optional[str] = None
    hr_comments: Optional[str] = None
    finance_comments: Optional[str] = None
    md_comment: Optional[str] = None

    updated_by_head_tech: Optional[date] = None
    updated_by_head_tech_name: Optional[str] = None
    head_tech_comments: Optional[str] = None

    total_excl_gst: Optional[Decimal] = None
    total_gst: Optional[Decimal] = None
    total_incl_gst: Optional[Decimal] = None
    advance_taken: Optional[Decimal] = None
    amount_receivable_payable: Optional[Decimal] = None

    comments: Optional[str] = None
    status: Optional[str] = None
    violation: Optional[str] = None
    purpose: Optional[str] = None


class DailyAllowanceSheetCreate(DailyAllowanceSheetBase):
    pass


class DailyAllowanceSheetUpdate(DailyAllowanceSheetBase):
    pass


class DailyAllowanceSheetResponse(DailyAllowanceSheetBase):
    da_sheet_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class DailyAllowanceDetailBase(BaseModel):
    user_id: Optional[int]
    da_sheet_id: Optional[int] 
    time_duration: Optional[str] 
    travel_from: Optional[str] 
    travel_to: Optional[str]
    distance_from_station: Optional[str] 
    purpose: Optional[str] 
    da_amount: Optional[float] 
    da_gst: Optional[float] 
    da_total: Optional[float] 
    remarks: Optional[str] 
    from_location: Optional[str]
    to_location: Optional[str] 
    from_date_time: Optional[datetime] 
    to_date_time: Optional[datetime]


class DailyAllowanceDetailCreate(DailyAllowanceDetailBase):
    pass


class DailyAllowanceDetailUpdate(DailyAllowanceDetailBase):
    pass


class DailyAllowanceDetailResponse(DailyAllowanceDetailBase):
    da_sheet_detail_id: int
    da_proof: Optional[str]  # comma-separated file paths

    class Config:
        orm_mode = True
