from sqlalchemy import Column, Integer, Numeric, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
 
Base = declarative_base()
 
class LeaveBalance(Base):
    __tablename__ = "leave_balances"
 
    balance_id = Column(Integer, primary_key=True)
 
    user_id = Column(Integer, nullable=True)
    type_id = Column(Integer, nullable=True)
 
    allocated = Column(Numeric, nullable=True)
    used = Column(Numeric, default=0, nullable=True)
    balance = Column(Numeric, nullable=True)
 
    is_usable = Column(Boolean, default=True, nullable=True)
 
    created_date = Column(DateTime, default=func.now(), nullable=True)