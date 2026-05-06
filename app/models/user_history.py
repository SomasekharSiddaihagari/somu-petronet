from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date,JSON
from app.database import Base
from datetime import datetime
from app.database import Base
from app.models.UserModel import users
 
target_metadata = Base.metadata
 
class UserHistory(Base):
    __tablename__ = "users_history"
 
    history_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
 
    username = Column(String)
    hashed_password = Column(String)
 
    role_id = Column(Integer)
    station_id = Column(Integer)
 
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
 
    contact_phone = Column(String)
    emergency_mobile = Column(String)
 
    email = Column(String)
    personal_email = Column(String)
 
    employee_code = Column(String)
    designation = Column(String)
    station = Column(String)
    grade = Column(String)
    supervisor_id = Column(Integer)
 
    sap_loacation_code = Column(String)
    employment_type = Column(String)
 
    date_of_joining = Column(Date)
    dob = Column(Date)
    probation_from = Column(Date)
    probation_to = Column(Date)
    permanent_from = Column(Date)
 
    current_address = Column(Text)
    current_address_proof = Column(String)
    permanent_address = Column(Text)
    permanent_address_proof = Column(String)
    pr_address_document_details = Column(Text, nullable=True)
    cr_address_document_details = Column(Text, nullable=True)
 
    qualification = Column(String)
    year_of_completion = Column(Integer)
    education_document = Column(String)
    employee_vendor_code = Column(String(255), nullable=True)
    aadhaar = Column(String)
    aadhaar_file = Column(String)
    pan = Column(String)
    pan_file = Column(String)
    driving_license = Column(String)
    driving_license_file = Column(String)
    passport = Column(String)
    passport_file = Column(String)
 
    bank_name = Column(String)
    branch_name = Column(String)
    account_number = Column(String)
    ifsc_code = Column(String)
    account_holder_name = Column(String)
    account_type = Column(String)
    cancelled_cheque = Column(String)
    status_basic_info = Column(String, nullable=True)
    status_address = Column(String, nullable=True)
    status_bank = Column(String, nullable=True)
    status_identity_proof = Column(String, nullable=True)
    created_by = Column(String)
    created_date = Column(DateTime)
    modified_by = Column(String)
    modified_date = Column(DateTime)
    is_deleted = Column(Boolean)
    uploaded_document = Column(String)
    changes_requested_in = Column(String, nullable=True)
    comments = Column(String, nullable=True)
    data_card_number = Column(String(50), nullable=True)
    profile_pic = Column(Text, nullable=True)
    basic_document_details = Column(Text, nullable=True)
    basic_comment = Column(Text, nullable=True)

    address_document_details = Column(Text, nullable=True)
    address_comment = Column(Text, nullable=True)

    identity_document_details = Column(Text, nullable=True)
    identity_comment = Column(Text, nullable=True)
    history_created_at = Column(DateTime, default=datetime.utcnow)
    changed_fields = Column(JSON, nullable=False, server_default='[]')