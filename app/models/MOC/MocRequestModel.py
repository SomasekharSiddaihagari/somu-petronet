from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class MoCRequest(Base):
    __tablename__ = "moc_requests"

    moc_request_id = Column(Integer, primary_key=True, index=True)
    moc_request_no = Column(String(120), unique=True, nullable=False, index=True)
    station_name = Column(String(150), nullable=False)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)

    priority = Column(String(40), nullable=False)
    modification_type = Column(String(40), nullable=False)
    time_limit = Column(String(80), nullable=True)
    shutdown_required = Column(String(20), default="No")
    
    present_system = Column(Text, nullable=True)
    proposed_change = Column(Text, nullable=False)
    justification = Column(Text, nullable=False)
    objectives = Column(Text, nullable=True)

    other_units_impacted = Column(String(40), nullable=False)
    statutory_approval_required = Column(String(40), default="No")
    statutory_approval_details = Column(Text, nullable=True)
    impact_of_modification = Column(Text, nullable=False)
    consequences_non_implementation = Column(Text, nullable=False)

    hse = Column(Boolean, default=False)
    efficiency = Column(Boolean, default=False)
    quality = Column(Boolean, default=False)
    reliability = Column(Boolean, default=False)
    other_aspects = Column(Text, nullable=True)

    objectives_achieved = Column(String(40), nullable=True)
    attachments = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    reviewer_comments = Column(Text, nullable=True)
    approver_comments = Column(Text, nullable=True)
    submission_date = Column(DateTime,nullable=True)
    hira_approved_date = Column(DateTime,nullable=True)
    sic_approved_date = Column(DateTime,nullable=True)
    approved_date = Column(DateTime,nullable=True)
    sic_comments = Column(Text, nullable=True)

    closure_date = Column(DateTime,nullable=True)
    closure_comments =  Column(Text, nullable=True)

    status = Column(String(50), default="draft")
    is_active = Column(Boolean, default=True)
    short_text = Column(String(40), nullable=True)
    created_by = Column(String(50), nullable=True)
    updated_by = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (no cascade delete to protect data)
    hira_entries = relationship("HIRAEntry", back_populates="moc_request", cascade="save-update, merge")
    closure = relationship("MoCClosure", back_populates="moc_request", uselist=False)
    histories = relationship("MoCRequestHistory", back_populates="moc_request", cascade="save-update, merge")

