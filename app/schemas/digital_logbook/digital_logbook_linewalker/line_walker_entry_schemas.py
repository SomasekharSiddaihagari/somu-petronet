from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


class LineWalkerEntryBase(BaseModel):
    line_walker_id: Optional[int] = None

    location_from: Optional[str] = None
    location_to: Optional[str] = None
    walker_name: Optional[str] = None

    start_time: Optional[time] = None
    start_officer_initials: Optional[str] = None

    end_time: Optional[time] = None
    end_officer_initials: Optional[str] = None

    device_status: Optional[str] = None
    remarks: Optional[str] = None

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
class LineWalkerEntryCreate(LineWalkerEntryBase):
    pass


class LineWalkerEntryUpdate(LineWalkerEntryBase):
    pass
