from sqlalchemy import (
    Column, BigInteger, Integer, String,
    Date, DateTime, Numeric, Boolean, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class LaptopMaintenanceReimbursementHistory(Base):
    __tablename__ = "laptop_maintenance_reimbursement_history"
 
    laptop_maintenance_reimbursement_history_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    laptop_maintenance_reimbursement_id = Column(BigInteger, nullable=True)
    ra_claim_id = Column(BigInteger, nullable=True)
 
    date_of_purchase = Column(Date, nullable=True)
    date_of_claim = Column(Date, nullable=True)
    date_of_previous_claim = Column(Date, nullable=True)
 
    amount_claimed = Column(Numeric(12, 2), nullable=True)
 
    annual_limit = Column(Numeric(12, 2), nullable=True)
    eligible_amount = Column(Numeric(12, 2), nullable=True)
 
    document_names = Column(Text, nullable=True)
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
 
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 