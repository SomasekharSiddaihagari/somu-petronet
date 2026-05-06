from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base
 
 
class InwardMaterialDetailHistory(Base):

    __tablename__ = "inward_material_details_history"
 
    id = Column(Integer, primary_key=True, index=True)

    inward_id = Column(Integer, ForeignKey("inward_gate_pass.inward_id", ondelete="CASCADE"))
 
    # --- Material Details ---

    description = Column(Text, nullable=False)

    ordered_quantity = Column(Float, nullable=False)

    received_quantity = Column(Float, nullable=False)

    unit = Column(String(50), nullable=True)

    remarks = Column(Text, nullable=True)

    goods_photo = Column(String(255), nullable=False)  # Per-material photo
 
    # --- Relationship ---

    inward_gate_pass = relationship("InwardGatePassHistory", back_populates="materials")
 
    def __repr__(self):

        return f"<InwardMaterialDetailHistory(id={self.id}, description='{self.description}', ordered_qty={self.ordered_quantity})>"

 