from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class MFMLogNERMaster(Base):
    __tablename__ = "mfm_log_ner_master"
 
    mfm_log_ner_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # Header
    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
 
    # Bottom Electrical / Power / Battery / DG Fields (from UI)
    psp = Column(Float, nullable=True)
 
    dc_voltage_op = Column(Float, nullable=True)
    dc_current_op = Column(Float, nullable=True)
 
    cp_charger = Column(String(50), nullable=True)
 
    cp_ac_ip_voltage = Column(Float, nullable=True)
    cp_ac_ip_current = Column(Float, nullable=True)
 
    cp_dc_op_voltage = Column(Float, nullable=True)
    cp_dc_op_current = Column(Float, nullable=True)
    

    cp_battery_cell_voltage = Column(Float, nullable=True)
    cp_battery_earth_leak = Column(Float, nullable=True)
 
    telecom_charger = Column(String(50), nullable=True)
    
    ac_ip_voltage_telecom = Column(Float, nullable=True)
    ac_ip_current_telecom = Column(Float, nullable=True)
    telecom_charger_dc_op_voltage = Column(Float, nullable=True)
    telecom_charger_dc_op_current = Column(Float, nullable=True)
    

    telecom_charger_battery_cell_voltage = Column(Float, nullable=True)
    telecom_charger_battery_earth_leak = Column(Float, nullable=True)
    kva_dg = Column(Float, nullable=True)

    dg_ltrs = Column(Float, nullable=True)
    
    sv3_import = Column(Float, nullable=True)
    sv3_export = Column(Float, nullable=True)
    sv3_dg_ltrs = Column(Float, nullable=True)
    sv3_neriya_station = Column(String(100), nullable=True)
    sv3_kwh = Column(Float, nullable=True)
    sv3_kvarh = Column(Float, nullable=True)
    sv3_pf = Column(Float, nullable=True)
    sv3_psp = Column(Float, nullable=True)
    sv3_volt = Column(Float, nullable=True)
    sv3_curr = Column(Float, nullable=True)
    sv3_tc = Column(Float, nullable=True)
    sv3_fwt_level = Column(Float, nullable=True)
    sv3_fwt_1 = Column(Float, nullable=True)
    sv3_fwt_2 = Column(Float, nullable=True)
    sv3_dg_ltrs_2 = Column(Float, nullable=True)
 
    # ---------- SV-4 ----------
    sv4_import = Column(Float, nullable=True)
    sv4_export = Column(Float, nullable=True)
    sv4_dg_ltrs = Column(Float, nullable=True)
    sv4_neriya_station = Column(String(100), nullable=True)
    sv4_kwh = Column(Float, nullable=True)
    sv4_kvarh = Column(Float, nullable=True)
    sv4_pf = Column(Float, nullable=True)
    sv4_psp = Column(Float, nullable=True)
    sv4_volt = Column(Float, nullable=True)
    sv4_curr = Column(Float, nullable=True)
    sv4_tc = Column(Float, nullable=True)
    sv4_fwt_level = Column(Float, nullable=True)
    sv4_fwt_1 = Column(Float, nullable=True)
    sv4_fwt_2 = Column(Float, nullable=True)
    sv4_dg_ltrs_2 = Column(Float, nullable=True)
    # Metadata
    remarks = Column(Text, nullable=True)
    status = Column(String(20), nullable=True)
 
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)