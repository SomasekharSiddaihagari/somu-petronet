from sqlalchemy import Column, Integer, Date, Time, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
 
class KPTCLHSNEntry(Base):
    __tablename__ = "kptcl_hsn_entry"

    kptcl_hsn_entry_id = Column(Integer, primary_key=True, autoincrement=True)

    master_id = Column(
        Integer,
        ForeignKey("kptcl_hsn_master.kptcl_hsn_id", ondelete="CASCADE"),
        nullable=True
    )
 
    reading_date = Column(Date, nullable=True)
    reading_time = Column(Time, nullable=True)
 
    t1c_kwh = Column(Numeric(14, 3), nullable=True)
    t1c_kvah = Column(Numeric(14, 3), nullable=True)
 
    calculated_pf = Column(Numeric(10, 4), nullable=True)
    t1pr_pf = Column(Numeric(10, 4), nullable=True)
    t1pr_kva = Column(Numeric(10, 4), nullable=True)
    

    initial_final_kwh = Column(Numeric(14, 3), nullable=True)

    initial_final_kvah = Column(Numeric(14, 3), nullable=True)

    kwh_kvah = Column(Numeric(14, 3), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)