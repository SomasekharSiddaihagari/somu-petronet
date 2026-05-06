from optparse import Option
from pydantic import BaseModel, ConfigDict
import datetime
from typing import Any, Optional, List
 
 
# =========================================================
# CREATE REQUEST
# =========================================================
class MOCRequest(BaseModel):
    station_name: str
    title: str
    date: datetime.date                     # ✅ fixed
    priority: str
    modification_type: str
    time_limit: str
    shutdown_required: bool
    present_system: Optional[str] = None
    proposed_change: Optional[str] = None
    justification: Optional[str] = None
    objectives: Optional[str] = None
    other_units_impacted: Optional[str] = None
    other_aspects_required: Optional[bool] = None
    statutory_approval_required: Optional[bool] = None
    statutory_approval_details: Optional[str] = None
    impact_of_modification: Optional[str] = None
    consequences_non_implementation: Optional[str] = None
    hse: Optional[bool] = None
    efficiency: Optional[bool] = None
    quality: Optional[bool] = None
    reliability: Optional[bool] = None
    other_aspects: Optional[str] = None
    objectives_achieved: Optional[str] = None
    attachments: Optional[str] = None
    comments: Optional[str] = None
    status: str
    is_active: Optional[bool] = None
    created_by: str
    updated_by: str
    submission_date: Optional[datetime.datetime]   # ✅ fixed
    short_text: Optional[str] = None
 
class ReviewerInfo(BaseModel):
    reviewer_id: Optional[int] = None
    reviewer_name: Optional[str] = None
    reviewer_designation: Optional[str] = None

 
class HIRAEntryDetail(BaseModel):
    hira_id: int

    # 🔹 NEW FIELDS
    risk: Optional[str] = None
    division_dept_name: Optional[str] = None
    project_requisition_no: Optional[str] = None
    job_description: Optional[str] = None

    # 🔹 EXISTING FIELDS
    activity: str
    hazard: str
    risk_level: str
    consequence: str
    control_measures: str
    comments_initiator: Optional[str] = None
    hira_reviewer_id: Optional[int] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True
        
# =========================================================
# DETAIL RESPONSE
# =========================================================
class MOCRequestDetail(BaseModel):
    moc_request_id: Optional[int] = None
    moc_request_no: str
    station_name: str
    title: str
    date: datetime.date
    priority: str
    modification_type: str

    time_limit: Optional[str] = None
    shutdown_required: Optional[bool] = None
    present_system: Optional[str] = None
    proposed_change: Optional[str] = None
    justification: Optional[str] = None
    objectives: Optional[str] = None
    other_units_impacted: Optional[str] = None
    statutory_approval_required: Optional[bool] = None
    statutory_approval_details: Optional[str] = None
    impact_of_modification: Optional[str] = None
    consequences_non_implementation: Optional[str] = None
    short_text: Optional[str] = None
    hse: Optional[bool] = None
    efficiency: Optional[bool] = None
    quality: Optional[bool] = None
    reliability: Optional[bool] = None
    other_aspects_required: Optional[bool] = None
    other_aspects: Optional[str] = None
    objectives_achieved: Optional[str] = None
    attachments: Optional[str] = None
    comments: Optional[str] = None
    reviewer_comments: Optional[str] = None
    approver_comments: Optional[str] = None

    status: Optional[str] = None
    is_active: Optional[bool] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    submission_date: Optional[datetime.datetime] = None
    hira_approved_date: Optional[datetime.datetime] = None
    sic_approved_date: Optional[datetime.datetime] = None
    approved_date: Optional[datetime.datetime] = None
    sic_comments: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    hira_entries: Optional[List[HIRAEntryDetail]] = None
    hira_reviewer_id: Optional[int] = None
    hira_reviewer_name: Optional[str] = None
    sic_id: Optional[int] = None
    sic_name: Optional[str] = None
    approver_id: Optional[int] = None
    approver_name: Optional[str] = None
    hira_reviewer_designation: Optional[str] = None
    sic_designation: Optional[str] = None
    approver_designation: Optional[str] = None
    created_by_designation: Optional[str] = None

    available_approver: Optional[List[ReviewerInfo]] = None

    model_config = ConfigDict(from_attributes=True)
    closure_date: Optional[str] = None         
    closure_comments: Optional[str] = None     
    closure_exists: Optional[bool] = None
    closure_data: Optional[dict] = None
 
# =========================================================
# STATUS COUNT
# =========================================================
class MOCStatusCountRequest(BaseModel):
    user_id: int

from pydantic import BaseModel

class MOCStatusCountRequestStation(BaseModel):
    station_name: str
 
 
# =========================================================
# UPDATE REQUEST
# =========================================================
class UpdateMOCRequest(BaseModel):
    moc_request_no: str
    station_name: str
    title: str
    date: datetime.date                      
    priority: str
    modification_type: str
    time_limit:str               
    shutdown_required: Optional[bool] = None
    other_aspects_required: Optional[bool] = None
    present_system: str
    proposed_change: str
    justification: str
    objectives: str
    other_units_impacted: str
    statutory_approval_required: Optional[bool] = None
    statutory_approval_details: Optional[str]
    impact_of_modification: Optional[str]
    consequences_non_implementation: Optional[str]
 
    hse: Optional[bool] = None
    efficiency: Optional[bool] = None
    quality: Optional[bool] = None
    reliability: Optional[bool] = None
    other_aspects: Optional[str]
    objectives_achieved: Optional[str]
 
    attachments: Optional[str]
    comments: Optional[str]
    reviewer_comments: Optional[str]
    approver_comments: Optional[str]
 
    submission_date: Optional[datetime.datetime]
    hira_approved_date: Optional[datetime.datetime]
    sic_approved_date: Optional[datetime.datetime]
    approved_date: Optional[datetime.datetime]
    closure_date: Optional[datetime.datetime] = None
 
    sic_comments: Optional[str] = None
    closure_comments: Optional[str] = None
 
    status: str
    is_active: bool
    updated_by: str
    short_text: Optional[str] = None
 
 
# =========================================================
# ENGINEER
# =========================================================
class EngineerDetail(BaseModel):
    user_id: Optional[int]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    contact_phone: Optional[str]
    role_name: Optional[str]
 
    class Config:
        from_attributes = True   # ✅ Pydantic v2 fix
 
 
class EngineerListResponse(BaseModel):
    statusCode: str
    statusMessage: str
    data: List[EngineerDetail]
 
 
# =========================================================
# LIST BY USER
# =========================================================
class MOCRequestByUser(BaseModel):
    moc_request_id: Optional[int]
    moc_request_no: Optional[str]
    station_name: Optional[str]
    title: Optional[str]
    date: Optional[datetime.date]            # ✅ fixed
    priority: Optional[str]
    modification_type: Optional[str]
    time_limit: Optional[str]
    shutdown_required: Optional[bool]
    present_system: Optional[str]
    proposed_change: Optional[str]
    justification: Optional[str]
    objectives: Optional[str]
    other_units_impacted: Optional[str]
    statutory_approval_required: Optional[bool]
    statutory_approval_details: Optional[str]
    impact_of_modification: Optional[str]
    consequences_non_implementation: Optional[str]
 
    hse: Optional[bool]
    efficiency: Optional[bool]
    quality: Optional[bool]
    reliability: Optional[bool]
 
    other_aspects: Optional[str]
    objectives_achieved: Optional[str]
    attachments: Optional[str]
    comments: Optional[str]
    reviewer_comments: Optional[str]
    approver_comments: Optional[str]
 
    status: Optional[str]
    is_active: Optional[bool]
    created_by: Optional[str]
    updated_by: Optional[str]
 
    closure_date: Optional[datetime.datetime] = None
    sic_comments: Optional[str] = None
    closure_comments: Optional[str] = None
 
    submission_date: Optional[datetime.datetime]
    hira_approved_date: Optional[datetime.datetime]
    sic_approved_date: Optional[datetime.datetime]
    approved_date: Optional[datetime.datetime]
 
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    short_text: Optional[str] = None
    class Config:
        from_attributes = True   # ✅ Pydantic v2 fix



