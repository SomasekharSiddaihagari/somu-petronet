from sqlalchemy import Column, BigInteger, Date, ForeignKey, Integer, String, DateTime, Text, Numeric, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.travel_expense.travel_requisition_car import TravelRequisitionCar
from app.models.travel_expense.meal_allowance_sheet_detail import MealAllowanceSheetDetail
 
 
 
 
class MealAllowanceSheet(Base):
    __tablename__ = "meal_allowance_sheet"
 
    meal_sheet_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
 
    requisition_number = Column(
        String(50),
        nullable=True,
        server_default=text("generate_meal_requisition_number()")  
    )
 
    employee_name = Column(String(150), nullable=True)
    employee_number = Column(String(50), nullable=True)
    designation = Column(String(100), nullable=True)
    grade = Column(String(50), nullable=True)
    station = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    purpose_of_travel = Column(Text, nullable=True)
 
    # Totals
    total_excl_gst = Column(Numeric(12, 2), nullable=True)
    total_gst = Column(Numeric(12, 2), nullable=True)
    total_incl_gst = Column(Numeric(12, 2), nullable=True)
    advance_taken = Column(Numeric(12, 2), nullable=True)
    amount_receivable_payable = Column(Numeric(12, 2), nullable=True)
 
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
 
    
    supervisor_comments = Column(Text, nullable=True)
    hr_comments = Column(Text, nullable=True)
    finance_comments = Column(Text, nullable=True)

    # Totals
  
    comments = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
    violation = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
    entries = relationship("MealAllowanceSheetDetail", back_populates="sheet")
    # user = relationship("User", back_populates="meal_sheets")