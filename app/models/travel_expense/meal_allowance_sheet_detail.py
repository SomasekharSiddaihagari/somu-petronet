from sqlalchemy import Column, BigInteger, String, Date, DateTime, ForeignKey, Numeric, Text, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class MealAllowanceSheetDetail(Base):
    __tablename__ = "meal_allowance_sheet_detail"
 
    meal_sheet_detail_id = Column(BigInteger, primary_key=True, autoincrement=True)
    meal_sheet_id = Column(BigInteger, ForeignKey("meal_allowance_sheet.meal_sheet_id"), nullable=True)
 
    date = Column(Date, nullable=True)
    from_time = Column(Time, nullable=True)
    to_time = Column(Time, nullable=True)
    travel_route = Column(String(255), nullable=True)
    time_duration = Column(String(50), nullable=True)  # Time (From-To)
    distance_from_station = Column(String(50), nullable=True)
    purpose = Column(Text, nullable=True)
 
    # Amount + GST
    meal_amount = Column(Numeric(12, 2), nullable=True)
    meal_gst = Column(Numeric(12, 2), nullable=True)
    meal_total = Column(Numeric(12, 2), nullable=True)
 
    meal_proof = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=True)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    sheet = relationship("MealAllowanceSheet", back_populates="entries")