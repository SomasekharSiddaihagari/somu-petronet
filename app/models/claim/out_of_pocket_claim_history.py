from sqlalchemy import (
    Column, BigInteger, Integer, String,
    Date, DateTime, Numeric, Boolean, Text,
    ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base
 

class OutOfPocketClaimHistory(Base):

    __tablename__ = "out_of_pocket_claim_history"
 
    out_of_pocket_claim_history_id = Column(

        BigInteger, primary_key=True, autoincrement=True

    )
 
    out_of_pocket_claim_id = Column(BigInteger, nullable=True)

    ra_claim_id = Column(BigInteger, nullable=True)
 
    claim_month_year = Column(String(20), nullable=True)

    total_claims = Column(Integer, nullable=True)

    total_amount = Column(Numeric(12, 2), nullable=True)
 
    document_names = Column(Text, nullable=True)

    remarks = Column(Text, nullable=True)

    declaration_accepted = Column(Boolean, nullable=True)

    status = Column(String(30), nullable=True)
 
    # Supervisor / HR / Finance (same as main)

    updated_by_supervisor = Column(Date, nullable=True)

    updated_by_supervisor_name = Column(String(150), nullable=True)

    supervisor_comment = Column(Text, nullable=True)
 
    updated_by_hr = Column(Date, nullable=True)

    updated_by_hr_name = Column(String(150), nullable=True)

    hr_comment = Column(Text, nullable=True)
 
    updated_by_finance = Column(Date, nullable=True)

    updated_by_finance_name = Column(String(150), nullable=True)

    finance_comment = Column(Text, nullable=True)

    updated_by_hop = Column(Date, nullable=True)

    updated_by_hop_name = Column(String(150), nullable=True)

    hop_comment = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

 

 