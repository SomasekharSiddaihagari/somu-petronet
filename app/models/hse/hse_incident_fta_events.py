from sqlalchemy import Column, ForeignKey, ForeignKey, Integer, String, Date, Time, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 

class HSEIncidentFTAEvents(Base):
    __tablename__ = "hse_incident_fta_events"
 
    fta_id = Column(Integer, primary_key=True, autoincrement=True)
 
    incident_id = Column(
        Integer,
        ForeignKey("hse_incident_investigation_master.hiim_id", ondelete="CASCADE"),
        nullable=False
    )
 
    event_type = Column(String(50), nullable=True)  
    # TopEvent / IntermediateEvent / BasicEvent
 
    event_code = Column(String(50), nullable=True)  # IE1, B1, etc
    description = Column(Text, nullable=True)