from sqlalchemy import Column, Integer, String, Date, Time, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
class MFMShutdownDetail(Base):
    __tablename__ = "mfm_shutdown_detail_dkn"
 
    mfm_shutdown_id = Column(Integer, primary_key=True, autoincrement=True)
    master_id = Column(Integer, ForeignKey("mfm_log_master.mfm_log_dkn_id"), nullable=True)
 
   
    from_time = Column(Time, nullable=True)
    to_time = Column(Time, nullable=True)
    reason = Column(Text, nullable=True)
 
    kwh = Column(Float, nullable=True)
    kvah = Column(Float, nullable=True)
    pf = Column(Float, nullable=True)
    
    psd_time_from = Column(Time, nullable=True)
    psd_time_to = Column(Time, nullable=True)
    psd_cul_daily = Column(Float, nullable=True)
    psd_cul_monthly = Column(Float, nullable=True)

    dg_from = Column(Time, nullable=True)
    dg_to = Column(Time, nullable=True)
 
    engery_meter_reading = Column(Float, nullable=True)
    hours_meter = Column(Float, nullable=True)

    tank1 = Column(Float, nullable=True)
    tank2 = Column(Float, nullable=True)
    tank3 = Column(Float, nullable=True)
    
    fw1 = Column(Float, nullable=True)
    fw2 = Column(Float, nullable=True)
    fw3 = Column(Float, nullable=True)
    fw4 = Column(Float, nullable=True)
    fw5 = Column(Float, nullable=True)

    # prevcumrunhour = Column(int, nullable=True)
    # cummrunhour = Column(int, nullable=True)    
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)