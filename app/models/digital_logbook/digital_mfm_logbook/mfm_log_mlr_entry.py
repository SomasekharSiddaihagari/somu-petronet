from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMLogMLREntry(Base):
    __tablename__ = "mfm_log_mlr_entry"
 
    mfm_log_mlr_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    master_id = Column(Integer, ForeignKey("mfm_log_mlr_master.mfm_log_mlr_id"), nullable=False)
 
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
 
    mrpl_dip = Column(String(50), nullable=True)
 
    # MFM Reading
    gross = Column(String(50), nullable=True)
    net = Column(String(50), nullable=True)
    mt = Column(String(50), nullable=True)
    den_at_nat = Column(String(50), nullable=True)
    temperature = Column(String(50), nullable=True)
    den_at_15_deg = Column(String(50), nullable=True)
 
    # Commulative
    mrpl_atg = Column(String(50), nullable=True)
    mrpl_mfm = Column(String(50), nullable=True)
 
    # Flow Rate
    mrpl_atg_flow = Column(String(50), nullable=True)
    mrpl_mfm_flow = Column(String(50), nullable=True)
 
    diff_in_percent = Column(String(50), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)