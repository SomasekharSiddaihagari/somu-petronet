from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Float, Time, Enum, UniqueConstraint, CheckConstraint
)
from sqlalchemy.sql import func
from app.database import Base
import enum


class LocationAccessApproval(Base):
    __tablename__ = "location_access_approval_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, nullable=True)
 
    requested_station_id = Column(
        Integer, ForeignKey("station.station_id"), nullable=False
    )
    requested_by_user_id = Column(
        Integer, ForeignKey("users.user_id"), nullable=False
    )
 
    approved_by_user_id = Column(
        Integer, ForeignKey("users.user_id"), nullable=False
    )
    approved_by_station_id = Column(
        Integer, ForeignKey("station.station_id"), nullable=False
    )
 
    approved_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at = Column(DateTime(timezone=True), nullable=False)
 
    __table_args__ = (
        CheckConstraint(
            "approved_by_station_id <> requested_station_id",
            name="chk_cross_station_approval_only"
        ),
    )