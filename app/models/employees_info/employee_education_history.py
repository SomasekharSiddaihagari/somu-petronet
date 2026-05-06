from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.database import Base
from datetime import datetime
 
 
class UserEducationHistory(Base):
    __tablename__ = "user_education_history"
 
    history_id = Column(Integer, primary_key=True)
    education_id = Column(Integer)
    user_id = Column(Integer)
    submission_id = Column(
        Integer,
        nullable=True
    )
    qualification = Column(String, nullable=True)
    year_of_completion = Column(Integer, nullable=True)
    education_document = Column(String, nullable=True)
 
    created_at = Column(DateTime)
    history_created_at = Column(DateTime, default=datetime.utcnow)
    changed_fields = Column(JSON, nullable=True, server_default='[]')