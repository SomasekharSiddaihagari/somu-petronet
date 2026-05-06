from datetime import datetime, timedelta
import os
import shutil
from typing import List
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, Path, Request, Response, UploadFile
from sqlalchemy.orm import Session
from app.crud.leave.hr_leave_allocation import run_monthly_leave_cron
from app.models.UserModel import User
from app.routers.employees_info.asset_declaration_routers import UPLOAD_ROOT
from app.routers.employees_info.employee_family_routers import UPLOAD_DIR
from app.schemas.UserSchema import  DeleteUserResponse, UserCreate, UserCreate_profile, UserLogin, UserUpdate
from app.database import get_db
from app.utils.EmailUtils import send_email
from app.utils.UserAuthUtils import (
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    # REFRESH_TOKEN_EXPIRE_MINUTES,
    get_password_hash,
)
from app.crud import UserCrud

router = APIRouter(prefix="/User", tags=["User"])

UPLOAD_ROOT = "files/users"
os.makedirs(UPLOAD_ROOT, exist_ok=True)
# ---------------- REGISTER ----------------
@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if UserCrud.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if UserCrud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserCrud.create_user(db, user_in)

    return {
        "statusCode": "201",
        "statusMessage": "User added successfully",
        "userId": str(new_user.user_id),
        "username": new_user.username,
        "emailId": new_user.email,
    }

# ---------------- LOGIN ----------------
@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):

    result = UserCrud.login_user(db, user_in)
    return {
        **result,
        "statusCode": "200",
        "statusMessage": "Success",
    }

# @router.get("/verify")
# async def verify_token(request: Request):
#     # If request reaches here, JWTMiddleware already validated the token
#     # because /User/verify is NOT in PUBLIC_PATHS
#     return Response(status_code=200)



@router.post("/refresh-token")
def refresh_token_endpoint(
    body: dict = Body(...),
    db: Session = Depends(get_db)
):
    print("🔍 DEBUG: Received Body ->", body)

    refresh_token = body.get("refreshToken") or body.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=422,
            detail="refreshToken or refresh_token is required in the body"
        )

    result = UserCrud.refresh_access_token(db, refresh_token)

    return {
        **result,
        "statusCode": "200",
        "statusMessage": "Success"
    }





@router.get("/non-employees")
def get_non_employees(db: Session = Depends(get_db)):

    query = text("""
        SELECT 
            user_id,
            username,
            email,
            first_name,
            last_name,
            is_employee
        FROM users
        WHERE is_employee = FALSE
    """)

    result = db.execute(query).fetchall()

    data = [dict(row._mapping) for row in result]

    return {
        "status": True,
        "data": data
    }


@router.post("/logout")
def logout():
    return {
        "statusCode": "200",
        "statusMessage": "Logged out successfully"
    }
def save_uploaded_files(files: List[UploadFile], user_id: int):
    # Create user folder: files/users/<id>
    user_dir = os.path.join(UPLOAD_ROOT, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    saved_paths = []

    for file in files:
        file_path = os.path.join(user_dir, file.filename)

        # Write file to directory
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        saved_paths.append(file_path)

    return saved_paths






def create_user_crud(db: Session, user_in: UserCreate_profile, upload_document):

    # Check if username exists
    exists = db.query(User).filter(User.username == user_in.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Generate password
    raw_password = UserCrud.generate_random_password(8)
    hashed_pw = get_password_hash(raw_password)

    # Create user first (without files)
    new_user = User(
        role_id=user_in.role_id,
        station_id=user_in.station_id,
        username=user_in.username,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        personal_email=user_in.personal_email,
        contact_phone=user_in.contact_phone,
        is_employee=user_in.is_employee,

        emergency_mobile=user_in.emergency_mobile,
        gender=user_in.gender,

        employee_code=user_in.employee_code,
        designation=user_in.designation,
        grade=user_in.grade,
        supervisor_id=user_in.supervisor_id,
        sap_location_code=user_in.sap_location_code,
        employment_type=user_in.employment_type,
        
        date_of_joining=user_in.date_of_joining,
        dob=user_in.dob,
        probation_from=user_in.probation_from,
        probation_to=user_in.probation_to,
        permanent_from=user_in.permanent_from,

        current_address=user_in.current_address,
        current_address_proof=user_in.current_address_proof,
        permanent_address=user_in.permanent_address,
        permanent_address_proof=user_in.permanent_address_proof,

        aadhaar=user_in.aadhaar,
        aadhaar_file=user_in.aadhaar_file,
        pan=user_in.pan,
        pan_file=user_in.pan_file,
        driving_license=user_in.driving_license,
        driving_license_file=user_in.driving_license_file,
        passport=user_in.passport,
        passport_file=user_in.passport_file,
        employee_vendor_code=user_in.employee_vendor_code,
        blood_group=user_in.blood_group,
        data_card_number=user_in.data_card_number,
        bank_name=user_in.bank_name,
        branch_name=user_in.branch_name,
        account_number=user_in.account_number,
        ifsc_code=user_in.ifsc_code,
        account_holder_name=user_in.account_holder_name,
        account_type=user_in.account_type,
        cancelled_cheque=user_in.cancelled_cheque,
        status_basic_info=user_in.status_basic_info,
        status_address=user_in.status_address,
        status_bank=user_in.status_bank,
        status_identity_proof=user_in.status_identity_proof,
        hashed_password=hashed_pw,
        created_by=user_in.created_by,
        document_details=user_in.document_details,
        cr_address_document_details=user_in.cr_address_document_details,
        pr_address_document_details=user_in.pr_address_document_details,
        basic_document_details=user_in.basic_document_details,
        basic_comment=user_in.basic_comment,
        address_document_details=user_in.address_document_details,
        address_comment=user_in.address_comment,
        identity_document_details=user_in.identity_document_details,
        identity_comment=user_in.identity_comment,
        comment=user_in.comment,
        created_date=datetime.now()
    )
    file_paths = []
    if upload_document:
            file_paths = save_uploaded_files(upload_document, new_user.user_id)

            # COMMA-SEPARATED STRING
            new_user.upload_document = ",".join(file_paths)

           

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    temp_userid=new_user.user_id
    email_subject = "Your Account Password"
    email_body = (
        f"Hello {user_in.first_name},\n\n"
        f"Your account has been created.\n\n"
        f"Username : {user_in.email}\n\n"
        f"Temporary Password: {raw_password}\n\n"
        f"Please log in and change your password immediately.\n\n"
        f"Thank you."
    )
 
    print("raw_password",raw_password)
    print(        f"Username : {user_in.email}\n\n")
 
    send_email(to_email=user_in.email, subject=email_subject, body=email_body)
 
    hashed_pw = get_password_hash(raw_password)


    # Create user record
    new_user = User(
        user_id= temp_userid,

        role_id=user_in.role_id,
        station_id=user_in.station_id,
        username=user_in.username,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=hashed_pw,
        email=user_in.email,
        contact_phone=user_in.contact_phone,
        created_by=user_in.created_by,
        created_date=datetime.now()
    )
    # ---- FILE UPLOAD ----
    
    return {
        "userId": new_user.user_id,
        "username": new_user.username,
        "email": new_user.email,
        "upload_document": file_paths
    }



@router.post("/createUser")
async def create_user(
    user_in: UserCreate_profile = Depends(UserCreate_profile.as_form),
    upload_document: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    result = create_user_crud(db, user_in, upload_document)
    print("hiii bro i wam here ")
    run_monthly_leave_cron(db)
    return {
        **result,
        "statusCode": "200",
        "statusMessage": "User created successfully"
    }



def sanitize_filename(name: str) -> str:
    name = os.path.basename(name)
    illegal = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for c in illegal:
        name = name.replace(c, "_")
    return name

def save_file(file: UploadFile | None, user_id: int):
    # ❌ Ignore empty or URL input (frontend sends URL when no new file is uploaded)
    if (
        file is None or
        file.filename is None or
        file.filename == "" or
        file.filename.startswith("http")
    ):
        return None

    # Clean filename
    filename = sanitize_filename(file.filename)

    # Create user directory
    user_folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(user_folder, filename)

    # Save file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Normalize slashes for db storage
    return file_path.replace("\\", "/")


@router.put("/update/{user_id}")
async def update_user(
    user_id: int,

    # Fields from form
    station_id: int | None = Form(None),
    role_id: int | None = Form(None),
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    gender: str | None = Form(None),
    is_employee: bool | None = Form(None),

    contact_phone: str | None = Form(None),
    emergency_mobile: str | None = Form(None),
    personal_email: str | None = Form(None),
    employee_code: str | None = Form(None),
    designation: str | None = Form(None),
    blood_group: str | None = Form(None),

    grade: str | None = Form(None),
    supervisor_id: int | None = Form(None),
    sap_location_code: str | None = Form(None),
    employment_type: str | None = Form(None),
    date_of_joining: str | None = Form(None),
    dob: str | None = Form(None),
    probation_from: str | None = Form(None),
    probation_to: str | None = Form(None),
    permanent_from: str | None = Form(None),

    employee_vendor_code: str | None = Form(None),

    bank_name: str | None = Form(None),
    branch_name: str | None = Form(None),
    account_number: str | None = Form(None),
    ifsc_code: str | None = Form(None),
    account_holder_name: str | None = Form(None),
    account_type: str | None = Form(None),
    cancelled_cheque: str | None = Form(None),

    # File uploads
    aadhaar_file: UploadFile | None = File(None),
    pan_file: UploadFile | None = File(None),
    driving_license_file: UploadFile | None = File(None),
    passport_file: UploadFile | None = File(None),

    db: Session = Depends(get_db)
):

    # Build dynamic dictionary for UserUpdate
    update_data = {
        "station_id": station_id,
        "role_id": role_id,
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "contact_phone": contact_phone,
        "emergency_mobile": emergency_mobile,
        "personal_email": personal_email,
        "employee_code": employee_code,
        "designation": designation,
        "blood_group":blood_group,
        "grade": grade,
        "supervisor_id": supervisor_id,
        "sap_location_code": sap_location_code,
        "employment_type": employment_type,
        "date_of_joining": date_of_joining,
        "is_employee":is_employee,
        "dob": dob,
        "probation_from": probation_from,
        "probation_to": probation_to,
        "permanent_from": permanent_from,
        "employee_vendor_code":employee_vendor_code,
        "bank_name": bank_name,
        "branch_name": branch_name,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
        "account_holder_name": account_holder_name,
        "account_type": account_type,
        "cancelled_cheque": cancelled_cheque,
    }

    # Clean empty strings → None
    update_data = {k: (None if v == "" else v) for k, v in update_data.items()}

    # Convert to Pydantic
    user_in = UserUpdate(**update_data)

    # Save files
    file_paths = {
        "aadhaar_file": save_file(aadhaar_file, user_id),
        "pan_file": save_file(pan_file, user_id),
        "driving_license_file": save_file(driving_license_file, user_id),
        "passport_file": save_file(passport_file, user_id),
    }

    # Remove None values
    file_paths = {k: v for k, v in file_paths.items() if v}

    # Update DB
    result = UserCrud.update_user_crud(db, user_id, user_in)

    # Now update file paths also
    for key, path in file_paths.items():
        setattr(db.query(User).filter(User.user_id == user_id).first(), key, path)

    db.commit()

    return {
        **result,
        "statusCode": "200",
        "statusMessage": "User updated successfully"
    }




@router.delete("/{user_id}", response_model=DeleteUserResponse)
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    """
    Soft delete user by setting is_deleted = True using SQL function.
    """
    return UserCrud.delete_user(db, user_id)





@router.get("/get-all")
def get_all_users(db: Session = Depends(get_db)):
    result = UserCrud.get_all_users_crud(db)

    return {
        "data": result,
        "statusCode": "200",
        "statusMessage": "Success"
    }





@router.get("/get/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    result = UserCrud.get_user_by_id_crud(db, user_id)

    return {
        "data": result,
        "statusCode": "200",
        "statusMessage": "Success"
    }

from sqlalchemy import func, text





@router.get("/users/role-1")
def get_role_1_users(db: Session = Depends(get_db)):

    sql = text("""
        SELECT
            CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, '')) AS full_name,
            u.designation,
            u.station
        FROM users u
        JOIN role_permissions rp 
            ON u.user_id = rp.user_id
        WHERE rp.role_id = 1
        AND u.is_deleted = FALSE
        GROUP BY u.first_name, u.last_name, u.designation, u.station
        ORDER BY full_name
    """)

    result = db.execute(sql).mappings().all()

    return result
