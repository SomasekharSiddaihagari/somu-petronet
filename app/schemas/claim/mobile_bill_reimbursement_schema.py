from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date


# -------------------------
# CREATE
# -------------------------
class MobileBillReimbursementCreate(BaseModel):
    ra_claim_id: int

    bill_month_year: Optional[str] = None

    mobile_number_1: Optional[str]=None
    bill_amount_1: Optional[Decimal]=None

    mobile_number_2: Optional[str]=None
    bill_amount_2: Optional[Decimal]=None

    total_claimed_amount: Optional[Decimal]=None
    monthly_limit: Optional[Decimal]=None


    document_names: Optional[str] = None 
    remarks: Optional[str]=None

    declaration_accepted: Optional[bool]=None
    status: Optional[str]=None

    supervisor_comment: Optional[str]=None
    hr_comment: Optional[str]=None
    finance_comment: Optional[str]= None
    created_by: Optional[int]= None 
    updated_by: Optional[int]= None 

    updated_by_supervisor: Optional[date]= None 
    updated_by_supervisor_name: Optional[str] = None 

    updated_by_hr: Optional[date]= None 
    updated_by_hr_name: Optional[str] = None 

    updated_by_finance: Optional[date]= None 
    updated_by_finance_name: Optional[str] = None 


# -------------------------
# UPDATE (ALL FIELDS)
# -------------------------
class MobileBillReimbursementUpdate(BaseModel):
    bill_month_year: Optional[str] = None

    mobile_number_1: Optional[str]=None
    bill_amount_1: Optional[Decimal]=None

    mobile_number_2: Optional[str]=None
    bill_amount_2: Optional[Decimal]=None

    total_claimed_amount: Optional[Decimal]=None
    monthly_limit: Optional[Decimal]=None


    document_names: Optional[str] = None 
    remarks: Optional[str]=None

    declaration_accepted: Optional[bool]=None
    status: Optional[str]=None

    supervisor_comment: Optional[str]=None
    hr_comment: Optional[str]=None
    finance_comment: Optional[str]= None
    created_by: Optional[str]= None
    updated_by: Optional[int]= None 

    updated_by_supervisor: Optional[date]= None 
    updated_by_supervisor_name: Optional[str] = None 

    updated_by_hr: Optional[date]= None 
    updated_by_hr_name: Optional[str] = None 

    updated_by_finance: Optional[date]= None 
    updated_by_finance_name: Optional[str] = None 
