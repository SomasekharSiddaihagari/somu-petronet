from sqlalchemy import Column, Integer, Date, DateTime, Boolean, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class ReviewDigitalLogs(Base):
    __tablename__ = "review_digital_logs"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, nullable=False, unique=True, index=True)

    # Acknowledgement fields
    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledged_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    is_acknowledged = Column(Boolean, default=False)

    # Audit fields
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    station = Column(String(255), nullable=True)
