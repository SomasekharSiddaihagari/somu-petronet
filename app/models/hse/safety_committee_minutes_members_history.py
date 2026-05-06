from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
class SafetyCommitteeMinutesMemberHistory(Base):
    __tablename__ = "safety_committee_minutes_members_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    scmm_id = Column(Integer, nullable=True)
    minutes_id = Column(
        Integer,
        ForeignKey("safety_committee_minutes.scmm_id"),
        nullable=True,
    )
    
    member_name = Column(String(150), nullable=True)
    user_id = Column(Integer, index=True, nullable=True)
 
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )