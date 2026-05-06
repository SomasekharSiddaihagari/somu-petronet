from sqlalchemy import (
    Column, BigInteger, String, Date, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
 
Base = declarative_base()
 
 
class HRPublicHoliday(Base):
    __tablename__ = "hr_public_holiday"   # table for Add Public Holiday popup
 
    public_holiday_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    # From UI
    holiday_name = Column(String(150), nullable=True)   # e.g. "Holi"
    holiday_type = Column(String(50), nullable=True)    # "Public Holidays" / "Restricted Holidays"
    holiday_date = Column(Date, nullable=True)          # Date picker
 
    # Status (active / inactive etc. if you need later)
    status = Column(String(20), nullable=True)
 
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())