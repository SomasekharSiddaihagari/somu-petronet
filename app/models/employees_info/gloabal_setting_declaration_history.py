from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from app.database import Base
from datetime import datetime
 
 
class DeclarationSettingsHistory(Base):
    __tablename__ = "declaration_settings_history"
 
    history_id = Column(Integer, primary_key=True)
 
    # Reference to main table
    dec_id = Column(Integer)
 
    declaration_type = Column(String(50))
    opening_date = Column(Date)
    closing_date = Column(Date)
    is_active = Column(Boolean)
 
    # History timestamp
    history_created_at = Column(DateTime, default=datetime.utcnow)