from sqlalchemy import (
    Column, BigInteger, Integer, String, Date,
    DateTime, Numeric, Boolean, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class LeaveEncashment(Base):
    __tablename__ = "leave_encashment"
 
    leave_encashment_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    encashment_main_id = Column(BigInteger, nullable=True)
 
    # Employee Information
    employee_name = Column(String(150), nullable=True)
    employee_code = Column(String(50), nullable=True)
    designation = Column(String(100), nullable=True)
    station = Column(String(100), nullable=True)
    encashment_date = Column(Date, nullable=True)
    leave_type = Column(String(50), nullable=True)
    encashment_opening = Column(Numeric(10, 2), nullable=True)
    non_encashment_opening = Column(Numeric(10, 2), nullable=True)
    total_encashment_opening = Column(Numeric(10, 2), nullable=True)
    # Leave Balance Details
    el_encashable = Column(Numeric(10, 2), nullable=True)
    encash_el = Column(Numeric(10, 2), nullable=True)
    balance_as_on_date = Column(Numeric(10, 2), nullable=True)
    amount_claimed = Column(Numeric(12, 2), nullable=True)

 
    # Request & Declaration
    request_text = Column(Text, nullable=True)
    declaration_accepted = Column(Boolean, nullable=True)
 
    # Status
    status = Column(String(30), nullable=True)
 
    # Audit
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    updated_by_supervisor = Column(Date, nullable=True)
    updated_by_supervisor_name = Column(String(150), nullable=True)
    # HR
    updated_by_hr = Column(Date, nullable=True)
    updated_by_hr_name = Column(String(150), nullable=True)

    # Finance
    updated_by_finance = Column(Date, nullable=True)
    updated_by_finance_name = Column(String(150), nullable=True)