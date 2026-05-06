from pydantic import BaseModel
from typing import Optional
from datetime import date, time


# =========================
# BASE (SHARED FIELDS)
# =========================
class SafetyCommitteeMeetingBase(BaseModel):
    location: Optional[str] = None
    meeting_date: Optional[date] = None
    meeting_time: Optional[time] = None
    is_active: Optional[bool] = None


# =========================
# CREATE
# =========================
class SafetyCommitteeMeetingCreate(SafetyCommitteeMeetingBase):
    created_by: int


# =========================
# UPDATE
# =========================
class SafetyCommitteeMeetingUpdate(SafetyCommitteeMeetingBase):
    updated_by: int
