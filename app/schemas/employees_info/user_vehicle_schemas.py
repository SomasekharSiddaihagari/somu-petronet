from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from pydantic import Field
from sqlalchemy import Text


# -------------------------
# Base Schema
# -------------------------
class UserVehicleBase(BaseModel):
    vehicle_type: Optional[str]
    vehicle_make: Optional[str]
    vehicle_model: Optional[str]
    color: Optional[str]
    fuel_type: Optional[str]
    vehicle_registration_no: Optional[str]
    rc_expiry_date: Optional[date]
    insurance_provider: Optional[str]
    insurance_policy_number: Optional[str]
    insurance_expiry_date: Optional[date]
    puc_expiry_date: Optional[date]
    status:Optional[str]
    document_upload: Optional[str]  
    document_details: Optional[str] = None  
    comment: Optional[str] = None
    active: Optional[bool]
    changed_fields: List[dict] = Field(default_factory=list)


# -------------------------
# Create
# -------------------------
class UserVehicleCreate(UserVehicleBase):
    user_id: int


# -------------------------
# Update
# -------------------------
class UserVehicleUpdate(UserVehicleBase):
    pass


# -------------------------
# Response
# -------------------------
class UserVehicleResponse(UserVehicleBase):
    id: int
    user_id: int
    created_date: date
    modified_date: Optional[date]
    download_url: List[str] = []

    class Config:
        orm_mode = True


# -------------------------
# History Response
# -------------------------
class UserVehicleHistoryResponse(UserVehicleBase):
    history_id: int
    user_id: int
    history_created_at: datetime

    class Config:
        orm_mode = True