from sqlalchemy import Column, Integer, Text, DateTime, func
from app.database import Base


class JobSafetyAnalysisStepHistory(Base):
    __tablename__ = "job_safety_analysis_step_history"

    step_history_id = Column(Integer, primary_key=True, index=True)

    # REFERENCE TO ORIGINAL STEP AND PARENT
    step_id = Column(Integer, nullable=True)   # original step_id (nullable if step was deleted)
    jsa_id = Column(Integer, nullable=False)   # always keep jsa reference
    history_id = Column(Integer, nullable=False)  # link to parent history record

    # SNAPSHOT OF STEP
    row_no = Column(Integer, nullable=True)
    job_steps = Column(Text, nullable=True)
    potential_hazards = Column(Text, nullable=True)
    hazard_control_measures = Column(Text, nullable=True)
    ppe_required = Column(Text, nullable=True)

    # HISTORY TRACKING
    action = Column(Text, nullable=True)  # created / updated / deleted
    action_by = Column(Integer, nullable=True)
    action_at = Column(DateTime(timezone=True), server_default=func.now())