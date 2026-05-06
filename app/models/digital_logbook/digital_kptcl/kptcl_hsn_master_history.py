from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Numeric
from sqlalchemy.sql import func
from app.database import Base
 
 
class KPTCLHSNMasterHistory(Base):
    __tablename__ = "kptcl_hsn_master_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    kptcl_hsn_id = Column(Integer, nullable=True)
    ms_logbook_id = Column(Integer, nullable=True)
    station_name = Column(String(100), nullable=True)
    station_incharge = Column(String(150), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
    document_number = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)
 
    billing_kwh_rdg = Column(Numeric(14, 3), nullable=True)
    billing_kvah_rdg = Column(Numeric(14, 3), nullable=True)
    monthly_avg_pf = Column(Numeric(10, 4), nullable=True)
    monthly_avg_kva = Column(Numeric(14, 3), nullable=True)
    technician_id = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)