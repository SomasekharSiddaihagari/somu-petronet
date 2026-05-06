from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FamilySubmissionCreate(BaseModel):
    user_id: int
    status: Optional[str] = None
    hr_comment: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None


class FamilySubmissionUpdate(BaseModel):
    status: Optional[str] = None
    hr_comment: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
