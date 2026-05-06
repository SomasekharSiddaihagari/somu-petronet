from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
 
class ReturnableMaterialDetail(Base):
    __tablename__ = "returnable_material_details"
 
    id = Column(Integer, primary_key=True, index=True)
    returnable_id = Column(Integer, ForeignKey("returnable_gate_pass.id", ondelete="CASCADE"), nullable=False)
 
    description = Column(Text, nullable=True)
    actual_quantity = Column(Float, nullable=False)
    received_quantity = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)
    condition = Column(String(50), nullable=True)
    remarks = Column(Text, nullable=True)
    goods_photo = Column(String(255), nullable=True)
    returned_goods_photo = Column(String(255), nullable=True)
 
    returnable_gate_pass = relationship("ReturnableGatePass", back_populates="materials")