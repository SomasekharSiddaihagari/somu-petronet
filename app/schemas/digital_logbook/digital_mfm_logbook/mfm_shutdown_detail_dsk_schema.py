# app/schemas/mfm_shutdown_detail_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time


class MFMShutdownDetailBase(BaseModel):
    master_id: Optional[int] = None

    from_time: Optional[time] = None
    to_time: Optional[time] = None
    reason: Optional[str] = None

    kwh: Optional[float] = None
    kvah: Optional[float] = None
    pf: Optional[float] = None

    psd_time_from: Optional[time] = None
    psd_time_to: Optional[time] = None
    psd_cul_daily: Optional[float] = None
    psd_cul_monthly: Optional[float] = None

    dg_from: Optional[time] = None
    dg_to: Optional[time] = None

    engery_meter_reading: Optional[float] = None
    hours_meter: Optional[float] = None

    tank1: Optional[float] = None
    tank2: Optional[float] = None
    tank3: Optional[float] = None

    fw1: Optional[float] = None
    fw2: Optional[float] = None
    fw3: Optional[float] = None
    fw4: Optional[float] = None
    fw5: Optional[float] = None

    # prevcumrunhour: Optional[int] = None
    # cummrunhour: Optional[int] = None

    remarks: Optional[str] = None
    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class MFMShutdownDetailCreate(MFMShutdownDetailBase):
    pass


class MFMShutdownDetailUpdate(MFMShutdownDetailBase):
    pass
