from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal




class AllowanceClaimBase(BaseModel):
    ra_claim_id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_id: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    station: Optional[str] = None
    grade: Optional[str] = None

    from_location: Optional[str] = None
    to_location: Optional[str] = None
    effective_transfer_date: Optional[date] = None
    claim_date: Optional[date] = None

    travel_from: Optional[str] = None
    travel_to: Optional[str] = None
    travel_mode: Optional[str] = None
    travel_date: Optional[date] = None
    number_of_passengers: Optional[int] = None
    travel_amount: Optional[Decimal] = None
    travel_remarks: Optional[str] = None
    travel_documents: Optional[str] = None
    include_travel: Optional[bool] = None

    displacement_city: Optional[str] = None
    no_of_days_claimed: Optional[int] = None
    displacement_rate: Optional[Decimal] = None
    displacement_amount: Optional[Decimal] = None
    maximum_eligible_days: Optional[int] = None
    displacement_remarks: Optional[str] = None
    displacement_documents: Optional[str] = None
    include_displacement: Optional[bool] = None

    basic_pay_monthly: Optional[Decimal] = None
    dearness_allowance_monthly: Optional[Decimal] = None
    eligible_settling_amount: Optional[Decimal] = None
    settling_remarks: Optional[str] = None
    settling_documents: Optional[str] = None
    include_settling: Optional[bool] = None

    transport_mode: Optional[str] = None
    transport_distance_km: Optional[Decimal] = None
    freight_amount: Optional[Decimal] = None
    goods_transport_remarks: Optional[str] = None
    goods_transport_documents: Optional[str] = None
    include_goods_transport: Optional[bool] = None
    amount_claimed_household_transport: Optional[Decimal] = None

    amount_claimed_packaging: Optional[Decimal] = None
    packaging_vendor: Optional[str] = None
    packaging_bill_no: Optional[str] = None
    packaging_remarks: Optional[str] = None
    packaging_documents: Optional[str] = None
    include_packaging: Optional[bool] = None
    maximum_eligible_amount_packaging: Optional[Decimal] = None

    insurance_company: Optional[str] = None
    policy_no: Optional[str] = None
    insurance_amount: Optional[Decimal] = None
    insurance_start_date: Optional[date] = None
    insurance_end_date: Optional[date] = None
    insurance_remarks: Optional[str] = None
    insurance_documents: Optional[str] = None
    include_insurance: Optional[bool] = None
    settling_no_of_days: Optional[int] = None
    t_house_hold_rate: Optional[float] = None
    vehicle_rate: Optional[float] = None

    vehicle_type: Optional[str] = None
    vehicle_registration_no: Optional[str] = None
    vehicle_transport_mode: Optional[str] = None
    vehicle_transport_amount: Optional[Decimal] = None
    vehicle_transport_remarks: Optional[str] = None
    vehicle_transport_documents: Optional[str] = None
    include_vehicle_transport: Optional[bool] = None
    vehicle_transport_distance_km: Optional[Decimal] = None

    total_travel: Optional[Decimal] = None
    total_displacement: Optional[Decimal] = None
    total_settling: Optional[Decimal] = None
    total_goods_transport: Optional[Decimal] = None
    total_packaging: Optional[Decimal] = None
    total_insurance: Optional[Decimal] = None
    total_vehicle_transport: Optional[Decimal] = None
    total_admission: Optional[Decimal] = None
    grand_total: Optional[Decimal] = None
    updated_by_supervisor: Optional[date] = None
    updated_by_supervisor_name: Optional[str] = None
    supervisor_comment: Optional[str] = None

    # HR
    updated_by_hr: Optional[date] = None
    updated_by_hr_name: Optional[str] = None
    hr_comment: Optional[str] = None

    # Finance
    updated_by_finance: Optional[date] = None
    updated_by_finance_name: Optional[str] = None
    finance_comment: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class AllowanceClaimCreate(AllowanceClaimBase):
    ra_claim_id: int


class AllowanceClaimUpdate(AllowanceClaimBase):
    pass


# =================================================
# ALLOWANCE ADMISSION CHILD
# =================================================
class AllowanceAdmissionChildBase(BaseModel):
    allowance_claim_id: Optional[int] = None
    child_name: Optional[str] = None
    relationship: Optional[str] = None
    class_studying: Optional[str] = None
    school_name: Optional[str] = None
    amount_claimed: Optional[Decimal] = None
    remarks: Optional[str] = None
    document_names: Optional[str] = None
    user_id: Optional[int] = None
    station_id: Optional[int] = None
    city_class: Optional[str] = None
    city_name: Optional[str]=None


class AllowanceAdmissionChildCreate(AllowanceAdmissionChildBase):
    pass


class AllowanceAdmissionChildUpdate(AllowanceAdmissionChildBase):
    pass



class EmployeeChildDropdown(BaseModel):
    ef_id: int
    full_name: str

    class Config:
        from_attributes = True