# app/schemas/digital_logbook/digital_cp_reading/cp_reading_hsn_master_schema.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime
from .cp_reading_hsn_entry_schema import CPReadingHSNEntryResponse


class CPReadingHSNBase(BaseModel):
    station: Optional[str] = None
    station_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[FlexTime] = None
    log_date: Optional[FlexDate] = None
    status: Optional[str] = None
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None

    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class CPReadingHSNMasterCreate(CPReadingHSNBase):
    pass


class CPReadingHSNMasterUpdate(CPReadingHSNBase):
    pass


class CPReadingHSNMasterResponse(CPReadingHSNBase):
    cp_hsn_id: int
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
    entries: List[CPReadingHSNEntryResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
