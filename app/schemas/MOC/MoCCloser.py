from pydantic import BaseModel, ConfigDict

from typing import List, Optional
from datetime import date
from datetime import date as Date, datetime
# ============================================================
# 🔹 Base Schema
# ============================================================
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List


class MoCClosureBase(BaseModel):
    moc_request_id: Optional[int] = None
    moc_request_no: Optional[str] = None
    title_of_moc: Optional[str] = None
    brief_description: Optional[str] = None
    moc_initiator_dept: Optional[str] = None
    executing_dept: Optional[str] = None
    moc_execution_details: Optional[str] = None
    hira_recommendation_status: Optional[str] = None
    revised_operating_procedure: Optional[str] = None
    training_completed: Optional[str] = None

    relevant_manuals: Optional[list[str]] = None

    comments_initiator: Optional[str] = None
    status: Optional[str] = "draft"

    date: Optional[Date] = None        # ← uses the alias, no collision
    job_start_date: Optional[Date] = None
    job_completion_date: Optional[Date] = None





# ============================================================
# 🔹 Create Schema
# ============================================================
class MoCClosureCreate(MoCClosureBase):
    """
    Schema for creating a new MoC Closure.
    Only moc_request_id and moc_request_no are required.
    All other fields are optional.
    """
    moc_request_id: int
    moc_request_no: str


# ============================================================
# 🔹 Update Schema
# ============================================================
class MoCClosureUpdate(MoCClosureBase):
    """
    Schema for updating an existing MoC Closure.
    All fields are optional — you can update any or all.
    """
    pass


# ============================================================
# 🔹 Output Schema
# ============================================================
class MoCClosureOut(MoCClosureBase):
    """
    Response schema for returning MoC Closure details.
    Matches database return structure from PostgreSQL functions.
    """
    moc_closure_id: Optional[int] = None
    created_at: Optional[datetime] = None  # Keep datetime for audit timestamps
    updated_at: Optional[datetime] = None

    # ✅ Pydantic v2 ORM compatibility
    model_config = ConfigDict(from_attributes=True)
