from sqlalchemy import Column, Integer, Date, Time, Float, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class DG250KVAEntryHistory(Base):
    __tablename__ = "dg_250kva_entry_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    dg_entry_id = Column(Integer, nullable=True)
    master_ref_id = Column(Integer, nullable=True)
 
    log_date = Column(Date, nullable=True)
    start_time = Column(DateTime, nullable=True)
    stop_time = Column(DateTime, nullable=True)
    run_time = Column(String(20), nullable=True)
 
    cumulative = Column(Float, nullable=True)
    hmr = Column(Float, nullable=True)
    battery_voltage = Column(Float, nullable=True)
    lube_oil_pressure = Column(Float, nullable=True)
    rpm = Column(Float, nullable=True)
    electrical_hmr = Column(Float, nullable=True)
    water_temperature = Column(Float, nullable=True)
 
    voltage_load = Column(Float, nullable=True)
    voltage_ry = Column(Float, nullable=True)
    voltage_yb = Column(Float, nullable=True)
    voltage_br = Column(Float, nullable=True)
 
    current_r = Column(Float, nullable=True)
    current_y = Column(Float, nullable=True)
    current_b = Column(Float, nullable=True)
 
    kwh_initial = Column(Float, nullable=True)
    kwh_final = Column(Float, nullable=True)
    kwh_consumed = Column(Float, nullable=True)
    kwh_cumulative = Column(Float, nullable=True)
 
    diesel_initial = Column(Float, nullable=True)
    diesel_final = Column(Float, nullable=True)
    diesel_consumed = Column(Float, nullable=True)
    diesel_total = Column(Float, nullable=True)
 
    remarks = Column(String(500), nullable=True)
    signature = Column(String(100), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)