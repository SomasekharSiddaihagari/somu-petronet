from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


class HsnDigitalLogBookEntryCreate(BaseModel):
    hsn_logbook_id: Optional[int] = None
    entry_time: Optional[time] = None
    location: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    logs : Optional[str] = None

class HsnDigitalLogBookEntryUpdate(BaseModel):
    entry_time: Optional[time] = None
    location: Optional[str] = None

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    logs : Optional[str] = None

class HsnDigitalLogBookEntryResponse(BaseModel):
    hsn_entry_id: int
    hsn_logbook_id: Optional[int]

    entry_time: Optional[time]
    location: Optional[str]

    dkn: Optional[str]
    ner: Optional[str]
    mlr: Optional[str]
    sv5: Optional[str]
    sv6: Optional[str]
    sv7: Optional[str]

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = False
