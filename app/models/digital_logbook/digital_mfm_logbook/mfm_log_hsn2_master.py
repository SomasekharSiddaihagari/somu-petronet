from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMLogHSN2Master(Base):
    __tablename__ = "mfm_log_hsn2_master"
 
    mfm_hsn_two_id = Column(Integer, primary_key=True, autoincrement=True)
 
    station = Column(String(50), nullable=False)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
 
    # Footer / summary section
    fqy_changed_from = Column(String(50), nullable=True)
    fqy_changed_to = Column(String(50), nullable=True)
    fqy_changed_at = Column(Time, nullable=True)

    initial_fmr_of = Column(String(20), nullable=True)
    final_fmr = Column(String(20), nullable=True)
 
    initial_fmr_g = Column(String(20), nullable=True)
    initial_fmr_n = Column(String(20), nullable=True)
    initial_fmr_m = Column(String(20), nullable=True)
 
    final_fmr_g = Column(String(20), nullable=True)
    final_fmr_n = Column(String(20), nullable=True)
    final_fmr_m = Column(String(20), nullable=True)
 
    sic_name = Column(String(100), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)