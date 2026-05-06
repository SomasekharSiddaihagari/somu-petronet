from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date


# -------------------------
# CREATE (NO RESIDUAL FIELDS)
# -------------------------
class AssetClaimSubmissionCreate(BaseModel):
    asset_claim_id: Optional[int]

    # Claim Details
    item_type: Optional[str] = None
    item_name: Optional[str] = None
    claim_amount: Optional[Decimal] = None

    # Vendor Details
    vendor_name: Optional[str] = None
    vendor_gstin: Optional[str] = None
    vendor_address: Optional[str] = None
    vendor_contact_no: Optional[str] = None
    invoice_date: Optional[date] = None
    invoice_no: Optional[str] = None

    # Documents
    document_names: Optional[str] = None
    owned_by:Optional[str]=None
    # Declaration
    declaration_accepted: Optional[bool] = None

    status: Optional[str] = None
    created_by: Optional[int] = None



# -------------------------
# UPDATE (ADD 3 FIELDS HERE)
# -------------------------
class AssetClaimSubmissionUpdate(BaseModel):
    asset_claim_id: Optional[int] = None

    item_type: Optional[str] = None
    item_name: Optional[str] = None
    claim_amount: Optional[Decimal] = None

    vendor_name: Optional[str] = None
    vendor_gstin: Optional[str] = None
    vendor_address: Optional[str] = None
    vendor_contact_no: Optional[str] = None
    invoice_date: Optional[date] = None
    invoice_no: Optional[str] = None
    sap_assets_no: Optional[int] = None
    document_names: Optional[str] = None
    declaration_accepted: Optional[bool] = None
    owned_by:Optional[str]=None
    status: Optional[str] = None

    # ✅ NEW — ONLY IN UPDATE
    residual_value_percent: Optional[Decimal] = None
    residual_value_amount: Optional[Decimal] = None
    amount_to_be_disbursed: Optional[Decimal] = None

    # Comments & Workflow
    hr_comment: Optional[str] = None
    finance_comment: Optional[str] = None
    supervisor_comment: Optional[str] = None
    
    updated_by: Optional[int] = None

    updated_by_supervisor: Optional[date] = None
    updated_by_supervisor_name: Optional[str] = None

    updated_by_hr: Optional[date] = None
    updated_by_hr_name: Optional[str] = None

    updated_by_finance: Optional[date] = None
    updated_by_finance_name: Optional[str] = None
