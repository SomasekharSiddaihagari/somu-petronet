from sqlalchemy import (
 
    Column, Integer, String, Float, Date, Text, ForeignKey
 
)
 
from sqlalchemy.orm import relationship
 
from app.database import Base
 
 
class EmployeeForm12C(Base):
 
    __tablename__ = "employee_form_12c"
 
    form_id = Column(Integer, primary_key=True)
 
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
 
    # ============ (a) Annual Lettable Value ============================
 
    self_alv = Column(String, nullable=True)
 
    lo1_alv = Column(String, nullable=True)
 
    lo2_alv = Column(String, nullable=True)
 
    # ============ (b) Municipal Taxes Paid =============================
 
    self_municipal_tax = Column(String, nullable=True)
 
    lo1_municipal_tax = Column(String, nullable=True)
 
    lo2_municipal_tax = Column(String, nullable=True)
 
    # ============ Annual Value (a-b) ==================================
 
    self_annual_value = Column(String, nullable=True)
 
    lo1_annual_value = Column(String, nullable=True)
 
    lo2_annual_value = Column(String, nullable=True)
 
    # ============ Less 30% of Annual Value =============================
 
    self_less_30 = Column(String, nullable=True)
 
    lo1_less_30 = Column(String, nullable=True)
 
    lo2_less_30 = Column(String, nullable=True)
 
    # ============ House Type (dropdowns) ===============================
 
    house_type_self = Column(String, nullable=True)
 
    house_type_lo1 = Column(String, nullable=True)
 
    house_type_lo2 = Column(String, nullable=True)
 
    # ============ Interest on borrowed capital =========================
 
    self_interest = Column(String, nullable=True)
 
    lo1_interest = Column(String, nullable=True)
 
    lo2_interest = Column(String, nullable=True)
 
 
 
 
    # ============ Loan Dates ==========================================
 
    self_loan_date = Column(Date, nullable=True)
 
    lo1_loan_date = Column(Date, nullable=True)
 
    lo2_loan_date = Column(Date, nullable=True)
 
 
 
 
    # ===== NEW FIELD (1/5th of interest before construction completes) ==
    self_one_fifth_interest = Column(String, nullable=True)
    lo1_one_fifth_interest = Column(String, nullable=True)
    lo2_one_fifth_interest = Column(String, nullable=True)
 
    # ============ Net Income / Loss ===================================
 
    self_net_income = Column(String, nullable=True)
 
    lo1_net_income = Column(String, nullable=True)
 
    lo2_net_income = Column(String, nullable=True)
 
    # ============ TDS on Self Lease ===================================
 
    self_tds_self_lease = Column(String, nullable=True)
 
    lo1_tds_self_lease = Column(String, nullable=True)
 
    lo2_tds_self_lease = Column(String, nullable=True)
 
    # ============ CESS on Self Lease ==================================
 
    self_cess_self_lease = Column(String, nullable=True)
 
    lo1_cess_self_lease = Column(String, nullable=True)
 
    lo2_cess_self_lease = Column(String, nullable=True)



    # ============ profit and gains bussiness professional ==================================
 
    self_cess_self_business = Column(String, nullable=True)
 
    lo1_cess_self_business = Column(String, nullable=True)
 
    lo2_cess_self_business = Column(String, nullable=True)


 
    # ============ Capital Gains (No Loss) ==============================
 
    self_capital_gains = Column(String, nullable=True)
 
    lo1_capital_gains = Column(String, nullable=True)
 
    lo2_capital_gains = Column(String, nullable=True)
 
    # ============ Other Sources (No Loss) ==============================
 
    self_other_sources = Column(String, nullable=True)
 
    lo1_other_sources = Column(String, nullable=True)
 
    lo2_other_sources = Column(String, nullable=True)
 
    # ============ Aggregate of Items (i to iv) =========================
 
    self_aggregate_items = Column(String, nullable=True)
 
    lo1_aggregate_items = Column(String, nullable=True)
 
    lo2_aggregate_items = Column(String, nullable=True)
 
    # ============ TDS on Other Income =================================
 
    self_tds_other_income = Column(String, nullable=True)
 
    lo1_tds_other_income = Column(String, nullable=True)
 
    lo2_tds_other_income = Column(String, nullable=True)
 
    # ============ CESS on Other Income ================================
 
    self_cess_other_income = Column(String, nullable=True)
 
    lo1_cess_other_income = Column(String, nullable=True)
 
    lo2_cess_other_income = Column(String, nullable=True)
 
    # ============ Total TDS (a + c) ===================================
 
    self_total_tds = Column(String, nullable=True)
 
    lo1_total_tds = Column(String, nullable=True)
 
    lo2_total_tds = Column(String, nullable=True)
 
    # ============ Total CESS (b + d) ==================================
 
    self_total_cess = Column(String, nullable=True)
 
    lo1_total_cess = Column(String, nullable=True)
 
    lo2_total_cess = Column(String, nullable=True)
 
    # ============ File Upload =========================================
 
    upload_document = Column(String, nullable=True)
    signature = Column(String, nullable=True)
 
    # ============ Declaration =========================================
 
    declared_place = Column(String, nullable=True)
 
    declared_date = Column(Date, nullable=True)
 
    signature_name = Column(String, nullable=True)
 
    signature = Column(Text, nullable=True)
 
    status = Column(String, nullable=True)
 
    user = relationship("User", back_populates="form_12c")