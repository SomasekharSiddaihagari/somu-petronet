from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
 
class ERVLogMLREntry(Base):
    __tablename__ = "mfm_log_mlr_two_entry"
 
    mfm_log_mlr_two_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    master_id = Column(Integer, ForeignKey("mfm_log_mlr_two_master.mfm_log_mlr_two_id"), nullable=False)
 
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
 
    pump_disch_hdr_press_1108 = Column(String(50), nullable=True)
    pump_inlet_press_1104 = Column(String(50), nullable=True)
    press_after_pcv_1110 = Column(String(50), nullable=True)
    pcv_open_percent = Column(String(50), nullable=True)
 
    water_temp = Column(String(50), nullable=True)
 
    mtr_de_nde_casing_temp_1 = Column(String(50), nullable=True)
    pump_de_nde_vibration_1 = Column(String(50), nullable=True)
    thrust_brg_xy = Column(String(50), nullable=True)
 
    water_temp_2 = Column(String(50), nullable=True)
 
    mtr_de_nde_casing_temp_2 = Column(String(50), nullable=True)
    pump_de_vibration_xy = Column(String(50), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)