from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Time
from sqlalchemy.sql import func
from app.database import Base
 
 
class LineWalkerMasterHistory(Base):
    __tablename__ = "line_walker_master_history"
 
    history_id = Column(Integer, primary_key=True)
    ms_logbook_id = Column(Integer, nullable=True)
    station_name = Column(String(100), nullable=True)
    line_walker_id = Column(Integer, nullable=True)
    station_incharge_name = Column(String(150), nullable=True)
    shift_start_time = Column(Time, nullable=True)
    shift_name = Column(String(10), nullable=True)
    reporting_location = Column(String(200), nullable=True)
    report_date = Column(Date, nullable=True)
    log_date = Column(Date, nullable=True)
    station_incharge_signature = Column(String(200), nullable=True)
    critical_report = Column(Text, nullable=True)


    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)