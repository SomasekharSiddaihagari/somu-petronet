# app/models/digital_logbook/digital_cp_reading/cp_reading_mlr_entry.py
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base

class CPReadingMLREntry(Base):
    __tablename__ = "cp_reading_mlr_entry"

    cp_mlr_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    master_id = Column(
        Integer,
        ForeignKey("cp_reading_mlr_master.cp_mlr_id", ondelete="CASCADE"),
        nullable=True
    )

    sr_no = Column(Integer, nullable=True)
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
    remarks = Column(String(255), nullable=True)

    # -------- MLR --------
    mlr_ac_ip_v = Column(String(20), nullable=True)
    mlr_psp_ve = Column(String(20), nullable=True)
    mlr_ac_ip_amp = Column(String(20), nullable=True)
    mlr_op_dc_v = Column(String(20), nullable=True)
    mlr_op_dc_amp = Column(String(20), nullable=True)

    # -------- SV1 --------
    sv1_ac_ip_v = Column(String(20), nullable=True)
    sv1_psp_ve = Column(String(20), nullable=True)
    sv1_ac_ip_amp = Column(String(20), nullable=True)
    sv1_op_dc_v = Column(String(20), nullable=True)
    sv1_op_dc_amp = Column(String(20), nullable=True)

    # -------- SV2 --------
    sv2_ac_ip_v = Column(String(20), nullable=True)
    sv2_psp_ve = Column(String(20), nullable=True)
    sv2_ac_ip_amp = Column(String(20), nullable=True)
    sv2_op_dc_v = Column(String(20), nullable=True)
    sv2_op_dc_amp = Column(String(20), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)