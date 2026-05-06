from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime
from app.schemas.digital_logbook.digital_erv_logbook.erv_vehicle_inspection_entry_schema import (
    ERVVehicleInspectionResponse,
)


class ErvLogbookBase(BaseModel):
    station: Optional[str] = None
    shift_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[FlexTime] = None
    logbook_date: Optional[FlexDate] = None
    ms_logbook_id: Optional[int] = None
    technician_id: Optional[int] = None

    # Audit Fields
    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ErvLogbookCreate(ErvLogbookBase):
    pass


class ErvLogbookUpdate(ErvLogbookBase):
    pass


class ErvLogbookResponse(ErvLogbookBase):
    erv_id: Optional[int] = None
    station: Optional[str] = None
    shift_in_charge: Optional[str] = None
    shift: Optional[str] = None
    start_time: Optional[FlexTime] = None
    logbook_date: Optional[FlexDate] = None

    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None

    entries: List[ERVVehicleInspectionResponse] = []
