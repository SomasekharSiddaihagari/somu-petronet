# app/schemas/hse/hse_incident_investigation_team_schema.py
from pydantic import BaseModel
from typing import Optional


class InvestigationTeamCreate(BaseModel):
    incident_id: int

    sl_no: Optional[int] = None
    name: Optional[str] = None
    designation: Optional[str] = None
    role: Optional[str] = None
    is_acknowledged: Optional[bool] = None


class InvestigationTeamUpdate(BaseModel):
    sl_no: Optional[int] = None
    name: Optional[str] = None
    designation: Optional[str] = None
    role: Optional[str] = None
    is_acknowledged: Optional[bool] = None
