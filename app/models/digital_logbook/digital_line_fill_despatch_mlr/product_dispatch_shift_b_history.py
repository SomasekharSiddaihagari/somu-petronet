from sqlalchemy import Column, Integer, String, Float, Date, Time, DateTime, ForeignKey, Boolean, Text, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
 
Base = declarative_base()
 
class ERVBShiftLog(Base):
    __tablename__ = "b_shift_log_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    b_shift_log_id = Column(Integer, nullable=True)
    # ----------------------------
    # FK TO MASTER TABLE
    # ----------------------------
    category_master_id = Column(
        Integer,
        nullable=True
    )
 
    # ----------------------------
    # BASIC
    # ----------------------------
    log_date = Column(Date, nullable=True)
    shift_name = Column(String(20), nullable=True)      # B Shift
    shift_start_time = Column(Time, nullable=True)
    lpe_frl_at = Column(String(50), nullable=True)
 
    # ----------------------------
    # SUCTION / MLR
    # ----------------------------
    suction_line = Column(String(100), nullable=True)
    mlr = Column(String(100), nullable=True)
 
    # ----------------------------
    # FIRE SYSTEM
    # ----------------------------
    fire_pump_auto = Column(Boolean, nullable=True)
    fire_pump_manual = Column(Boolean, nullable=True)
    availability_auto = Column(Boolean, nullable=True)
    availability_manual = Column(Boolean, nullable=True)
 
    # ----------------------------
    # PRODUCT QUANTITIES
    # ----------------------------
    sku = Column(Float, nullable=True)
    hsd = Column(Float, nullable=True)
    ms = Column(Float, nullable=True)
    dkn = Column(Float, nullable=True)
 
    batch = Column(String(50), nullable=True)
    qty = Column(Float, nullable=True)
 
    # ----------------------------
    # SHIFT TOTALS
    # ----------------------------
    sump_level_percent = Column(Float, nullable=True)
    ci_pumped_percent = Column(Float, nullable=True)
 
    net_qty_of_shift = Column(Float, nullable=True)
    gross_qty_of_shift = Column(Float, nullable=True)
    atg_qty_of_shift = Column(Float, nullable=True)
 
    # ----------------------------
    # PUMP RUNNING HRS (ALL IN SAME TABLE)
    # ----------------------------
    bp_101a_previous_hrs = Column(Float, nullable=True)
    bp_101a_current_hrs = Column(Float, nullable=True)
    bp_101a_cumulative_hrs = Column(Float, nullable=True)
    bp_101a_availability = Column(String(50), nullable=True)
    bp_101a_product = Column(String(50), nullable=True)
 
    bp_101b_previous_hrs = Column(Float, nullable=True)
    bp_101b_current_hrs = Column(Float, nullable=True)
    bp_101b_cumulative_hrs = Column(Float, nullable=True)
    bp_101b_availability = Column(String(50), nullable=True)
    bp_101b_product = Column(String(50), nullable=True)
 
    bp_102a_previous_hrs = Column(Float, nullable=True)
    bp_102a_current_hrs = Column(Float, nullable=True)
    bp_102a_cumulative_hrs = Column(Float, nullable=True)
    bp_102a_availability = Column(String(50), nullable=True)
    bp_102a_product = Column(String(50), nullable=True)
 
    bp_102b_previous_hrs = Column(Float, nullable=True)
    bp_102b_current_hrs = Column(Float, nullable=True)
    bp_102b_cumulative_hrs = Column(Float, nullable=True)
    bp_102b_availability = Column(String(50), nullable=True)
    bp_102b_product = Column(String(50), nullable=True)
 
    bp_102c_previous_hrs = Column(Float, nullable=True)
    bp_102c_current_hrs = Column(Float, nullable=True)
    bp_102c_cumulative_hrs = Column(Float, nullable=True)
    bp_102c_availability = Column(String(50), nullable=True)
    bp_102c_product = Column(String(50), nullable=True)
 
    sump_pump_previous_hrs = Column(Float, nullable=True)
    sump_pump_current_hrs = Column(Float, nullable=True)
    sump_pump_cumulative_hrs = Column(Float, nullable=True)
    sump_pump_availability = Column(String(50), nullable=True)
    sump_pump_product = Column(String(50), nullable=True)
 
    ci_pump_101a_previous_hrs = Column(Float, nullable=True)
    ci_pump_101a_current_hrs = Column(Float, nullable=True)
    ci_pump_101a_cumulative_hrs = Column(Float, nullable=True)
    ci_pump_101a_availability = Column(String(50), nullable=True)
    ci_pump_101a_product = Column(String(50), nullable=True)
 
    ci_pump_101b_previous_hrs = Column(Float, nullable=True)
    ci_pump_101b_current_hrs = Column(Float, nullable=True)
    ci_pump_101b_cumulative_hrs = Column(Float, nullable=True)
    ci_pump_101b_availability = Column(String(50), nullable=True)
    ci_pump_101b_product = Column(String(50), nullable=True)
 
    # ----------------------------
    # MAINTENANCE & SIGN
    # ----------------------------
    maintenance_details = Column(Text, nullable=True)
    shift_engineer_name = Column(String(100), nullable=True)
    signature = Column(String(255), nullable=True)
 
    # ----------------------------
    # SYSTEM
    # ----------------------------
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)