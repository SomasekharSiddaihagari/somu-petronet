from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class ERVLogMLRMasterHistory(Base):
    __tablename__ = "mfm_log_mlr_master_two_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    mfm_log_mlr_two_id = Column(Integer, nullable=False)
 
    station = Column(String(50), nullable=False)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
 
    mrpl_qc_den_15c = Column(String(50), nullable=True)
    flash_point_fbp = Column(String(50), nullable=True)
    kv = Column(String(50), nullable=True)
 
    ci = Column(String(50), nullable=True)
    ron_no = Column(String(50), nullable=True)
    cn = Column(String(50), nullable=True)
 
    mainline_pump_no = Column(String(50), nullable=True)
    booster_pump = Column(String(50), nullable=True)
 
    total_sulphur = Column(String(50), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)