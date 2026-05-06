
from sqlalchemy import Column, Integer, Boolean, DateTime, String
from app.database import Base
from datetime import datetime





class CircularUserActivityHistory(Base):
    __tablename__ = "circular_user_activity_history"

    history_id = Column(Integer, primary_key=True, index=True)
    circular_user_activity_id = Column(Integer, nullable=False)

    circular_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    is_read = Column(Boolean, default=False)
    is_acknowledged = Column(Boolean, default=False)

    read_at = Column(DateTime, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    action = Column(String, nullable=True)  # INSERT/UPDATE/DELETE