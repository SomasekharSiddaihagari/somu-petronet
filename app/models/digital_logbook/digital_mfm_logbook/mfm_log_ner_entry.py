from sqlalchemy import Column, Integer, String, Date, Time, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class MFMLogNEREntry(Base):
    __tablename__ = "mfm_log_ner_entry"
 
    mfm_log_ner_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    master_id = Column(Integer, ForeignKey("mfm_log_ner_master.mfm_log_ner_id"), nullable=True)
 
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
    
    entry_date_two = Column(Date, nullable=True)
    entry_time_two = Column(Time, nullable=True)

    product = Column(String(100), nullable=True)
    batch = Column(String(100), nullable=True)
 
    density = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
 
    pump_abc = Column(String(50), nullable=True)
    lube_oil_pressure = Column(Float, nullable=True)
    lube_oil_diff_pressure = Column(Float, nullable=True)
    diff_basket_filter_ab = Column(Float, nullable=True)
 
    fmr_gross = Column(Float, nullable=True)
    fmr_net = Column(Float, nullable=True)
    fmr_mass = Column(Float, nullable=True)
 
    flow_rate_net = Column(Float, nullable=True)
    flow_rate_mass = Column(Float, nullable=True)
 
    pcv_percent = Column(Float, nullable=True)
 
    ic_voltage_1 = Column(Float, nullable=True)
    ic_voltage_2 = Column(Float, nullable=True)
 
    load_current_r = Column(Float, nullable=True)
    load_current_y = Column(Float, nullable=True)
    load_current_b = Column(Float, nullable=True)
 
    frequency = Column(Float, nullable=True)
    load_percent = Column(Float, nullable=True)
 
    remarks = Column(Text, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)