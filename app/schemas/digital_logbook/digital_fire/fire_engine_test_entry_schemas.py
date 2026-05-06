from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel


class FireEngineTestEntryBase(BaseModel):
    master_id: Optional[int] = None

    entry_date: Optional[date] = None
    fire_engine_no: Optional[str] = None

    time_start: Optional[time] = None
    time_stop: Optional[time] = None
    running_hours: Optional[float] = None

    battery_voltage: Optional[str] = None
    lube_oil_level: Optional[str] = None
    fuel_level_lts: Optional[float] = None
    radiator_water_level: Optional[str] = None

    lube_oil_temp: Optional[float] = None
    lube_oil_pressure: Optional[float] = None

    fwt_1: Optional[float] = None
    fwt_2: Optional[float] = None
    fwt_3: Optional[float] = None

    cooling_water_temp: Optional[float] = None
    rpm: Optional[int] = None

    mode_of_test: Optional[str] = None
    tech_sign: Optional[str] = None
    engg_sign: Optional[str] = None

    remarks: Optional[str] = None

    created_at : Optional[datetime] = None
    created_by :Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
class FireEngineTestEntryCreate(FireEngineTestEntryBase):
    pass


class FireEngineTestEntryUpdate(FireEngineTestEntryBase):
    pass
