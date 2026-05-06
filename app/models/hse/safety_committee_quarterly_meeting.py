from sqlalchemy import Column, Integer, String, Date, Time, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class SafetyCommitteeMeeting(Base):
    __tablename__ = "safety_committee_quarterly_meetings"
 
    scm_id = Column(Integer, primary_key=True, autoincrement=True)
 
 
 
    location = Column(String(150), nullable=True)
    meeting_date = Column(Date, nullable=True)
    meeting_time = Column(Time, nullable=True)
 
    is_active = Column(Boolean, nullable=True)
 
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
 
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )