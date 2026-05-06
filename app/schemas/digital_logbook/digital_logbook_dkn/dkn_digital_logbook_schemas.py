from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime


class DknDigitalLogBookCreate(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    logbook_ref_no: Optional[str] = None
    log_date: Optional[date] = None
    start_time: Optional[time] = None

    handed_over_by: Optional[str] = None
    taken_over_by: Optional[str] = None

    is_shift_closed: Optional[bool] = False
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    hsn: Optional[str] = None
    ner: Optional[str] = None
    mlr: Optional[str] = None
    svb: Optional[str] = None
    ip1: Optional[str] = None
    sv9: Optional[str] = None
    sv10: Optional[str] = None
    ms_logbook_id: Optional[int] = None

class DknDigitalLogBookUpdate(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    logbook_ref_no: Optional[str] = None
    log_date: Optional[date] = None
    start_time: Optional[time] = None

    handed_over_by: Optional[str] = None
    taken_over_by: Optional[str] = None

    is_shift_closed: Optional[bool] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    hsn: Optional[str] = None
    ner: Optional[str] = None
    mlr: Optional[str] = None
    svb: Optional[str] = None
    ip1: Optional[str] = None
    sv9: Optional[str] = None
    sv10: Optional[str] = None
    ms_logbook_id: Optional[int] = None

class DknDigitalLogBookResponse(BaseModel):
    dkn_logbook_id: int
    station: Optional[str]
    station_in_charge: Optional[str]
    shift: Optional[str]
    logbook_ref_no: Optional[str]
    log_date: Optional[date]
    start_time: Optional[time]

    handed_over_by: Optional[str]
    taken_over_by: Optional[str]

    is_shift_closed: Optional[bool]
    created_by: Optional[int]
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    
    class Config:
        orm_mode = False
