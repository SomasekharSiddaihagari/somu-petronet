from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey,
    Text, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
class SafetyCommitteeMinutes(Base):
    __tablename__ = "safety_committee_minutes"
 
    scmm_id = Column(Integer, primary_key=True, index=True)
    meeting_no = Column(String(100), nullable=False)
    location = Column(String(255))
    frequency = Column(String(100))
    meeting_date = Column(Date)
    next_meeting = Column(String(255))
    remarks = Column(Text, nullable=True)
    station_id = Column(Integer, nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
    # ✅ prevent duplicate meeting numbers
    __table_args__ = (
        UniqueConstraint("meeting_no", name="uq_scmm_meeting_no"),
    )
 
    # 🔥 relationships
    members = relationship(
        "SafetyCommitteeMinutesMember",
        back_populates="minutes",
        cascade="all, delete-orphan",
    )
 
    discussions = relationship(
        "SafetyCommitteeMinutesDiscussion",
        back_populates="minutes",
        cascade="all, delete-orphan",
    )
 
    incidents = relationship(
        "SafetyCommitteeMinutesIncident",
        back_populates="minutes",
        cascade="all, delete-orphan",
    )