from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base


class CPReadingDKNEntryHistory(Base):
    __tablename__ = "cp_reading_dkn_entry_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    cp_dkn_entry_id = Column(Integer, nullable=True)
    master_id = Column(Integer, nullable=True)
    sr_no = Column(Integer, nullable=True)
    entry_date = Column(Date, nullable=True)
    entry_time = Column(Time, nullable=True)
    remarks = Column(String(255), nullable=True)

    dkn_ac_ip_v = Column(String(20), nullable=True)
    dkn_psp_ve = Column(String(20), nullable=True)
    dkn_ac_ip_amp = Column(String(20), nullable=True)
    dkn_op_dc_v = Column(String(20), nullable=True)
    dkn_op_dc_amp = Column(String(20), nullable=True)

    sv8_ac_ip_v = Column(String(20), nullable=True)
    sv8_psp_ve = Column(String(20), nullable=True)
    sv8_ac_ip_amp = Column(String(20), nullable=True)
    sv8_op_dc_v = Column(String(20), nullable=True)
    sv8_op_dc_amp = Column(String(20), nullable=True)

    ipstn_ac_ip_v = Column(String(20), nullable=True)
    ipstn_psp_ve = Column(String(20), nullable=True)
    ipstn_ac_ip_amp = Column(String(20), nullable=True)
    ipstn_op_dc_v = Column(String(20), nullable=True)
    ipstn_op_dc_amp = Column(String(20), nullable=True)

    sv9_ac_ip_v = Column(String(20), nullable=True)
    sv9_psp_ve = Column(String(20), nullable=True)
    sv9_ac_ip_amp = Column(String(20), nullable=True)
    sv9_op_dc_v = Column(String(20), nullable=True)
    sv9_op_dc_amp = Column(String(20), nullable=True)

    sv10_ac_ip_v = Column(String(20), nullable=True)
    sv10_psp_ve = Column(String(20), nullable=True)
    sv10_ac_ip_amp = Column(String(20), nullable=True)
    sv10_op_dc_v = Column(String(20), nullable=True)
    sv10_op_dc_amp = Column(String(20), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
