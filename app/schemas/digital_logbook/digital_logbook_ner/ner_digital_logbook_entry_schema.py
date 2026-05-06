# app/schemas/ner_digital_logbook_entry_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time


class NerDigitalLogBookEntryBase(BaseModel):
    ner_logbook_id: Optional[int] = None

    entry_time: Optional[time] = None
    location: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    logs: Optional[str] =None

class NerDigitalLogBookEntryCreate(NerDigitalLogBookEntryBase):
    pass


class NerDigitalLogBookEntryUpdate(NerDigitalLogBookEntryBase):
    pass
