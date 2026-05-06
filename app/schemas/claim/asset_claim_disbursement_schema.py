from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date


# -------------------------
# CREATE
# -------------------------
class AssetClaimDisbursementCreate(BaseModel):
    asset_claim_submission_id: Optional[int]

    claim_amount: Optional[Decimal]
    disbursed_amount: Optional[Decimal]
    payment_mode: Optional[str]
    disbursement_date: Optional[date]
    sap_assets_no: Optional[int]
    transaction_reference_no: Optional[str]

    bank_name: Optional[str]
    account_number: Optional[str]

    remarks: Optional[str]
    status: Optional[str]

    created_by: Optional[int]


# -------------------------
# UPDATE (ALL FIELDS)
# -------------------------
class AssetClaimDisbursementUpdate(BaseModel):
    asset_claim_submission_id: Optional[int]

    claim_amount: Optional[Decimal]
    disbursed_amount: Optional[Decimal]
    payment_mode: Optional[str]
    disbursement_date: Optional[date]
    sap_assets_no: Optional[int]
    transaction_reference_no: Optional[str]

    bank_name: Optional[str]
    account_number: Optional[str]

    remarks: Optional[str]
    status: Optional[str]

    updated_by: Optional[int]

    updated_by_supervisor: Optional[date]
    updated_by_supervisor_name: Optional[str]
    sap_assets_no: Optional[int]
    updated_by_hr: Optional[date]
    updated_by_hr_name: Optional[str]

    updated_by_finance: Optional[date]
    updated_by_finance_name: Optional[str]
