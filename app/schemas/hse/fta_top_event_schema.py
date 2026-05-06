from pydantic import BaseModel
from datetime import datetime


# =========================
# CREATE
# =========================
class FTATopEventCreate(BaseModel):
    event_description: str | None = None


# =========================
# UPDATE
# =========================
class FTATopEventUpdate(BaseModel):
    event_description: str | None = None


# =========================
# RESPONSE
# =========================
class FTATopEventResponse(BaseModel):
    hiim_id: int
    fta_top_id: int
    event_description: str | None
    created_at: datetime

    class Config:
        from_attributes = True