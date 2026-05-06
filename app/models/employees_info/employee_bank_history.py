from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
 
class EmployeeBankHistory(Base):
    __tablename__ = "employee_bank_history"
    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    bank_name = Column(String, nullable=True)
    branch_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    account_holder_name = Column(String, nullable=True)
    account_type = Column(String, nullable=True)
    cancelled_cheque = Column(String, nullable=True)
    document_name = Column(String, nullable=True) 
    is_active = Column(Boolean, nullable=True)   # <-- Added field
    status = Column(String, nullable=True)   # <-- Added field
    remarks = Column(Text, nullable=True)  # <-- Added field
    changed_fields = Column(JSON, nullable=True, server_default='[]')