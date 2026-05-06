from sqlalchemy import Column, ForeignKey, ForeignKey, Integer, String, Date, Time, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 

class HSEIncidentFTAEventsHistory(Base):
    __tablename__ = "hse_incident_fta_events_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    fta_id = Column(
        Integer,
        nullable=True
    )
    incident_id = Column(
        Integer,
        nullable=True
    )
 
    event_type = Column(String(50), nullable=True)  
    # TopEvent / IntermediateEvent / BasicEvent
 
    event_code = Column(String(50), nullable=True)  # IE1, B1, etc
    description = Column(Text, nullable=True)