from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
class DailySamplingMaster(Base):
    __tablename__ = "daily_sampling_master"
 
    sampling_id = Column(Integer, primary_key=True, autoincrement=True)
    document_number = Column(String(50), nullable=True)
    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
    status = Column(String(30), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)