from datetime import datetime,date
from pydantic import BaseModel
from typing import Any, Optional


class TravelRequisitionBase(BaseModel):
    user_id: Optional[int]
    employee_name: Optional[str]
    employee_number: Optional[str]
    designation: Optional[str]
    grade: Optional[str]
    station: Optional[str]
    department: Optional[str]

    purpose_of_travel: Optional[str]
    status: Optional[str]
    approver_comments: Optional[str]

    visa_for: Optional[str]
    emigration_required: Optional[bool]

    foreign_exchange: Optional[str]
    created_at: datetime
    updated_at: datetime





class TravelRequisitionCreate(TravelRequisitionBase):
    user_id: int


class TravelRequisitionUpdate(TravelRequisitionBase):
    pass


class TravelRequisitionResponse(BaseModel):
    travel_id: int
    user_id: int
    employee_name: str
    employee_number: str
    designation: str
    grade: str
    station: str
    department: str
    purpose_of_travel: str
    status: str
    approver_comments: Optional[str]
    visa_for: Optional[str]
    emigration_required: Optional[bool]
    foreign_exchange: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None    # FIXED

    class Config:
        orm_mode = True


class TravelRequisitionFullResponse(BaseModel):
    requisition: Any
    travels: Any
    hotels: Any
    cars: Any