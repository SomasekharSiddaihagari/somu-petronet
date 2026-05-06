from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


# ===============================
# REQUEST SCHEMA
# ===============================

class   LeaveValidationRequest(BaseModel):
    user_id: int = Field(..., description="ID of the employee")
    leave_type: str = Field(..., description="User-selected leave type")
    from_date: date = Field(..., description="Start date of leave")
    to_date: date = Field(..., description="End date of leave")
    half_day_count: Optional[int] = Field(0, description="Number of half-days (each = 0.5)")
    selected_days: int = Field(..., description="Selected Days")
    has_med_cert: Optional[bool] = Field(False)
    expected_delivery_date: Optional[date] = None
    maternity_type: Optional[str] = "biological"


    # NEW FIELD
    reversal: Optional[bool] = Field(
        False,
        description="If true, overlapping leave validation will be skipped"
    )
# ===============================
# RESPONSE SCHEMA
# ===============================

class LeaveValidationResponse(BaseModel):
    can_apply: Optional[bool] = None
    number_of_days: Optional[float] = None
    comment: Optional[str] = None
    approver_id: Optional[int] = None
    sandwich_days_count: Optional[int] = None
    holiday_days_count: Optional[int] = None
    weekend_days_count: Optional[int] = None
    half_day_allowed: Optional[bool] = None
    special_approval_needed: Optional[bool] = None

