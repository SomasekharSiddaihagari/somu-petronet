from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class Station(Base):
    __tablename__ = "station"

    station_id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String(100), nullable=False)
    station_code = Column(String(50), unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    users = relationship("User", back_populates="station")
