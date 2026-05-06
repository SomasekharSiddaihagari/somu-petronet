from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Tank10KLFfeMasterHistory(Base):
    __tablename__ = "tank_10kl_ffe_master_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    tank_ffe_id = Column(Integer, nullable=True)

    station = Column(String(50), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(10), nullable=True)
    start_time = Column(Time, nullable=True)
    logbook_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=True)

    sign_shift_a = Column(String(100), nullable=True)
    sign_shift_b = Column(String(100), nullable=True)
    sign_shift_c = Column(String(100), nullable=True)
    sign_station_incharge = Column(String(100), nullable=True)

    name_shift_a = Column(String(100), nullable=True)
    name_shift_b = Column(String(100), nullable=True)
    name_shift_c = Column(String(100), nullable=True)
    name_station_incharge = Column(String(100), nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)

    action_type = Column(String(20), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    ms_logbook_id = Column(Integer, nullable=True)
    technician_id = Column(Integer, nullable=True)
