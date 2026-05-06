from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey,JSON
from sqlalchemy.orm import relationship
from app.database import Base
 
class UserFinance(Base):
    __tablename__ = "user_finance"
 
    user_finance_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
 
   
 
    # -------- Investment Details --------
    date = Column(Date, nullable=True)
    financial_year = Column(String, nullable=True)
    opting_for_concessional_rate = Column(String, nullable=True)
 
    residing_in_rented_house = Column(String, nullable=True)
    monthly_rent = Column(Float, nullable=True)
    landlord_name = Column(String, nullable=True)
    temporary_address = Column(Text, nullable=True)
 
    pension_plan = Column(String, nullable=True)
    lic_premium = Column(String, nullable=True)
    ppf = Column(String, nullable=True)
    ulip = Column(String, nullable=True)
    tuition_fees = Column(String, nullable=True)
    nsc = Column(String, nullable=True)
    nsc_interest = Column(String, nullable=True)
    housing_loan_repayment = Column(String, nullable=True)
    other_investments = Column(String, nullable=True)
    medical_insurance_80d = Column(String, nullable=True)
    interest_housing_24b = Column(Float, nullable=True)
    infrastructure_bond = Column(String, nullable=True)
    educational_loan_interest = Column(String, nullable=True)
    contribution_to_nps = Column(String, nullable=True)
 
    upload_document = Column(String, nullable=True)
    declaration_text = Column(Text, nullable=True)
    signature_name = Column(String, nullable=True)
    status = Column(String, nullable=True)
    changed_fields = Column(JSON, nullable=True, server_default='[]')
    user = relationship("User", back_populates="finance")
 