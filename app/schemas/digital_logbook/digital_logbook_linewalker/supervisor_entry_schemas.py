from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


class SupervisorEntryBase(BaseModel):
    line_walker_id: Optional[int] = None
    sl_no: Optional[int] = None
    spread: Optional[str] = None
    supervisor_name: Optional[str] = None

    start_time: Optional[time] = None
    end_time: Optional[time] = None

    area_of_visit: Optional[str] = None
    report: Optional[str] = None
    officer_initials: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class SupervisorEntryCreate(SupervisorEntryBase):
    pass


class SupervisorEntryUpdate(SupervisorEntryBase):
    pass
