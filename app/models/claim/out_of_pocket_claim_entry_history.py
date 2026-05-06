from sqlalchemy import (
    Column, BigInteger, Integer, String,
    Date, DateTime, Numeric, Boolean,
    Text, ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base
 

class OutOfPocketClaimEntryHistory(Base):

    __tablename__ = "out_of_pocket_claim_entry_history"
 
    out_of_pocket_claim_entry_history_id = Column(

        BigInteger, primary_key=True, autoincrement=True

    )
 
    out_of_pocket_claim_entry_id = Column(BigInteger, nullable=True)

    out_of_pocket_claim_id = Column(BigInteger, nullable=True)
 
    entry_type = Column(String(30), nullable=True)

    hours = Column(Numeric(5, 2), nullable=True)

    claim_date = Column(Date, nullable=True)

    amount = Column(Numeric(12, 2), nullable=True)

    justification = Column(Text, nullable=True)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

 
