from sqlalchemy import (
    Column, BigInteger, Integer, String,
    Date, DateTime, Numeric, Boolean, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class FurnitureRMReimbursementHistory(Base):
    __tablename__ = "furniture_rm_reimbursement_history"
 
    furniture_rm_reimbursement_history_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    furniture_rm_reimbursement_id = Column(BigInteger, nullable=True)
    ra_claim_id = Column(BigInteger, nullable=True)
 
    # Snapshot
    furniture_name = Column(String(150), nullable=True)
    claim_month_year = Column(String(20), nullable=True)
 
    total_cost_under_policy = Column(Numeric(12, 2), nullable=True)
    expenditure_claimed = Column(Numeric(12, 2), nullable=True)
    maximum_eligible_amount = Column(Numeric(12, 2), nullable=True)
    amount_claimed = Column(Numeric(12, 2), nullable=True)
    eligible_amount = Column(Numeric(12, 2), nullable=True)
 
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