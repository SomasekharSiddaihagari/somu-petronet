from sqlalchemy import Column, Date, Integer, String, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class OutwardMaterialDetail(Base):
    __tablename__ = "outward_material_details"

    id = Column(Integer, primary_key=True, index=True)
    outward_id = Column(Integer, ForeignKey("outward_gate_pass.outward_id", ondelete="CASCADE"), nullable=True)

    # --- Material Details ---
    description = Column(Text, nullable=True)
    quantity = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)
    returnable = Column(Boolean, nullable=True)
    returnable_date = Column(Date, nullable=True)
    remarks = Column(Text, nullable=True)
    goods_photo = Column(String(255), nullable=True)

    outward_gate_pass = relationship("OutwardGatePass", back_populates="materials")

    def __repr__(self):
        return f"<OutwardMaterialDetail(id={self.id}, description='{self.description}', quantity={self.quantity})>"
