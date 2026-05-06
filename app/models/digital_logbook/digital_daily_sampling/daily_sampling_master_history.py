from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
class DailySamplingMasterHistory(Base):
    __tablename__ = "daily_sampling_master_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    sampling_id = Column(Integer, nullable=True)
    document_number = Column(String(50), nullable=True)
    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
    status = Column(String(30), nullable=True)
    ms_logbook_id = Column(Integer, nullable=True)
    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)
    temperature = Column(String(50), nullable=True)