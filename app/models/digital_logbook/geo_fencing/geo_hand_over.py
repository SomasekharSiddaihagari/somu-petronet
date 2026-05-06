from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Float, Time, Enum, UniqueConstraint, CheckConstraint
)
from sqlalchemy.sql import func
from app.database import Base
import enum

class ShiftHandoverLog(Base):
    __tablename__ = "shift_handover_log"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("station.station_id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shift.shift_id"), nullable=False)
 
    from_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
 
    event_type = Column(String(50), nullable=False)
    # REQUESTED | ACCEPTED | REJECTED | TIMEOUT
 
    event_time = Column(DateTime(timezone=True), server_default=func.now())
    remarks = Column(String(255), nullable=True)
    is_acknowledge = Column(Boolean, nullable=True)