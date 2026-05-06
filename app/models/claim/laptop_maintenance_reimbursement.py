from sqlalchemy import (
    Column, BigInteger, Integer, String,
    Date, DateTime, Numeric, Boolean,
    Text, ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class LaptopMaintenanceReimbursement(Base):
    __tablename__ = "laptop_maintenance_reimbursement"
 
    laptop_maintenance_reimbursement_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    # FK to R&A main claim
    ra_claim_id = Column(
        BigInteger,
        ForeignKey("ra_claim.ra_claim_id", ondelete="CASCADE"),
        nullable=False
    )
 
    # -------- Claim Details --------
    date_of_purchase = Column(Date, nullable=True)
    date_of_claim = Column(Date, nullable=True)
    date_of_previous_claim = Column(Date, nullable=True)
 
    amount_claimed = Column(Numeric(12, 2), nullable=True)
 
    # -------- Entitlement Snapshot --------
    annual_limit = Column(Numeric(12, 2), nullable=True)
    eligible_amount = Column(Numeric(12, 2), nullable=True)
 
    # -------- Documents --------
    document_names = Column(Text, nullable=True)
 
    # -------- Remarks --------
    remarks = Column(Text, nullable=True)
 
    # -------- Declaration --------
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
 