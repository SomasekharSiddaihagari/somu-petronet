from sqlalchemy import Column, Integer, String, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class SupervisorEntryHistory(Base):
    __tablename__ = "supervisor_entry_history"
 
    history_id = Column(Integer, primary_key=True)
 
    sup_entry_id = Column(Integer, nullable=True)
    line_walker_id = Column(Integer, nullable=True)
 
    sl_no = Column(Integer, nullable=True)
    spread = Column(String(100), nullable=True)
    supervisor_name = Column(String(150), nullable=True)
 
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
 
    area_of_visit = Column(String(300), nullable=True)
    report = Column(String(500), nullable=True)
    officer_initials = Column(String(50), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)