from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class PressureLogEntryHistory(Base):
    __tablename__ = "pressure_log_entry_history"
 
    history_id = Column(Integer, primary_key=True,autoincrement=True)
 
    # Reference fields (NO FK)
    pressure_entry_id = Column(Integer, nullable=True)
    pressure_id = Column(Integer, nullable=True)
 
    # Entry data
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
 
    mangalore = Column(String(50), nullable=True)
    sv1 = Column(String(50), nullable=True)
    sv2 = Column(String(50), nullable=True)
    sv3 = Column(String(50), nullable=True)
 
    neriya = Column(String(50), nullable=True)
    sv4 = Column(String(50), nullable=True)
    sv5 = Column(String(50), nullable=True)
 
    hassan = Column(String(50), nullable=True)
    sv6 = Column(String(50), nullable=True)
    sv7 = Column(String(50), nullable=True)
    sv8 = Column(String(50), nullable=True)
 
    ip = Column(String(50), nullable=True)
    sv9 = Column(String(50), nullable=True)
    sv10 = Column(String(50), nullable=True)
 
    bangalore = Column(String(50), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)