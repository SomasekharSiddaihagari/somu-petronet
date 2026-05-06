from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel


class FireEngineTestMasterBase(BaseModel):
    document_number: Optional[str] = None
    station_name: Optional[str] = None
    station_incharge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[time] = None
    log_date: Optional[date] = None
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None
    technician_name: Optional[str] = None
    technician_signature: Optional[str] = None

    engineer_name: Optional[str] = None
    engineer_signature: Optional[str] = None

    status: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class FireEngineTestMasterCreate(FireEngineTestMasterBase):
    pass


class FireEngineTestMasterUpdate(FireEngineTestMasterBase):
    pass


class FireEngineTestMasterResponse(FireEngineTestMasterBase):
    fire_id: int
    created_at : Optional[datetime] = None

    class Config:
        orm_mode = True
