from pydantic import BaseModel
from typing import Optional


class HIRABase(BaseModel):
    moc_request_id: int

    # NEW FIELDS
    risk: Optional[str] = None
    division_dept_name: Optional[str] = None
    project_requisition_no: Optional[str] = None
    job_description: Optional[str] = None

    activity: str
    hazard: str
    risk_level: str
    consequence: str
    control_measures: str
    comments_initiator: Optional[str] = None
    hira_reviewer_id: Optional[int] = None
    status: Optional[str] = "draft"


class HIRACreate(HIRABase):
    pass


class HIRAUpdate(BaseModel):
    # NEW FIELDS
    risk: Optional[str]
    division_dept_name: Optional[str]
    project_requisition_no: Optional[str]
    job_description: Optional[str]

    activity: Optional[str]
    hazard: Optional[str]
    risk_level: Optional[str]
    consequence: Optional[str]
    control_measures: Optional[str]
    comments_initiator: Optional[str]
    hira_reviewer_id: Optional[int]
    status: Optional[str]
