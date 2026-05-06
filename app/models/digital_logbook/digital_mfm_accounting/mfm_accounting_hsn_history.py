from sqlalchemy import Column, Integer, String, Date, Time, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMAccountingHSNHistory(Base):
    __tablename__ = "mfm_accounting_hsn_history"
 
    history_id = Column(Integer, primary_key=True,autoincrement=True)
    mfm_acc_hsn_id = Column(Integer, nullable=True)   # mfm_accounting_hsn.id
    document_number = Column(String(50), nullable=True)
    station = Column(String(50), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(10), nullable=True)
    start_time = Column(Time, nullable=True)
    status = Column(String(20), nullable=True)
 
    otr_no = Column(String(50), nullable=True)
    mfm_number = Column(String(50), nullable=True)
    receiving_company = Column(String(50), nullable=True)
    entry_date = Column(Date, nullable=True)
 
    tank_no = Column(String(50), nullable=True)
    product = Column(String(50), nullable=True)
    mrpl_batch_no = Column(String(50), nullable=True)
    pmhbl_batch_no = Column(String(50), nullable=True)
 
    open_vol_kl_amb = Column(Float, nullable=True)
    open_vol_kl_15c = Column(Float, nullable=True)
    open_mass_mt = Column(Float, nullable=True)
    open_density_amb = Column(Float, nullable=True)
    open_density_15c = Column(Float, nullable=True)
    open_temp = Column(Float, nullable=True)
    open_date = Column(Date, nullable=True)
    open_time = Column(Time, nullable=True)
 
    close_vol_kl_amb = Column(Float, nullable=True)
    close_vol_kl_15c = Column(Float, nullable=True)
    close_mass_mt = Column(Float, nullable=True)
    close_density_amb = Column(Float, nullable=True)
    close_density_15c = Column(Float, nullable=True)
    close_temp = Column(Float, nullable=True)
    close_date = Column(Date, nullable=True)
    close_time = Column(Time, nullable=True)
 
    remarks = Column(String(500), nullable=True)
 
    sign_open_pmhbl = Column(String(100), nullable=True)
    sign_open_hpcl = Column(String(100), nullable=True)
    sign_close_pmhbl = Column(String(100), nullable=True)
    sign_close_hpcl = Column(String(100), nullable=True)

    sign_open_pmhbl_time = Column(DateTime, nullable=True)
    sign_open_hpcl_time = Column(DateTime, nullable=True)
    sign_close_pmhbl_time = Column(DateTime, nullable=True)
    sign_close_hpcl_time = Column(DateTime, nullable=True)
    
    name_open_pmhbl = Column(String(100), nullable=True)
    name_open_hpcl = Column(String(100), nullable=True)
    name_close_pmhbl = Column(String(100), nullable=True)
    name_close_hpcl = Column(String(100), nullable=True)

    quality_tranfered_amb_total = Column(Float, nullable=True)
    quality_tranfered_15c_total = Column(Float, nullable=True)
    quality_tranfered_mass_total = Column(Float, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)