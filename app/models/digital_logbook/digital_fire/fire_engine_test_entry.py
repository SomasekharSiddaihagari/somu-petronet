from sqlalchemy import Column, Integer, String, Date, Time, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
 
class FireEngineTestEntry(Base):
    __tablename__ = "fire_engine_test_entry"
 
    fire_entry_id = Column(Integer, primary_key=True, autoincrement=True)
 
    master_id = Column(
        Integer,
        ForeignKey("fire_engine_test_master.fire_id", ondelete="CASCADE"),
        nullable=True
    )
 
    entry_date = Column(Date, nullable=True)
    fire_engine_no = Column(String(50), nullable=True)
 
    time_start = Column(Time, nullable=True)
    time_stop = Column(Time, nullable=True)
    running_hours = Column(Float, nullable=True)
 
    battery_voltage = Column(String(20), nullable=True)
    lube_oil_level = Column(String(20), nullable=True)
    fuel_level_lts = Column(Float, nullable=True)
    radiator_water_level = Column(String(20), nullable=True)
 
    lube_oil_temp = Column(Float, nullable=True)
    lube_oil_pressure = Column(Float, nullable=True)
 
    fwt_1 = Column(Float, nullable=True)
    fwt_2 = Column(Float, nullable=True)
    fwt_3 = Column(Float, nullable=True)
 
    cooling_water_temp = Column(Float, nullable=True)
    rpm = Column(Integer, nullable=True)
 
    mode_of_test = Column(String(50), nullable=True)
 
    tech_sign = Column(String(100), nullable=True)
    engg_sign = Column(String(100), nullable=True)
 
    remarks = Column(Text, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)