from sqlalchemy import (
 
    Column, BigInteger, Date, DateTime, ForeignKey
 
)
 
from sqlalchemy.sql import func
 
from app.database import Base
 
 
class HRLeaveCompOffDay(Base):
 
    __tablename__ = "hr_leave_compof_day"
 
    leave_compof_id = Column(
 
        BigInteger,
 
        primary_key=True,
 
        autoincrement=True
 
    )
 
    leave_application_id = Column(
 
        BigInteger,
 
        ForeignKey(
 
            "hr_leave_application.leave_id",
 
            ondelete="CASCADE"
 
        ),
 
        nullable=False
 
    )
 
    leave_date = Column(
 
        Date,
 
        nullable=True
 
    )
 
    created_at = Column(
 
        DateTime(timezone=True),
 
        server_default=func.now(),
 
        nullable=False
 
    )
 