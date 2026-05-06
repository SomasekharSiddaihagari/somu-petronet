from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime


class LineWalkerMasterBase(BaseModel):
    document_no: Optional[str] = None
    station_name: Optional[str] = None
    station_incharge_name: Optional[str] = None
    shift_name: Optional[str] = None
    shift_start_time: Optional[time] = None
    log_date: Optional[date] = None
    ms_logbook_id: Optional[int] = None  

    reporting_location: Optional[str] = None
    critical_report: Optional[str] = None
    station_incharge_signature: Optional[str] = None

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class LineWalkerMasterCreate(LineWalkerMasterBase):
    pass


class LineWalkerMasterUpdate(LineWalkerMasterBase):
    pass
