import datetime

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class EmployeeTransfer(Base):
    __tablename__ = "employee_transfers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    current_station = Column(Integer, nullable=False)
    new_station = Column(Integer, nullable=False)
    effective_date = Column(DateTime, nullable=False)
    remarks = Column(Text, nullable=True)
    acknowledgement = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime)
    created_by = Column(Integer, nullable=True)
    comments =  Column(Text, nullable=True)
    office_order_number = Column(Text, nullable=True)
    actual_joining_date = Column(DateTime, default=datetime)