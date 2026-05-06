from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime
from app.database import Base
from datetime import datetime
 
class UserAssetDeclarationHistory(Base):
    __tablename__ = "user_asset_declaration_history"
 
    history_id = Column(Integer, primary_key=True, index=True)
 
    # Link to original row
    asset_id = Column(Integer)
    user_id = Column(Integer)
 
    # Declaration Info
    date = Column(Date, nullable=True)
    financial_year = Column(String, nullable=True)
    document = Column(String, nullable=True)
 
    # Asset Type
    asset_type = Column(String, nullable=True)
 
    # Common Fields
    details = Column(Text, nullable=True)
    held_in_name = Column(String, nullable=True)
    acquisition_date = Column(Date, nullable=True)
    nature = Column(String, nullable=True)
    party = Column(String, nullable=True)
    finance_amount = Column(Float, nullable=True)
    source_of_finance = Column(String, nullable=True)
    profit_amount = Column(Float, nullable=True)
    signature = Column(Text, nullable=True)
    status = Column(String, nullable=True)
    
    # History timestamp
    history_created_at = Column(DateTime, default=datetime.utcnow)