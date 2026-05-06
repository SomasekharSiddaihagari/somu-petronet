from sqlalchemy import (
    Column, BigInteger, Integer, String, DateTime, Date, ForeignKey, Numeric, Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class DailyAllowanceSheetDetail(Base):
    __tablename__ = "daily_allowance_sheet_detail"

    da_sheet_detail_id = Column(BigInteger, primary_key=True, autoincrement=True)
    da_sheet_id = Column(BigInteger, ForeignKey("daily_allowance_sheet.da_sheet_id"), nullable=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)

    # Main Fields
    from_date = Column(Date, nullable=True)
    time_duration = Column(String(50), nullable=True)
    travel_from = Column(String(100), nullable=True)
    travel_to = Column(String(100), nullable=True)
    distance_from_station = Column(String(50), nullable=True)

    purpose = Column(Text, nullable=True)

    da_amount = Column(Numeric(12, 2), nullable=True)
    da_gst = Column(Numeric(12, 2), nullable=True)
    da_total = Column(Numeric(12, 2), nullable=True)

    da_proof = Column(Text, nullable=True) 
    remarks = Column(Text, nullable=True)

    # New fields found in DB
    from_location = Column(String(255), nullable=True)
    to_location = Column(String(255), nullable=True)
    from_date_time = Column(DateTime(timezone=True), nullable=True)
    to_date_time = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    sheet = relationship("DailyAllowanceSheet", back_populates="entries")
