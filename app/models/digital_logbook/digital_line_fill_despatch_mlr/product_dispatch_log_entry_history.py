from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class ProductDispatchLogEntryHistory(Base):
    __tablename__ = "product_dispatch_log_entry_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(Integer, nullable=False) # Reference to original entry
    shift_log_id = Column(Integer, nullable=False)
    
    # SUCTION, LINE_FILL, CAPACITY
    entry_type = Column(String(50), nullable=True)

    # Common fields
    section_name = Column(String(100), nullable=True)
    product = Column(String(50), nullable=True)
    pmhbl_batch_no = Column(String(50), nullable=True)
    mrpl_batch_no = Column(String(50), nullable=True)
    quantity_kl = Column(Float, default=0.0)

    # Specific to Capacity
    section_capacity = Column(Float, default=0.0)
    section_current_fill = Column(Float, default=0.0)

    # Audit (from original)
    created_at = Column(DateTime)

    # History Fields
    history_at = Column(DateTime, server_default=func.now())
