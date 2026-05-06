from sqlalchemy import Column, Integer, String, Date, Time, DateTime, func
from app.database import Base


class ProductDispatchCategory(Base):
    __tablename__ = "product_dispatch_category_master"

    p_category_master_id = Column(Integer, primary_key=True, autoincrement=True)

    station = Column(String(100), nullable=True)
    station_in_charge = Column(String(100), nullable=True)
    shift = Column(String(50), nullable=True)
    start_time = Column(Time, nullable=True)
    logbook_date = Column(Date, nullable=True)

    acknowledge_id = Column(String(255), nullable=True)
    acknowledge_date = Column(DateTime, nullable=True)
    acknowledge_by = Column(Integer, nullable=True)


    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
    ms_logbook_id = Column(Integer, nullable=True)
    technician_id = Column(Integer, nullable=True)
