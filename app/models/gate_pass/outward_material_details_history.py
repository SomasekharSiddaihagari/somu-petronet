from sqlalchemy import Column, Date, Integer, String, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OutwardMaterialDetailHistory(Base):
    __tablename__ = "outward_material_details_history"

    id = Column(Integer, primary_key=True, index=True)

    # ✅ Corrected FK reference
    outward_id = Column(Integer, ForeignKey("outward_gate_pass.outward_id", ondelete="CASCADE"), nullable=False)

    description = Column(Text, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    returnable = Column(Boolean, nullable=False)
    returnable_date = Column(Date, nullable=True)
    remarks = Column(Text, nullable=False)
    goods_photo = Column(String(255), nullable=False)

    # ✅ Corrected relationship class name
    outward_gate_pass = relationship("OutwardGatePassHistory", back_populates="materials")

    def __repr__(self):
        return f"<OutwardMaterialDetailHistory(id={self.id}, description='{self.description}', quantity={self.quantity})>"
