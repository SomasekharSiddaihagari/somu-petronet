# app/schemas/dg_250kva_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time


class DG250KVABase(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[time] = None
    entry_date: Optional[date] = None
    status: Optional[str] = None
    document_number: Optional[str] = None
    ms_logbook_id: Optional[int] = None       # ← ADDED
    technician_id: Optional[int] = None       # ← ADDED
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None


class DG250KVACreate(DG250KVABase):
    pass


class DG250KVAUpdate(DG250KVABase):
    pass
