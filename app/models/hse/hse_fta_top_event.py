from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class FTATopEvent(Base):
    __tablename__ = "fta_top_event"
 
    fta_top_id = Column(Integer, primary_key=True, autoincrement=True)
    hiim_id = Column(
        Integer,
        ForeignKey("hse_incident_investigation_master.hiim_id", ondelete="CASCADE"),
        nullable=False
    )
    event_description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
 
    