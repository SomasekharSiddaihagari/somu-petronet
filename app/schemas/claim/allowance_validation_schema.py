from pydantic import BaseModel

from typing import List

from decimal import Decimal
 
 
# -------------------------

# Packing & Loading Charges

# -------------------------

class PackingChargesRequest(BaseModel):

    grade: str                # E1 .. E7

    amount_claimed: Decimal
 
 
class PackingChargesResponse(BaseModel):

    status: str

    grade: str

    approved_amount: Decimal

    max_allowed: Decimal
 
 
# -------------------------

# Admission – Child Details

# -------------------------

class AdmissionChild(BaseModel):

    child_name: str
    
    amount_claimed: Decimal
 
 
class AdmissionClaimRequest(BaseModel):
    user_id: int
    station_id: int
    city: str
    children: List[AdmissionChild]

 
 
class AdmissionClaimResponse(BaseModel):

    status: str

    children_count: int

    total_approved_amount: Decimal

 