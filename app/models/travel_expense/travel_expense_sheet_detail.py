from sqlalchemy import Boolean, Column, BigInteger, Integer, String, Date, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class TravelExpenseSheetDetail(Base):
    __tablename__ = "travel_expense_sheet_detail"
 
    tesd_id = Column(BigInteger, primary_key=True, autoincrement=True)
    expense_sheet_id = Column(BigInteger, ForeignKey("travel_expense_sheet.tes_id"), nullable=True)
    from_date = Column(Date, nullable=True)
    travel_route = Column(String(255), nullable=True)
    air_rail_bus_amount = Column(Numeric(12, 2), nullable=True)
    air_rail_bus_gst = Column(Numeric(12, 2), nullable=True)
    air_rail_bus_total = Column(Numeric(12, 2), nullable=True)
    hotel_amount = Column(Numeric(12, 2), nullable=True)
    hotel_gst = Column(Numeric(12, 2), nullable=True)
    hotel_total = Column(Numeric(12, 2), nullable=True)
    daily_allowance_amount = Column(Numeric(12, 2), nullable=True)
    daily_allowance_gst = Column(Numeric(12, 2), nullable=True)
    daily_allowance_total = Column(Numeric(12, 2), nullable=True)
    local_conveyance_amount = Column(Numeric(12, 2), nullable=True)
    local_conveyance_gst = Column(Numeric(12, 2), nullable=True)
    local_conveyance_total = Column(Numeric(12, 2), nullable=True)
    other_amount = Column(Numeric(12, 2), nullable=True)
    other_gst = Column(Numeric(12, 2), nullable=True)
    other_total = Column(Numeric(12, 2), nullable=True)
    hotel_proof = Column(Text, nullable=True)

    air_rail_bus_proof = Column(Text, nullable=True)
    daily_allowance_proof = Column(Text, nullable=True)
    local_conveyance_proof = Column(Text, nullable=True)
    other_proof = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    from_location = Column(String(255), nullable=True)
    to_location = Column(String(255), nullable=True)
    to_date = Column(Date, nullable=True)
    user_id = Column(Integer, nullable=True)
    is_overseas = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    expense_sheet = relationship("TravelExpenseSheet", back_populates="expense_details")
    