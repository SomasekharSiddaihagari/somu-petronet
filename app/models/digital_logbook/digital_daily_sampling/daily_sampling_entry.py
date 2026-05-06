from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
class DailySamplingEntry(Base):
    __tablename__ = "daily_sampling_entry"
 
    sampling_entry_id = Column(Integer, primary_key=True, autoincrement=True)
 
    master_id = Column(
        Integer,
        ForeignKey("daily_sampling_master.sampling_id", ondelete="CASCADE"),
        nullable=True
    )
 
    sr_no = Column(Integer, nullable=True)
    date = Column(Date, nullable=True)
    sample_time = Column(Time, nullable=True)
 
    product = Column(String(100), nullable=True)
    batch_no = Column(String(100), nullable=True)
    tank = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    appearance = Column(String(100), nullable=True)
    colour = Column(String(100), nullable=True)
    temperature = Column(String(50), nullable=True)

 
    density = Column(String(50), nullable=True)
    kinematic_viscosity = Column(String(50), nullable=True)
    density_at_15c = Column(String(50), nullable=True)
    qc_density = Column(String(50), nullable=True)
    difference = Column(String(50), nullable=True)
 
    drawn_by = Column(String(100), nullable=True)
    reason_for_sample_testing = Column(String, nullable=True)
 
    disposal_date = Column(Date, nullable=True)
    disposed_by = Column(String(100), nullable=True)
    org_sign = Column(String, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)




    