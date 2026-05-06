from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class CompositeToolboxTalkBase(BaseModel):
    composite_work_permit_id: Optional[int] = None

    cross_reference_of_other_permit: Optional[str] = None

    work_clearance_time: Optional[time] = None
    work_clearance_date: Optional[date] = None

    contractor_engineer_name: Optional[str] = None
    work_installation_unit_facility_name: Optional[str] = None

    tbt_delivered_by: Optional[str] = None
    contract_supervisor_name: Optional[str] = None

    topics_issues_discussed: Optional[str] = None
    other_points_raised: Optional[str] = None

    status: Optional[str] = None
    created_by: Optional[str] = None


class CompositeToolboxTalkCreate(CompositeToolboxTalkBase):
    pass


class CompositeToolboxTalkUpdate(CompositeToolboxTalkBase):
    pass
