from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime


class NPTReportMasterBase(BaseModel):
    station: Optional[str] = None
    station_id: Optional[int] = None
    station_in_charge: Optional[str] = None
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


class NPTReportMasterCreate(NPTReportMasterBase):
    pass


class NPTReportMasterUpdate(NPTReportMasterBase):
    pass


from app.schemas.digital_logbook.digital_npt.npt_report_entry_schema import (
    NPTReportEntryResponse,
)
from typing import List


class NPTReportMasterResponse(NPTReportMasterBase):
    npt_id: Optional[int] = None
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
    entries: List[NPTReportEntryResponse] = []
