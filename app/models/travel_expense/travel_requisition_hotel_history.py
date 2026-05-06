from sqlalchemy import Column, BigInteger, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
 
 
class TravelRequisitionHotelHistory(Base):
    __tablename__ = "travel_requisition_hotel_history"
 
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    requisition_id = Column(BigInteger, nullable=True)
 
    city = Column(String(100), nullable=True)
    hotel_name = Column(String(150), nullable=True)
    hotel_remarks = Column(Text, nullable=True)
 
    updated_at = Column(DateTime(timezone=True), server_default=func.now())