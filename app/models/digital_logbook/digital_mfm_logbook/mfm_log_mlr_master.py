from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMLogMLRMaster(Base):
    __tablename__ = "mfm_log_mlr_master"

    mfm_log_mlr_id = Column(Integer, primary_key=True, autoincrement=True)

    # Header
    station = Column(String(50), nullable=False)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
 
    # Header Details section
    tank_no = Column(String(50), nullable=True)
    hpcl_batch_no = Column(String(50), nullable=True)
    mrpl_batch_no = Column(String(50), nullable=True)
    pmhbl_batch_no = Column(String(50), nullable=True)
 
    product_name = Column(String(100), nullable=True)
    cycle_no = Column(String(50), nullable=True)
    tank_temp = Column(String(50), nullable=True)
    tank_factor = Column(String(50), nullable=True)
 
    flow_meter = Column(String(50), nullable=True)  # MRPL/MFM
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)