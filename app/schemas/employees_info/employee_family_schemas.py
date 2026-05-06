from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


# ---------- FAMILY MEMBER ----------

class EmployeeFamilyBase(BaseModel):
    user_id: int
    submission_id: int
    relation: Optional[str] = None
    full_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    place_of_birth: Optional[str] = None
    date_of_marriage: Optional[date] = None
    document: Optional[str] = None
    document_details: Optional[str] = None  
    comment: Optional[str] = None
    changed_fields: Optional[List[dict]] = Field(default_factory=list)


class EmployeeFamilyResponse(EmployeeFamilyBase):
    ef_id: int

    class Config:
        from_attributes = True


# ---------- SUBMISSION ----------

class FamilySubmissionCreate(BaseModel):
    user_id: int
    status: Optional[str] = None
    hr_comments: Optional[str] = None


class FamilySubmissionUpdate(BaseModel):
    status: Optional[str] = None
    hr_comments: Optional[str] = None


class FamilySubmissionResponse(BaseModel):
    submission_id: int
    user_id: int
    status: Optional[str]
    hr_comments: Optional[str]

    class Config:
        from_attributes = True
