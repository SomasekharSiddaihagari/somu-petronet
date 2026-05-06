from sqlalchemy import (
    Column, BigInteger, String, Date, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class HRLeaveApplicationDay(Base):
    __tablename__ = "hr_leave_application_day"

    leave_day_id = Column(BigInteger, primary_key=True, autoincrement=True)

    leave_application_id = Column(
        BigInteger,
        ForeignKey("hr_leave_application.leave_id"),
        nullable=False
    )

    leave_date = Column(Date, nullable=True)
    day_type = Column(String(10), nullable=True)
    half_session = Column(String(20), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # RELATIONSHIP
    leave_application = relationship("HRLeaveApplication", back_populates="leave_days")
