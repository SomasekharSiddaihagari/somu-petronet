from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
 
class SafetyCommitteeMember(Base):
    __tablename__ = "safety_committee_members"
 
    scm_id = Column(Integer, primary_key=True, autoincrement=True)
 
    sl_no = Column(Integer, nullable=True)
 
    name = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    station = Column(Integer, nullable=True)
 
    is_active = Column(Boolean, nullable=True)
    user_id = Column(Integer, index=True, nullable=True)
 
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