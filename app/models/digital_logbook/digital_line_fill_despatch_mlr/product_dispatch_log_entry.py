from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class ProductDispatchLogEntry(Base):
    __tablename__ = "product_dispatch_log_entry"

    entry_id = Column(Integer, primary_key=True, autoincrement=True)
    shift_log_id = Column(Integer, ForeignKey("product_dispatch_shift_log.shift_log_id", ondelete="CASCADE"), nullable=False)
    
    # Entry Type: 'SUCTION', 'LINE_FILL', or 'CAPACITY'
    entry_type = Column(String(20), nullable=False)
    
    # Common Fields
    section_name = Column(String(100), nullable=True)
    product = Column(String(100), nullable=True)
    pmhbl_batch_no = Column(String(100), nullable=True)
    mrpl_batch_no = Column(String(100), nullable=True)
    quantity_kl = Column(Float, nullable=True)
    
    # Specific to Capacity
    section_capacity = Column(Float, nullable=True)
    section_current_fill = Column(Float, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
