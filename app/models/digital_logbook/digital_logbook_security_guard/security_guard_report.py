from sqlalchemy import (
    Column, Integer, String, Date, Time, DateTime, Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class SecurityGuardReport(Base):
    __tablename__ = "security_guard_report"

    security_guard_id = Column(Integer, primary_key=True, index=True)

    # =========================
    # HEADER (MASTER FIELDS)
    # =========================
    station_name = Column(String(100), nullable=True)
    station_incharge_name = Column(String(150), nullable=True)
    shift_code = Column(String(20), nullable=True)
    shift_start_time = Column(Time, nullable=True)
    log_date = Column(Date, nullable=True)
    document_number = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)

    # =========================
    # FOOTER
    # =========================
    critical_report = Column(Text, nullable=True)

    # =========================
    # RELATIONSHIP
    # =========================
    lines = relationship(
        "SecurityGuardReportLine",
        back_populates="report",
        cascade="all, delete-orphan"
    )

    # =========================
    # AUDIT
    # =========================
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)