from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
# from database import Base
Base = declarative_base()

class SafetyCommitteeMinutesIncidentHistory(Base):

    __tablename__ = "safety_committee_minutes_incidents_history"
    history_id = Column(Integer, primary_key=True, index=True)
    scmi_id = Column(Integer, nullable=True)  # 🔥 store original incident ID for reference
 
    scmm_id = Column(Integer, nullable=True)
 
    incident_id = Column(Integer, nullable=False)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    minutes = relationship(

        "SafetyCommitteeMinutes",

        back_populates="incidents",

    )
