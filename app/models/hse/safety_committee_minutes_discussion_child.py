from sqlalchemy import (
    Column, Integer, String, Date, DateTime,
    ForeignKey, Text, func, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class SafetyCommitteeMinutesDiscussionChild(Base):
    __tablename__ = "safety_committee_minutes_discussion_child"

    scmdc_id = Column(Integer, primary_key=True, index=True)

    # ✅ FIXED → link to DISCUSSION (not minutes)
    discussion_id = Column(
        Integer,
        ForeignKey("safety_committee_minutes_discussions.id", ondelete="CASCADE"),
        nullable=False
    )

    issues_discussed = Column(Text, nullable=True)
    action_taken = Column(Text, nullable=True)

    completed_on = Column(Date, nullable=True)
    action_by = Column(String(255), nullable=True)
    target_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    discussion = relationship(
        "SafetyCommitteeMinutesDiscussion",
        back_populates="children"
    )