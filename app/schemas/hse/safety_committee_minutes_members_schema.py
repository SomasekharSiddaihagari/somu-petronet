from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SafetyCommitteeMinutesMemberBase(BaseModel):
    minutes_id: Optional[int] = None
    member_name: Optional[str] = None
    user_id: Optional[int] = None
   
    

class SafetyCommitteeMinutesMemberCreate(SafetyCommitteeMinutesMemberBase):
    created_by: Optional[int] = None

class SafetyCommitteeMinutesMemberUpdate(SafetyCommitteeMinutesMemberBase):
    updated_by: Optional[int] = None
