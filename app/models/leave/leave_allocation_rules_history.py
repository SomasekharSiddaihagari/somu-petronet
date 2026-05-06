from sqlalchemy import Column, Integer, Boolean, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
 
Base = declarative_base()
 
class LeaveAllocationRuleHistory(Base):
    __tablename__ = "leave_allocation_rules_history"
 
    history_id = Column(Integer, primary_key=True, autoincrement=True)
 
    allocation_id = Column(Integer, nullable=True)
 
    employee_type_id = Column(Integer, nullable=True)
    leave_type_id = Column(Integer, nullable=True)
 
    allow = Column(Boolean, nullable=True)
    pro_rata = Column(Boolean, nullable=True)
 
    annual_allotment = Column(Integer, nullable=True)
    quarterly_allotment = Column(Integer, nullable=True)
    max_limit = Column(Integer, nullable=True)
 
    special_rules = Column(JSON, nullable=True)
 
    created_at = Column(DateTime, server_default=func.now(), nullable=True)