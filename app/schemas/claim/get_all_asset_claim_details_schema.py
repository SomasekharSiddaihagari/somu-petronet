from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal


class AssetEntitlementResponse(BaseModel):
    category: str
    item_type: str

    total_entitlement_limit: Decimal
    amount_utilized: Decimal
    balance_available: Decimal

    eligibility: str
    can_apply: bool

    last_claim_date: Optional[date]
    next_eligible_date: Optional[date]

    policy_message: str
