from sqlalchemy import Column, BigInteger, String, Date, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
 
 
class TravelRequisitionTravelHistory(Base):
    __tablename__ = "travel_requisition_travel_history"
 
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    requisition_id = Column(BigInteger, nullable=True)
    to_date = Column(Date, nullable=True)
    from_location = Column(String(100), nullable=True)
    to_location = Column(String(100), nullable=True)
    travel_date = Column(Date, nullable=True)
    flight_train_number = Column(String(100), nullable=True)
    class_of_travel = Column(String(50), nullable=True)
    travel_remarks = Column(Text, nullable=True)
    to_date=Column(Date, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())