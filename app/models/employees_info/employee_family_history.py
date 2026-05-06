from sqlalchemy import Column, Integer, String, Date, DateTime, JSON
from app.database import Base
from datetime import datetime
 
 
class EmployeeFamilyHistory(Base):
    __tablename__ = "employee_family_history"
 
    history_id = Column(Integer, primary_key=True)
 
    # Reference to main table
    ef_id = Column(Integer)
    user_id = Column(Integer)
 
    relation = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    document = Column(String, nullable=True)
 
    # History timestamp
    history_created_at = Column(DateTime, default=datetime.utcnow)
    changed_fields = Column(JSON, nullable=True, server_default='[]')