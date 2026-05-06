from sqlalchemy import (
    Boolean, Column, BigInteger, Date, DateTime, Integer, String
)
from sqlalchemy.sql import func
from app.database import Base


class HRLeaveCompOffDay_New_History(Base):
    __tablename__ = "hr_leave_compof_day_new_history"

    history_id = Column(BigInteger, primary_key=True, autoincrement=True)

    id = Column(BigInteger, nullable=False)

    employee_name = Column(String(150), nullable=True)
    employee_code = Column(String(50), nullable=True)
    is_used = Column(Boolean, default=False, nullable=True) 
    leave_application_id = Column(BigInteger, nullable=True)
    leave_date = Column(Date, nullable=True)

    station_id = Column(Integer, nullable=True)
    type_id = Column(Integer, nullable=True)
    user_id = Column(
        nullable=False,
        index=True
    )

    supervisor_id = Column(
        BigInteger,
        nullable=True
    )
    action = Column(String(20), nullable=False)
    action_by = Column(String(100), nullable=True)

    action_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )