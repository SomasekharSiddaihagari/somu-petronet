from sqlalchemy import Column, Integer, String, Date, Time, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
class MFMLogEntry(Base):
    __tablename__ = "mfm_log_entry_dkn_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    mfm_log_dsk_id = Column(Integer, nullable=True)
    master_id = Column(Integer, nullable=True)

    entry_time = Column(Time, nullable=True)
 
    mainline_density = Column(Float, nullable=True)
    mainline_temp = Column(Float, nullable=True)
 
    sampling_density = Column(Float, nullable=True)
    sampling_temp = Column(Float, nullable=True)
 
    manifold_density = Column(Float, nullable=True)
    manifold_temp = Column(Float, nullable=True)
 
    corresponding_density = Column(Float, nullable=True)
 
    receiving_tank_no = Column(String(50), nullable=True)
    tank_dip = Column(Float, nullable=True)
    tank_quantity = Column(Float, nullable=True)
 
    flow_gross = Column(Float, nullable=True)
    flow_net = Column(Float, nullable=True)
    flow_mass = Column(Float, nullable=True)
 
    delivered_fc_klhr = Column(Float, nullable=True)
    delivered_fc_cumu = Column(Float, nullable=True)
    delivered_qd_klhr = Column(Float, nullable=True)
    delivered_qd_cumu = Column(Float, nullable=True)
 
    delivered_tank_dip = Column(Float, nullable=True)
 
    remarks = Column(Text, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)