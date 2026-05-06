from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException
from app.crud.leave.hr_leave_allocation import run_monthly_leave_cron
from app.models.hr_action_tracker.disciplinary_incidents import DisciplinaryIncident
from app.routers.UserAuthR2 import make_download_url
from app.utils.EmailUtils import send_email
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from app.models.UserModel import User
from app.models.RoleModel import Role
from app.models.RolePermissionModel import RolePermission  
from app.models.MenuModel import Menu, SubMenu
from app.schemas.UserSchema import UserCreate, UserCreate_profile, UserLogin, UserUpdate
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.utils.UserAuthUtils import (
    ALGORITHM,
    # REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    # REFRESH_TOKEN_EXPIRE_MINUTES,
)

# -----------------------------
# Helper functions
# -----------------------------
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


# -----------------------------
# Create/Register new user
# -----------------------------
def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user record in DB after hashing password.
    """
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user_in.password)

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw,
        role_id=user_in.role_id if hasattr(user_in, "role_id") else None,
        created_by="system",
        created_date=datetime.now(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -----------------------------
# Authenticate user
# -----------------------------
def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from fastapi import HTTPException


def login_user(db: Session, user_in: UserLogin) -> dict:

    # --- Step 1: Load User (NO permissions here) ---
    user = (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.username == user_in.username)
        .first()
    )

    # --- Step 2: Authentication ---
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
        
    # --- Step 2.5: Termination Check ---
    termination_check = (
        db.query(DisciplinaryIncident)
        .filter(
            DisciplinaryIncident.user_id == user.user_id,
            DisciplinaryIncident.enable_termination == True,
        )
        .first()
    )
    
    if termination_check:
        raise HTTPException(
            status_code=403,
            detail="Your account has been terminated. Please contact HR."
        )
 
    # --- Step 3: Station name ---
    station_name = None
    if user.station_id:
        station = db.execute(
            text("SELECT station_name FROM station WHERE station_id = :sid"),
            {"sid": user.station_id}
        ).fetchone()
        if station:
            station_name = station[0]

    # --- Step 4: Supervisor name ---
    supervisor_name = None
    if user.supervisor_id:
        supervisor = db.query(User).filter(
            User.user_id == user.supervisor_id
        ).first()
        if supervisor:
            supervisor_name = f"{supervisor.first_name} {supervisor.last_name}"

    # --- Step 4.5: Check if user is a supervisor ---
    subordinates = db.query(User.user_id).filter(
        User.supervisor_id == user.user_id
    ).all()

    if subordinates:
        is_supervisor = True
        subordinate_ids = [s.user_id for s in subordinates]
    else:
        is_supervisor = False
        subordinate_ids = []

    # --- Step 5: Tokens ---
    now = datetime.now(timezone.utc)

    access_expiry = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_expiry = timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))

    access_exp_time = now + access_expiry
    refresh_exp_time = now + refresh_expiry

    access_token = create_access_token(
        {"sub": str(user.user_id)},
        expires_delta=access_expiry
    )
    refresh_token = create_refresh_token(
        {"sub": str(user.user_id)},
        expires_delta=refresh_expiry
    )

    # --- Step 6: Fetch permissions using SQL function ---
    rows = db.execute(
        text("SELECT * FROM get_user_role_permissions(:uid)"),
        {"uid": user.user_id}
    ).fetchall()

    role_map = {}

    for r in rows:
        if r.role_id not in role_map:
            role_map[r.role_id] = {
                "roleId": r.role_id,
                "roleName": r.role_name,
                "menus": {}
            }

        menus = role_map[r.role_id]["menus"]

        if r.menu_id not in menus:
            menus[r.menu_id] = {
                "menuId": r.menu_id,
                "menuName": r.menu_name,
                "menuUrl": r.menu_url,
                "menuIcon": r.menu_icon,
                "subMenus": []
            }

        menus[r.menu_id]["subMenus"].append({
            "subMenuId": r.submenu_id,
            "subMenuName": r.submenu_name,
            "subMenuUrl": r.submenu_url,
            "subMenuIcon": r.submenu_icon
        })

    profile_picture_url = serialize_profile_picture(
        getattr(user, "profile_pic", None)
    )

    # --- Step 6.5: Disciplinary check — override permissions if suspended or terminated ---
    SUSPENSION_ALLOWED_SUBMENUS = {6, 7}

    active_incident = (
        db.query(DisciplinaryIncident)
        .filter(
            DisciplinaryIncident.user_id == user.user_id,
            DisciplinaryIncident.is_deleted != True,
            (DisciplinaryIncident.enable_suspension == True) |
            (DisciplinaryIncident.enable_termination == True)
        )
        .order_by(DisciplinaryIncident.created_at.desc())
        .first()
    )

    is_terminated = False
    is_suspended = False

    if active_incident:
        if active_incident.enable_termination:
            is_terminated = True
            # Wipe all menu/submenu access
            role_map = {}
        elif active_incident.enable_suspension:
            is_suspended = True
            # Keep only allowed submenus across all roles and menus
            for role_id, role in role_map.items():
                for menu_id, menu in role["menus"].items():
                    menu["subMenus"] = [
                        sub for sub in menu["subMenus"]
                        if sub["subMenuId"] in SUSPENSION_ALLOWED_SUBMENUS
                    ]
                # Drop menus that now have no submenus
                role["menus"] = {
                    mid: menu
                    for mid, menu in role["menus"].items()
                    if menu["subMenus"]
                }

    # --- Step 7: Convert maps to lists ---
    role_permissions = []
    for role in role_map.values():
        role["menus"] = list(role["menus"].values())
        role_permissions.append(role)

    # --- Step 8: Final response ---
    return {
        "userId": user.user_id,
        "username": user.username,
        "emailAddress": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "grade": user.grade,

        "supervisorId": user.supervisor_id,
        "supervisorName": supervisor_name,

        "isSupervisor": is_supervisor,
        "isEmployee": user.is_employee,
        "subordinateIds": subordinate_ids,
        "profilePicture": profile_picture_url,

        "roleName": user.role.role_name if user.role else None,
        "stationId": user.station_id,
        "stationName": station_name,

        "accessToken": access_token,
        "accessTokenExpTime": access_exp_time.isoformat(),
        "refreshToken": refresh_token,
        "refreshTokenExpTime": refresh_exp_time.isoformat(),

        "rolePermissions": role_permissions,

        # Optional: surface the disciplinary state to the frontend
        "isSuspended": is_suspended,
        "isTerminated": is_terminated,
        "suspensionEffectiveFrom": active_incident.suspension_effective_from if active_incident else None,
        "suspensionEffectiveTo": active_incident.suspension_effective_to if active_incident else None,
    }


def serialize_profile_picture(path: str):
    if not path:
        return None
    return make_download_url(path)

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError




def refresh_access_token(db, refresh_token: str) -> dict:
    try:
        # print("\n================= REFRESH TOKEN DEBUG =================")
        # print("🔍 Incoming Refresh Token:", refresh_token)

        # Decode refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("🔍 Decoded Refresh Payload:", payload)

        user_id = payload.get("sub")
        exp = payload.get("exp")

        if not user_id:
            # print("❌ DEBUG: No user_id found in refresh token")
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Debug expiration time of refresh token
        refresh_exp_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        # print("⏳ Refresh Token Expires At:", refresh_exp_at)

        # Create NEW access token (30 seconds)
        access_expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # print("⏳ Access Token validity (seconds):", ACCESS_TOKEN_EXPIRE_MINUTES)

        new_access_token = create_access_token(
            {"sub": str(user_id)},
            expires_delta=access_expiry
        )

        now = datetime.now(timezone.utc)
        access_exp_time = now + access_expiry
        # print("🔐 New Access Token Created:", new_access_token)
        # print("⏳ New Access Token Expires At:", access_exp_time)

        # print("=========================================================\n")

        return {
            "accessToken": new_access_token,
            "accessTokenExpTime": access_exp_time.isoformat(),
        }

    except ExpiredSignatureError:
        print("❌ DEBUG: Refresh token has EXPIRED")
        raise HTTPException(status_code=401, detail="Refresh token expired")

    except JWTError as e:
        print("❌ DEBUG: Invalid refresh token error ->", str(e))
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    


import random
import string
import random
import string

def generate_random_password(length: int = 8):
    chars = string.ascii_letters + string.digits + "!@#$%^&*?"
    return ''.join(random.choice(chars) for _ in range(length))

def nullify_empty(value):
    return None if value in ("", " ", None) else value


def create_user_crud(db: Session, user_in: UserCreate_profile) -> dict:

    # Check if username already exists
    exists = db.query(User).filter(User.username == user_in.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Generate random password
    raw_password = generate_random_password(8)

    # Send email
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

    # Create user
    new_user = User(
        role_id=user_in.role_id,
        station_id=user_in.station_id,
        username=user_in.username,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        personal_email=user_in.personal_email,
        contact_phone=user_in.contact_phone,
        emergency_mobile=user_in.emergency_mobile,
        gender=user_in.gender,
        document_details=user_in.document_details,
        comment=user_in.comment,
        employee_code=user_in.employee_code,
        designation=user_in.designation,
        grade=user_in.grade,
        supervisor_id=user_in.supervisor_id,
        sap_location_code=nullify_empty(user_in.sap_location_code),
        employment_type=nullify_empty(user_in.employment_type),
        data_card_number=nullify_empty(user_in.data_card_number),
        date_of_joining=nullify_empty(user_in.date_of_joining),
        dob=nullify_empty(user_in.dob),
        probation_from=nullify_empty(user_in.probation_from),
        probation_to=nullify_empty(user_in.probation_to),
        permanent_from=nullify_empty(user_in.permanent_from),
        blood_group=nullify_empty(user_in.blood_group),
        basic_document_details=user_in.basic_document_details,
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

        bank_name=user_in.bank_name,
        branch_name=user_in.branch_name,
        account_number=user_in.account_number,
        ifsc_code=user_in.ifsc_code,
        account_holder_name=user_in.account_holder_name,
        account_type=user_in.account_type,
        cancelled_cheque=user_in.cancelled_cheque,

        hashed_password=hashed_pw,
        created_by=user_in.created_by,
        created_date=datetime.utcnow()
    )
    print("hiii bro i wam here ")
    run_monthly_leave_cron()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "userId": new_user.user_id,
        "username": new_user.username,
        "email": new_user.email
    }





def update_user_crud(db: Session, user_id: int, user_in: UserUpdate) -> dict:

        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update only fields user sent
        update_fields = user_in.dict(exclude_unset=True)

        for key, value in update_fields.items():
            setattr(user, key, value)

        # Always update the modified date
        user.modified_date = datetime.utcnow()

        db.commit()
        db.refresh(user)
        print("hiii bro i wam here update ")

        run_monthly_leave_cron()
        return {
            "userId": user.user_id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role_id": user.role_id,
            "station_id": user.station_id,
            "contact_phone": user.contact_phone
        }

def get_all_users_crud(db: Session):

    users = (
        db.query(User)
        .options(
            joinedload(User.role),
            joinedload(User.station)
        )
        .filter(User.is_deleted == False)
        .all()
    )

    result = []

    for u in users:
        supervisor_name = None

        if u.supervisor_id:
            supervisor = (
                db.query(User)
                .filter(User.user_id == u.supervisor_id)
                .first()
            )
            if supervisor:
                supervisor_name = " ".join(
                    filter(None, [supervisor.first_name, supervisor.last_name])
                )

        result.append({
            "userId": u.user_id,
            "roleId": u.role_id,
            "roleName": u.role.role_name if u.role else None,
            "stationId": u.station_id,
            "stationName": u.station.station_name if u.station else None,
            "username": u.username,
            "is_employee": u.is_employee,
            "employee_code": u.employee_code,
            "employeeVendorCode": u.employee_vendor_code,
            "supervisorId": u.supervisor_id,
            "supervisorName": supervisor_name,
            "designation": u.designation,
            "firstName": u.first_name,
            "lastName": u.last_name,
            "email": u.email,
            "contactPhone": u.contact_phone,
            "createdBy": u.created_by,
            "createdDate": u.created_date.isoformat() if u.created_date else None,
            "modifiedBy": u.modified_by,
            "modifiedDate": u.modified_date.isoformat() if u.modified_date else None,
            "isDeleted": u.is_deleted
        })

    return result



def get_user_by_id_crud(db: Session, user_id: int):

    user = (
        db.query(User)
        .options(
            joinedload(User.role),
            joinedload(User.station)
        )
        .filter(User.user_id == user_id, User.is_deleted == False)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "userId": user.user_id,
        "roleId": user.role_id,
        "roleName": user.role.role_name if user.role else None,
        "stationId": user.station_id,
        "is_employee":user.is_employee,
        "stationName": user.station.station_name if user.station else None,
        "username": user.username,
                "employee_code": user.employee_code,
        "designation": user.designation,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "contactPhone": user.contact_phone,
        "profilePic": user.profile_pic,
        "createdBy": user.created_by,
        "createdDate": user.created_date.isoformat() if user.created_date else None,
        "modifiedBy": user.modified_by,
        "modifiedDate": user.modified_date.isoformat() if user.modified_date else None,
        "isDeleted": user.is_deleted
    }


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    db.execute(text("SELECT delete_user_hard(:uid)"), {"uid": user_id})
    db.commit()

    return {"message": "User permanently deleted", "user_id": user_id}