from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Tank10KLFfeEntry(Base):
    __tablename__ = "tank_10kl_ffe_entry"

    tank_ffe_entry_id = Column(Integer, primary_key=True, autoincrement=True)

    master_id = Column(
        Integer,
        ForeignKey("tank_10kl_ffe_master.tank_ffe_id", ondelete="CASCADE"),
        nullable=True,
    )

    entry_date = Column(DateTime, nullable=True)

    opening_dip = Column(Float, nullable=True)
    opening_qty = Column(Float, nullable=True)

    qtv_10kl = Column(Float, nullable=True)
    received_250kva = Column(Float, nullable=True)

    fe_01 = Column(Float, nullable=True)
    fe_02 = Column(Float, nullable=True)
    fe_03 = Column(Float, nullable=True)

    sv_08 = Column(Float, nullable=True)
    ip = Column(Float, nullable=True)
    sv_09 = Column(Float, nullable=True)
    sv_10 = Column(Float, nullable=True)

    final_dip = Column(Float, nullable=True)
    final_qty = Column(Float, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
