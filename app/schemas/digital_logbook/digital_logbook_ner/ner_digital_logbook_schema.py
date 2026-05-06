# app/schemas/ner_digital_logbook_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time


class NerDigitalLogBookBase(BaseModel):
    logbook_ref_no: Optional[str] = None

    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None

    log_date: Optional[date] = None
    start_time: Optional[time] = None

    handed_over_by: Optional[str] = None
    taken_over_by: Optional[str] = None

    is_shift_closed: Optional[bool] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    dkn: Optional[str] = None
    hsn: Optional[str] = None
    mlr: Optional[str] = None
    sv3: Optional[str] = None
    sv4: Optional[str] = None
    ms_logbook_id: Optional[int] = None

class NerDigitalLogBookCreate(NerDigitalLogBookBase):
    pass


class NerDigitalLogBookUpdate(NerDigitalLogBookBase):
    pass
