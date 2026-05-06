from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class JobSafetyAnalysisStep(Base):
    __tablename__ = "job_safety_analysis_steps"

    step_id = Column(Integer, primary_key=True, index=True)

    # FK to parent
    jsa_id = Column(
        Integer,
        ForeignKey("job_safety_analysis.jsa_id", ondelete="CASCADE"),
        nullable=False
    )

    # STEP DETAILS
    row_no = Column(Integer, nullable=True)
    job_steps = Column(Text, nullable=True)
    potential_hazards = Column(Text, nullable=True)
    hazard_control_measures = Column(Text, nullable=True)
    ppe_required = Column(Text, nullable=True)

    # AUDIT
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # RELATIONSHIP
    jsa = relationship("JobSafetyAnalysis", back_populates="job_steps")