from pydantic import BaseModel
from typing import Optional
from datetime import date


class SafetyCommitteeMinutesBase(BaseModel):
    location: Optional[str] = None
    frequency: Optional[str] = None
    station_id: Optional[int] = None
    meeting_date: Optional[date] = None
    next_meeting: Optional[str] = None
    remarks: Optional[str] = None


class SafetyCommitteeMinutesCreate(SafetyCommitteeMinutesBase):
    created_by: int
    meeting_no: str
    # ❌ do NOT take meeting_no from frontend


class SafetyCommitteeMinutesUpdate(SafetyCommitteeMinutesBase):
    updated_by: int
    is_active: Optional[bool] = True   # optional for soft delete/update


# response schema
class SafetyCommitteeMinutesOut(SafetyCommitteeMinutesBase):
    scmm_id: int
    meeting_no: str
    is_active: bool
