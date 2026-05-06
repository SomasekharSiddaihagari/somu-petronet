from sqlalchemy import Column, BigInteger, Integer, String, Numeric, ForeignKey, Text
from app.database import Base
 
 
class AllowanceAdmissionChild(Base):
    __tablename__ = "allowance_admission_child"
 
    allowance_admission_child_id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
 
    allowance_claim_id = Column(
        BigInteger,
        ForeignKey("allowance_claim.allowance_claim_id", ondelete="CASCADE"),
        nullable=False
    )
    city_class = Column(String(100), nullable=True)
    city_name = Column(String(150), nullable=True)
    child_name = Column(String(150), nullable=True)
    relationship = Column(String(50), nullable=True)
    class_studying = Column(String(50), nullable=True)
    school_name = Column(String(150), nullable=True)
    amount_claimed = Column(Numeric(12, 2), nullable=True)
    remarks = Column(Text, nullable=True)
    document_names = Column(Text, nullable=True)
    user_id = Column(BigInteger, nullable=True)
    station_id = Column(BigInteger, nullable=True)