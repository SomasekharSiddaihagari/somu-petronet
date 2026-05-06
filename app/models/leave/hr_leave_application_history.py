from sqlalchemy import (
    ARRAY, Column, BigInteger, Integer, String, Date, DateTime, Numeric, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
 
Base = declarative_base()
 
class HRLeaveApplicationHistory(Base):
    __tablename__ = "hr_leave_application_history"
 
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    leave_id = Column(BigInteger, nullable=True)
    user_id = Column(BigInteger, nullable=True)
    comp_dates = Column(ARRAY(Date), nullable=True)
    supervisor_id = Column(Integer, nullable=True)
    supervisor_name = Column(String(100), nullable=True)
    user_name = Column(String(100), nullable=True)
 
    leave_type = Column(String(50), nullable=True)
 
    from_date = Column(Date, nullable=True)
    to_date = Column(Date, nullable=True)
 
    number_of_days = Column(Numeric(5, 2), nullable=True)
 
    reason = Column(Text, nullable=True)
    document_path = Column(String(255), nullable=True)
 
    contact_address = Column(Text, nullable=True)
    phone_number = Column(String(20), nullable=True)
 
    reversal_from_date = Column(Date, nullable=True)
    reversal_to_date = Column(Date, nullable=True)
    reversal_remarks = Column(Text, nullable=True)
 
    status = Column(String(20), nullable=True)
    
    supervisor_remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())