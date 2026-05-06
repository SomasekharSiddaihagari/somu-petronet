from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class OutwardGatePassPhoto(Base):
    __tablename__ = "outward_gate_pass_photos"

    id = Column(Integer, primary_key=True, index=True)
    outward_id = Column(Integer, ForeignKey("outward_gate_pass.outward_id", ondelete="CASCADE"), nullable=True)

    # --- Photo Documentation ---
    vehicle_photo = Column(String(255), nullable=True)
    delivery_personnel_photo = Column(String(255), nullable=True)
    delivery_personnel_id_photo = Column(String(255), nullable=True)
    goods_photo = Column(String(255), nullable=True)

    uploaded_by = Column(String(100), nullable=True)
    uploaded_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    outward_gate_pass = relationship("OutwardGatePass", back_populates="photos")

    def __repr__(self):
        return f"<OutwardGatePassPhoto(id={self.id}, outward_id={self.outward_id}, uploaded_by='{self.uploaded_by}')>"
