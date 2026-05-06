from sqlalchemy import Column, Integer, String, Date, Time, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class ErvMasterLogbook(Base):
    __tablename__ = "erv_logbook_master"
 
    erv_id = Column(Integer, primary_key=True, autoincrement=True)
    technician_id = Column(Integer, nullable=True)

    station = Column(String(100), nullable=True)            
    shift_in_charge = Column(String(100), nullable=True) 
    shift = Column(String(50), nullable=True)               
    start_time = Column(Time, nullable=True)                
    logbook_date = Column(Date, nullable=True)              
    ms_logbook_id = Column(Integer, nullable=True)
    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)