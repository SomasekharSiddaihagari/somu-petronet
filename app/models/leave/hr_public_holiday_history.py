from sqlalchemy import Column, BigInteger, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
 
Base = declarative_base()
 
class HRPublicHolidayHistory(Base):
    __tablename__ = "hr_public_holiday_history"
 
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    public_holiday_id = Column(BigInteger, nullable=True)
 
    holiday_name = Column(String(150), nullable=True)
    holiday_type = Column(String(50), nullable=True)
    holiday_date = Column(Date, nullable=True)
 
    status = Column(String(20), nullable=True)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())