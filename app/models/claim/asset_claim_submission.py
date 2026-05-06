from sqlalchemy import (
    Column, BigInteger, Integer, String, Date,
    DateTime, Numeric, Boolean, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class AssetClaimSubmission(Base):
    __tablename__ = "asset_claim_submission"
 
    asset_claim_submission_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    # Reference (optional linkage to main claim)
    asset_claim_id = Column(BigInteger, nullable=True)
 
    # 1. Claim Details
    item_type = Column(String(150), nullable=True)
    item_name = Column(String(150), nullable=True)
    claim_amount = Column(Numeric(12, 2), nullable=True)
    owned_by = Column(Text, nullable=True)
 
    # 2. Vendor Details
    vendor_name = Column(String(150), nullable=True)
    vendor_gstin = Column(String(50), nullable=True)
    vendor_address = Column(Text, nullable=True)
    vendor_contact_no = Column(String(50), nullable=True)
    invoice_date = Column(Date, nullable=True)
    invoice_no = Column(String(100), nullable=True)
    sap_assets_no = Column(BigInteger, nullable=True)
    # 3. Document Upload (metadata only)
    document_names = Column(Text, nullable=True)   # comma-separated or JSON string
 
    # 4. Declaration
    declaration_accepted = Column(Boolean, nullable=True)
 
    # Status
    status = Column(String(30), nullable=True)
 
    # Audit
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
    residual_value_percent = Column(Numeric(5, 2), nullable=True)
    residual_value_amount = Column(Numeric(12, 2), nullable=True)
    amount_to_be_disbursed = Column(Numeric(12, 2), nullable=True)
   
    hr_comment = Column(Text, nullable=True)
    finance_comment = Column(Text, nullable=True)
    supervisor_comment = Column(Text, nullable=True)    
 
    updated_by_supervisor = Column(Date, nullable=True)
    updated_by_supervisor_name = Column(String(150), nullable=True)
    # HR
    updated_by_hr = Column(Date, nullable=True)
    updated_by_hr_name = Column(String(150), nullable=True)
 
    # Finance
    updated_by_finance = Column(Date, nullable=True)
    updated_by_finance_name = Column(String(150), nullable=True)
 