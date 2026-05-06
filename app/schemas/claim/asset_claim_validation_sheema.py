from pydantic import BaseModel
from datetime import date
 
class AssetClaimValidateRequest(BaseModel):
    employee_id: str
    employee_type: str            # Permanent / Contract
    grade: str                    # E1 - E7
    category: str                 # Laptop/Desktop, Data Card, Furniture
    sub_category: str | None = None
    item_type: str
    claim_amount: float
    invoice_date: date
 
 
class AssetClaimValidateResponse(BaseModel):
    eligible: bool
    eligible_amount: float | None
    ceiling: float | None
    next_eligible_date: date | None
    message: str