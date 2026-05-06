from sqlalchemy import Column, Float, Integer, String, Date, Time, DateTime, Text, Numeric
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMLogHSNMaster(Base):
    __tablename__ = "mfm_log_hsn_master"
 
    mfm_log_hsn_id = Column(Integer, primary_key=True,autoincrement=True)
 
    station = Column(String(50), default="HSN")
    station_in_charge = Column(String(100))
    shift = Column(String(10))
    start_time = Column(Time)
    log_date = Column(Date)
    document_no = Column(String(100))
    
    left_initial_tank_no = Column(String(50), nullable=True)
    left_initial_dip_in_cms = Column(Float, nullable=True)
    left_tank_co_time = Column(Time, nullable=True)
 
    left_final_tank_dip_in_cms = Column(Float, nullable=True)
    left_new_tank_initial_dip_in_cm = Column(Float, nullable=True)
    left_new_tank_no = Column(String(50), nullable=True)
 
    left_co_fm_reading_gross = Column(Float, nullable=True)
    left_co_fm_reading_nett = Column(Float, nullable=True)
    left_co_fm_reading_mass = Column(Float, nullable=True)
 
    # ----------------------------
    # LEFT SECTION (SECOND BLOCK)
    # ----------------------------
    left2_initial_tank_no = Column(String(50), nullable=True)
    left2_initial_dip_in_cms = Column(Float, nullable=True)
    left2_tank_co_time = Column(Time, nullable=True)
 
    left2_final_tank_dip_in_cms = Column(Float, nullable=True)
    left2_new_tank_initial_dip_in_cm = Column(Float, nullable=True)
    left2_new_tank_no = Column(String(50), nullable=True)
 
    left2_co_fm_reading_gross = Column(Float, nullable=True)
    left2_co_fm_reading_nett = Column(Float, nullable=True)
    left2_co_fm_reading_mass = Column(Float, nullable=True)
 
    # ----------------------------
    # RIGHT SECTION
    # ----------------------------
    right_initial_tank_no = Column(String(50), nullable=True)
    right_initial_dip_in_cms = Column(Float, nullable=True)
    right_tank_co_time = Column(Time, nullable=True)
 
    right_final_tank_dip_in_cms = Column(Float, nullable=True)
    right_new_tank_initial_dip_in_cm = Column(Float, nullable=True)
    right_new_tank_no = Column(String(50), nullable=True)
 
    right_co_fm_reading_gross = Column(Float, nullable=True)
    right_co_fm_reading_nett = Column(Float, nullable=True)
    right_co_fm_reading_mass = Column(Float, nullable=True)
 
    # ----------------------------
    # FM CHANGED SECTION
    # ----------------------------
    faq_changed_from = Column(String(50), nullable=True)
    faq_changed_to = Column(String(50), nullable=True)
    faq_changed_at = Column(Time, nullable=True)
 
    # ----------------------------
    # FMR READINGS
    # ----------------------------
    initial_fmr_g = Column(Float, nullable=True)
    initial_fmr_n = Column(Float, nullable=True)
    initial_fmr_m = Column(Float, nullable=True)
 
    final_fmr_g = Column(Float, nullable=True)
    final_fmr_n = Column(Float, nullable=True)
    final_fmr_m = Column(Float, nullable=True)
 
    # ----------------------------
    # STATION
    # ----------------------------
    sic_name = Column(String(100), nullable=True)

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
    created_at = Column(DateTime, server_default=func.now())