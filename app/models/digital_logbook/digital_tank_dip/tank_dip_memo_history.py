from sqlalchemy import Column, Integer, String, Date, Time, Float, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class TankDipMemoHistory(Base):
    __tablename__ = "tank_dip_memo_history"
 
    history_id = Column(Integer, primary_key=True,autoincrement=True)
 
    tank_id = Column(Integer, nullable=True)
    document_no = Column(String(100), nullable=True)
    station_name = Column(String(100), nullable=True)
    station_incharge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    status = Column(String(50), nullable=True)
 
    tank_no = Column(String(50), nullable=True)
    company = Column(String(100), nullable=True)
    product = Column(String(100), nullable=True)
    memo_no = Column(String(50), nullable=True)
 
    mrpl_batch_no = Column(String(100), nullable=True)
    pmhbl_batch_no = Column(String(100), nullable=True)
    before_after_mrpl = Column(String(50), nullable=True)
 
    dip_time = Column(Time, nullable=True)
    dip_date = Column(Date, nullable=True)
 
    ref_height_cm = Column(Float, nullable=True)
    ullage_at_natural = Column(Float, nullable=True)
    gross_dip_cm = Column(Float, nullable=True)
    dip_of_water_mm = Column(Float, nullable=True)
 
    temp_top = Column(Float, nullable=True)
    temp_middle = Column(Float, nullable=True)
    temp_bottom = Column(Float, nullable=True)
    temp_average = Column(Float, nullable=True)
    tank_temp = Column(Float, nullable=True)
 
    density_top = Column(Float, nullable=True)
    density_middle = Column(Float, nullable=True)
    density_bottom = Column(Float, nullable=True)
    density_average = Column(Float, nullable=True)
    density_tank = Column(Float, nullable=True)
 
    density_at_15c = Column(Float, nullable=True)
 
    settling_time_pmhbl = Column(Float, nullable=True)
    settling_time_hpcl = Column(Float, nullable=True)
    settling_time_bpcl_iocl = Column(Float, nullable=True)
 
    entered_by_name = Column(String(100), nullable=True)
    entered_date = Column(Date, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)
    before_after_mrpl_qty = Column(String(50), nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)