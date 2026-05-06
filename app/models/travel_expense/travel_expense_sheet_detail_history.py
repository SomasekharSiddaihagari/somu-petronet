
from sqlalchemy import Boolean, Column, BigInteger, Integer, String, DateTime, Date, Numeric, Text
from sqlalchemy.sql import func
from app.database import Base
 
class TravelExpenseSheetDetailHistory(Base):
    __tablename__ = "travel_expense_sheet_detail_history"

    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    tesd_id = Column(Integer, nullable=True)  #


    expense_sheet_id = Column(Integer, nullable=True)
    from_date = Column(Date, nullable=True)

    travel_route = Column(String(255), nullable=True)
    from_location = Column(String(255), nullable=True)
    to_location = Column(String(255), nullable=True)

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
    from_location = Column(String(255), nullable=True)
    to_location = Column(String(255), nullable=True)
    air_rail_bus_proof = Column(String(255), nullable=True)
    hotel_proof = Column(String(255), nullable=True)
    daily_allowance_proof = Column(String(255), nullable=True)
    local_conveyance_proof = Column(String(255), nullable=True)
    other_proof = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    remarks = Column(Text, nullable=True)
    user_id = Column(Integer, nullable=True)
    is_overseas = Column(Boolean, nullable=True)

    
