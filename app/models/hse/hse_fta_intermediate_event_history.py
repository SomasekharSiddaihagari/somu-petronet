from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class FTAIntermediateEventHistory(Base):
    __tablename__ = "fta_intermediate_event_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    intermediate_event_id = Column(Integer, nullable=True)
    top_event_id = Column(Integer, ForeignKey("fta_top_event.fta_top_id"), nullable=False)
    intermediate_e1=Column(String(500), nullable=True)
    intermediate_e2=Column(String(500), nullable=True)
    