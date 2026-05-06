from pydantic import BaseModel
from typing import List, Optional

class MemberItem(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    station: Optional[int] = None
    is_active: Optional[bool] = True
    user_id: Optional[int] = None
    


class SafetyCommitteeMemberCreate(BaseModel):
    created_by: Optional[int] = None
    members: List[MemberItem]   # 🔥 multiple members array


class SafetyCommitteeMemberUpdate(BaseModel):
    sl_no: Optional[int] = None
    name: Optional[str] = None
    designation: Optional[str] = None
    station: Optional[int] = None
    is_active: Optional[bool] = True
    updated_by: Optional[int] = None
    user_id: Optional[int] = None
    


class TeamResponse(BaseModel):
    team_id: int
    message: str
