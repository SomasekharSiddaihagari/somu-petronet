from sqlalchemy import Column, Integer, Date, String, Time, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
 
 
class KPTCLNEREntry(Base):
    __tablename__ = "kptcl_ner_entry"
 
    kptcl_ner_id = Column(Integer, primary_key=True, autoincrement=True)
 
    master_id = Column(
        Integer,
        ForeignKey("kptcl_ner_master.kptcl_ner_id", ondelete="CASCADE"),
        nullable=True
    )
 
    reading_date = Column(Date, nullable=True)
    reading_time = Column(Time, nullable=True)
 
    kwh = Column(Numeric(14, 3), nullable=True)
    kvah = Column(Numeric(14, 3), nullable=True)
 
    pf_meter = Column(Numeric(10, 4), nullable=True)
 
    calculated_pf_day = Column(String(50), nullable=True)      # Auto
    calculated_pf_month = Column(String(50), nullable=True)    # Auto
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime,nullable=True)
    updated_by = Column(Integer, nullable=True)