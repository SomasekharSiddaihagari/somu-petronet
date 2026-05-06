from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class LineWalkerMaster(Base):
    __tablename__ = "line_walker_master"
 
    line_walker_id = Column(Integer, primary_key=True)
    ms_logbook_id = Column(Integer, nullable=True)
    document_no = Column(String(50), nullable=True)
    station_name = Column(String(100), nullable=True)
    station_incharge_name = Column(String(150), nullable=True)
    shift_name = Column(String(20), nullable=True)
    shift_start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)

    reporting_location = Column(String(200), nullable=True)
    critical_report = Column(Text, nullable=True)
    station_incharge_signature = Column(String(200), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)