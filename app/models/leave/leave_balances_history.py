from sqlalchemy import Column, Integer, Numeric, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
 
Base = declarative_base()
 
class LeaveBalanceHistory(Base):
    __tablename__ = "leave_balances_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    balance_id = Column(Integer, nullable=True)
 
    user_id = Column(Integer, nullable=True)
    type_id = Column(Integer, nullable=True)
 
    allocated = Column(Numeric, nullable=True)
    used = Column(Numeric, nullable=True)
    balance = Column(Numeric, nullable=True)
 
    is_usable = Column(Boolean, nullable=True)
 
    created_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)