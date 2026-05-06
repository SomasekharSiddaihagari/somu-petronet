from sqlalchemy import Column, Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
 
class LineWalkerEntry(Base):
    __tablename__ = "line_walker_entry"
 
    line_entry_id = Column(Integer, primary_key=True)
 
    line_walker_id = Column(
        Integer,
        ForeignKey("line_walker_master.line_walker_id", ondelete="CASCADE"),
        nullable=True
    )
 
    location_from = Column(String(100), nullable=True)
    location_to = Column(String(100), nullable=True)
 
    walker_name = Column(String(150), nullable=True)
 
    start_time = Column(Time, nullable=True)
    start_officer_initials = Column(String(50), nullable=True)
 
    end_time = Column(Time, nullable=True)
    end_officer_initials = Column(String(50), nullable=True)
 
    device_status = Column(String(100), nullable=True)
    remarks = Column(String(500), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)