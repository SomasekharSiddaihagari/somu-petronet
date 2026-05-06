from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class ShiftHandoverMaster(Base):
    __tablename__ = "shift_handover_master"

    handover_master_id = Column(Integer, primary_key=True, autoincrement=True)

    next_incharge_id = Column(Integer, nullable=True)
 
    notes_for_next_shift = Column(Text, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)