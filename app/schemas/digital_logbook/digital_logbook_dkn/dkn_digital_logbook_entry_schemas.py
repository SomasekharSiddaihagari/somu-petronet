from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


class DknDigitalLogBookEntryCreate(BaseModel):
    logbook_id: Optional[int] = None
    entry_time: Optional[time] = None
    location: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    logs: Optional[str] = None

class DknDigitalLogBookEntryUpdate(BaseModel):
    entry_time: Optional[time] = None
    location: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    logs: Optional[str] = None

class DknDigitalLogBookEntryResponse(BaseModel):
    dkn_entry_id: int
    logbook_id: Optional[int]
    entry_time: Optional[time]
    location: Optional[str]

    hsn: Optional[str]
    ner: Optional[str]
    mlr: Optional[str]
    svb: Optional[str]
    ip1: Optional[str]
    sv9: Optional[str]
    sv10: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    logs: Optional[str] = None
    class Config:
        orm_mode = False
