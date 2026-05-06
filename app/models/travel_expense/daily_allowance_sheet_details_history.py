from sqlalchemy import Column, BigInteger, ForeignKey, Integer, String, DateTime, Date, Numeric, Text
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
 
class DailyAllowanceSheetDetailHistory(Base):
    __tablename__ = "daily_allowance_sheet_detail_history"
 
    da_sheet_detail_history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    da_sheet_id = Column(BigInteger, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    date = Column(Date, nullable=True)
    time_duration = Column(String(50), nullable=True)
    travel_from = Column(String(100), nullable=True)
    travel_to = Column(String(100), nullable=True)
    distance_from_station = Column(String(20), nullable=True)
    purpose = Column(Text, nullable=True)
 
    da_amount = Column(Numeric(12, 2), nullable=True)
    da_gst = Column(Numeric(12, 2), nullable=True)
    da_total = Column(Numeric(12, 2), nullable=True)
 
    da_proof = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=True)
 
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    # user=relationship("User")
 