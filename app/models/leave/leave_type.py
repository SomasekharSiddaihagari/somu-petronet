from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class LeaveType(Base):
    __tablename__ = "leave_types"
 
    type_id = Column(Integer, primary_key=True)
 
    code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)