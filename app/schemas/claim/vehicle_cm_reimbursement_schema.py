from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


# ---------- Base ----------
class VehicleCMReimbursementBase(BaseModel):
    vehicle_name: Optional[str] = None
    claim_month_year: Optional[str] = None

    vehicle_no: Optional[str] = None
    vehicle_type: Optional[str] = None
    fuel_type: Optional[str] = None

    rc_expiry_date: Optional[date] = None
    insurance_expiry_date: Optional[date] = None

    fuel_claim_amount: Optional[float] = None
    applicable_fuel_rate: Optional[float] = None
    fuel_claimed_liters: Optional[float] = None

    maintenance_claim_amount: Optional[float] = None
    fixed_conveyance_claim: Optional[bool] = None
    fixed_conveyance_claim_amount: Optional[float] = None

    annual_entitlement_fuel: Optional[float] = None
    annual_entitlement_maintenance: Optional[float] = None

    monthly_ceiling_fuel: Optional[float] = None
    monthly_ceiling_maintenance: Optional[float] = None

    adjustment_previous_month_fuel: Optional[float] = None
    adjustment_previous_month_maintenance: Optional[float] = None

    net_available_balance_fuel: Optional[float] = None
    net_available_balance_maintenance: Optional[float] = None

    max_claim_allowed_fuel: Optional[float] = None
    max_claim_allowed_maintenance: Optional[float] = None

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
class VehicleCMReimbursementCreate(VehicleCMReimbursementBase):
    ra_claim_id: int
    created_by: Optional[int] = None


# ---------- Update ----------
class VehicleCMReimbursementUpdate(VehicleCMReimbursementBase):
    updated_by: Optional[int] = None


# ---------- Response ----------
class VehicleCMReimbursementResponse(VehicleCMReimbursementBase):
    vehicle_cm_reimbursement_id: int
    ra_claim_id: int
    created_by: Optional[int]
    created_at: datetime
    updated_by: Optional[int]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
