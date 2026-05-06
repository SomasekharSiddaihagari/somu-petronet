from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ReturnableMaterialDetailHistory(Base):
    __tablename__ = "returnable_material_details_history"

    id = Column(Integer, primary_key=True, index=True)
    returnable_id = Column(Integer, ForeignKey("returnable_gate_pass.returnable_id", ondelete="CASCADE"), nullable=False)

    description = Column(Text, nullable=True)
    actual_quantity = Column(Float, nullable=False)
    received_quantity = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)
    condition = Column(String(50), nullable=True)
    remarks = Column(Text, nullable=True)
    goods_photo = Column(String(255), nullable=True)
    returned_goods_photo = Column(String(255), nullable=True)

    returnable_gate_pass = relationship("ReturnableGatePassHistory", back_populates="materials")

    def __repr__(self):
        return f"<ReturnableMaterialDetailHistory(id={self.id}, returnable_id={self.returnable_id}, description='{self.description}')>"
