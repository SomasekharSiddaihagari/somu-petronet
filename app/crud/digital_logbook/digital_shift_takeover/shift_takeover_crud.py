from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class ShiftTakeover(Base):
    __tablename__ = "shift_takeover"
 
    shift_takeover_id = Column(Integer, primary_key=True, autoincrement=True)
 
    # Shift info
    shift_code = Column(String(20), nullable=True)        # Shift A / B / C
 
    # Current shift in-charge (optional persistence)
    current_incharge_id = Column(Integer, nullable=True)
 
    # Notes
    previous_shift_notes = Column(Text, nullable=True)
    takeover_notes = Column(Text, nullable=True)
 
    # Emergency handling
    is_emergency = Column(Boolean, nullable=True)
    emergency_assigned_to = Column(Integer, nullable=True)
 
    # Status
    status = Column(String(50), nullable=True)            # TAKEN_OVER / DRAFT
 
    # Audit
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)