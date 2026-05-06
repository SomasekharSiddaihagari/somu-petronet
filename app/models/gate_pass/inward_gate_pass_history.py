from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
 
 
# class InwardGatePassHistory(Base):
#     __tablename__ = "inward_gate_pass_history"

#     inward_id = Column(Integer, primary_key=True, index=True)
#     # --- Basic Information ---
#     gate_pass_no = Column(String(50), nullable=False)
#     date_time = Column(DateTime, default=datetime.utcnow)
#     station = Column(String(100), nullable=False)
#     po_type = Column(String(50), nullable=False)  # "With PO" / "Without PO"
#     po_number = Column(String(100), nullable=True)
#     received_from = Column(String(150), nullable=False)
#     supplier_address = Column(Text, nullable=True)
#     purpose = Column(Text, nullable=False)
#     reference_document = Column(String(150), nullable=True)
#     vehicle_no = Column(String(50), nullable=True)
#     driver_name = Column(String(100), nullable=True)
#     driver_phone = Column(String(20), nullable=True)
#     # --- 3-Level Approval Section ---
#     security_guard = Column(String(100), nullable=False)
#     approver_name = Column(String(100), nullable=False)
#     # --- System Columns ---
#     status = Column(String(50), default="draft")  # draft / pending / approved / rejected
#     created_by = Column(String(100), nullable=False)
#     updated_by = Column(String(100), nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, onupdate=datetime.utcnow)
#     # --- Relationships ---
#     materials = relationship(
#         "InwardMaterialDetailHistory",
#         back_populates="inward_gate_pass",
#         cascade="all, delete-orphan"
#     )
 
#     photos = relationship(
#         "InwardGatePassPhotoHistory",
#         back_populates="inward_gate_pass",
#         cascade="all, delete-orphan"
#     )
class InwardGatePassHistory(Base):
    __tablename__ = "inward_gate_pass_history"

    inward_id = Column(Integer, primary_key=True, index=True)

    gate_pass_no = Column(String(50), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    station = Column(String(100), nullable=False)
    po_type = Column(String(50), nullable=False)
    po_number = Column(String(100))
    received_from = Column(String(150), nullable=False)
    supplier_address = Column(Text)
    purpose = Column(Text, nullable=False)
    reference_document = Column(String(150))
    vehicle_no = Column(String(50))
    driver_name = Column(String(100))
    driver_phone = Column(String(20))

    security_guard = Column(String(100), nullable=False)
    approver_name = Column(String(100), nullable=False)

    status = Column(String(50), default="draft")

    created_by = Column(String(100), nullable=False)
    updated_by = Column(String(100), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow) 
 
