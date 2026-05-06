from sqlalchemy import (
    Column, BigInteger, String, Numeric, DateTime, Text
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class AllowanceAdmissionChildHistory(Base):
    __tablename__ = "allowance_admission_child_history"
 
    allowance_admission_child_history_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    allowance_admission_child_id = Column(BigInteger, nullable=True)
    allowance_claim_id = Column(BigInteger, nullable=True)
    city_class = Column(String(100), nullable=True)
    city_name = Column(String(150), nullable=True)
    child_name = Column(String(150), nullable=True)
    relationship = Column(String(50), nullable=True)
    class_studying = Column(String(50), nullable=True)
    school_name = Column(String(150), nullable=True)
    amount_claimed = Column(Numeric(12, 2), nullable=True)
    remarks = Column(Text, nullable=True)
    document_names = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )