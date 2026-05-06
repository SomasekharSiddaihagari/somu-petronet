from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


# ---------- Base ----------
class FurnitureRMReimbursementBase(BaseModel):
    furniture_name: Optional[str] = None
    claim_month_year: Optional[str] = None

    total_cost_under_policy: Optional[float] = None
    expenditure_claimed: Optional[float] = None
    maximum_eligible_amount: Optional[float] = None
    amount_claimed: Optional[float] = None
    eligible_amount: Optional[float] = None

    document_names: Optional[str] = None
    remarks: Optional[str] = None
    declaration_accepted: Optional[bool] = None
    status: Optional[str] = None

    # Supervisor
    updated_by_supervisor: Optional[date] = None
    updated_by_supervisor_name: Optional[str] = None
    supervisor_comment: Optional[str] = None

    # HR
    updated_by_hr: Optional[date] = None
    updated_by_hr_name: Optional[str] = None
    hr_comment: Optional[str] = None

    # Finance
    updated_by_finance: Optional[date] = None
    updated_by_finance_name: Optional[str] = None
    finance_comment: Optional[str] = None


# ---------- Create ----------
class FurnitureRMReimbursementCreate(FurnitureRMReimbursementBase):
    ra_claim_id: int
    created_by: Optional[int] = None


# ---------- Update ----------
class FurnitureRMReimbursementUpdate(FurnitureRMReimbursementBase):
    updated_by: Optional[int] = None


# ---------- Response ----------
class FurnitureRMReimbursementResponse(FurnitureRMReimbursementBase):
    furniture_rm_reimbursement_id: int
    ra_claim_id: int
    created_by: Optional[int]
    created_at: datetime
    updated_by: Optional[int]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
