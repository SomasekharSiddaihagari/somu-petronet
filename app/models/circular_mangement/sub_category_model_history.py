
from datetime import datetime
from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from enum import Enum as PyEnum




class SubCategoryMasterHistory(Base):
    __tablename__ = "subcategory_master_history"
    history_id = Column(Integer, primary_key=True,autoincrement=True)
    subcategory_name = Column(String(150),nullable=True)
    category_id = Column(Integer,nullable=True)
    description = Column(Text,nullable=True)
    is_deleted = Column(Boolean, default=False,nullable=True)