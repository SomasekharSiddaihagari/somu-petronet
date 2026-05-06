from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class KPTCLDKNMaster(Base):
    __tablename__ = "kptcl_dkn_master"

    kptcl_dkn_id = Column(Integer, primary_key=True, autoincrement=True)

    # Header fields

    station_name = Column(String(100), nullable=True)          # Devangonthi
    station_incharge = Column(String(150), nullable=True)      # Rajesh Kumar
    shift = Column(String(20), nullable=True)                  # Shift A
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
    document_number = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)                 # Active / Submitted
 
    # Audit
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)