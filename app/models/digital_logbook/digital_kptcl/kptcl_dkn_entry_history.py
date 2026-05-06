from sqlalchemy import Column, Integer, Date, String, Time, Numeric, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class KPTCLDKNEntryHistory(Base):
    __tablename__ = "kptcl_dkn_entry_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    kptcl_dkn_entry_id = Column(Integer, nullable=True)
 
    master_id = Column(Integer, nullable=True)
 
    reading_date = Column(Date, nullable=True)
    reading_time = Column(Time, nullable=True)
 
    kwh = Column(Numeric(12, 2), nullable=True)
    kvah = Column(Numeric(12, 2), nullable=True)
    pf_meter = Column(Numeric(10, 4), nullable=True)
 
    calculated_pf_day = Column(String(50), nullable=True)
    calculated_pf_month = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)