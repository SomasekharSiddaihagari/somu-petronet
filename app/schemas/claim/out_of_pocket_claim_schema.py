from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


# ---------- Base ----------
class OutOfPocketClaimBase(BaseModel):
    claim_month_year: Optional[str] = None

    total_claims: Optional[int] = None
    total_amount: Optional[float] = None

    document_names: Optional[str] = None
    remarks: Optional[str] = None
    declaration_accepted: Optional[bool] = None
    status: Optional[str] = None

    # Supervisor
    updated_by_supervisor: Optional[date] = None
    updated_by_supervisor_name: Optional[str] = None
    supervisor_comment: Optional[str] = None

    # HOP
    updated_by_hop: Optional[date] = None
    updated_by_hop_name: Optional[str] = None
    hop_comment: Optional[str] = None
    
    # HR
    updated_by_hr: Optional[date] = None
    updated_by_hr_name: Optional[str] = None
    hr_comment: Optional[str] = None

    # Finance
    updated_by_finance: Optional[date] = None
    updated_by_finance_name: Optional[str] = None
    finance_comment: Optional[str] = None


# ---------- Create ----------
class OutOfPocketClaimCreate(OutOfPocketClaimBase):
    ra_claim_id: int
    created_by: Optional[int] = None


# ---------- Update ----------
class OutOfPocketClaimUpdate(OutOfPocketClaimBase):
    updated_by: Optional[int] = None


# ---------- Response ----------
class OutOfPocketClaimResponse(OutOfPocketClaimBase):
    out_of_pocket_claim_id: int
    ra_claim_id: int
    created_by: Optional[int]
    created_at: datetime
    updated_by: Optional[int]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
