from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
 
Base = declarative_base()
 
class LeaveTypeHistory(Base):
    __tablename__ = "leave_types_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    type_id = Column(Integer, nullable=True)
    code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)