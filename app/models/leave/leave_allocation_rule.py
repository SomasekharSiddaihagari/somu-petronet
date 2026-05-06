from sqlalchemy import Column, Integer, Boolean, JSON, String
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class LeaveAllocationRule(Base):
    __tablename__ = "leave_allocation_rules"
 
    allocation_id = Column(Integer, primary_key=True)
 
    employee_type = Column(String, nullable=True)  
    leave_type_id = Column(Integer, nullable=True)
 
    allow = Column(Boolean, default=True, nullable=True)
    pro_rata = Column(Boolean, default=False, nullable=True)
 
    annual_allotment = Column(Integer, nullable=True)
    quarterly_allotment = Column(Integer, nullable=True)
    max_limit = Column(Integer, nullable=True)
 
    special_rules = Column(JSON, nullable=True)