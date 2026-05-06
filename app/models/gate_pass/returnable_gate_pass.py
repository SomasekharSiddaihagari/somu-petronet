from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base
 
class ReturnableGatePass(Base):

    __tablename__ = "returnable_gate_pass"
 
    returnable_id = Column(Integer, primary_key=True, index=True)
    
    returnable_gate_pass_no = Column(String(50), nullable=False, unique=True)

    outward_id = Column(Integer, ForeignKey("outward_gate_pass.id", ondelete="CASCADE"), nullable=False)
 
    # Only return-specific fields

    approved_by = Column(String(100), nullable=False)
    reviewer_id = Column(Integer, nullable=True)
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
    # Relationships
    returnable_passes = relationship(
            "ReturnableGatePass",
            back_populates="outward_gate_pass",
            cascade="all, delete-orphan"
        )

    outward_gate_pass = relationship("OutwardGatePass", back_populates="returnable_passes")

    materials = relationship("ReturnableMaterialDetail", back_populates="returnable_gate_pass", cascade="all, delete-orphan")

    photos = relationship("ReturnableGatePassPhoto", back_populates="returnable_gate_pass", cascade="all, delete-orphan")
 
    def __repr__(self):

        return f"<ReturnableGatePass(id={self.id}, returnable_no='{self.returnable_gate_pass_no}', outward_id={self.outward_id})>"

