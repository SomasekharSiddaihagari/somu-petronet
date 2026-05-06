from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# =================================================
# BASE
# =================================================
class OutOfPocketClaimEntryBase(BaseModel):
    out_of_pocket_claim_id: Optional[int] = None
    entry_type: Optional[str] = None
    hours: Optional[Decimal] = None
    claim_date: Optional[date] = None
    amount: Optional[Decimal] = None
    justification: Optional[str] = None


# =================================================
# CREATE
# =================================================
class OutOfPocketClaimEntryCreate(OutOfPocketClaimEntryBase):
    out_of_pocket_claim_id: int  # REQUIRED


# =================================================
# UPDATE
# =================================================
class OutOfPocketClaimEntryUpdate(OutOfPocketClaimEntryBase):
    pass


# =================================================
# RESPONSE
# =================================================
class OutOfPocketClaimEntryResponse(OutOfPocketClaimEntryBase):
    out_of_pocket_claim_entry_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True