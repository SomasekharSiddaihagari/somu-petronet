from typing import Any, Dict, List
from pydantic import BaseModel
from datetime import date, time, datetime  # ← add time here

class TravelFormItem(BaseModel):
    data: Dict[str, Any]

    class Config:
        from_attributes = True

from pydantic import BaseModel
class SupervisorTravelResponse(BaseModel):
    forms: List[TravelFormItem]
    form_ids: Dict[str, List[int]]

    class Config:
        from_attributes = True
from typing import Optional
from decimal import Decimal
from datetime import date, datetime


from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime



class MealAllowanceBase(BaseModel):
    # Employee Info
    employee_name: Optional[str] = None
    employee_number: Optional[str] = None
    designation: Optional[str] = None
    grade: Optional[str] = None
    station: Optional[str] = None
    department: Optional[str] = None
    purpose_of_travel: Optional[str] = None

    # Totals
    total_excl_gst: Optional[Decimal] = None
    total_gst: Optional[Decimal] = None
    total_incl_gst: Optional[Decimal] = None
    advance_taken: Optional[Decimal] = None
    amount_receivable_payable: Optional[Decimal] = None

    # General Status & Comments
    comments: Optional[str] = None
    status: Optional[str] = None
    violation: Optional[str] = None

    # Supervisor
    updated_by_supervisor: Optional[datetime] = None
    updated_by_supervisor_name: Optional[str] = None
    supervisor_comments: Optional[str] = None


    updated_by_head_tech: Optional[date] = None
    updated_by_head_tech_name: Optional[str] = None
    head_tech_comments: Optional[str] = None



    # HR
    updated_by_hr: Optional[datetime] = None
    updated_by_hr_name: Optional[str] = None
    hr_comments: Optional[str] = None

    # MD
    updated_by_md: Optional[datetime] = None
    updated_by_md_name: Optional[str] = None
    md_comment: Optional[str] = None


    # Finance
    updated_by_finance: Optional[datetime] = None
    updated_by_finance_name: Optional[str] = None
    finance_comments: Optional[str] = None


class MealAllowanceCreate(MealAllowanceBase):
    user_id: int


class MealAllowanceUpdate(MealAllowanceBase):
    pass


class MealAllowanceResponse(MealAllowanceBase):
    meal_sheet_id: int
    requisition_number: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True



class MealAllowanceDetailBase(BaseModel):
    meal_sheet_id: int
    date: Optional[date]
    from_time: Optional[time] = None    # ← str → time
    to_time: Optional[time] = None      # ← str → time   
    travel_route: Optional[str]
    time_duration: Optional[str]
    distance_from_station: Optional[str]
    purpose: Optional[str]
    
    meal_amount: Optional[Decimal]
    meal_gst: Optional[Decimal]
    meal_total: Optional[Decimal]

    meal_proof: Optional[str]
    remarks: Optional[str]


class MealAllowanceDetailCreate(MealAllowanceDetailBase):
    pass


class MealAllowanceDetailUpdate(MealAllowanceDetailBase):
    pass


class MealAllowanceDetailResponse(MealAllowanceDetailBase):
    meal_sheet_detail_id: int
    created_at: datetime | None

    class Config:
        from_attributes = True