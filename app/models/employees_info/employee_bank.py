
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
 
 
class EmployeeBank(Base):
    __tablename__ = "employee_bank"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

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