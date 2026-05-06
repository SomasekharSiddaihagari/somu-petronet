from sqlalchemy import Column, Integer, String, Float, Date, Time, DateTime, ForeignKey, func
from app.database import Base

class ProductDispatchHourlyLog(Base):
    __tablename__ = "product_dispatch_hourly_log"

    p_dispatch_hour_id = Column(Integer, primary_key=True, autoincrement=True)
    category_master_id = Column(Integer, ForeignKey("product_dispatch_category_master.p_category_master_id"), nullable=True)

    log_date = Column(Date, nullable=True)
    log_time = Column(Time, nullable=True)

    # Mangalore Station
    mangalore_product = Column(String(100), nullable=True)
    mangalore_tank = Column(String(100), nullable=True)
    mangalore_batch = Column(String(100), nullable=True)
    mangalore_volt = Column(Float, nullable=True)
    mangalore_curr = Column(Float, nullable=True)
    mangalore_ld = Column(Float, nullable=True)
    mangalore_temp = Column(Float, nullable=True)
    mangalore_den = Column(Float, nullable=True)
    mangalore_fmr = Column(Float, nullable=True)
    mangalore_ofc = Column(String(100), nullable=True)
    mangalore_rcil = Column(String(100), nullable=True)
    mangalore_flow = Column(Float, nullable=True)
    mangalore_dpg = Column(Float, nullable=True)

    # Neriya Station
    neriya_product = Column(String(100), nullable=True)
    neriya_batch = Column(String(100), nullable=True)
    neriya_fmr = Column(Float, nullable=True)
    neriya_flow = Column(Float, nullable=True)

    # Hassan Station
    hassan_product = Column(String(100), nullable=True)
    hassan_batch = Column(String(100), nullable=True)
    hassan_bpfmr = Column(Float, nullable=True)
    hassan_dfmr = Column(Float, nullable=True)
    hassan_flow = Column(Float, nullable=True)
    hassan_tank = Column(String(100), nullable=True)

    # Bangalore Station
    bangalore_product = Column(String(100), nullable=True)
    bangalore_batch = Column(String(100), nullable=True)
    bangalore_dfmr = Column(Float, nullable=True)
    bangalore_flow = Column(Float, nullable=True)
    bangalore_tank = Column(String(100), nullable=True)
    bangalore_omc = Column(String(100), nullable=True)

    # System
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)