from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Text, Time, DateTime
 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
 

class DigitalLogBookEntry(Base):
    __tablename__ = "digital_logbook_entry"
 
    entry_id = Column(Integer, primary_key=True, autoincrement=True)
 
    logbook_id = Column(
        Integer,
        ForeignKey("digital_logbook.logbook_id", ondelete="CASCADE"),
        nullable=True,
    )
 
    entry_time = Column(Time, nullable=True)
    location = Column(String(100), nullable=True)
 
    # 🔥 NEW FIELD
    logs = Column(Text, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
 