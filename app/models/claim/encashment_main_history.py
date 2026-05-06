from sqlalchemy import (
    Column, BigInteger, Date, Integer, String, DateTime
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class EncashmentMainHistory(Base):
    __tablename__ = "encashment_main_history"
 
    encashment_main_history_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    encashment_main_id = Column(BigInteger, nullable=True)
 
    # Snapshot fields
    encashment_ref_id = Column(String(50), nullable=True)
    employee_name = Column(String(150), nullable=True)
    employee_code = Column(String(50), nullable=True)
    department = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    station = Column(String(100), nullable=True)
    grade = Column(String(50), nullable=True)
 
    status = Column(String(30), nullable=True)
 
    # Audit
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    updated_by_supervisor = Column(Date, nullable=True)
    updated_by_supervisor_name = Column(String(150), nullable=True)
    # HR
    updated_by_hr = Column(Date, nullable=True)
    updated_by_hr_name = Column(String(150), nullable=True)

    # Finance
    updated_by_finance = Column(Date, nullable=True)
    updated_by_finance_name = Column(String(150), nullable=True)