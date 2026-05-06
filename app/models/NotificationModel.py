from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# app/models/notification_model.py
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, nullable=True)
    module_status = Column(String, nullable=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    from_user = Column(String, nullable=False)
    to_user = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    reference_id = Column(String, nullable=True)
    redirect_url = Column(String, nullable=True)
    