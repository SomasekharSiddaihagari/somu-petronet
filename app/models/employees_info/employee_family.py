from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text,JSON
from sqlalchemy.orm import relationship
from app.database import Base

class EmployeeFamily(Base):
    __tablename__ = "employee_family"

    ef_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    submission_id = Column(
        Integer,
        ForeignKey("submission.submission_id"),
        nullable=True
    )

    relation = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    document = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    place_of_birth = Column(String, nullable=True)
    date_of_marriage = Column(Date, nullable=True)
    document_details = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    status = Column(String, nullable=True)
    changed_fields = Column(JSON, nullable=True, server_default='[]')

    # ✅ FIX HERE
    submission = relationship(
        "FamilySubmission",
        back_populates="family_members"
    )

    user = relationship("User", back_populates="family_members")
























