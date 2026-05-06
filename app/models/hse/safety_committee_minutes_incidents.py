from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey,
    Text, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()






class SafetyCommitteeMinutesIncident(Base):
 
    __tablename__ = "safety_committee_minutes_incidents"
 
    scmi_id = Column(Integer, primary_key=True, autoincrement=True)
 
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