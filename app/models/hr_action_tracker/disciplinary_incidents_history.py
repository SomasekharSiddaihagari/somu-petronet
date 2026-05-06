import datetime

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class DisciplinaryIncidentHistory(Base):
    __tablename__ = "disciplinary_incidents_history"
    history_id = Column(Integer, primary_key=True, index=True)
    disciplinary_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    incident_date = Column(DateTime, nullable=False)
    severity = Column(String(50), nullable=False)
    incident_details = Column(Text, nullable=False)
    investigation_finding = Column(Text, nullable=True)
    measures_taken = Column(Text, nullable=True)
    enable_suspension = Column(Boolean, default=False)
    enable_termination = Column(Boolean, default=False)
    suspension_effective_from = Column(DateTime, nullable=True)
    suspension_effective_to = Column(DateTime, nullable=True)
    termination_effective_from = Column(DateTime, nullable=True)
    outcome = Column(Text, nullable=True)
    acknowledgement = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    comments =  Column(Text, nullable=True) 