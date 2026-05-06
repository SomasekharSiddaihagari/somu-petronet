from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Numeric
from sqlalchemy.sql import func
from app.database import Base
 
 
class MFMAccountingMasterHistory(Base):
    __tablename__ = "mfm_accounting_dkn_history"
 
    history_id = Column(Integer, primary_key=True,autoincrement=True)
    mfm_acc_dkn_id = Column(Integer, nullable=True)
 
   # Header
    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=True)
    document_number = Column(String(50), nullable=True)
    otr_no = Column(String(50), nullable=True)
    mfm_number = Column(String(50), nullable=True)
    receiving_company = Column(String(50), nullable=True)
    log_date = Column(Date, nullable=True)
 
    tank_no = Column(String(50), nullable=True)
    product = Column(String(50), nullable=True)
    mrpl_batch_no = Column(String(50), nullable=True)
    pmhbl_batch_no = Column(String(50), nullable=True)
 
    # Opening Readings
    opening_vol_kl_amb = Column(Numeric(12, 3), nullable=True)
    opening_vol_kl_15c = Column(Numeric(12, 3), nullable=True)
    opening_mass_mt = Column(Numeric(12, 3), nullable=True)
    opening_weighted_amb_density = Column(Numeric(10, 4), nullable=True)
    opening_weighted_temp = Column(Numeric(6, 2), nullable=True)
    opening_weighted_15c_density = Column(Numeric(10, 4), nullable=True)
    opening_date = Column(Date, nullable=True)
    opening_time = Column(Time, nullable=True)
 
    # Closing Readings
    closing_vol_kl_amb = Column(Numeric(12, 3), nullable=True)
    closing_vol_kl_15c = Column(Numeric(12, 3), nullable=True)
    closing_mass_mt = Column(Numeric(12, 3), nullable=True)
    closing_weighted_amb_density = Column(Numeric(10, 4), nullable=True)
    closing_weighted_temp = Column(Numeric(6, 2), nullable=True)
    closing_weighted_15c_density = Column(Numeric(10, 4), nullable=True)
    closing_date = Column(Date, nullable=True)
    closing_time = Column(Time, nullable=True)
 
    # Auto-calculated
    qty_transferred_vol_kl = Column(Numeric(12, 3), nullable=True)
    qty_transferred_mass_mt = Column(Numeric(12, 3), nullable=True)
    qty_transferred_15c_total = Column(Numeric(12, 3), nullable=True)
    qty_transferred_mass_total = Column(Numeric(12, 3), nullable=True)
    qty_transferred_amb_total = Column(Numeric(12, 3), nullable=True)
   
    # Seal Description & Valve Status
    hpcl_hsd_line_mov_seal = Column(String(50), nullable=True)
    hpcl_hsd_line_mov_status = Column(String(30), nullable=True)
 
    bpcl_hsd_line_mov_seal = Column(String(50), nullable=True)
    bpcl_hsd_line_mov_status = Column(String(30), nullable=True)
 
    iocl_hsd_line_mov_seal = Column(String(50), nullable=True)
    iocl_hsd_line_mov_status = Column(String(30), nullable=True)
 
    hpcl_hsd_line_hov_seal = Column(String(50), nullable=True)
    hpcl_hsd_line_hov_status = Column(String(30), nullable=True)
 
    bpcl_hsd_line_hov_seal = Column(String(50), nullable=True)
    bpcl_hsd_line_hov_status = Column(String(30), nullable=True)
 
    iocl_hsd_line_hov_seal = Column(String(50), nullable=True)
    iocl_hsd_line_hov_status = Column(String(30), nullable=True)
 
    mrpl_hsd_line_mov_seal = Column(String(50), nullable=True)
    mrpl_hsd_line_mov_status = Column(String(30), nullable=True)
 
    if_tank_101_mov_seal = Column(String(50), nullable=True)
    if_tank_101_mov_status = Column(String(30), nullable=True)
 
    if_tank_102_mov_seal = Column(String(50), nullable=True)
    if_tank_102_mov_status = Column(String(30), nullable=True)
 
    ms_header_line_mov_1415_seal = Column(String(50), nullable=True)
    ms_header_line_mov_1415_status = Column(String(30), nullable=True)
 
    ms_header_line_mov_1416_seal = Column(String(50), nullable=True)
    ms_header_line_mov_1416_status = Column(String(30), nullable=True)
    
    mrpl_hsd_dbvb_mov_seal = Column(String(50), nullable=True)
    mrpl_hsd_dbvb_mov_status = Column(String(30), nullable=True)
 
    # Remarks
    remarks = Column(String, nullable=True)
 
    # Signatures
    opening_pmhbl_signature = Column(String, nullable=True)
    opening_mrpl_signature = Column(String, nullable=True)
    closing_pmhbl_signature = Column(String, nullable=True)
    closing_mrpl_signature = Column(String, nullable=True)

    opening_pmhbl_signature_time = Column(DateTime, nullable=True)
    opening_mrpl_signature_time = Column(DateTime, nullable=True)
    closing_pmhbl_signature_time = Column(DateTime, nullable=True)
    closing_mrpl_signature_time = Column(DateTime, nullable=True)
    

    name_open_pmhbl = Column(String(100), nullable=True)
    name_open_hpcl = Column(String(100), nullable=True)
    name_close_pmhbl = Column(String(100), nullable=True)
    name_close_hpcl = Column(String(100), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)