from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class SafetyCommitteeMinutesDiscussion(Base):
    __tablename__ = "safety_committee_minutes_discussions"
 
    id = Column(Integer, primary_key=True,autoincrement=True)
    scmm_id = Column(Integer, ForeignKey("safety_committee_minutes.scmm_id", ondelete="CASCADE"))
 
    # ✅ which row (1–10 from UI)
    row_no = Column(Integer, nullable=False)
 
    description_of_discussion = Column(Text)
    issues_discussed = Column(Text)
    action_taken = Column(Text)
    completed_on = Column(Date)
    action_by = Column(String(255))
    target_date = Column(Date)
    user_id = Column(Integer, index=True, nullable=True)
 
    minutes = relationship("SafetyCommitteeMinutes", back_populates="discussions")