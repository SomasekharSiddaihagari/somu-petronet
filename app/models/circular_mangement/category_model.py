from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base

class CategoryMaster(Base):
    __tablename__ = "category_master"
    category_id = Column(Integer, primary_key=True,autoincrement=True)
    category_name = Column(String(150), unique=True, nullable=True)
    description = Column(Text,nullable=True)
    is_deleted = Column(Boolean, default=False,nullable=True)
    created_by = Column(Integer,nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    updated_by = Column(Integer,nullable=True)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)