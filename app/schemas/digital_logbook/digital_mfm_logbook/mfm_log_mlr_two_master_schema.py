from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class ERVLogMLRMaster(Base):
    __tablename__ = "mfm_log_mlr_master_two"
 
    mfm_log_mlr_two_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # Common Header
    station = Column(String(50), nullable=False)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
 
    # Header Details
    mrpl_qc_den_15c = Column(String(50), nullable=True)   # Kg/m3
    flash_point_fbp = Column(String(50), nullable=True)  # C
    kv = Column(String(50), nullable=True)
 
    ci = Column(String(50), nullable=True)
    ron_no = Column(String(50), nullable=True)
    cn = Column(String(50), nullable=True)
 
    mainline_pump_no = Column(String(50), nullable=True)   # 102-A/B/C
    booster_pump = Column(String(50), nullable=True)      # 101-A/B
 
    total_sulphur = Column(String(50), nullable=True)     # mg/kg
 
    created_at = Column(DateTime, server_default=func.now())