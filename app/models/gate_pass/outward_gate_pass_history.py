from sqlalchemy import Column, Date, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class OutwardGatePassHistory(Base):
    __tablename__ = "outward_gate_pass_history"

    outward_id = Column(Integer, primary_key=True, index=True)

    # --- Basic Information ---
    gate_pass_no = Column(String(50), nullable=False)
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    station = Column(String(100), nullable=False)
    issuing_authority = Column(String(150), nullable=False)
    department_contractor_name = Column(String(150), nullable=False)
    purpose = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    material_taken_by = Column(String(100), nullable=False)
    vehicle_no = Column(String(50), nullable=False)
    driver_phone = Column(String(20), nullable=False)

    # --- Approval Section ---
    initiator_name = Column(String(100), nullable=False)
    approver_name = Column(String(100), nullable=False)
    approved_at = Column(DateTime, nullable=True)

    # --- System Columns ---
    status = Column(String(50), nullable=False, default="draft")
    created_by = Column(String(100), nullable=False)
    updated_by = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)

    # --- Relationships ---
    materials = relationship(
        "OutwardMaterialDetailHistory",
        back_populates="outward_gate_pass",
        cascade="all, delete-orphan"
    )

    photos = relationship(
        "OutwardGatePassPhotoHistory",
        back_populates="outward_gate_pass",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<OutwardGatePassHistory(outward_id={self.outward_id}, gate_pass_no='{self.gate_pass_no}', station='{self.station}')>"
