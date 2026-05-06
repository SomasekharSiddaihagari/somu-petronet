from sqlalchemy import (
    Column, BigInteger, Integer, String,
    Date, DateTime, Numeric, Boolean,
    Text, ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class VehicleCMReimbursement(Base):
    __tablename__ = "vehicle_cm_reimbursement"
 
    vehicle_cm_reimbursement_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    # FK to R&A main claim
    ra_claim_id = Column(
        BigInteger,
        ForeignKey("ra_claim.ra_claim_id", ondelete="CASCADE"),
        nullable=False
    )
 
    # -------- Vehicle Details --------
    vehicle_name = Column(String(150), nullable=True)
    claim_month_year = Column(String(20), nullable=True)
 
    vehicle_no = Column(String(50), nullable=True)
    vehicle_type = Column(String(50), nullable=True)
    fuel_type = Column(String(50), nullable=True)
 
    rc_expiry_date = Column(Date, nullable=True)
    insurance_expiry_date = Column(Date, nullable=True)
 
    # -------- Claim Details --------
    fuel_claim_amount = Column(Numeric(12, 2), nullable=True)
    applicable_fuel_rate = Column(Numeric(10, 2), nullable=True)
    fuel_claimed_liters = Column(Numeric(10, 2), nullable=True)
 
    maintenance_claim_amount = Column(Numeric(12, 2), nullable=True)
 
    fixed_conveyance_claim = Column(Boolean, nullable=True)
    fixed_conveyance_claim_amount = Column(Numeric(12, 2), nullable=True)
    # -------- Entitlement Snapshot --------
    annual_entitlement_fuel = Column(Numeric(12, 2), nullable=True)
    annual_entitlement_maintenance = Column(Numeric(12, 2), nullable=True)
 
    monthly_ceiling_fuel = Column(Numeric(12, 2), nullable=True)
    monthly_ceiling_maintenance = Column(Numeric(12, 2), nullable=True)
 
    adjustment_previous_month_fuel = Column(Numeric(12, 2), nullable=True)
    adjustment_previous_month_maintenance = Column(Numeric(12, 2), nullable=True)
 
    net_available_balance_fuel = Column(Numeric(12, 2), nullable=True)
    net_available_balance_maintenance = Column(Numeric(12, 2), nullable=True)
 
    max_claim_allowed_fuel = Column(Numeric(12, 2), nullable=True)
    max_claim_allowed_maintenance = Column(Numeric(12, 2), nullable=True)
 
    # -------- Documents --------
    document_names = Column(Text, nullable=True)
 
    # -------- Remarks & Declaration --------
    remarks = Column(Text, nullable=True)
    declaration_accepted = Column(Boolean, nullable=True)
 
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