from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class EmployeePerformanceDocument(Base):
    __tablename__ = "employee_performance_documents"
    id = Column(Integer, primary_key=True, index=True)
    performance_id = Column(Integer, ForeignKey("employee_performance.performance_id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    acknowledgement = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
