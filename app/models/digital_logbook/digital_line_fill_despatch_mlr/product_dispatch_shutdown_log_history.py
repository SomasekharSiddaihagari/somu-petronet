from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from app.database import Base


class ProductDispatchShutdownLogHistory(Base):
    __tablename__ = "product_dispatch_shutdown_log_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    p_dispatch_shutdown_id = Column(Integer, nullable=True)
    category_master_id = Column(Integer, nullable=True)
    log_date = Column(Date, nullable=True)

    # Shift Metrics
    shift_a_from = Column(Float, nullable=True)
    shift_a_to = Column(Float, nullable=True)
    shift_a_subtotal = Column(Float, nullable=True)

    shift_b_from = Column(Float, nullable=True)
    shift_b_to = Column(Float, nullable=True)
    shift_b_subtotal = Column(Float, nullable=True)

    shift_c_from = Column(Float, nullable=True)
    shift_c_to = Column(Float, nullable=True)
    shift_c_subtotal = Column(Float, nullable=True)

    # Summary Information
    total = Column(Float, nullable=True)
    pre_sd_hrs = Column(Float, nullable=True)
    cumulative = Column(Float, nullable=True)
    reason_remarks = Column(String(255), nullable=True)

    # System Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
