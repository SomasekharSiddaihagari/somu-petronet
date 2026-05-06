from pydantic import BaseModel, Field
from typing import Optional, Literal


class IncidentInvestigationTeamCreate(BaseModel):
    prevention_id: Optional[int] = None

    sl_no: Optional[int] = None
    member_name: Optional[str] = None
    designation: Optional[str] = None
    station: Optional[str] = None

    role: Optional[str] = None   # Leader/Member

    is_leader: Optional[bool] = False
    is_member: Optional[bool] = True

    leader_acknowledged: Optional[bool] = False
    member_acknowledged: Optional[bool] = False
    user_id: Optional[int] = None


class IncidentInvestigationTeamUpdate(BaseModel):
    prevention_id: Optional[int] = None
    sl_no: Optional[int] = None
    member_name: Optional[str] = None
    designation: Optional[str] = None
    station: Optional[str] = None
    role: Optional[str] = None

    is_leader: Optional[bool] = None
    is_member: Optional[bool] = None

    leader_acknowledged: Optional[bool] = None
    member_acknowledged: Optional[bool] = None

    user_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None