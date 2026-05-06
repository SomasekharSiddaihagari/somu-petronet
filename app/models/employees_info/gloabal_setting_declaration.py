from sqlalchemy import Column, Integer, String, Boolean, Date
from app.database import Base
 
class DeclarationSettings(Base):
    __tablename__ = "declaration_settings"
 
    dec_id = Column(Integer, primary_key=True, index=True)
 
    # Types: Asset / Investment / 12C
    declaration_type = Column(String(50), nullable=False, unique=True)
 
    opening_date = Column(Date, nullable=True)
    closing_date = Column(Date, nullable=True)
 
    is_active = Column(Boolean, default=False)