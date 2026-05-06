from sqlalchemy import (
    Boolean, Column, BigInteger, Date, Integer, String, DateTime,
    Numeric, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class AssetClaim(Base):
    __tablename__ = "asset_claim"
 
    asset_claim_id = Column(BigInteger, primary_key=True, autoincrement=True)
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
    claim_date = Column(Date, nullable=True)
    # Status
    status = Column(String(30), nullable=True)
    remarks = Column(Text, nullable=True)
    bought_back=Column(Boolean, nullable=True)
    buy_back_date=Column(Date, nullable=True)
 
   
   
    
    # Audit
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 

















