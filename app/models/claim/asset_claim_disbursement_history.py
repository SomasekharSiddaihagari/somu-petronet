from sqlalchemy import (
    Column, BigInteger, Integer, String, Date,
    DateTime, Numeric, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class AssetClaimDisbursementHistory(Base):
    __tablename__ = "asset_claim_disbursement_history"
 
    asset_claim_disbursement_history_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    asset_claim_disbursement_id = Column(BigInteger, nullable=True)
    asset_claim_submission_id = Column(BigInteger, nullable=True)
 
    claim_amount = Column(Numeric(12, 2), nullable=True)
    disbursed_amount = Column(Numeric(12, 2), nullable=True)
    payment_mode = Column(String(50), nullable=True)
    disbursement_date = Column(Date, nullable=True)
 
    transaction_reference_no = Column(String(100), nullable=True)
 
    bank_name = Column(String(150), nullable=True)
    account_number = Column(String(50), nullable=True)
    sap_assets_no = Column(BigInteger, nullable=True)
    remarks = Column(Text, nullable=True)
 
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