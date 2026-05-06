
from datetime import datetime
from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import JSONB


class CircularMasterHistory(Base):
    __tablename__ = "circular_master_history"
    history_id = Column(Integer, primary_key=True,autoincrement=True)
    circular_id = Column(Integer,nullable=True)
    document_no = Column(String(255), nullable=True)
    title = Column(String(250),nullable=True)
    removed_user = Column(JSONB, nullable=True)
    category_id = Column(Integer, nullable=True)
    subcategory_id = Column(Integer, nullable=True)
    content = Column(Text,nullable=True)
    change_type = Column(String(50),nullable=True)
    mandatory_status = Column(Boolean, default=False,nullable=True)
    status = Column(String(50),nullable=True)
    is_deleted = Column(Boolean, default=False,nullable=True)
    is_archived = Column(Boolean, default=False,nullable=True)
    read_count = Column(Integer, default=0,nullable=True)
    acknowledge_count = Column(Integer, default=0,nullable=True)
    created_by = Column(Integer,nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    reason=Column(Text,nullable=True)
    updated_by = Column(Integer,nullable=True)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)

    tags = Column(String(50),nullable=True)
