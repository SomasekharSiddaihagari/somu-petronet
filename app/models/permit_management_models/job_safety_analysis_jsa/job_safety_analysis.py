from sqlalchemy import Column, Integer, String, Date, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.database import Base

class JobSafetyAnalysis(Base):
    __tablename__ = "job_safety_analysis"

    jsa_id = Column(Integer, primary_key=True, index=True)

    # JOB DETAILS
    date = Column(Date, nullable=True)
    jsa_no = Column(String(100), nullable=True)
    job_type = Column(String(255), nullable=True)
    work_permit_ref_no = Column(String(255), nullable=True)
    job_executed_by = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=True)
    job_location = Column(String(255), nullable=True)

    # ADDITIONAL COMMENTS
    additional_comments = Column(Text, nullable=True)

    # JSA PREPARED BY
    jsa_prepared_by = Column(String(255), nullable=True)

    # JSA REVIEWED & APPROVED BY
    jsa_reviewed_approved_by = Column(String(255), nullable=True)

    # STATUS
    status = Column(String(50), nullable=True, default="draft")

    # AUDIT
    station_id = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # RELATIONSHIP
    job_steps = relationship(
        "JobSafetyAnalysisStep",
        back_populates="jsa",
        cascade="all, delete-orphan"
    )
    
    