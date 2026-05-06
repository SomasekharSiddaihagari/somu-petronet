from sqlalchemy import Column, Integer, String, Date, Time, DateTime, func
from app.database import Base

class CPReadingMasterHistory(Base):
    __tablename__ = "cp_reading_master_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    cp_master_id = Column(Integer, nullable=False, index=True) # Original ID
    
    station_id = Column(Integer, nullable=True) # 1=MLR, 2=NER, 3=HSN, 4=DKN
    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(255), nullable=True)
    shift = Column(String(50), nullable=True)
    start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)
    
    ms_logbook_id = Column(Integer, nullable=True)
    technician_id = Column(Integer, nullable=True)

    created_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
