from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class HIRAEntry(Base):
    __tablename__ = "hira_entries"
 
    hira_id = Column(Integer, primary_key=True, index=True)
    moc_request_id = Column(Integer, ForeignKey("moc_requests.moc_request_id", ondelete="CASCADE"), nullable=False)
 
    activity = Column(String(255), nullable=False)
    hazard = Column(String(255), nullable=False)
    risk_level = Column(String(50), nullable=False)
    consequence = Column(String(255), nullable=False)
    control_measures = Column(Text, nullable=False)
 
    comments_initiator = Column(Text, nullable=True)
    hira_reviewer_id = Column(Integer, nullable=True)
    status = Column(String(50), default="draft")
 
    moc_request = relationship("MoCRequest", back_populates="hira_entries")
 
    def __repr__(self):
        return f"<HIRAEntry(id={self.hira_id}, activity='{self.activity}', risk='{self.risk_level}')>"
