from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base
 
 
class ShiftHandoverTaskHistory(Base):
    __tablename__ = "shift_handover_task_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    handover_master_id = Column(Integer, nullable=True)
    task_id = Column(Integer, nullable=True)
 
    pending_task = Column(String(255), nullable=True)
    due_date = Column(Date, nullable=True)
    assigned_to = Column(Integer, nullable=True)
    priority = Column(String(20), nullable=True)
    is_acknowledged = Column(Boolean, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)