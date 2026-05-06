from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class HIRAEntryHistory(Base):
    __tablename__ = "hira_history"
 
    hira_id = Column(Integer, primary_key=True, index=True)
    moc_request_id = Column(Integer, ForeignKey("moc_request_history.moc_request_id", ondelete="CASCADE"), nullable=False)
 
    activity = Column(String(255), nullable=False)
    hazard = Column(String(255), nullable=False)
    risk_level = Column(String(50), nullable=False)
    consequence = Column(String(255), nullable=False)
    control_measures = Column(Text, nullable=False)
 
    comments_initiator = Column(Text, nullable=True)
    hira_reviewer_id = Column(Integer, nullable=True)
    status = Column(String(50), default="draft")
 
    # Relationship to request history
    moc_request = relationship("MoCRequestHistory", back_populates="hira_entries")
 
    def __repr__(self):
        return f"<HIRAEntryHistory(id={self.hira_id}, activity='{self.activity}', risk='{self.risk_level}')>"
