from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
 
from app.database import Base
 
 
class GroupMaster(Base):
    __tablename__ = "group_master"
 
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(150), nullable=False, unique=True)
    description = Column(Text, nullable=True)
 
    # Stores list of employee/user IDs coming from UI (checkbox selection)
    employee_ids = Column(JSONB, nullable=False)
 
    is_deleted = Column(Boolean, default=False)
 
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, nullable=True)
 
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(Integer, nullable=True)

    