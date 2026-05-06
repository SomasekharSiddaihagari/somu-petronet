# app/schemas/digital_logbook/digital_cp_reading/cp_reading_master_schema.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any, Dict
from app.utils.schema_validators import FlexDate, FlexTime, FlexDatetime

class CPReadingMasterBase(BaseModel):
    station_id: Optional[int] = Field(None, description="1=MLR, 2=NER, 3=HSN, 4=DKN")
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
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class CPReadingMasterCreate(CPReadingMasterBase):
    station_id: int = Field(..., description="1=MLR, 2=NER, 3=HSN, 4=DKN")

class CPReadingMasterUpdate(CPReadingMasterBase):
    pass

class CPReadingMasterResponse(CPReadingMasterBase):
    cp_master_id: Optional[int] = None
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
    entries: List[Any] = Field(default_factory=list)
