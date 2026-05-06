from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class LeaveBase(BaseModel):
    leave_id: int
    user_id: Optional[int]
    supervisor_id: Optional[int]
    supervisor_name: Optional[str]
    user_name: Optional[str]
    leave_type: Optional[str]
    from_date: Optional[date]
    to_date: Optional[date]
    number_of_days: Optional[float]
    reason: Optional[str]
    status: Optional[str]
    comp_dates: Optional[List[date]] = None
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
