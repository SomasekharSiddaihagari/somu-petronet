from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, DateTime
 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class LogbookShiftMaster(Base):
    __tablename__ = "logbook_shift_master"
   
    ms_logbook_id = Column(Integer, primary_key=True, autoincrement=True)
    technician_id = Column(Integer, nullable=True)
 
    # Station & shift info
 
    mlr_logbook_id = Column(
            Integer,
            ForeignKey("mlr_digital_logbook.mlr_logbook_id"),
            nullable=False
        )
    hsn_logbook_id = Column(
            Integer,
            ForeignKey("hsn_digital_logbook.hsn_logbook_id"),
            nullable=False
        )
    dkn_logbook_id = Column(
            Integer,
            ForeignKey("dkn_digital_logbook.dkn_logbook_id"),
            nullable=False
        )
 
 
    shift_a = Column(String(20), nullable=True)          # Shift A / B / C
    shift_b = Column(String(20), nullable=True)          # Shift A / B / C
    shift_c = Column(String(20), nullable=True)          # Shift A / B / C
 
    shift_a_start_time = Column(Time, nullable=True)
    shift_b_start_time = Column(Time, nullable=True)
    shift_c_start_time = Column(Time, nullable=True)
 
    shift_a_end_time = Column(Time, nullable=True)
    shift_b_end_time = Column(Time, nullable=True)
    shift_c_end_time = Column(Time, nullable=True)
 
    log_date = Column(Date, nullable=True)
 
    # Status & notes
 
    shift_a_status = Column(String(30), nullable=True)         # ACTIVE / PENDING / COMPLETED
    shift_b_status = Column(String(30), nullable=True)         # ACTIVE / PENDING / COMPLETED
    shift_c_status = Column(String(30), nullable=True)         # ACTIVE / PENDING / COMPLETED
 
    shift_a_handover_notes = Column(String(500), nullable=True)
    shift_b_handover_notes = Column(String(500), nullable=True)
    shift_c_handover_notes = Column(String(500), nullable=True)
 
    # Signatures (UI mapping)
 
   
    shift_a_engineer = Column(String(100), nullable=True)
    shift_b_engineer = Column(String(100), nullable=True)
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
    # Audit
 

 
    closed_at = Column(DateTime, nullable=True)
 
    mlr_digital_logs = relationship(
        "MlrDigitalLogBook",
        back_populates="master_shift",
    )
    hsn_digital_logs = relationship(
        "HsnDigitalLogBook",
        back_populates="master_shift",
    )
    dkn_digital_logs = relationship(
        "DknDigitalLogBook",
        back_populates="master_shift",
    )
   

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)










