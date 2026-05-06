from sqlalchemy import Column, Integer, String, Date, DateTime, Text, func
from app.database import Base


class JobSafetyAnalysisHistory(Base):
    __tablename__ = "job_safety_analysis_history"

    history_id = Column(Integer, primary_key=True, index=True)

    # REFERENCE TO ORIGINAL
    jsa_id = Column(Integer, nullable=False)

    # SNAPSHOT OF PARENT
    date = Column(Date, nullable=True)
    jsa_no = Column(String(100), nullable=True)
    job_type = Column(String(255), nullable=True)
    work_permit_ref_no = Column(String(255), nullable=True)
    job_executed_by = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=True)
    job_location = Column(String(255), nullable=True)
    additional_comments = Column(Text, nullable=True)
    jsa_prepared_by = Column(String(255), nullable=True)
    jsa_reviewed_approved_by = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)
    station_id = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    # HISTORY TRACKING
    action = Column(String(50), nullable=True)  # created / updated / submitted / approved
    action_by = Column(Integer, nullable=True)
    action_at = Column(DateTime(timezone=True), server_default=func.now())
    remarks = Column(Text, nullable=True)