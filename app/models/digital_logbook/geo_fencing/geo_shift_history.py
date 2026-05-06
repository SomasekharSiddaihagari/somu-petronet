from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Float, Time, Enum, UniqueConstraint, CheckConstraint
)
from sqlalchemy.sql import func
from app.database import Base
import enum

class Shift(Base):
    __tablename__ = "shift_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    shift_id = Column(Integer, nullable=True)
    shift_name = Column(String(50), nullable=False, unique=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)