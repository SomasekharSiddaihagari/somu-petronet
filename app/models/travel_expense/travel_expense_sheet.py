
from sqlalchemy import (
    Boolean, Column, BigInteger, ForeignKey, Integer, String, DateTime, Text, Numeric, Date
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class TravelExpenseSheet(Base):
    __tablename__ = "travel_expense_sheet"
 
    tes_id = Column(BigInteger, primary_key=True, autoincrement=True)
 
    # Mapping to Travel Requisition (REQ-001 etc.)
    requisition_number = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    travel_id = Column(BigInteger,nullable=True )
    # Employee Info
    employee_name = Column(String(150), nullable=True)
    employee_number = Column(String(50), nullable=True)
    designation = Column(String(100), nullable=True)
    grade = Column(String(50), nullable=True)
    station = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
 
    # Travel Info
    travel_mode = Column(String(100), nullable=True)
    purpose_of_travel = Column(Text, nullable=True)
    violation = Column(String(255), nullable=True)
 
    # Total Summary
    total_excl_gst = Column(Numeric(12, 2), nullable=True)
    total_gst = Column(Numeric(12, 2), nullable=True)
    total_incl_gst = Column(Numeric(12, 2), nullable=True)
    advance_taken = Column(Numeric(12, 2), nullable=True)
    amount_payable_receivable = Column(Numeric(12, 2), nullable=True)
 
    # Footer Comments
    comments = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
    updated_by_supervisor = Column(Date, nullable=True)
    updated_by_supervisor_name = Column(String(150), nullable=True)
 
    # HR
    updated_by_hr = Column(Date, nullable=True)
    updated_by_hr_name = Column(String(150), nullable=True)
 
    # MD
    updated_by_md = Column(Date, nullable=True)
    updated_by_md_name = Column(String(150), nullable=True)

    updated_by_head_tech = Column(Date, nullable=True)
    updated_by_head_tech_name = Column(String(150), nullable=True)
    head_tech_comments = Column(Text, nullable=True)
 
    # Finance
    updated_by_finance = Column(Date, nullable=True)
    updated_by_finance_name = Column(String(150), nullable=True)
    is_dollar = Column(Boolean, nullable=True)
   
    supervisor_comments = Column(Text, nullable=True)
    hr_comments = Column(Text, nullable=True)
    finance_comments = Column(Text, nullable=True)
 
    # Default Time Stamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
    # Relationships
    expense_details = relationship(
        "TravelExpenseSheetDetail",
        back_populates="expense_sheet"
    )
    # user = relationship("User", back_populates="travel_expense_sheets")
 
 