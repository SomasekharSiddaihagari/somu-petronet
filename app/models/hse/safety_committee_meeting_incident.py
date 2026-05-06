from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
# from database import Base
Base = declarative_base()

class SafetyCommitteeMinutesIncident(Base):

    __tablename__ = "safety_committee_minutes_incidents"
 
    scmi_id = Column(Integer, primary_key=True, index=True)
 
    scmm_id = Column(

        Integer,

        ForeignKey("safety_committee_minutes.scmm_id", ondelete="CASCADE"),

        nullable=False,

    )
 
    incident_id = Column(Integer, nullable=False)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    minutes = relationship(

        "SafetyCommitteeMinutes",

        back_populates="incidents",

    )
 