# app/models/digital_logbook/digital_cp_reading/cp_reading_ner_entry.py
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base

class CPReadingNEREntry(Base):
    __tablename__ = "cp_reading_ner_entry"

    cp_ner_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    master_id = Column(
        Integer,
        ForeignKey("cp_reading_ner_master.cp_ner_id", ondelete="CASCADE"),
        nullable=True
    )

    sr_no = Column(Integer, nullable=True)
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
    remarks = Column(String(255), nullable=True)

    # -------- NER --------
    ner_ac_ip_v = Column(String(20), nullable=True)
    ner_psp_ve = Column(String(20), nullable=True)
    ner_ac_ip_amp = Column(String(20), nullable=True)
    ner_op_dc_v = Column(String(20), nullable=True)
    ner_op_dc_amp = Column(String(20), nullable=True)

    # -------- SV3 --------
    sv3_ac_ip_v = Column(String(20), nullable=True)
    sv3_psp_ve = Column(String(20), nullable=True)
    sv3_ac_ip_amp = Column(String(20), nullable=True)
    sv3_op_dc_v = Column(String(20), nullable=True)
    sv3_op_dc_amp = Column(String(20), nullable=True)

    # -------- SV4 --------
    sv4_ac_ip_v = Column(String(20), nullable=True)
    sv4_psp_ve = Column(String(20), nullable=True)
    sv4_ac_ip_amp = Column(String(20), nullable=True)
    sv4_op_dc_v = Column(String(20), nullable=True)
    sv4_op_dc_amp = Column(String(20), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
