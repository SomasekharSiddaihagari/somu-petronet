from sqlalchemy import (
    Column, BigInteger, Text, Date, DateTime, Boolean, func
)
from app.database import Base
 
 
class EmployeeWeeklyOff(Base):
    __tablename__ = "employee_weekly_off"
 
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    week_off_day = Column(Text, nullable=False)  # 1=Mon … 7=Sun
 
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
 
    is_active = Column(Boolean, nullable=False, default=True)
 
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

 
 