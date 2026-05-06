import datetime

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class EmployeePerformance(Base):
    __tablename__ = "employee_performance"
    performance_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    appraisal_start_date = Column(DateTime, nullable=False)
    appraisal_end_date = Column(DateTime, nullable=False)
    annual_appraisal_rating = Column(String(50), nullable=True)
    annual_rating_score = Column(String(20), nullable=True)
    acknowledgement = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    comments =  Column(Text, nullable=True)