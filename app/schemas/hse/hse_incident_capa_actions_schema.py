# app/schemas/hse/hse_incident_capa_actions_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import date


class IncidentCAPACreate(BaseModel):
    incident_id: int
    action: Optional[str] = None
    action_type: Optional[str] = None
    target_date: Optional[date] = None


class IncidentCAPAUpdate(BaseModel):
    action: Optional[str] = None
    action_type: Optional[str] = None
    target_date: Optional[date] = None
