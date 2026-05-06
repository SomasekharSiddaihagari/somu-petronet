from sqlalchemy import Column, Integer, String, Date, Time, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
class MFMPLTDetail(Base):
    __tablename__ = "mfm_plt_detail_dkn"
 
    mfm_plt_dkn_id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey("mfm_log_master.mfm_log_dkn_id"), nullable=True)
 

    # plt_sd_start_time = Column(Time, nullable=True)
    # plt_sd_end_time = Column(Time, nullable=True)
 
    omc_with_tank_no = Column(String(50), nullable=True)
    start_time = Column(Time, nullable=True)
    stop_time = Column(Time, nullable=True)
 
    opening_dip = Column(Float, nullable=True)
    opening_qty = Column(Float, nullable=True)
 
    closing_dip = Column(Float, nullable=True)
    closing_qty = Column(Float, nullable=True)
 
    fmr_opening_net = Column(Float, nullable=True)
    fmr_opening_gross = Column(Float, nullable=True)
    fmr_opening_mass = Column(Float, nullable=True)
 
    fmr_closing_net = Column(Float, nullable=True)
    fmr_closing_gross = Column(Float, nullable=True)
    fmr_closing_mass = Column(Float, nullable=True)
 
    qty_as_per_dip = Column(Float, nullable=True)
    qty_as_per_fmr = Column(Float, nullable=True)
 
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

