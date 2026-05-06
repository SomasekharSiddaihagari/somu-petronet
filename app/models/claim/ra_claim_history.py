from sqlalchemy import (
    Column, BigInteger, Integer, String,
    Date, DateTime, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class RAClaimHistory(Base):
    __tablename__ = "ra_claim_history"
 
    ra_claim_history_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    ra_claim_id = Column(BigInteger, nullable=True)
    ra_claim_ref_id = Column(String(50), nullable=True)
 
    # Snapshot of employee & claim
    employee_name = Column(String(150), nullable=True)
    employee_id = Column(String(50), nullable=True)
    department = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    station = Column(String(100), nullable=True)
    grade = Column(String(50), nullable=True)
 
    claim_module = Column(String(30), nullable=True)
    category = Column(String(150), nullable=True)
 
    status = Column(String(30), nullable=True)
    remarks = Column(Text, nullable=True)
 
    # Supervisor
    updated_by_supervisor = Column(Date, nullable=True)
    updated_by_supervisor_name = Column(String(150), nullable=True)
 
    # HR
    updated_by_hr = Column(Date, nullable=True)
    updated_by_hr_name = Column(String(150), nullable=True)
 
    # Finance
    updated_by_finance = Column(Date, nullable=True)
    updated_by_finance_name = Column(String(150), nullable=True)
 
    # Audit
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())