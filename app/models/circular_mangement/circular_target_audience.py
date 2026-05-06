
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

 
class CircularTargetAudience(Base):
    __tablename__ = "circular_target_audience"
 
    audience_id = Column(Integer, primary_key=True, autoincrement=True)
 
    circular_id = Column(
        Integer,
        ForeignKey("circular_master.circular_id"),
        nullable=False
    )
 
    # GROUP | DEPARTMENT | STATION | INDIVIDUAL
    audience_type = Column(String(50), nullable=True)
 
    # stores ID of group_id / department_id / station_id / user_id
    audience_ref_id = Column(JSONB, nullable=False)
    created_by = Column(Integer, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    
    updated_by = Column(Integer, nullable=True)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)

    version = Column(String(20), nullable=True)
