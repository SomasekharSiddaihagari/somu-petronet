
from datetime import datetime
from app.database import Base
from sqlalchemy import JSON, Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from enum import Enum as PyEnum


class PublisherMaster(Base):
    __tablename__ = "publisher_master"
    publisher_id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer,nullable=True)
    category_id = Column(Integer, nullable=True)
    role_id = Column(Integer, nullable=True)
    role_name = Column(String(50), nullable=True)
    status = Column(String(50),nullable=True)