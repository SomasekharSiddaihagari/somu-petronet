from sqlalchemy import Column, BigInteger, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
 
Base = declarative_base()
 
class HRLeaveApplicationDayHistory(Base):
    __tablename__ = "hr_leave_application_day_history"
 
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    leave_day_id = Column(BigInteger, nullable=True)
    leave_application_id = Column(BigInteger, nullable=True)
 
    leave_date = Column(Date, nullable=True)
 
    day_type = Column(String(10), nullable=True)
    half_session = Column(String(20), nullable=True)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())