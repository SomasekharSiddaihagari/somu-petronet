from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class DknDigitalLogBook(Base):
    __tablename__ = "dkn_digital_logbook"

    dkn_logbook_id = Column(Integer, primary_key=True, autoincrement=True)

    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(20), nullable=True)
    logbook_ref_no = Column(String(50), nullable=True)
    log_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)

    handed_over_by = Column(String(100), nullable=True)
    taken_over_by = Column(String(100), nullable=True)

    # 🔥 MOVED FROM ENTRY
    hsn = Column(String(50), nullable=True)
    ner = Column(String(50), nullable=True)
    mlr = Column(String(50), nullable=True)
    svb = Column(String(50), nullable=True)
    ip1 = Column(String(50), nullable=True)
    sv9 = Column(String(50), nullable=True)
    sv10 = Column(String(50), nullable=True)

    # 🔥 NEW
    technician_id = Column(Integer, nullable=True)

    is_shift_closed = Column(Boolean, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)
