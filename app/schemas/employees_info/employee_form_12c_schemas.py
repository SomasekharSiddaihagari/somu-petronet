from pydantic import BaseModel
from typing import Optional
from datetime import date


class Form12CBase(BaseModel):
    user_id: int
    
    self_alv: Optional[str] = None
    lo1_alv: Optional[str] = None
    lo2_alv: Optional[str] = None

    self_municipal_tax: Optional[str] = None
    lo1_municipal_tax: Optional[str] = None
    lo2_municipal_tax: Optional[str] = None

    self_annual_value: Optional[str] = None
    lo1_annual_value: Optional[str] = None
    lo2_annual_value: Optional[str] = None

    self_less_30: Optional[str] = None
    lo1_less_30: Optional[str] = None
    lo2_less_30: Optional[str] = None

    house_type_self: Optional[str] = None
    house_type_lo1: Optional[str] = None
    house_type_lo2: Optional[str] = None

    self_interest: Optional[str] = None
    lo1_interest: Optional[str] = None
    lo2_interest: Optional[str] = None

    self_loan_date: Optional[date] = None
    lo1_loan_date: Optional[date] = None
    lo2_loan_date: Optional[date] = None

    self_one_fifth_interest: Optional[str] = None
    lo1_one_fifth_interest: Optional[str] = None
    lo2_one_fifth_interest: Optional[str] = None

    self_net_income: Optional[str] = None
    lo1_net_income: Optional[str] = None
    lo2_net_income: Optional[str] = None

    self_tds_self_lease: Optional[str] = None
    lo1_tds_self_lease: Optional[str] = None
    lo2_tds_self_lease: Optional[str] = None

    self_cess_self_lease: Optional[str] = None
    lo1_cess_self_lease: Optional[str] = None
    lo2_cess_self_lease: Optional[str] = None

    self_cess_self_business: Optional[str] = None   # ← ADDED
    lo1_cess_self_business: Optional[str] = None    # ← ADDED
    lo2_cess_self_business: Optional[str] = None    # ← ADDED

    self_capital_gains: Optional[str] = None
    lo1_capital_gains: Optional[str] = None
    lo2_capital_gains: Optional[str] = None

    self_other_sources: Optional[str] = None
    lo1_other_sources: Optional[str] = None
    lo2_other_sources: Optional[str] = None

    self_aggregate_items: Optional[str] = None
    lo1_aggregate_items: Optional[str] = None
    lo2_aggregate_items: Optional[str] = None

    self_tds_other_income: Optional[str] = None
    lo1_tds_other_income: Optional[str] = None
    lo2_tds_other_income: Optional[str] = None

    self_cess_other_income: Optional[str] = None
    lo1_cess_other_income: Optional[str] = None
    lo2_cess_other_income: Optional[str] = None

    self_total_tds: Optional[str] = None
    lo1_total_tds: Optional[str] = None
    lo2_total_tds: Optional[str] = None

    self_total_cess: Optional[str] = None
    lo1_total_cess: Optional[str] = None
    lo2_total_cess: Optional[str] = None

    upload_document: Optional[str] = None

    declared_place: Optional[str] = None
    declared_date: Optional[date] = None
    signature_name: Optional[str] = None


class Form12CUpdate(Form12CBase):
    form_id: int


class Form12CResponse(Form12CUpdate):
    pass
