from sqlalchemy import Column, BigInteger, Date, ForeignKey, Integer, String, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
 
from app.database import Base
 
 
class DailyAllowanceSheetHistory(Base):
 
    __tablename__ = "daily_allowance_sheet_history"
 
    da_sheet_history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    da_sheet_id = Column(BigInteger, nullable=True)
 
    employee_name = Column(String(150), nullable=True)
 
    employee_number = Column(String(50), nullable=True)
 
    designation = Column(String(150), nullable=True)
 
    grade = Column(String(50), nullable=True)
 
    station = Column(String(100), nullable=True)
 
    department = Column(String(100), nullable=True)
 
    total_excl_gst = Column(Numeric(12, 2), nullable=True)
 
    total_gst = Column(Numeric(12, 2), nullable=True)
 
    total_incl_gst = Column(Numeric(12, 2), nullable=True)
 
    advance_taken = Column(Numeric(12, 2), nullable=True)
 
    amount_receivable_payable = Column(Numeric(12, 2), nullable=True)


    updated_by_head_tech = Column(Date, nullable=True)
    updated_by_head_tech_name = Column(String(150), nullable=True)
    head_tech_comments = Column(Text, nullable=True)
 
    comments = Column(Text, nullable=True)
 
    status = Column(String(50), nullable=True)
    purpose = Column(String(255), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
 
    # user = relationship("User")
 
 
 