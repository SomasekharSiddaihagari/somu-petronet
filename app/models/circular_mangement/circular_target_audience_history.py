
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)
from app.database import Base
from sqlalchemy.dialects.postgresql import JSONB
 
 
class CircularTargetAudienceHistory(Base):
    __tablename__ = "circular_target_audience_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    circular_id = Column(Integer, nullable=True)
    audience_type = Column(String(50), nullable=True)
    audience_ref_id = Column(Integer, nullable=True)
    removed_user = Column(JSONB, nullable=True)
 
 
    created_by = Column(Integer, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
 
    updated_by = Column(Integer, nullable=True)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)

    version = Column(String(20), nullable=True) 