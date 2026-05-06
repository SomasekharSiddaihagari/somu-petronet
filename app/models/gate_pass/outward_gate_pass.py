from sqlalchemy import Column, Date, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class OutwardGatePass(Base):
    __tablename__ = "outward_gate_pass"

    outward_id = Column(Integer, primary_key=True, index=True)

    # --- Basic Information ---
    gate_pass_no = Column(String(50), nullable=True, unique=False)
    date_time = Column(DateTime, nullable=True, default=datetime.utcnow)
    station = Column(String(100), nullable=True)
    issuing_authority = Column(String(150), nullable=True)
    department_contractor_name = Column(String(150), nullable=True)
    purpose = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    material_taken_by = Column(String(100), nullable=True)
    vehicle_no = Column(String(50), nullable=True)
    driver_phone = Column(String(20), nullable=True)

    # --- Approval Section ---
    initiator_name = Column(String(100), nullable=True)
    approver_name = Column(String(100), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    # --- System Columns ---
    status = Column(String(50), nullable=True, default="draft")
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=True)

    # --- Relationships ---
    materials = relationship(
        "OutwardMaterialDetail",
        back_populates="outward_gate_pass",
        cascade="all, delete-orphan"
    )

    photos = relationship(
        "OutwardGatePassPhoto",
        back_populates="outward_gate_pass",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<OutwardGatePass(outward_id={self.outward_id}, gate_pass_no='{self.gate_pass_no}', station='{self.station}')>"
