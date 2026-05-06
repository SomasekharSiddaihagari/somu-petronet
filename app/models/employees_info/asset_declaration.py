from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
 
class UserAssetDeclaration(Base):
    __tablename__ = "user_asset_declaration"
 
    asset_id = Column(Integer, primary_key=True)
 
    # ✅ Link directly to users table
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
 
    # ✅ Declaration Info
    date = Column(Date, nullable=True)
    financial_year = Column(String, nullable=True)
    document = Column(String, nullable=True)
 
    # ✅ Asset Type
    asset_type = Column(String, nullable=True)   # movable / immovable
 
    # ✅ Common Fields (merged movable + immovable)
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
    user = relationship("User", back_populates="asset_declaration")