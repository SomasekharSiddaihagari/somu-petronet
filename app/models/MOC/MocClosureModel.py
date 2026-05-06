from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class MoCClosure(Base):
    __tablename__ = "moc_closures"

    moc_closure_id = Column(Integer, primary_key=True, index=True)
    moc_request_id = Column(Integer, ForeignKey("moc_requests.moc_request_id"), nullable=False)
    moc_request_no = Column(String(120), nullable=False, index=True)
    title_of_moc = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    brief_description = Column(Text)

    moc_initiator_dept = Column(String(120), nullable=False)
    executing_dept = Column(String(120), nullable=False)
    moc_execution_details = Column(Text)

    job_start_date = Column(Date, nullable=False)
    job_completion_date = Column(Date, nullable=False)

    hira_recommendation_status = Column(String(120), nullable=False)
    revised_operating_procedure = Column(String(200), nullable=False)
    training_completed = Column(String(200), nullable=False)
    relevant_manuals = Column(String(200))
    comments_initiator = Column(Text)
    status = Column(String(50), default="draft")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    moc_request = relationship("MoCRequest", back_populates="closure")

    # ✅ Correct relationship to MoCRequestHistory
    histories = relationship(
        "MoCRequestHistory",
        back_populates="closure",
        primaryjoin="MoCClosure.moc_closure_id == MoCRequestHistory.moc_closure_id"
    )
