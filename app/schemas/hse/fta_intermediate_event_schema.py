# app/schemas/hse/fta_intermediate_event_schema.py
from pydantic import BaseModel


class FTAIntermediateEventCreate(BaseModel):
    top_event_id: int
    intermediate_e1: str | None = None
    intermediate_e2: str | None = None


class FTAIntermediateEventUpdate(BaseModel):
    intermediate_e1: str | None = None
    intermediate_e2: str | None = None


class FTAIntermediateEventResponse(BaseModel):
    intermediate_event_id: int
    top_event_id: int
    intermediate_e1: str | None
    intermediate_e2: str | None

    class Config:
        from_attributes = True
