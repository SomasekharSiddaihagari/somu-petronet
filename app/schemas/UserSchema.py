from pydantic import BaseModel, EmailStr
from typing import Optional, List
from pydantic import BaseModel
from fastapi import Form, UploadFile
from typing import Optional, List

# ---------- Sub Schemas ----------
class SubMenuBase(BaseModel):
    id: int
    name: str
    url: Optional[str]
    icon: Optional[str]

    class Config:
        from_attributes = True

class MenuBase(BaseModel):
    id: int
    name: str
    url: Optional[str]
    icon: Optional[str]
    submenus: Optional[List[SubMenuBase]] = []

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    id: int
    role_name: str

    class Config:
        from_attributes = True

# ---------- Main Schemas ----------

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Optional[RoleBase]
    is_deleted: bool = False

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class UserCreate(BaseModel):
    role_id: Optional[int] = None
    station_id: int | None = None
    # supervisor_id: int | None = None    
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr
    contact_phone: str | None = None
    created_by: str

    
class UserUpdate(BaseModel):
    station_id: Optional[int] = None
    role_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_mobile: Optional[str] = None
    personal_email: Optional[str] = None
    employee_code: Optional[str] = None
    employee_vendor_code: Optional[str]=None
    designation: Optional[str] = None
    blood_group:Optional[str] = None
    grade: Optional[str] = None
    supervisor_id: Optional[int] = None
    sap_location_code: Optional[str] = None
    employment_type: Optional[str] = None
    date_of_joining: Optional[str] = None
    dob: Optional[str] = None
    probation_from: Optional[str] = None
    probation_to: Optional[str] = None
    permanent_from: Optional[str] = None
   
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    account_holder_name: Optional[str] = None
    account_type: Optional[str] = None
    cancelled_cheque: Optional[str] = None
    status_basic_info: Optional[str] = None
    status_address: Optional[str] = None
    status_bank: Optional[str] = None
    status_identity_proof: Optional[str] = None


class UserCreate_profile(BaseModel):
    station_id: Optional[int] = None
    username: str
    first_name: str
    last_name: str
    email: str
    is_employee: Optional[bool] = None
    employee_vendor_code: Optional[str]=None
    role_id:  Optional[int] = None
    blood_group:Optional[str] = None
    personal_email: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_mobile: Optional[str] = None
    gender: Optional[str] = None
    document_details: Optional[str] = None
    employee_code: Optional[str] = None
    designation: Optional[str] = None
    grade: Optional[str] = None
    supervisor_id: Optional[int] = None
    sap_location_code: Optional[str] = None
    employment_type: Optional[str] = None

    date_of_joining: Optional[str] = None
    dob: Optional[str] = None
    probation_from: Optional[str] = None
    probation_to: Optional[str] = None
    permanent_from: Optional[str] = None

    current_address: Optional[str] = None
    current_address_proof: Optional[str] = None
    permanent_address: Optional[str] = None
    permanent_address_proof: Optional[str] = None

    aadhaar: Optional[str] = None
    aadhaar_file: Optional[str] = None
    pan: Optional[str] = None
    pan_file: Optional[str] = None
    driving_license: Optional[str] = None
    driving_license_file: Optional[str] = None
    passport: Optional[str] = None
    passport_file: Optional[str] = None
    data_card_number: Optional[str] = None,
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    account_holder_name: Optional[str] = None
    account_type: Optional[str] = None
    cancelled_cheque: Optional[str] = None
    status_basic_info: Optional[str] = None
    status_address: Optional[str] = None
    status_bank: Optional[str] = None
    status_identity_proof: Optional[str] = None
    basic_document_details: Optional[str] = None
    basic_comment: Optional[str] = None
    pr_address_document_details: Optional[str] = None
    cr_address_document_details: Optional[str] = None
    address_document_details: Optional[str] = None
    address_comment: Optional[str] = None
    identity_document_details: Optional[str] = None
    identity_comment: Optional[str] = None
    comment: Optional[str] = None
    
    created_by:  Optional[str] = None

    @classmethod
    def as_form(
        cls,
        role_id: int = Form(None),
        blood_group:Optional[str] = Form(...),
        is_employee: Optional[bool] = Form(None),
        station_id: int = Form(...),
        username: str = Form(...),
        first_name: str = Form(...),
        employee_vendor_code: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        personal_email: str = Form(None),
        contact_phone: str = Form(None),
        emergency_mobile: str = Form(None),
        gender: str = Form(None),

        employee_code: str = Form(None),
        designation: str = Form(None),
        grade: str = Form(None),
        supervisor_id: int = Form(None),
        sap_location_code: str = Form(None),
        employment_type: str = Form(None),

        date_of_joining: str = Form(None),
        dob: str = Form(None),
        probation_from: str = Form(None),
        probation_to: str = Form(None),
        permanent_from: str = Form(None),
        data_card_number: str=Form(None),
        current_address: str = Form(None),
        current_address_proof: str = Form(None),
        permanent_address: str = Form(None),
        permanent_address_proof: str = Form(None),

        aadhaar: str = Form(None),
        aadhaar_file: str = Form(None),
        pan: str = Form(None),
        pan_file: str = Form(None),
        driving_license: str = Form(None),
        driving_license_file: str = Form(None),
        passport: str = Form(None),
        passport_file: str = Form(None),
        status_basic_info: str = Form(None),
        status_address: str = Form(None),
        status_bank: str = Form(None),
        status_identity_proof: str = Form(None),
        bank_name: str = Form(None),
        branch_name: str = Form(None),
        account_number: str = Form(None),
        ifsc_code: str = Form(None),
        account_holder_name: str = Form(None),
        account_type: str = Form(None),
        document_details: str = Form(None),
        cancelled_cheque: str = Form(None),
        basic_document_details: str = Form(None),
        basic_comment: str = Form(None),
        pr_address_document_details: str = Form(None),
        cr_address_document_details: str = Form(None),
        address_document_details: str = Form(None),
        address_comment: str = Form(None),
        identity_document_details: str = Form(None),
        identity_comment: str = Form(None),
        comment: str = Form(None),
        created_by: str = Form(...)
    ):
        return cls(
            role_id=role_id,
            blood_group=blood_group,
            is_employee=is_employee,
            station_id=station_id,
            username=username,
            first_name=first_name,
            employee_vendor_code=employee_vendor_code,
            last_name=last_name,
            email=email,
            personal_email=personal_email,
            contact_phone=contact_phone,
            emergency_mobile=emergency_mobile,
            gender=gender,

            employee_code=employee_code,
            designation=designation,
            grade=grade,
            supervisor_id=supervisor_id,
            sap_location_code=sap_location_code,
            employment_type=employment_type,

            date_of_joining=date_of_joining,
            dob=dob,
            probation_from=probation_from,
            probation_to=probation_to,
            permanent_from=permanent_from,

            current_address=current_address,
            current_address_proof=current_address_proof,
            permanent_address=permanent_address,
            permanent_address_proof=permanent_address_proof,
            data_card_number=data_card_number,
            aadhaar=aadhaar,
            aadhaar_file=aadhaar_file,
            pan=pan,
            pan_file=pan_file,
            driving_license=driving_license,
            driving_license_file=driving_license_file,
            passport=passport,
            passport_file=passport_file,
            document_details=document_details,
            comment=comment,
            status_basic_info=status_basic_info,
            status_address=status_address,
            status_bank=status_bank,
            status_identity_proof=status_identity_proof,
            bank_name=bank_name,
            branch_name=branch_name,
            account_number=account_number,
            ifsc_code=ifsc_code,
            account_holder_name=account_holder_name,
            account_type=account_type,
            cancelled_cheque=cancelled_cheque,
            basic_document_details=basic_document_details,
            basic_comment=basic_comment,
            pr_address_document_details=pr_address_document_details,
            cr_address_document_details=cr_address_document_details,
            address_document_details=address_document_details,
            address_comment=address_comment,
            identity_document_details=identity_document_details,
            identity_comment=identity_comment,
            created_by=created_by
        )
    
class DeleteUserResponse(BaseModel):
    message: str
    user_id: int
