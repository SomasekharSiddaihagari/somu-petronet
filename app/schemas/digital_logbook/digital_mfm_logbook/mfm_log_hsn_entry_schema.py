from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMLogHSNEntry(Base):
    __tablename__ = "mfm_log_hsn_entry"

    mfm_log_hsn_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    master_id = Column(Integer, ForeignKey("mfm_log_hsn_master.mfm_log_hsn_id", ondelete="CASCADE"))

    entry_date = Column(Date)
    entry_time = Column(Time)
 
    pt_1308_pressure = Column(Numeric(10, 3), nullable=True)
    pt_1306_pressure = Column(Numeric(10, 3), nullable=True)
 
    flow_rate_net = Column(Numeric(12, 3), nullable=True)
    flow_rate_gross = Column(Numeric(12, 3), nullable=True)
 
    hpcl_fcv_opening_1315 = Column(Numeric(12, 3), nullable=True)
 
    gross_vol_reading_fqy = Column(Numeric(12, 3), nullable=True)
    gross_qty_delivered_kl = Column(Numeric(12, 3), nullable=True)
 
    net_vol_reading_fqy = Column(Numeric(12, 3), nullable=True)
    net_qty_delivered_kl = Column(Numeric(12, 3), nullable=True)
 
    mass_reading_mt_fqy = Column(Numeric(12, 3), nullable=True)
    mass_qty_delivered_mt_kl = Column(Numeric(12, 3), nullable=True)
 
    product_density = Column(Numeric(10, 4), nullable=True)
    product_temp = Column(Numeric(6, 2), nullable=True)
    density_15deg = Column(Numeric(10, 4), nullable=True)
 
    hpcl_line_no = Column(String(50), nullable=True)
    tank_dip_during_plt_cm = Column(Numeric(10, 2), nullable=True)
    qty_as_per_atg = Column(Numeric(12, 3), nullable=True)
 
    diff_atg_fmr = Column(Numeric(12, 3), nullable=True)
    sign_shift_ie = Column(String(100), nullable=True)

    remarks = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())