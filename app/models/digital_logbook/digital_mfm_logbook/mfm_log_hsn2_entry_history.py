from sqlalchemy import Column, Float, Integer, String, Date, Time, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMLogHSN2EntryHistory(Base):
    __tablename__ = "mfm_log_hsn2_entry_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    mfm_log_hsn2_entry_id = Column(Integer, nullable=True)
    master_id = Column(Integer, nullable=False)
 
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
 
    # Pump & pressure
    pump_inlet_header_pr = Column(String(50), nullable=True)
    pump_outlet_header_pr = Column(String(50), nullable=True)
    digital_fcva_opening = Column(String(50), nullable=True)
 
    # Flow rate
    flow_rate_net = Column(String(50), nullable=True)
    flow_rate_gross = Column(String(50), nullable=True)
 
    # Volume readings
    gross_vol_fqy = Column(String(50), nullable=True)
    gross_qty_per_gross = Column(String(50), nullable=True)
 
    nett_vol_fqy = Column(String(50), nullable=True)
    nett_qty_per_gross = Column(String(50), nullable=True)
 
    mass_vol_fqy = Column(String(50), nullable=True)
    qty_delivered_mt = Column(String(50), nullable=True)
 
    # Product sample
    density = Column(String(50), nullable=True)
    temperature = Column(String(50), nullable=True)
    density_15_deg = Column(String(50), nullable=True)
 
    # Tank & line details
    tank_corr_during_cm = Column(float, nullable=True)
    ci_pump = Column(String(50), nullable=True)
    ci_line_pr = Column(float, nullable=True)
    stroke_len = Column(float, nullable=True)
    ci_dosing_rate = Column(float, nullable=True)
    sign_of_shift_ie = Column(String(100), nullable=True)
    remarks = Column(Text, nullable=True)
 

    b_left_initial_tank_no = Column(String(50), nullable=True)
    b_left_initial_dip_in_cms = Column(Float, nullable=True)
    b_left_tank_co_time = Column(Time, nullable=True)
 
    b_left_final_tank_dip_in_cms = Column(Float, nullable=True)
    b_left_new_tank_initial_dip_in_cm = Column(Float, nullable=True)
    b_left_new_tank_no = Column(String(50), nullable=True)

    b_left_co_fm_reading_gross = Column(Float, nullable=True)
    b_left_co_fm_reading_nett = Column(Float, nullable=True)
    b_left_co_fm_reading_mass = Column(Float, nullable=True)
 
    # ----------------------------
    # LEFT SECTION (SECOND BLOCK)
    # ----------------------------
    b_left2_initial_tank_no = Column(String(50), nullable=True)
    b_left2_initial_dip_in_cms = Column(Float, nullable=True)
    b_left2_tank_co_time = Column(Time, nullable=True)

    b_left2_final_tank_dip_in_cms = Column(Float, nullable=True)
    b_left2_new_tank_initial_dip_in_cm = Column(Float, nullable=True)
    b_left2_new_tank_no = Column(String(50), nullable=True)

    b_left2_co_fm_reading_gross = Column(Float, nullable=True)
    b_left2_co_fm_reading_nett = Column(Float, nullable=True)
    b_left2_co_fm_reading_mass = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)