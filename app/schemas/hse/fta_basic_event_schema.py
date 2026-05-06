# app/schemas/hse/fta_basic_event_schema.py
from pydantic import BaseModel
from typing import Optional


class FTABasicEventCreate(BaseModel):
    intermediate_event_id: int
    e1_b1: Optional[str] = None
    e1_b2: Optional[str] = None
    e2_b1: Optional[str] = None
    e2_b2: Optional[str] = None


class FTABasicEventUpdate(BaseModel):
    e1_b1: Optional[str] = None
    e1_b2: Optional[str] = None
    e2_b1: Optional[str] = None
    e2_b2: Optional[str] = None
