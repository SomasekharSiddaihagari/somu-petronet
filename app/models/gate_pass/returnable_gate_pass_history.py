from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ReturnableGatePassHistory(Base):
    __tablename__ = "returnable_gate_pass_history"

    returnable_id = Column(Integer, primary_key=True, index=True)
    returnable_gate_pass_no = Column(String(50), nullable=False, unique=True)

    # ✅ Reference to outward history table
    outward_id = Column(Integer, ForeignKey("outward_gate_pass.outward_id", ondelete="CASCADE"), nullable=False)

    # --- Return-specific fields ---
    approved_by = Column(String(100), nullable=False)
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(50), nullable=False, default="pending")
    created_by = Column(String(100), nullable=False)
    updated_by = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    gate_pass_no = Column(String(50), nullable=True, unique=False)
    date_time_ret = Column(DateTime, nullable=True)
    station = Column(String(100), nullable=True)
    department_contractor_name = Column(String(150), nullable=True)
    purpose = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    material_taken_by = Column(String(100), nullable=True)
    vehicle_no = Column(String(50), nullable=True)
    driver_phone = Column(String(20), nullable=True)
    # --- Relationships ---
    outward_gate_pass = relationship("OutwardGatePassHistory", back_populates="returnable_passes")
    materials = relationship("ReturnableMaterialDetailHistory", back_populates="returnable_gate_pass", cascade="all, delete-orphan")
    photos = relationship("ReturnableGatePassPhotoHistory", back_populates="returnable_gate_pass", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ReturnableGatePassHistory(id={self.returnable_id}, returnable_no='{self.returnable_gate_pass_no}', outward_id={self.outward_id})>"
