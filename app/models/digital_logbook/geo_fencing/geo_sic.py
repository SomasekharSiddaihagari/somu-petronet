from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Float, Time, Enum, UniqueConstraint, CheckConstraint
)
from sqlalchemy.sql import func
from app.database import Base
import enum

class StationShiftIncharge(Base):
    __tablename__ = "station_shift_incharge"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
 
    station_id = Column(Integer, ForeignKey("station.station_id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shift.shift_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
 
    # Responsibility window
    responsibility_from = Column(DateTime(timezone=True), nullable=False)
    responsibility_to = Column(DateTime(timezone=True), nullable=True)  # NULL = still responsible
 
    # Handover tracking
    handover_requested_at = Column(DateTime(timezone=True), nullable=True)
    handover_accepted_at = Column(DateTime(timezone=True), nullable=True)
    handover_to_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    comment_for_next_incharge = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())




    