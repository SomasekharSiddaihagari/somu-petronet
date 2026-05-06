import datetime

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
 

class HRActionDocument(Base):
    __tablename__ = "hr_action_documents"
    id = Column(Integer, primary_key=True, index=True)
    hr_action_id = Column(Integer, ForeignKey("hr_action.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    acknowledgement = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)