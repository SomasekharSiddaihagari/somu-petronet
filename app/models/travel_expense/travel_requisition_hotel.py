from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class TravelRequisitionHotel(Base):
    __tablename__ = "travel_requisition_hotel"
 
    trh_id = Column(BigInteger, primary_key=True, autoincrement=True)
    requisition_id = Column(BigInteger, ForeignKey("travel_requisition.travel_id"), nullable=True)
 
    city = Column(String(100), nullable=True)
    hotel_name = Column(String(150), nullable=True)
    hotel_remarks = Column(Text, nullable=True)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    requisition = relationship("TravelRequisition", back_populates="hotels")