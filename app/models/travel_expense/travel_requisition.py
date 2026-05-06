from sqlalchemy import Boolean, Column, BigInteger, Date, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.travel_expense.travel_requisition_travel import TravelRequisitionTravel
from app.models.travel_expense.travel_requisition_hotel import TravelRequisitionHotel
from app.models.travel_expense.travel_requisition_car import TravelRequisitionCar

 
class TravelRequisition(Base):
    __tablename__ = "travel_requisition"
    travel_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    employee_name = Column(String(150), nullable=True)
    employee_number = Column(String(50), nullable=True)
    designation = Column(String(100), nullable=True)
    grade = Column(String(100), nullable=True)
    station = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True) 
    purpose_of_travel = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
    approver_comments = Column(Text, nullable=True)
    # Special Services
    visa_for = Column(Text, nullable=True)
    emigration_required = Column(Boolean, nullable=True)
    foreign_exchange = Column(Text, nullable=True)
    to_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 
    travels = relationship("TravelRequisitionTravel", back_populates="requisition")
    hotels = relationship("TravelRequisitionHotel", back_populates="requisition")
    cars = relationship("TravelRequisitionCar", back_populates="requisition")
    # services = relationship("TravelRequisitionSpecialServices", back_populates="requisition")
    # user = relationship("User", back_populates="travel_requisitions")






