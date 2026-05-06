from sqlalchemy import Column, Integer, String, Date, Time, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class VibrationTemperatureMaster(Base):
    __tablename__ = "vibration_temperature_master_mlr_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    vtm_id = Column(Integer, nullable=True)

    # ----------------------------
    # ERV / LOGBOOK HEADER
    # ----------------------------
    station = Column(String(100), nullable=True)            # Mangalore
    station_in_charge = Column(String(100), nullable=True) # Rajesh Kumar
    shift = Column(String(50), nullable=True)               # Shift A
    start_time = Column(Time, nullable=True)                # 04:13
    logbook_date = Column(Date, nullable=True)              # 28-12-2025
 
    # ----------------------------
    # SHIFT SIGNATURE SECTION
    # ----------------------------
    shift_engineer_a_name = Column(String(100), nullable=True)
    shift_engineer_a_signature = Column(String(255), nullable=True)
 
    shift_engineer_b_name = Column(String(100), nullable=True)
    shift_engineer_b_signature = Column(String(255), nullable=True)

    shift_engineer_c_name = Column(String(100), nullable=True)
    shift_engineer_c_signature = Column(String(255), nullable=True)

    
    technician_a_name = Column(String(100), nullable=True)
    technician_a_id = Column(Integer, nullable=True)
  

    technician_b_name = Column(String(100), nullable=True)
    technician_b_id = Column(Integer, nullable=True)
   
    
    technician_c_name = Column(String(100), nullable=True)
    technician_c_id = Column(Integer, nullable=True)
    technician_c_signature = Column(String(255), nullable=True)
 
    # ----------------------------
    # SYSTEM
    # ----------------------------
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)