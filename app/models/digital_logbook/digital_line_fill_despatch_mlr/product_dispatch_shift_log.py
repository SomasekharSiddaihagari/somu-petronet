from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ProductDispatchShiftLog(Base):
    __tablename__ = "product_dispatch_shift_log"

    shift_log_id = Column(Integer, primary_key=True, autoincrement=True)
    category_master_id = Column(Integer, ForeignKey("product_dispatch_category_master.p_category_master_id"), nullable=False)
    
    # Metadata
    shift_id = Column(Integer, nullable=True) # Linked to public.shift
    shift = Column(String(20), nullable=True) # A, B, or C
    log_date = Column(Date, nullable=True)

    # Relationships to the new Entry table
    sub_entries = relationship("ProductDispatchLogEntry", backref="parent_log", cascade="all, delete-orphan")

    # Booster Pump 101A
    bp_101a_previous_hrs = Column(Float, nullable=True)
    bp_101a_current_hrs = Column(Float, nullable=True)
    bp_101a_cumulative_hrs = Column(Float, nullable=True)
    bp_101a_availability = Column(Boolean, default=True)
    bp_101a_product = Column(String(50), nullable=True)

    # Booster Pump 101B
    bp_101b_previous_hrs = Column(Float, nullable=True)
    bp_101b_current_hrs = Column(Float, nullable=True)
    bp_101b_cumulative_hrs = Column(Float, nullable=True)
    bp_101b_availability = Column(Boolean, default=True)
    bp_101b_product = Column(String(50), nullable=True)

    # Multi-Stage Pump 102A
    mp_102a_previous_hrs = Column(Float, nullable=True)
    mp_102a_current_hrs = Column(Float, nullable=True)
    mp_102a_cumulative_hrs = Column(Float, nullable=True)
    mp_102a_availability = Column(Boolean, default=True)
    mp_102a_product = Column(String(50), nullable=True)

    # Multi-Stage Pump 102B
    mp_102b_previous_hrs = Column(Float, nullable=True)
    mp_102b_current_hrs = Column(Float, nullable=True)
    mp_102b_cumulative_hrs = Column(Float, nullable=True)
    mp_102b_availability = Column(Boolean, default=True)
    mp_102b_product = Column(String(50), nullable=True)

    # Multi-Stage Pump 102C
    mp_102c_previous_hrs = Column(Float, nullable=True)
    mp_102c_current_hrs = Column(Float, nullable=True)
    mp_102c_cumulative_hrs = Column(Float, nullable=True)
    mp_102c_availability = Column(Boolean, default=True)
    mp_102c_product = Column(String(50), nullable=True)

    # Sump Pump
    sump_pump_previous_hrs = Column(Float, nullable=True)
    sump_pump_current_hrs = Column(Float, nullable=True)
    sump_pump_cumulative_hrs = Column(Float, nullable=True)
    sump_pump_availability = Column(Boolean, default=True)
    sump_pump_product = Column(String(50), nullable=True)

    # Corrosion Inhibitor Pump 101A
    ci_pump_101a_previous_hrs = Column(Float, nullable=True)
    ci_pump_101a_current_hrs = Column(Float, nullable=True)
    ci_pump_101a_cumulative_hrs = Column(Float, nullable=True)
    ci_pump_101a_availability = Column(Boolean, default=True)
    ci_pump_101a_product = Column(String(50), nullable=True)

    # Corrosion Inhibitor Pump 101B
    ci_pump_101b_previous_hrs = Column(Float, nullable=True)
    ci_pump_101b_current_hrs = Column(Float, nullable=True)
    ci_pump_101b_cumulative_hrs = Column(Float, nullable=True)
    ci_pump_101b_availability = Column(Boolean, default=True)
    ci_pump_101b_product = Column(String(50), nullable=True)

    # DRA Engine
    dra_previous_hrs = Column(Float, nullable=True)
    dra_current_hrs = Column(Float, nullable=True)
    dra_cumulative_hrs = Column(Float, nullable=True)
    dra_availability = Column(Boolean, default=True)
    dra_product = Column(String(50), nullable=True)
    total_pump_hrs = Column(Float, nullable=True)

    # Fire System
    fire_pump_auto = Column(Boolean, default=True)
    fire_pump_manual = Column(Boolean, default=False)
    fire_pump_1_available = Column(Boolean, default=True)
    fire_pump_2_available = Column(Boolean, default=True)
    fire_pump_3_available = Column(Boolean, default=True)

    # Performance
    sump_level_percent = Column(Float, nullable=True)
    ci_pumped_percent = Column(Float, nullable=True)
    net_qty_of_shift = Column(Float, nullable=True)
    gross_qty_of_shift = Column(Float, nullable=True)
    atg_qty_of_shift = Column(Float, nullable=True)

    # Maintenance & Signature
    maintenance_details = Column(String(500), nullable=True)
    shift_engineer_name = Column(String(100), nullable=True)
    signature = Column(String(200), nullable=True)

    # Audit
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
