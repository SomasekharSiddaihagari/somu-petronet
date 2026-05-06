from sqlalchemy import (
    Column, BigInteger, Integer, String, Date,
    DateTime, Numeric, Boolean, Text, ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class AllowanceClaim(Base):
    __tablename__ = "allowance_claim"
 
    allowance_claim_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    # FK to RA master
    ra_claim_id = Column(
        BigInteger,
        ForeignKey("ra_claim.ra_claim_id", ondelete="CASCADE"),
        nullable=False
    )
 
    # -------- Employee Info --------
    employee_name = Column(String(150), nullable=True)
    employee_id = Column(String(50), nullable=True)
    department = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    station = Column(String(100), nullable=True)
    grade = Column(String(50), nullable=True)
 
    from_location = Column(String(100), nullable=True)
    to_location = Column(String(100), nullable=True)
    effective_transfer_date = Column(Date, nullable=True)
    claim_date = Column(Date, nullable=True)
 
    # -------- Travel --------
    travel_from = Column(String(100), nullable=True)
    travel_to = Column(String(100), nullable=True)
    travel_mode = Column(String(50), nullable=True)
    travel_date = Column(Date, nullable=True)
    number_of_passengers = Column(Integer, nullable=True)
    travel_amount = Column(Numeric(12, 2), nullable=True)
    travel_remarks = Column(Text, nullable=True)
    travel_documents = Column(Text, nullable=True)
    include_travel = Column(Boolean, nullable=True)
 
    # -------- Displacement --------
    displacement_city = Column(String(100), nullable=True)
    no_of_days_claimed = Column(Integer, nullable=True)
    displacement_rate = Column(Numeric(10, 2), nullable=True)
    displacement_amount = Column(Numeric(12, 2), nullable=True)
    maximum_eligible_days = Column(Integer, nullable=True)
    displacement_remarks = Column(Text, nullable=True)
    displacement_documents = Column(Text, nullable=True)
    include_displacement = Column(Boolean, nullable=True)
 
    # -------- Settling Allowance --------
    basic_pay_monthly = Column(Numeric(12, 2), nullable=True)
    dearness_allowance_monthly = Column(Numeric(12, 2), nullable=True)
    eligible_settling_amount = Column(Numeric(12, 2), nullable=True)
    settling_remarks = Column(Text, nullable=True)
    settling_documents = Column(Text, nullable=True)
    include_settling = Column(Boolean, nullable=True)
 
    # -------- Transportation of Household Goods --------
    transport_mode = Column(String(50), nullable=True)
    transport_distance_km = Column(Numeric(10, 2), nullable=True)
    freight_amount = Column(Numeric(12, 2), nullable=True)
    goods_transport_remarks = Column(Text, nullable=True)
    goods_transport_documents = Column(Text, nullable=True)
    include_goods_transport = Column(Boolean, nullable=True)
    amount_claimed_household_transport = Column(Numeric(12, 2), nullable=True)

    # -------- Packaging --------
    amount_claimed_packaging = Column(Numeric(12, 2), nullable=True)
    packaging_vendor = Column(String(150), nullable=True)
    packaging_bill_no = Column(String(100), nullable=True)
    packaging_remarks = Column(Text, nullable=True)
    packaging_documents = Column(Text, nullable=True)
    include_packaging = Column(Boolean, nullable=True)
    maximum_eligible_amount_packaging = Column(Numeric(12, 2), nullable=True)
 
    # -------- Insurance --------
    insurance_company = Column(String(150), nullable=True)
    policy_no = Column(String(100), nullable=True)
    insurance_amount = Column(Numeric(12, 2), nullable=True)
    insurance_start_date = Column(Date, nullable=True)
    insurance_end_date = Column(Date, nullable=True)
    insurance_remarks = Column(Text, nullable=True)
    insurance_documents = Column(Text, nullable=True)
    include_insurance = Column(Boolean, nullable=True)
 
    # -------- Vehicle Transport --------
    vehicle_type = Column(String(50), nullable=True)
    vehicle_registration_no = Column(String(50), nullable=True)
    vehicle_transport_mode = Column(String(50), nullable=True)
    vehicle_transport_amount = Column(Numeric(12, 2), nullable=True)
    vehicle_transport_remarks = Column(Text, nullable=True)
    vehicle_transport_documents = Column(Text, nullable=True)
    include_vehicle_transport = Column(Boolean, nullable=True)
    vehicle_transport_distance_km = Column(Numeric(10, 2), nullable=True)
 
    # -------- Totals --------
    total_travel = Column(Numeric(12, 2), nullable=True)
    total_displacement = Column(Numeric(12, 2), nullable=True)
    total_settling = Column(Numeric(12, 2), nullable=True)
    total_goods_transport = Column(Numeric(12, 2), nullable=True)
    total_packaging = Column(Numeric(12, 2), nullable=True)
    total_insurance = Column(Numeric(12, 2), nullable=True)
    total_vehicle_transport = Column(Numeric(12, 2), nullable=True)
    total_admission = Column(Numeric(12, 2), nullable=True)
    grand_total = Column(Numeric(12, 2), nullable=True)
    settling_no_of_days = Column(Integer, nullable=True)
    t_house_hold_rate = Column(Numeric(10, 2), nullable=True)
    vehicle_rate = Column(Numeric(10, 2), nullable=True)

    remarks = Column(Text, nullable=True)
    status = Column(String(30), nullable=True)
 
    # -------- Supervisor --------
    updated_by_supervisor = Column(Date, nullable=True)
    updated_by_supervisor_name = Column(String(150), nullable=True)
    supervisor_comment = Column(Text, nullable=True)
 
    # -------- HR --------
    updated_by_hr = Column(Date, nullable=True)
    updated_by_hr_name = Column(String(150), nullable=True)
    hr_comment = Column(Text, nullable=True)
 
    # -------- Finance --------
    updated_by_finance = Column(Date, nullable=True)
    updated_by_finance_name = Column(String(150), nullable=True)
    finance_comment = Column(Text, nullable=True)
 
    # -------- Audit --------
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())