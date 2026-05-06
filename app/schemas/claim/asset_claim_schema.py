# app/schemas/asset_claim_schema.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date, datetime
 
 
# -----------------------
# Create
# -----------------------
class AssetClaimCreate(BaseModel):
    claim_ref_id: Optional[str]
    employee_name: Optional[str]
    employee_id: Optional[str]
    department: Optional[str]
    designation: Optional[str]
    station: Optional[str]
    grade: Optional[str]
    claim_date: Optional[date]
    bought_back: Optional[bool]
    buy_back_date: Optional[date]
    buy_back_submitted_date: Optional[date]
    bought_back_date: Optional[date]
    claim_module: Optional[str]
    category: Optional[str]
    sub_category: Optional[str]
    item_type: Optional[str]
 
    total_entitlement_limit: Optional[Decimal]
    amount_utilized: Optional[Decimal]
    balance_available: Optional[Decimal]
 
    status: Optional[str]
    remarks: Optional[str]
 
 
    created_by: Optional[int]
 
 
# -----------------------
# Update
# -----------------------
class AssetClaimUpdate(BaseModel):
    # Employee Information
    employee_name: Optional[str]
    employee_id: Optional[str]
    department: Optional[str]
    designation: Optional[str]
    station: Optional[str]
    grade: Optional[str]
 
    # Claim Selection
    claim_module: Optional[str]
    category: Optional[str]
    sub_category: Optional[str]
    item_type: Optional[str]
    claim_date: Optional[date]
    bought_back: Optional[bool]
    buy_back_date: Optional[date]
    buy_back_submitted_date: Optional[date]
    bought_back_date: Optional[date]
    # Entitlement & Utilization
    total_entitlement_limit: Optional[Decimal]
    amount_utilized: Optional[Decimal]
    balance_available: Optional[Decimal]
 
    # Status
    status: Optional[str]
    remarks: Optional[str]
 
   
    # Audit
    updated_by: Optional[int]
 
    # Supervisor
    updated_by_supervisor: Optional[date]
    updated_by_supervisor_name: Optional[str]
 
    # HR
    updated_by_hr: Optional[date]
    updated_by_hr_name: Optional[str]
 
    # Finance
    updated_by_finance: Optional[date]
    updated_by_finance_name: Optional[str]
# -----------------------
# Response
# -----------------------
class AssetClaimResponse(BaseModel):
    asset_claim_id: int
    claim_ref_id: Optional[str]
    status: Optional[str]
    created_at: datetime
 
    class Config:
        from_attributes = True
 
 