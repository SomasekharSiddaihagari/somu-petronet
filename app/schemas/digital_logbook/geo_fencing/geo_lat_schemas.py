from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Float, Time, Enum, UniqueConstraint, CheckConstraint
)
from sqlalchemy.sql import func
from app.database import Base
import enum

class AccessTypeEnum(str, enum.Enum):
    IP = "IP"
    GEO = "GEO"
    APPROVAL = "APPROVAL"
 
 
class LocationAccessToken(Base):
    __tablename__ = "location_access_token"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
 
    user_id = Column(
        Integer, ForeignKey("users.user_id"), nullable=False
    )
    station_id = Column(
        Integer, ForeignKey("station.station_id"), nullable=False
    )
 
    token = Column(String(128), nullable=False, unique=True)
 
    access_type = Column(
        Enum(AccessTypeEnum), nullable=False
    )
 
    # ALWAYS captured
    ip_address = Column(String(45), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    approved_by_user_id = Column(
        Integer, ForeignKey("users.user_id"), nullable=True
    )
 
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
 
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
 
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "station_id",
            "is_active",
            name="uq_one_active_token_per_station"
        ),
    )