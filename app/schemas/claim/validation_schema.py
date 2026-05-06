from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import date
from decimal import Decimal


# --------------------------------------------------
# Data Card
# --------------------------------------------------
class DataCardValidateRequest(BaseModel):
    user_id: int                      # 👈 ADD THIS
    employee_employment_type: str
    claim_month: str                  # YYYY-MM
    data_card_number: str
    service_provider: str
    connection_type: str
    bill_date: date
    bill_amount: Decimal
    declaration_accepted: bool



class DataCardValidateResponse(BaseModel):
    status: str
    eligible: bool
    bill_amount_total: Optional[Decimal] = None
    monthly_limit: Optional[Decimal] = None
    errors: Optional[list[str]] = None
    message: str


# --------------------------------------------------
# Furniture RM
# --------------------------------------------------
class FurnitureRMValidateRequest(BaseModel):
    user_id: int
    employee_employment_type: str = Field(..., examples=["Permanent"])
    claim_month_year: str  # YYYY-MM
    furniture_bought_back: bool = Field(
        ..., description="True if furniture already bought back"
    )
    declaration_accepted: bool


class FurnitureRMValidateResponse(BaseModel):
    status: str
    eligible: bool
    errors: Optional[list[str]] = None
    message: str


# --------------------------------------------------
# Laptop Maintenance
# --------------------------------------------------
class LaptopMaintenanceValidateRequest(BaseModel):
    user_id:int
    employee_employment_type: str = Field(..., examples=["Permanent"])
    date_of_purchase: date
    date_of_claim: date
    date_of_previous_claim: Optional[date] = None
    amount_claimed: Decimal
    declaration_accepted: bool


class LaptopMaintenanceValidateResponse(BaseModel):
    status: str
    eligible: bool
    annual_limit: Optional[Decimal] = None
    eligible_amount: Optional[Decimal] = None
    errors: Optional[list[str]] = None
    message: str


# --------------------------------------------------
# Mobile Bill
# --------------------------------------------------
class MobileBillValidateRequest(BaseModel):
    user_id: int    
    employee_grade: str = Field(..., examples=["E1", "E2", "E3", "E4", "E5", "E6", "E7"])
    employee_employment_type: Optional[str] = Field(
        None, examples=["Permanent"]
    )
    bill_month_year: str  # YYYY-MM
    mobile_number_1: Optional[str] = None
    bill_amount_1: Optional[Decimal] = None
    mobile_number_2: Optional[str] = None
    bill_amount_2: Optional[Decimal] = None
    declaration_accepted: bool


class MobileBillValidateResponse(BaseModel):
    status: str
    eligible: bool
    total_claimed_amount: Optional[Decimal] = None
    monthly_limit: Optional[Decimal] = None
    errors: Optional[list[str]] = None
    message: str


# --------------------------------------------------
# Out Of Pocket
# --------------------------------------------------
class OutOfPocketEntrySchema(BaseModel):
    
    entry_type: str = Field(
        ...,
        examples=["NORMAL_DAY", "HOLIDAY_NON_ROTATING", "HOLIDAY_ROTATING"]
    )
    claim_date: date
    hours: Literal["2-4", "4-6", "6-8", "8"]
    amount: Optional[Decimal] = None   # 🔥 AUTO-CALCULATED (UPDATED)
    justification: str


class OutOfPocketValidateRequest(BaseModel):
    user_id: int
    claim_month_year: str
    declaration_accepted: bool
    entries: List[OutOfPocketEntrySchema]
    is_new_joiner_or_relocation: bool = False   # ← NEW FIELD (default False)



class OutOfPocketValidateResponse(BaseModel):
    status: str
    eligible: bool
    total_claims: Optional[int] = None
    total_amount: Optional[Decimal] = None
    errors: Optional[List[str]] = None
    message: str


# --------------------------------------------------
# Vehicle CM
# --------------------------------------------------
class VehicleCMValidateRequest(BaseModel):
    user_id: int

    employee_grade: Optional[str] = Field(
        None, examples=["E1", "E2", "E3", "E4", "E5", "E6", "E7"]
    )

    employee_employment_type: Optional[str] = Field(
        None, examples=["Permanent"]
    )

    has_cross_month_adjustment: bool = False  # already optional by default

    vehicle_name: Optional[str] = None
    vehicle_no: Optional[str] = None

    fuel_type: Optional[str] = Field(
        None, examples=["Petrol", "Other"]
    )

    claim_month_year: Optional[str] = None  # YYYY-MM

    rc_expiry_date: Optional[date] = None
    insurance_expiry_date: Optional[date] = None
    fuel_claimed_liters: Optional[Decimal] = None
    applicable_fuel_rate: Optional[Decimal] = None
    maintenance_claim_amount: Optional[Decimal] = None

    fixed_conveyance_claim: Optional[bool] = None
    declaration_accepted: Optional[bool] = None



