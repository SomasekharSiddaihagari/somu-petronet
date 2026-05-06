from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class FireEngineTestMaster(Base):
    __tablename__ = "fire_engine_test_master"
 
    fire_id = Column(Integer, primary_key=True, autoincrement=True)
    document_number = Column(String(100), nullable=True)
    station_name = Column(String(100), nullable=True)
    station_incharge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
    ms_logbook_id = Column(Integer, nullable=True)
    technician_id = Column(Integer, nullable=True)
    technician_name = Column(String(100), nullable=True)
    technician_signature = Column(Text, nullable=True)
 
    engineer_name = Column(String(100), nullable=True)
    engineer_signature = Column(Text, nullable=True)
 
    status = Column(String(50), nullable=True)  # DRAFT / SUBMITTED

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)