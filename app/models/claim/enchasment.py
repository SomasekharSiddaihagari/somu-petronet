from sqlite3 import Date
from sqlalchemy import (

    Column, BigInteger, Integer, Numeric, String, DateTime

)

from sqlalchemy.sql import func

from app.database import Base
 
 
class EncashmentMain(Base):

    __tablename__ = "encashment_main"
 
    encashment_main_id = Column(

        BigInteger, primary_key=True, autoincrement=True

    )
 
    # Encashment Reference ID (GENERATED HERE)

    encashment_ref_id = Column(String(50), nullable=True)
 
    # Employee Information (from UI)

    employee_name = Column(String(150), nullable=True)

    employee_code = Column(String(50), nullable=True)

    department = Column(String(100), nullable=True)

    designation = Column(String(100), nullable=True)

    station = Column(String(100), nullable=True)

    grade = Column(String(50), nullable=True)
    claim_module = Column(String(50), nullable=True)
 
    # Status

    status = Column(String(30), nullable=True)
    amount_claimed = Column(Numeric(12, 2), nullable=True)
    # Audit

    created_by = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_by = Column(Integer, nullable=True)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    updated_by_supervisor = Column(Date, nullable=True)
    updated_by_supervisor_name = Column(String(150), nullable=True)
    # HR
    updated_by_hr = Column(Date, nullable=True)
    updated_by_hr_name = Column(String(150), nullable=True)

    # Finance
    updated_by_finance = Column(Date, nullable=True)
    updated_by_finance_name = Column(String(150), nullable=True)

 