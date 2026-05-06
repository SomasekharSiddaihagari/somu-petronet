from sqlalchemy import (
    Column, BigInteger, Date, DateTime, String
)
from sqlalchemy.sql import func
from app.database import Base
 
 
class HRLeaveCompOffDayHistory(Base):
    __tablename__ = "hr_leave_compof_day_history"
 
    history_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
 
    leave_compof_id = Column(
        BigInteger,
        nullable=False
    )
 
    leave_application_id = Column(
        BigInteger,
        nullable=False
    )
 
    leave_date = Column(
        Date,
        nullable=True
    )
 
    action = Column(
        String(20),
        nullable=False
    )  
    # CREATED / UPDATED / DELETED
 
    action_by = Column(
        BigInteger,
        nullable=True
    )
 
    action_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )