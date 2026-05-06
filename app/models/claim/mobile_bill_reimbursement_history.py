from sqlalchemy import (
    Column, BigInteger, Integer, String,
    Date, DateTime, Numeric, Boolean, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class MobileBillReimbursementHistory(Base):
    __tablename__ = "mobile_bill_reimbursement_history"
 
    mobile_bill_reimbursement_history_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    mobile_bill_reimbursement_id = Column(BigInteger, nullable=True)
    ra_claim_id = Column(BigInteger, nullable=True)
 
    # Snapshot
    bill_month_year = Column(String(20), nullable=True)
 
    mobile_number_1 = Column(String(20), nullable=True)
    bill_amount_1 = Column(Numeric(12, 2), nullable=True)
 
    mobile_number_2 = Column(String(20), nullable=True)
    bill_amount_2 = Column(Numeric(12, 2), nullable=True)
 
    total_claimed_amount = Column(Numeric(12, 2), nullable=True)
    monthly_limit = Column(Numeric(12, 2), nullable=True)
    document_names = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
 
    declaration_accepted = Column(Boolean, nullable=True)
    status = Column(String(30), nullable=True)
 
    # ---------- Supervisor ----------
    updated_by_supervisor = Column(Date, nullable=True)
    updated_by_supervisor_name = Column(String(150), nullable=True)
    supervisor_comment = Column(Text, nullable=True)
 
    # ---------- HR ----------
    updated_by_hr = Column(Date, nullable=True)
    updated_by_hr_name = Column(String(150), nullable=True)
    hr_comment = Column(Text, nullable=True)
 
    # ---------- Finance ----------
    updated_by_finance = Column(Date, nullable=True)
    updated_by_finance_name = Column(String(150), nullable=True)
    finance_comment = Column(Text, nullable=True)
 
    # Audit
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())