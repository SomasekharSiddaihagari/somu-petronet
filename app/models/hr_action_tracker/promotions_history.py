import datetime

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class PromotionHistory(Base):
    __tablename__ = "promotions_history"
    history_id = Column(Integer, primary_key=True, index=True)
    id= Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=False)
    current_grade = Column(String(50), nullable=False)
    new_grade = Column(String(50), nullable=False)
    current_designation = Column(String(100), nullable=False)
    new_designation = Column(String(100), nullable=False)
    effective_date = Column(DateTime, nullable=False)
    remarks = Column(Text, nullable=True)
    acknowledgement = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    comments =  Column(Text, nullable=True)