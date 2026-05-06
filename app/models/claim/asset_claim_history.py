from sqlite3 import Date
from sqlalchemy import (

    Column, BigInteger, Integer, String, DateTime,

    Numeric, Text

)

from sqlalchemy.sql import func

from app.database import Base
 
 
class AssetClaimHistory(Base):

    __tablename__ = "asset_claim_history"
 
    asset_claim_history_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    asset_claim_id = Column(BigInteger, nullable=True)
    claim_ref_id = Column(String(50), nullable=True)
    # Employee Information

    employee_name = Column(String(150), nullable=True)

    employee_id = Column(String(50), nullable=True)

    department = Column(String(100), nullable=True)

    designation = Column(String(100), nullable=True)

    station = Column(String(100), nullable=True)

    grade = Column(String(50), nullable=True)
 
    # Claim Selection

    claim_module = Column(String(50), nullable=True)

    category = Column(String(100), nullable=True)

    sub_category = Column(String(150), nullable=True)

    item_type = Column(String(100), nullable=True)
 
    # Entitlement & Utilization

    total_entitlement_limit = Column(Numeric(12, 2), nullable=True)

    amount_utilized = Column(Numeric(12, 2), nullable=True)

    balance_available = Column(Numeric(12, 2), nullable=True)
 
    # Status

  
   
    status = Column(String(30), nullable=True)

    remarks = Column(Text, nullable=True)
 
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

 