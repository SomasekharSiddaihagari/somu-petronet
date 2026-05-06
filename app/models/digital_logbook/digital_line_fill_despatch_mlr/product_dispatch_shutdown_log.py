from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from app.database import Base


class ProductDispatchShutdownLog(Base):
    __tablename__ = "product_dispatch_shutdown_log"

    p_dispatch_shutdown_id = Column(Integer, primary_key=True, autoincrement=True)
    category_master_id = Column(
        Integer,
        ForeignKey("product_dispatch_category_master.p_category_master_id"),
        nullable=True,
    )
    log_date = Column(Date, nullable=True)

    # SHIFT A
    shift_a_from = Column(Float, nullable=True)
    shift_a_to = Column(Float, nullable=True)
    shift_a_subtotal = Column(Float, nullable=True)

    # SHIFT B
    shift_b_from = Column(Float, nullable=True)
    shift_b_to = Column(Float, nullable=True)
    shift_b_subtotal = Column(Float, nullable=True)

    # SHIFT C
    shift_c_from = Column(Float, nullable=True)
    shift_c_to = Column(Float, nullable=True)
    shift_c_subtotal = Column(Float, nullable=True)

    # SUMMARY
    total = Column(Float, nullable=True)
    pre_sd_hrs = Column(Float, nullable=True)
    cumulative = Column(Float, nullable=True)
    reason_remarks = Column(String(255), nullable=True)

    # SYSTEM
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
