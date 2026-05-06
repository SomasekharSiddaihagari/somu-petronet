from sqlalchemy import Column, ForeignKey, ForeignKey, Integer, String, Date, Time, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()

class HSEIncidentRCA5Why(Base):
    __tablename__ = "hse_incident_rca_5why"
 
    rca_id = Column(Integer, primary_key=True, autoincrement=True)
 
    hiim_id = Column(
        Integer,
        ForeignKey("hse_incident_investigation_master.hiim_id", ondelete="CASCADE"),
        nullable=False
    )
 
    why1 = Column(Text, nullable=True)
    why2 = Column(Text, nullable=True)
    why3 = Column(Text, nullable=True)
    why4 = Column(Text, nullable=True)
    why5_root_cause = Column(Text, nullable=True)

    