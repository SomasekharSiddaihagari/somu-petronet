from sqlalchemy import Column, BigInteger, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class TravelRequisitionTravel(Base):
    __tablename__ = "travel_requisition_travel"
 
    trt_id = Column(BigInteger, primary_key=True, autoincrement=True)
    requisition_id = Column(BigInteger, ForeignKey("travel_requisition.travel_id"), nullable=True)
    to_date = Column(Date, nullable=True)
    from_location = Column(String(100), nullable=True)
    to_location = Column(String(100), nullable=True)
    travel_date = Column(Date, nullable=True)
    flight_train_number = Column(String(100), nullable=True)
    class_of_travel = Column(String(50), nullable=True)
    travel_remarks = Column(Text, nullable=True)
    to_date=Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    requisition = relationship("TravelRequisition", back_populates="travels")