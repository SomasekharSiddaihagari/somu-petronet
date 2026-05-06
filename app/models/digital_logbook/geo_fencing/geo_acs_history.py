from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Float, Time, Enum, UniqueConstraint, CheckConstraint
)
from sqlalchemy.sql import func
from app.database import Base
import enum

class AccessControlStation(Base):
    __tablename__ = "access_control_station_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    id=Column(Integer, nullable=True)
 
    station_id = Column(Integer, nullable=False, unique=True)
    station_name = Column(String(150), nullable=True)
 
    # IP range
    ip_from = Column(String(45), nullable=True)
    ip_to = Column(String(45), nullable=True)
 
    # Geo fence
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    radius = Column(Float, nullable=True)  # meters / km
 
    is_active = Column(Boolean, default=True)
 
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now()
    )