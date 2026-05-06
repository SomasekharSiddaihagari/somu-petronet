from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class DG250KVAMaster(Base):
    __tablename__ = "dg_250kva_master"

    dg_id = Column(Integer, primary_key=True, autoincrement=True)
    ms_logbook_id = Column(Integer, nullable=True)
    technician_id = Column(Integer, nullable=True)

    station = Column(String(50), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(10), nullable=True)
    start_time = Column(Time, nullable=True)
    entry_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=True)
    document_number = Column(String(100), nullable=True)
    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)