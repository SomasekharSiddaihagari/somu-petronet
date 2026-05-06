from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ReturnableGatePassPhotoHistory(Base):
    __tablename__ = "returnable_gate_pass_photos_history"

    id = Column(Integer, primary_key=True, index=True)
    returnable_id = Column(Integer, ForeignKey("returnable_gate_pass.returnable_id", ondelete="CASCADE"), nullable=False)

    vehicle_photo = Column(String(255), nullable=False)
    delivery_personnel_photo = Column(String(255), nullable=False)
    delivery_personnel_id_photo = Column(String(255), nullable=False)
    goods_photo = Column(String(255), nullable=False)
    uploaded_by = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    returnable_gate_pass = relationship("ReturnableGatePassHistory", back_populates="photos")

    def __repr__(self):
        return f"<ReturnableGatePassPhotoHistory(id={self.id}, returnable_id={self.returnable_id}, uploaded_by='{self.uploaded_by}')>"
