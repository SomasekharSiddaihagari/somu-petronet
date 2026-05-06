from sqlalchemy import Column, Integer, String, Date, DateTime,Text
from app.database import Base
from datetime import datetime
 
 
class EmployeeForm12CHistory(Base):
    __tablename__ = "employee_form_12c_history"
 
    history_id = Column(Integer, primary_key=True)
 
    # Reference to main table
    form_id = Column(Integer)
    user_id = Column(Integer)
 
    # All original fields
    self_alv = Column(String, nullable=True)
    lo1_alv = Column(String, nullable=True)
    lo2_alv = Column(String, nullable=True)
 
    self_municipal_tax = Column(String, nullable=True)
    lo1_municipal_tax = Column(String, nullable=True)
    lo2_municipal_tax = Column(String, nullable=True)
 
    self_annual_value = Column(String, nullable=True)
    lo1_annual_value = Column(String, nullable=True)
    lo2_annual_value = Column(String, nullable=True)
 
    self_less_30 = Column(String, nullable=True)
    lo1_less_30 = Column(String, nullable=True)
    lo2_less_30 = Column(String, nullable=True)
 
    house_type_self = Column(String, nullable=True)
    house_type_lo1 = Column(String, nullable=True)
    house_type_lo2 = Column(String, nullable=True)
 
    self_interest = Column(String, nullable=True)
    lo1_interest = Column(String, nullable=True)
    lo2_interest = Column(String, nullable=True)
 
    self_loan_date = Column(Date, nullable=True)
    lo1_loan_date = Column(Date, nullable=True)
    lo2_loan_date = Column(Date, nullable=True)
 
    self_one_fifth_interest = Column(String, nullable=True)
    lo1_one_fifth_interest = Column(String, nullable=True)
    lo2_one_fifth_interest = Column(String, nullable=True)
 
    self_net_income = Column(String, nullable=True)
    lo1_net_income = Column(String, nullable=True)
    lo2_net_income = Column(String, nullable=True)
 
    self_tds_self_lease = Column(String, nullable=True)
    lo1_tds_self_lease = Column(String, nullable=True)
    lo2_tds_self_lease = Column(String, nullable=True)
 
    self_cess_self_lease = Column(String, nullable=True)
    lo1_cess_self_lease = Column(String, nullable=True)
    lo2_cess_self_lease = Column(String, nullable=True)
 
    self_cess_self_business = Column(String, nullable=True)
    lo1_cess_self_business = Column(String, nullable=True)
    lo2_cess_self_business = Column(String, nullable=True)
 
    self_capital_gains = Column(String, nullable=True)
    lo1_capital_gains = Column(String, nullable=True)
    lo2_capital_gains = Column(String, nullable=True)
 
    self_other_sources = Column(String, nullable=True)
    lo1_other_sources = Column(String, nullable=True)
    lo2_other_sources = Column(String, nullable=True)
 
    self_aggregate_items = Column(String, nullable=True)
    lo1_aggregate_items = Column(String, nullable=True)
    lo2_aggregate_items = Column(String, nullable=True)
 
    self_tds_other_income = Column(String, nullable=True)
    lo1_tds_other_income = Column(String, nullable=True)
    lo2_tds_other_income = Column(String, nullable=True)
 
    self_cess_other_income = Column(String, nullable=True)
    lo1_cess_other_income = Column(String, nullable=True)
    lo2_cess_other_income = Column(String, nullable=True)
 
    self_total_tds = Column(String, nullable=True)
    lo1_total_tds = Column(String, nullable=True)
    lo2_total_tds = Column(String, nullable=True)
 
    self_total_cess = Column(String, nullable=True)
    lo1_total_cess = Column(String, nullable=True)
    lo2_total_cess = Column(String, nullable=True)
 
    upload_document = Column(String, nullable=True)
 
    declared_place = Column(String, nullable=True)
    declared_date = Column(Date, nullable=True)
    signature_name = Column(String, nullable=True)
    signature = Column(Text, nullable=True)
    status = Column(String, nullable=True)
 
    # History timestamp
    history_created_at = Column(DateTime, default=datetime.utcnow)