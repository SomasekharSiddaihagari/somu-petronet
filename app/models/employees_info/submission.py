from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
 
 
class FamilySubmission(Base):
    __tablename__ = "submission"

    submission_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    status = Column(String, default="Draft")
    hr_comment = Column(String, nullable=True)

    reviewed_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    family_members = relationship(
        "EmployeeFamily",
        back_populates="submission",
        cascade="all, delete-orphan"
    )
    education_detail = relationship(
        "UserEducation",
        back_populates="submission",
        cascade="all, delete-orphan"
    )
