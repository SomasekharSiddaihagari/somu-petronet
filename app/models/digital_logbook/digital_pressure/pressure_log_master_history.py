from sqlalchemy import (
    Column, Integer, String, Date, Time, DateTime, Boolean
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class PressureLogMasterHistory(Base):
    __tablename__ = "pressure_log_master_history"
 
    history_id = Column(Integer, primary_key=True,autoincrement=True)
 
    pressure_id = Column(Integer, nullable=True)
    ms_logbook_id = Column(Integer, nullable=True)
    technician_id = Column(Integer, nullable=True)
 
    logbook_ref_no = Column(String(100), nullable=True)
    station_name = Column(String(100), nullable=True)
    station_incharge = Column(String(100), nullable=True)
 
    shift = Column(String(10), nullable=True)
    log_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)
 
    # Shift A
    shift_a_technician_name = Column(String(100), nullable=True)
    shift_a_technician_signature = Column(String(255), nullable=True)
    shift_a_engineer_name = Column(String(100), nullable=True)
    shift_a_engineer_signature = Column(String(255), nullable=True)
 
    # Shift B
    shift_b_technician_name = Column(String(100), nullable=True)
    shift_b_technician_signature = Column(String(255), nullable=True)
    shift_b_engineer_name = Column(String(100), nullable=True)
    shift_b_engineer_signature = Column(String(255), nullable=True)
 
    # Shift C
    shift_c_technician_name = Column(String(100), nullable=True)
    shift_c_technician_signature = Column(String(255), nullable=True)
    shift_c_engineer_name = Column(String(100), nullable=True)
    shift_c_engineer_signature = Column(String(255), nullable=True)
    
 
    is_closed = Column(Boolean, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)