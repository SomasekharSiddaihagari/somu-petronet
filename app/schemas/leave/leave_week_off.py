from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class EmployeeWeeklyOffBase(BaseModel):
    user_id: Optional[int] = None
    week_off_day: Optional[int] = None  # 1=Mon … 7=Sun
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    is_active: Optional[bool] = True


class EmployeeWeeklyOffCreate(BaseModel):
    user_id: int
    week_off_day: str = Field(..., example="1,2")
    effective_from: date
    effective_to: Optional[date] = None
    is_active: Optional[bool] = True


class EmployeeWeeklyOffUpdate(BaseModel):
    week_off_day: Optional[str] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    is_active: Optional[bool] = None

    
from pydantic import BaseModel
from datetime import date
from typing import Optional

class EmployeeWeeklyOffResponse(BaseModel):
    id: int
    user_id: Optional[int]
    week_off_day: Optional[str]   # ✅ STRING
    effective_from: Optional[date]
    effective_to: Optional[date]
    is_active: bool

    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    designation: Optional[str] = None
    station_name: Optional[str] = None

    class Config:
        from_attributes = True



class EmployeeWeeklyOffCreateByEmail(BaseModel):
    email: str = Field(..., )
    week_off_day: str = Field(..., example="1,2,3")
    effective_from: date
    effective_to: Optional[date] = None
    is_active: Optional[bool] = True