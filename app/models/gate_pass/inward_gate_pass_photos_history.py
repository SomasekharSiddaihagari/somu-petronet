from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
 
 
class InwardGatePassPhotoHistory(Base):
    __tablename__ = "inward_gate_pass_photos_history"
 
    id = Column(Integer, primary_key=True, index=True)
    inward_id = Column(Integer, ForeignKey("inward_gate_pass.inward_id", ondelete="CASCADE"))
 
    # --- Photo Documentation ---
    vehicle_photo = Column(String(255), nullable=True)
    delivery_personnel_photo = Column(String(255), nullable=True)
    delivery_personnel_id_photo = Column(String(255), nullable=True)
    goods_photo = Column(String(255), nullable=True)  # Overall goods photo (not per item)
 
    uploaded_by = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
 
    inward_gate_pass = relationship("InwardGatePassHistory", back_populates="photos")
 
    def __repr__(self):
        return f"<InwardGatePassPhotoHistory(id={self.id}, inward_id={self.inward_id}, uploaded_by='{self.uploaded_by}')>"