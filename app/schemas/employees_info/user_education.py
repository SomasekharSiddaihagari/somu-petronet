from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# ===========================
# BASE MODEL (shared fields)
# ===========================
class UserEducationBase(BaseModel):
    qualification: str | None = None
    submission_id: int
    year_of_completion: int | None = None
    education_document: str | None = None
    status: str | None = None
    

# ===========================
# CREATE MODEL
# ===========================
class UserEducationCreate(UserEducationBase):
    # ONLY user_id is required
    user_id: int


# ===========================
# UPDATE MODEL
# ===========================
class UserEducationUpdate(BaseModel):
    # user_id cannot change OR you can allow it if needed
    qualification: str | None = None
    year_of_completion: int | None = None
    education_document: str | None = None
    changed_fields: List[dict] = Field(default_factory=list)


# ===========================
# OUTPUT MODEL
# ===========================
class UserEducationOut(BaseModel):
    education_id: int
    user_id: int
    submission_id: Optional[int] = None   # ✅ FIX

    qualification: Optional[str]
    year_of_completion: Optional[int]
    education_document: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    changed_fields: list | None = None

    class Config:
        from_attributes = True
