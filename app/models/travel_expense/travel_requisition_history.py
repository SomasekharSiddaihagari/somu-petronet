from sqlalchemy import Boolean, Column, BigInteger, Date, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
 
 
class TravelRequisitionHistory(Base):
    __tablename__ = "travel_requisition_history"
 
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    requisition_id = Column(BigInteger, nullable=True)
 
    employee_name = Column(String(150), nullable=True)
    employee_number = Column(String(50), nullable=True)
    designation = Column(String(100), nullable=True)
    grade = Column(String(100), nullable=True)
    station = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    to_date = Column(Date, nullable=True)
    purpose_of_travel = Column(Text, nullable=True)
 
    visa_for = Column(Text, nullable=True)
    emigration_required = Column(Boolean, nullable=True)
    foreign_exchange = Column(Text, nullable=True)
 
    status = Column(String(50), nullable=True)
    approver_comments = Column(Text, nullable=True)
 
    updated_at = Column(DateTime(timezone=True), server_default=func.now())