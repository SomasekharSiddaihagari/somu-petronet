from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


class MlrDigitalLogBookEntryCreate(BaseModel):
    mlr_logbook_id: Optional[int] = None
    entry_time: Optional[time] = None
    location: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    logs: Optional[str] = None

class MlrDigitalLogBookEntryUpdate(BaseModel):
    entry_time: Optional[time] = None
    location: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    logs : Optional[str] = None

class MlrDigitalLogBookEntryResponse(BaseModel):
    mlr_entry_id: int
    mlr_logbook_id: Optional[int]

    entry_time: Optional[time]
    location: Optional[str]

    dkn: Optional[str]
    hsn: Optional[str]
    ner: Optional[str]
    sv1: Optional[str]
    sv2: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = False
