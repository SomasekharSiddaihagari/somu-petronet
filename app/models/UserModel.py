from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,Text, Date, JSON
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,Text, Date
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
 
 
from app.models.employees_info.employee_education import UserEducation
from app.models.leave.hr_leave_application import HRLeaveApplication
 
from app.models.travel_expense.travel_requisition import TravelRequisition
 
 
class User(Base):
    __tablename__ = "users"
 
    user_id = Column(Integer, primary_key=True, index=True)
 
 
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) 
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=True)
    station_id = Column(Integer, ForeignKey('station.station_id'), nullable=True) 
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    emergency_mobile = Column(String, nullable=True) 
    email = Column(String, unique=True, nullable=True)
    personal_email = Column(String, nullable=True) 
    employee_code = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    station = Column(String, nullable=True)
    grade = Column(String, nullable=True)
    supervisor_id = Column(Integer, nullable=True)
    sap_location_code = Column(String, nullable=True)
    employment_type = Column(String, nullable=True) 
    date_of_joining = Column(Date, nullable=True)
    dob = Column(Date, nullable=True)
    probation_from = Column(Date, nullable=True)
    probation_to = Column(Date, nullable=True)
    permanent_from=Column(Date, nullable=True)
    blood_group = Column(Text, nullable=True)
    current_address = Column(Text, nullable=True)
    current_address_proof = Column(String, nullable=True)
    permanent_address = Column(Text, nullable=True)
    permanent_address_proof = Column(String, nullable=True)
    employee_vendor_code = Column(String(255), nullable=True) 
    pr_address_document_details = Column(Text, nullable=True)
    cr_address_document_details = Column(Text, nullable=True)
    # Identity Proof Fields
    aadhaar = Column(String, nullable=True)
    aadhaar_file = Column(String, nullable=True)
    pan = Column(String, nullable=True)
    pan_file = Column(String, nullable=True)
    driving_license = Column(String, nullable=True)
    driving_license_file = Column(String, nullable=True)
    passport = Column(String, nullable=True)
    passport_file = Column(String, nullable=True)
 
    # Bank Details
    bank_name = Column(String, nullable=True)
    branch_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    account_holder_name = Column(String, nullable=True)
    account_type = Column(String, nullable=True)
    cancelled_cheque = Column(String, nullable=True)
    created_by = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
    modified_by = Column(String, nullable=True)
    modified_date = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    upload_document = Column(String, nullable=True)
    changes_requested_in = Column(String, nullable=True)
    comments = Column(String, nullable=True)
    status_basic_info = Column(String, nullable=True)
    status_address = Column(String, nullable=True)
    status_bank = Column(String, nullable=True)
    status_identity_proof = Column(String, nullable=True)
    status = Column(String, nullable=True)
    data_card_number = Column(String(50), nullable=True)
    document_details = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    basic_document_details = Column(Text, nullable=True)
    basic_comment = Column(Text, nullable=True)

    address_document_details = Column(Text, nullable=True)
    address_comment = Column(Text, nullable=True)

    identity_document_details = Column(Text, nullable=True)
    identity_comment = Column(Text, nullable=True)
    # Relationships
    finance = relationship("UserFinance", back_populates="user", uselist=False)
    asset_declaration = relationship("UserAssetDeclaration", back_populates="user")
    changed_fields = Column(JSON, nullable=False, server_default='[]')
    family_members = relationship(
        "EmployeeFamily",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    education_detail = relationship(
    "UserEducation",
    overlaps="educations",
    back_populates="user",
    cascade="all, delete-orphan"
    )

    form_12c = relationship(
        "EmployeeForm12C",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    role = relationship("Role", back_populates="users")
    station = relationship("Station", back_populates="users")
    educations = relationship("UserEducation",overlaps="education_detail", back_populates="user", cascade="all, delete-orphan")
    leave_applications = relationship("HRLeaveApplication", back_populates="user")
    profile_pic = Column(Text, nullable=True)
#     travel_requisitions = relationship("TravelRequisition",back_populates="user",cascade="all, delete-orphan")
#     meal_sheets = relationship(
#     "MealAllowanceSheet",
#     back_populates="user",
#     cascade="all, delete-orphan"
# )
    is_employee = Column(Boolean, default=False, nullable=True)

    permissions = relationship("RolePermission", back_populates="user")
    vehicles = relationship(
    "UserVehicle",
    back_populates="user",
    cascade="all, delete-orphan"
)


 
    # history = relationship("UserHistory", back_populates="user", cascade="all, delete-orphan")