from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


# ---------- Base ----------
class LaptopMaintenanceReimbursementBase(BaseModel):
    date_of_purchase: Optional[date] = None
    date_of_claim: Optional[date] = None
    date_of_previous_claim: Optional[date] = None

    amount_claimed: Optional[float] = None

    annual_limit: Optional[float] = None
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
class LaptopMaintenanceReimbursementCreate(LaptopMaintenanceReimbursementBase):
    ra_claim_id: int
    created_by: Optional[int] = None


# ---------- Update ----------
class LaptopMaintenanceReimbursementUpdate(LaptopMaintenanceReimbursementBase):
    updated_by: Optional[int] = None


# ---------- Response ----------
class LaptopMaintenanceReimbursementResponse(LaptopMaintenanceReimbursementBase):
    laptop_maintenance_reimbursement_id: int
    ra_claim_id: int
    created_by: Optional[int]
    created_at: datetime
    updated_by: Optional[int]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
