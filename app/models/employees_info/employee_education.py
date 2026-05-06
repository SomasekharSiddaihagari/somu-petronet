from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
 
 
from datetime import datetime

class UserEducation(Base):
    __tablename__ = "user_education"
 
    education_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    submission_id = Column(
        Integer,
        ForeignKey("submission.submission_id"),
        nullable=True
    )
 
    qualification = Column(String, nullable=True)
    year_of_completion = Column(Integer, nullable=True)
    education_document = Column(String, nullable=True)
    status = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    changed_fields = Column(JSON, nullable=True, server_default='[]')

    submission = relationship(
        "FamilySubmission",
        back_populates="education_detail"
    )

    user = relationship(
        "User",
        back_populates="education_detail"
    )








