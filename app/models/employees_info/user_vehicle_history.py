from sqlalchemy import JSON, Column, Integer, String, Boolean, Date, Text
from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from app.database import Base
from datetime import datetime
 
 
class UserVehicleHistory(Base):
    __tablename__ = "user_vehicle_history"
 
    history_id = Column(Integer, primary_key=True, index=True)
 
    # Link to original row
    user_id = Column(Integer)           # User ID
 
    # Vehicle Details
    vehicle_type = Column(String, nullable=True)
    vehicle_make = Column(String, nullable=True)
    vehicle_model = Column(String, nullable=True)
    color = Column(String, nullable=True)
    fuel_type = Column(String, nullable=True)
 
    rc_expiry_date = Column(Date, nullable=True)
    insurance_provider = Column(String, nullable=True)
    insurance_policy_number = Column(String, nullable=True)
    insurance_expiry_date = Column(Date, nullable=True)
    puc_expiry_date = Column(Date, nullable=True)
    status=Column(String, nullable=True)
 
    vehicle_registration_no = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
    document_upload = Column(Text, nullable=True) 
 
    # Meta
    history_created_at = Column(DateTime, default=datetime.utcnow)
    changed_fields = Column(JSON, nullable=False, server_default='[]')