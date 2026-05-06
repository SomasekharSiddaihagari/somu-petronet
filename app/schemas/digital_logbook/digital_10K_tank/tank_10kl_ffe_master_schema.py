# app/schemas/digital_logbook/digital_10K_tank/tank_10kl_ffe_master_schema.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime
from app.schemas.digital_logbook.digital_10K_tank.tank_10kl_ffe_entry_schema import (
    Tank10KLFfeEntryResponse,
)


class Tank10KLFfeCreate(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[FlexTime] = None
    logbook_date: Optional[FlexDate] = None
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Tank10KLFfeUpdate(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[FlexTime] = None
    logbook_date: Optional[FlexDate] = None
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Tank10KLFfeResponse(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[FlexTime] = None
    logbook_date: Optional[FlexDate] = None
    tank_ffe_id: int
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None
    status: Optional[str] = None

    # Resolve Audit Names
    

    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None

    entries: List[Tank10KLFfeEntryResponse] = []

    model_config = ConfigDict(from_attributes=True)
