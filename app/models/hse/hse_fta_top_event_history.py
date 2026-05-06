from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class FTATopEventHistory(Base):
    __tablename__ = "fta_top_event_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    fta_top_id = Column(Integer, nullable=True)
    event_description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
