from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Numeric, Text
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMLogHSNMasterHistory(Base):
    __tablename__ = "mfm_log_hsn_master_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    mfm_log_hsn_id = Column(Integer)
    document_no = Column(String(100))
    station = Column(String(50))
    station_in_charge = Column(String(100))
    shift = Column(String(10))
    start_time = Column(Time)
    log_date = Column(Date)
 
    shift_a_tank_takeover = Column(String(100))
    shift_a_tank_handover = Column(String(100))
    shift_b_tank_takeover = Column(String(100))
    shift_b_tank_handover = Column(String(100))
    shift_c_tank_takeover = Column(String(100))
    shift_c_tank_handover = Column(String(100))
 
    qty_pumped_mangalore_kl = Column(Numeric(12, 3))
    receipt_hassan_kl = Column(Numeric(12, 3))
    receipt_bangalore_kl = Column(Numeric(12, 3))
 
    qty_available_tank101_kl = Column(Numeric(12, 3))
    qty_available_tank102_kl = Column(Numeric(12, 3))
 
    loss_gain_kl = Column(Numeric(12, 3))
 
    qty_pumped_last_24hrs_kl = Column(Numeric(12, 3))
    qty_pumped_plt_kl = Column(Numeric(12, 3))
    qty_pumped_month_kl = Column(Numeric(12, 3))
    qty_pumped_year_kl = Column(Numeric(12, 3))
 
    diesel_dg_tank_ltrs = Column(Numeric(12, 3))
    diesel_dg_set_tank_ltrs = Column(Numeric(12, 3))
    diesel_ffdu3_ser_tank_ltrs = Column(Numeric(12, 3))
    diesel_ffdu4_ser_tank_ltrs = Column(Numeric(12, 3))
    diesel_ffdu5_ser_tank_ltrs = Column(Numeric(12, 3))
 
    hrs_operation_last_24hrs = Column(Numeric(6, 2))
    hrs_operation_month = Column(Numeric(6, 2))
    hrs_operation_year = Column(Numeric(6, 2))
    sump_tank_dip_0700_hrs = Column(Numeric(12, 3))
 
    sic_signature = Column(String(100))
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)