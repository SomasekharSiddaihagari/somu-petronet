from pydantic import BaseModel
from typing import Optional
from datetime import date


# -------------------------
# CREATE
# -------------------------
class RAClaimCreate(BaseModel):
    employee_name: Optional[str]
    employee_id: Optional[str]
    department: Optional[str]
    designation: Optional[str]
    station: Optional[str]
    grade: Optional[str]

    claim_module: Optional[str]   # Reimbursement / Allowance
    category: Optional[str]

    status: Optional[str]
    remarks: Optional[str]

    created_by: Optional[int]


# -------------------------
# UPDATE (ALL FIELDS)
# -------------------------
class RAClaimUpdate(BaseModel):
    employee_name: Optional[str]
    employee_id: Optional[str]
    department: Optional[str]
    designation: Optional[str]
    station: Optional[str]
    grade: Optional[str]

    claim_module: Optional[str]
    category: Optional[str]

    status: Optional[str]
    remarks: Optional[str]

    updated_by: Optional[int]

    updated_by_supervisor: Optional[date]
    updated_by_supervisor_name: Optional[str]

    updated_by_hr: Optional[date]
    updated_by_hr_name: Optional[str]

    updated_by_finance: Optional[date]
    updated_by_finance_name: Optional[str]
