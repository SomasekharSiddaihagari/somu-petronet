from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, DateTime
 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
 
class DigitalLogBook(Base):
    __tablename__ = "digital_logbook"
 
    logbook_id = Column(Integer, primary_key=True, autoincrement=True)
 
    logbook_ref_no = Column(String(50), nullable=True)
 
    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
 
    log_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)
 
    handed_over_by = Column(String(100), nullable=True)
    taken_over_by = Column(String(100), nullable=True)
 
    # 🔥 MOVED FROM ENTRY
    dkn = Column(String(50), nullable=True)
    hsn = Column(String(50), nullable=True)
    ner = Column(String(50), nullable=True)
    mlr = Column(String(50), nullable=True)
    sv1 = Column(String(50), nullable=True)
    sv2 = Column(String(50), nullable=True)
    sv3 = Column(String(50), nullable=True)
    sv4 = Column(String(50), nullable=True)
    sv5 = Column(String(50), nullable=True)
    sv6 = Column(String(50), nullable=True)
    sv7 = Column(String(50), nullable=True)
    sv8 = Column(String(50), nullable=True)
    sv9 = Column(String(50), nullable=True)
    sv10 = Column(String(50), nullable=True)
 
 
    # 🔥 NEW
    technician_id = Column(Integer, nullable=True)
 
    is_shift_closed = Column(Boolean, nullable=True)
    ms_logbook_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)