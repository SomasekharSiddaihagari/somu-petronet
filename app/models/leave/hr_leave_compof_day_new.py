from sqlalchemy import (
    Boolean, Column, BigInteger, Date, DateTime, ForeignKey, Integer, String
)
from sqlalchemy.sql import func
from app.database import Base


class HRLeaveCompOffDay_New(Base):
    __tablename__ = "hr_leave_compof_day_new"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    employee_name = Column(String(150), nullable=True)
    employee_code = Column(String(50), nullable=True)

    leave_application_id = Column(
        BigInteger,
        ForeignKey("hr_leave_application.leave_id", ondelete="CASCADE"),
        nullable=True
    )

    leave_date = Column(Date, nullable=True)
    is_used = Column(Boolean, default=False, nullable=True) 
    station_id = Column(Integer, nullable=True)
    type_id = Column(Integer, nullable=True)
    user_id = Column(
        BigInteger,
        nullable=True,
    )

    supervisor_id = Column(
        BigInteger,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )