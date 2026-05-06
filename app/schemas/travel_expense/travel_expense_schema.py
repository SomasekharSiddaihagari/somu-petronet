from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date


class TravelExpenseSheetBase(BaseModel):
    requisition_number: Optional[str]
    user_id: Optional[int]
    travel_id: Optional[int]    
    employee_name: Optional[str]
    employee_number: Optional[str]
    designation: Optional[str]
    grade: Optional[str]
    station: Optional[str]
    department: Optional[str]
    is_dollar:Optional[bool]
    travel_mode: Optional[str]
    purpose_of_travel: Optional[str]
    violation: Optional[str]

    total_excl_gst: Optional[float]
    total_gst: Optional[float]
    total_incl_gst: Optional[float]
    advance_taken: Optional[float]
    amount_payable_receivable: Optional[float]

    comments: Optional[str]
    status: Optional[str]

    updated_by_supervisor: Optional[date]
    updated_by_supervisor_name: Optional[str]
    supervisor_comments: Optional[str]
    md_comment: Optional[str] = None
    
    updated_by_head_tech: Optional[date]
    updated_by_head_tech_name: Optional[str]
    head_tech_comments: Optional[str]

    updated_by_hr: Optional[date]
    updated_by_hr_name: Optional[str]
    hr_comments: Optional[str]

    updated_by_md: Optional[date]
    updated_by_md_name: Optional[str]

    updated_by_finance: Optional[date]
    updated_by_finance_name: Optional[str]
    finance_comments: Optional[str]

    # ⭐ THIS FIXES YOUR ISSUE FOR ALL DATE FIELDS
    @field_validator(
        "updated_by_supervisor",
        "updated_by_hr",
        "updated_by_md",
        "updated_by_finance",
        "updated_by_head_tech",
        mode="before"
    )
    def empty_string_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v


class TravelExpenseSheetCreate(TravelExpenseSheetBase):
    pass


class TravelExpenseSheetUpdate(TravelExpenseSheetBase):
    pass
