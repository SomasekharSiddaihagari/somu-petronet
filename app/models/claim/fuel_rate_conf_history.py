from sqlite3 import Date
from sqlalchemy import (
 
    Column, BigInteger, Float, Integer, Numeric, String, DateTime
 
)
 
from sqlalchemy.sql import func
 
from app.database import Base
 
 
class FuelRateConfig(Base):
    __tablename__ = "fuel_rate_config_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    fuel_claim_id = Column(Integer, nullable=True)
    petrol_rate = Column(Float, nullable=True)
    others_rate = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
 