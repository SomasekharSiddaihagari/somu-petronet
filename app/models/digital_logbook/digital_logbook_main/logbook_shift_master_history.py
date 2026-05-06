from sqlalchemy import Column, Integer, String, Date, Time, DateTime
 
from sqlalchemy.sql import func
 
from app.database import Base
 
 
class LogbookShiftMasterHistory(Base):
    __tablename__ = "logbook_shift_master_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # Reference (NO FK)
 
    ms_logbook_id = Column(Integer, nullable=True)
    technician_id = Column(Integer, nullable=True)
 
    # Replicated data
 
    station_name = Column(String(100), nullable=True)
 
    station_incharge = Column(String(100), nullable=True)
 
    shift = Column(String(20), nullable=True)
 
    shift_start_time = Column(Time, nullable=True)
 
    shift_end_time = Column(Time, nullable=True)
 
    log_date = Column(Date, nullable=True)
 
    status = Column(String(30), nullable=True)
 
    handover_notes = Column(String(500), nullable=True)
 
    shift_a_technician = Column(String(100), nullable=True)
 
    shift_a_engineer = Column(String(100), nullable=True)
 
    shift_b_technician = Column(String(100), nullable=True)
 
    shift_b_engineer = Column(String(100), nullable=True)
 
    shift_c_technician = Column(String(100), nullable=True)
 
    shift_c_engineer = Column(String(100), nullable=True)
   
 
 
    tank_ffe_id = Column(Integer, nullable=True)
 
    cp_dkn_id = Column(Integer, nullable=True)
    cp_hsn_id = Column(Integer, nullable=True)
    cp_mlr_id = Column(Integer, nullable=True)
    cp_ner_id = Column(Integer, nullable=True)
 
    dsc_id = Column(Integer, nullable=True)
 
    sampling_id = Column(Integer, nullable=True)
 
    dg_id = Column(Integer, nullable=True)
 
    erv_id = Column(Integer, nullable=True)
 
    fire_id = Column(Integer, nullable=True)
 
    kptcl_dkn_id = Column(Integer, nullable=True)
    kptcl_hsn_id = Column(Integer, nullable=True)
    kptcl_ner_id = Column(Integer, nullable=True)
 
    vtmn_id = Column(Integer, nullable=True)
    vtm_id = Column(Integer, nullable=True)
 
    tank_id = Column(Integer, nullable=True)   # kept single, removed duplicate
 
    pressure_id = Column(Integer, nullable=True)
 
    npt_id = Column(Integer, nullable=True)
 
    mfm_log_dkn_id = Column(Integer, nullable=True)
    mfm_log_ner_id = Column(Integer, nullable=True)
 
    mfm_acc_hsn_id = Column(Integer, nullable=True)
    mfm_acc_dkn_id = Column(Integer, nullable=True)
 
    security_guard_id = Column(Integer, nullable=True)
        # History metadata
 
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)
 