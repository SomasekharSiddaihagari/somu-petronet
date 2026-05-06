from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
 
class ShiftHandoverTask(Base):
    __tablename__ = "shift_handover_task"
 
    task_id = Column(Integer, primary_key=True, autoincrement=True)
 
    handover_id = Column(
        Integer,
        ForeignKey("shift_handover_master.id", ondelete="CASCADE"),
        nullable=True
    )

    used_handover_id = Column(
        Integer,
        ForeignKey("shift_handover_log.id", ondelete="CASCADE"),
        nullable=True
    )
    
 
    pending_task = Column(String(255), nullable=True)
    due_date = Column(Date, nullable=True)
    assigned_to = Column(Integer, nullable=True)
    priority = Column(String(20), nullable=True)  # High / Medium / Low
    is_acknowledged = Column(Boolean, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)