from sqlalchemy import Column, Integer, String, Time, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class HsnDigitalLogBookEntryHistory(Base):
    __tablename__ = "hsn_digital_logbook_entry_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)

    hsn_entry_id = Column(Integer, nullable=True)
    hsn_logbook_id = Column(Integer, nullable=True)

    entry_time = Column(Time, nullable=True)
    location = Column(String(100), nullable=True)

    # 🔥 NEW
    logs = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
