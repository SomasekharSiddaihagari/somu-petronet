from sqlalchemy import Column, Integer, String, Date, Time, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class NPTReportMaster(Base):
    __tablename__ = "npt_report_master_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    npt_id = Column(Integer, nullable=True)
    technician_id = Column(Integer, nullable=True)

    # ----------------------------
    # LOGBOOK HEADER
    # ----------------------------
    station = Column(String(100), nullable=True)            # Hassan
    station_id = Column(Integer, nullable=True)
    station_in_charge = Column(String(100), nullable=True) # Rajesh Kumar
    shift = Column(String(50), nullable=True)               # Shift A
    start_time = Column(Time, nullable=True)                # 04:13
    logbook_date = Column(Date, nullable=True)              # 28-12-2025
    ms_logbook_id = Column(Integer, nullable=True)
    action_type = Column(String(20), nullable=True)
 
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