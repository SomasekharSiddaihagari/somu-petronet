from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class ShiftTakeoverHistory(Base):
    __tablename__ = "shift_takeover_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    shift_takeover_id = Column(Integer, nullable=True)
 
    shift_code = Column(String(20), nullable=True)
    current_incharge_id = Column(Integer, nullable=True)
 
    previous_shift_notes = Column(Text, nullable=True)
    takeover_notes = Column(Text, nullable=True)
 
    is_emergency = Column(Boolean, nullable=True)
    emergency_assigned_to = Column(Integer, nullable=True)
 
    status = Column(String(50), nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)