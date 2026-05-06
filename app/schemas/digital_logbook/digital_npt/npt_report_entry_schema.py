from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.utils.schema_validators import FlexTime, FlexDate, FlexDatetime


class NPTReportEntryBase(BaseModel):
    npt_master_id: Optional[int] = None

    patrol_date: Optional[FlexDate] = None
    start_time: Optional[FlexTime] = None
    start_point: Optional[str] = None
    end_time: Optional[FlexTime] = None
    end_point: Optional[str] = None
    team_member: Optional[str] = None
    report_time: Optional[FlexTime] = None
    point_at_reporting_time: Optional[str] = None
    engg_sign: Optional[str] = None
    remarks: Optional[str] = None

    # Audit Fields
    created_at: Optional[FlexDatetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[FlexDatetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class NPTReportEntryCreate(NPTReportEntryBase):
    npt_master_id: int


class NPTReportEntryUpdate(NPTReportEntryBase):
    pass


class NPTReportEntryResponse(NPTReportEntryBase):
    npe_id: Optional[int] = None
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
