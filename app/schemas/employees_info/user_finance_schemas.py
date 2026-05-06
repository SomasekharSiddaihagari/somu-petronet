from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserFinanceBase(BaseModel):
    user_id: int
    date: Optional[datetime] = None
    financial_year: Optional[str] = None
    opting_for_concessional_rate: Optional[str] = None
    residing_in_rented_house: Optional[str] = None
    monthly_rent: Optional[float] = None
    landlord_name: Optional[str] = None
    temporary_address: Optional[str] = None
    pension_plan: Optional[str] = None
    lic_premium: Optional[str] = None
    ppf: Optional[str] = None
    ulip: Optional[str] = None
    tuition_fees: Optional[str] = None
    nsc: Optional[str] = None
    nsc_interest: Optional[str] = None
    housing_loan_repayment: Optional[str] = None
    other_investments: Optional[str] = None
    infrastructure_bond: Optional[str] = None
    educational_loan_interest: Optional[str] = None
    contribution_to_nps: Optional[str] = None
    medical_insurance_80D:Optional[str] = None
    interest_housing_24b: Optional[float] = None
    upload_document: Optional[str] = None
    declaration_text: Optional[str] = None
    signature_name: Optional[str] = None

class UserFinanceCreateUpdate(UserFinanceBase):

    user_finance_id: Optional[int] = None  # used to decide insert/update




from pydantic import BaseModel
from datetime import date

class UserFinanceResponse(BaseModel):
    user_finance_id: int
    user_id: int

    first_name: str | None
    last_name: str | None
    employee_code: str | None

    date: date | None
    financial_year: str | None
    opting_for_concessional_rate: str | None
    residing_in_rented_house: str | None
    monthly_rent: float | None
    landlord_name: str | None
    temporary_address: str | None
    form_type: str = "user_investment"  
    pension_plan: str | None
    lic_premium: str | None
    ppf: str | None
    ulip: str | None
    tuition_fees: str | None
    nsc: str | None
    nsc_interest: str | None
    housing_loan_repayment: str | None
    other_investments: str | None

    infrastructure_bond: str | None
    educational_loan_interest: str | None
    contribution_to_nps: str | None

    upload_document: str | None
    declaration_text: str | None
    signature_name: str | None
    changed_fields: List[dict] = Field(default_factory=list)

    class Config:
        orm_mode = True
