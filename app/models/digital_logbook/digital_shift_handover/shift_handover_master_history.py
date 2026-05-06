from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class ShiftHandoverMasterHistory(Base):
    __tablename__ = "shift_handover_master_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    handover_master_id = Column(Integer, nullable=True)
 
    next_incharge_id = Column(Integer, nullable=True)
    notes_for_next_shift = Column(Text, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)