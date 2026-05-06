import datetime

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class HRActionHistory(Base):
    __tablename__ = "hr_action_history"
    history_id = Column(Integer, primary_key=True, index=True)
    id= Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=False)
    action_type = Column(String(100), nullable=False)
    action_date = Column(DateTime, nullable=False)
    justification = Column(Text, nullable=False)
    acknowledgement = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    comments =  Column(Text, nullable=True)