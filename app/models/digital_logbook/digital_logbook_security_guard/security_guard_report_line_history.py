from sqlalchemy import (
    Column, DateTime, Integer, String, Time, Numeric, Text, ForeignKey, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class SecurityGuardReportLineHistory(Base):
    __tablename__ = "security_guard_report_line_history"

    sgrl_history_id = Column(Integer, primary_key=True, index=True)

    # 🔗 Link to HISTORY MASTER
    history_id = Column(
        Integer,
        ForeignKey("security_guard_report_history.history_id", ondelete="CASCADE"),
        nullable=False
    )

    # 🔗 Optional: reference to original line
    sgrl_id = Column(Integer, nullable=True)

    # =========================
    # ENTRY SNAPSHOT DATA
    # =========================
    location_name = Column(String(100), nullable=True)
    shift = Column(String(10), nullable=True)
    security_guard_name = Column(String(150), nullable=True)
    security_guard_name_two = Column(String(150), nullable=True)

    duty_start_time = Column(Time, nullable=True)
    duty_end_time = Column(Time, nullable=True)

    battery_cp_volt = Column(Numeric(10, 4), nullable=True)
    battery_tel_volt = Column(Numeric(10, 4), nullable=True)

    power_status = Column(String(50), nullable=True)
    report_details = Column(Text, nullable=True)
    officer_initials = Column(String(50), nullable=True)

    # =========================
    # RELATIONSHIP
    # =========================
    report = relationship(
        "SecurityGuardReportHistory",
        back_populates="lines"
    )

            # =========================
    # AUDIT
    # =========================
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)