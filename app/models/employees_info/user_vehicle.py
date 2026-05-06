
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Date, Text, JSON

 
class UserVehicle(Base):
    __tablename__ = "user_vehicle"
 
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
 
    vehicle_type = Column(String, nullable=True)            # Two-Wheeler / Four-Wheeler
    vehicle_make = Column(String, nullable=True)
    vehicle_model = Column(String, nullable=True)
    color = Column(String, nullable=True)
    fuel_type = Column(String, nullable=True)               # Petrol / Other
    
    rc_expiry_date = Column(Date, nullable=True)
    insurance_provider = Column(String, nullable=True)
    insurance_policy_number = Column(String, nullable=True)
    insurance_expiry_date = Column(Date, nullable=True)
    puc_expiry_date = Column(Date, nullable=True)
    vehicle_registration_no = Column(String, nullable=True)
    status = Column(String, nullable=True)
    document_details = Column(Text, nullable=True)             
    comment = Column(Text, nullable=True)                       
    document_upload = Column(Text, nullable=True)        # File path
    active = Column(Boolean, nullable=True)                # 1 for active, 0 for inactive
    created_date = Column(Date, default=datetime.utcnow)
    modified_date = Column(Date, nullable=True)
    changed_fields = Column(JSON, nullable=False, server_default='[]')
 
    # Relationship back reference
    user = relationship("User", back_populates="vehicles")