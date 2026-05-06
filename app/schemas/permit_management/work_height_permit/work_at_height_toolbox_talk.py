from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time


class WorkAtHeightToolboxTalkSchema(BaseModel):
    whtt_id: int

    work_at_height_permit_id: Optional[int]

    cross_reference_of_other_permit: Optional[str]

    work_clearance_time: Optional[time]
    work_clearance_date: Optional[date]

    contractor_engineer_name: Optional[str]
    work_installation_unit_facility_name: Optional[str]

    tbt_delivered_by: Optional[str]
    contract_supervisor_name: Optional[str]

    topics_issues_discussed: Optional[str]
    other_points_raised: Optional[str]

    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
