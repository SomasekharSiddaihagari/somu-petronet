from datetime import datetime
import os
import shutil
from typing import List, Optional, Union
import urllib.parse
import uuid
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException,BackgroundTasks
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.crud.employees_info.employee_education import get_educations_by_user_id
from sqlalchemy import text
from sqlalchemy.orm import Session, selectinload
from fastapi import Depends
from app.crud.employees_info.employee_notifications_crud import get_all_hr_usernames, handle_employee_update_notifications, notify_employee_on_status_change
from app.database import get_db
from app.models.MOC.StationModel import Station
from app.models.UserModel import User
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Union
from datetime import datetime
import json
import os
import shutil
import uuid
router = APIRouter(prefix="/api/usersProfile", tags=["Users crud for profile"])

UPLOAD_FOLDER = "files/users_file"


def make_download_url(path: str) -> str:
    if not path:
        return None

    base_url = os.getenv("BackEndPath")

    file_path = path.replace("\\", "/")

    if ":" in file_path:
        file_path = file_path.split(":", 1)[1]

    if file_path.startswith("/Petronet"):
        file_path = file_path.replace("/Petronet", "", 1)

    file_path = "/" + file_path.lstrip("/")
    encoded_path = urllib.parse.quote(file_path)

    return f"{base_url}{encoded_path}"


from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Union
from datetime import datetime
import json
import os
import shutil
import uuid





INT_FIELDS = {
    "station_id",
    "supervisor_id",
    "contact_phone",
    "emergency_mobile",
}


def clean(v):
    return None if v in ["", " ", "null", "None", None] else v

def clean_field(field, value):
    value = clean(value)
    if value is None:
        return None

    if field in INT_FIELDS:
        try:
            return int(value)
        except:
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field}' must be a number. Got '{value}'"
            )

    return value

def to_date(v):
    v = clean(v)
    if not v:
        return None

    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(v, fmt).date()
        except:
            pass

    raise HTTPException(
        status_code=400,
        detail=f"Invalid date format: {v}. Use YYYY-MM-DD or DD-MM-YYYY"
    )


def update_user_crud(db, user_id, user_data, file_paths):
    """
    Update user using SQL query with all data and file paths
    """
    try:
        # print("\n========== CRUD FUNCTION START ==========")
        # print(f"🔹 User ID: {user_id}")
        # print(f"🔹 User Data Keys: {list(user_data.keys())}")
        # print(f"🔹 File Paths: {file_paths}")

        # Check if user exists
        # print("\n🔹 Checking user existence in DB...")
        user_exists = db.execute(
            text("SELECT 1 FROM users WHERE user_id = :uid AND is_deleted = false"),
            {"uid": user_id}
        ).fetchone()

        # print("🔸 User exists:", bool(user_exists))

        if not user_exists:
            raise HTTPException(404, "User not found")

        # Build update fields
        sql_fields = {}
        
        # Add all user data fields (including None values)
        # print("\n🔹 PROCESSING USER DATA FIELDS:")
        for field, value in user_data.items():
            sql_fields[field] = value
            # print(f"  {field}: {value}")

        # Add file paths - ALWAYS include file fields (including None values)
        # print("\n🔹 PROCESSING FILE FIELDS:")
        for field, file_path in file_paths.items():
            sql_fields[field] = file_path
            # print(f"  {field}: {file_path}")

        # Build and execute SQL - update even if values are None
        if sql_fields:
            set_sql = ", ".join([f"{k} = :{k}" for k in sql_fields])
            params = {**sql_fields, "uid": user_id}

            # print("\n🔹 FINAL SQL FIELDS TO UPDATE:")
            # for k, v in sql_fields.items():
                # print(f"  {k}: {v}")

            sql = f"""
                UPDATE users
                SET {set_sql}
                WHERE user_id = :uid
            """

            # print("\n🔹 EXECUTING SQL UPDATE...")

            try:
                db.execute(text(sql), params)
                db.commit()
                # print("✅ UPDATE COMPLETED")
            except Exception as e:
                db.rollback()
                # print(f"❌ UPDATE FAILED: {e}")
                raise HTTPException(500, f"Database update failed: {e}")


        # print("========== CRUD FUNCTION END ==========\n")
        return True

    except Exception as e:
        db.rollback()
        # print(f"❌ CRUD ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.get("/by-supervisor-for-drop-down/{user_id}")
def get_users_by_supervisor(
    user_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT *
            FROM users
            WHERE supervisor_id = :supervisor_id
        """),
        {"supervisor_id": user_id}
    )

    rows = result.mappings().all()  # 🔥 KEY LINE

    return {
        "success": True,
        "count": len(rows),
        "data": rows
    }

def build_changed_fields(old_user, new_data: dict, existing_changes: list):
    result = []

    # Convert existing list → dict for quick access
    existing_map = {item["field"]: item for item in existing_changes}


    for field, new_value in new_data.items():

        # skip nulls
        if new_value in ["", None, " ", "null"]:
            continue

        old_value = getattr(old_user, field, None)

        # normalize
        if hasattr(old_value, "isoformat"):
            old_value = old_value.isoformat()
        if hasattr(new_value, "isoformat"):
            new_value = new_value.isoformat()

        # -------------------------------
        # CASE 1: FIELD NOT EXIST BEFORE
        # -------------------------------
        if field not in existing_map:
            result.append({
                "field": field,
                "old": old_value,
                "new": new_value
            })

        # -------------------------------
        # CASE 2: FIELD EXISTS → UPDATE
        # -------------------------------
        else:
            prev = existing_map[field]

            result.append({
                "field": field,
                "old": prev["new"],   # previous new becomes old
                "new": new_value
            })

    return result

def get_only_changed_fields(old_user, new_data: dict):
    changes = []

    for field, new_value in new_data.items():

        if new_value in ["", None, " ", "null"]:
            continue

        old_value = getattr(old_user, field, None)

        # normalize
        if hasattr(old_value, "isoformat"):
            old_value = old_value.isoformat()
        if hasattr(new_value, "isoformat"):
            new_value = new_value.isoformat()

        # ✅ ONLY DIFFERENCE
        if str(old_value) != str(new_value):
            changes.append({
                "field": field,
                "old": old_value,
                "new": new_value
            })

    return changes


@router.put("/update")
async def update_user(
    user_id: int = Query(...),

    # -------- BASIC INFO --------
    username: Optional[str] = Form(None),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    contact_phone: Optional[str] = Form(None),
    emergency_mobile: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    personal_email: Optional[str] = Form(None),
    comments: Optional[str] = Form(None),
    is_employee: Optional[bool] = Form(None),

    # -------- EMPLOYMENT --------
    employee_vendor_code: Optional[str] = Form(None),
    employee_code: Optional[str] = Form(None),
    designation: Optional[str] = Form(None),
    station_id: Optional[str] = Form(None),
    grade: Optional[str] = Form(None),
    supervisor_id: Optional[str] = Form(None),
    sap_location_code: Optional[str] = Form(None),
    employment_type: Optional[str] = Form(None),
    status: Optional[str] = Form(None),

    # -------- DATES --------
    date_of_joining: Optional[str] = Form(None),
    dob: Optional[str] = Form(None),
    probation_from: Optional[str] = Form(None),
    probation_to: Optional[str] = Form(None),
    permanent_from: Optional[str] = Form(None),

    # -------- ADDRESS --------
    current_address: Optional[str] = Form(None),
    permanent_address: Optional[str] = Form(None),

    # -------- IDENTITY --------
    aadhaar: Optional[str] = Form(None),
    pan: Optional[str] = Form(None),
    driving_license: Optional[str] = Form(None),
    passport: Optional[str] = Form(None),

    # -------- BANK --------
    bank_name: Optional[str] = Form(None),
    branch_name: Optional[str] = Form(None),
    account_number: Optional[str] = Form(None),
    ifsc_code: Optional[str] = Form(None),
    account_holder_name: Optional[str] = Form(None),
    account_type: Optional[str] = Form(None),
    blood_group: Optional[str] = Form(None),
    status_basic_info: Optional[str] = Form(None),
    status_address: Optional[str] = Form(None),
    status_bank: Optional[str] = Form(None),
    status_identity_proof: Optional[str] = Form(None),
    data_card_number: Optional[str]=Form(None),
    # -------- FILES --------
    current_address_proof: List[UploadFile] = File([]),
    permanent_address_proof: List[UploadFile] = File([]),
    aadhaar_file: Optional[UploadFile] = File(None),
    pan_file: Optional[UploadFile] = File(None),
    driving_license_file: Optional[UploadFile] = File(None),
    passport_file: Optional[UploadFile] = File(None),
    cancelled_cheque: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None,
    document_details: Optional[str] = Form(None),
    comment: Optional[str] = Form(None),
    basic_document_details: Optional[str] = Form(None),
    basic_comment: Optional[str] = Form(None),
    pr_address_document_details: Optional[str] = Form(None),
    cr_address_document_details: Optional[str] = Form(None),
    
    address_document_details: Optional[str] = Form(None),
    address_comment: Optional[str] = Form(None),
    identity_document_details: Optional[str] = Form(None),
    identity_comment: Optional[str] = Form(None),
    
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(404, "User not found")

        import copy
        old_user = copy.deepcopy(user)

        print("\n========== UPDATE DEBUG START ==========")
        print(f"USER ID: {user_id}")

        # -------- TEXT / BOOL FIELDS --------
        fields = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "contact_phone": contact_phone,
            "emergency_mobile": emergency_mobile,
            "email": email,
            "personal_email": personal_email,
            "comments": comments,
            "is_employee": is_employee,
            "employee_code": employee_code,
            "designation": designation,
            "station_id": station_id,
            "grade": grade,
            "supervisor_id": supervisor_id,
            "employee_vendor_code": employee_vendor_code,
            "sap_location_code": sap_location_code,
            "employment_type": employment_type,
            "status": status,
            "current_address": current_address,
            "permanent_address": permanent_address,
            "aadhaar": aadhaar,
            "pan": pan,
            "blood_group": blood_group,
            "driving_license": driving_license,
            "passport": passport,
            "bank_name": bank_name,
            "branch_name": branch_name,
            "account_number": account_number,
            "ifsc_code": ifsc_code,
            "account_holder_name": account_holder_name,
            "account_type": account_type,
            "status_basic_info": status_basic_info,
            "status_address": status_address,
            "status_bank": status_bank,
            "status_identity_proof": status_identity_proof,
            "data_card_number": data_card_number,
            "document_details": document_details,
            "basic_document_details": basic_document_details,
            "basic_comment": basic_comment,
            "pr_address_document_details": pr_address_document_details,
            "cr_address_document_details": cr_address_document_details,
            "address_document_details": address_document_details,
            "address_comment": address_comment,
            "identity_document_details": identity_document_details,
            "identity_comment": identity_comment,
            "comment": comment
        }

        for field, incoming in fields.items():
            if incoming is None:
                continue

            old_value = getattr(user, field)
            new_value = clean(incoming)

            print(f"\nFIELD: {field}")
            print(f"  OLD : {old_value!r}")
            print(f"  NEW : {new_value!r}")

            setattr(user, field, new_value)

        # -------- DATE FIELDS --------
        date_fields = {
            "date_of_joining": date_of_joining,
            "dob": dob,
            "probation_from": probation_from,
            "probation_to": probation_to,
            "permanent_from": permanent_from,
        }

        for field, incoming in date_fields.items():
            if incoming is None:
                continue

            old_value = getattr(user, field)
            new_value = to_date(incoming)

            print(f"\nDATE FIELD: {field}")
            print(f"  OLD : {old_value}")
            print(f"  NEW : {new_value}")

            setattr(user, field, new_value)

        # -------- FILE FIELDS --------
        file_fields = {
            "current_address_proof": current_address_proof,
            "permanent_address_proof": permanent_address_proof,
            "aadhaar_file": aadhaar_file,
            "pan_file": pan_file,
            "driving_license_file": driving_license_file,
            "passport_file": passport_file,
            "cancelled_cheque": cancelled_cheque,
        }

        for field, file_data in file_fields.items():
            if not file_data:
                continue

            # MULTIPLE FILES
            if isinstance(file_data, list):
                stored_files = []
                for file in file_data:
                    saved_path = save_file(file, user_id, field)
                    stored_files.append(saved_path)

                old_value = getattr(user, field)
                print(f"\nMULTI FILE FIELD: {field}")
                print(f"  OLD : {old_value}")
                print(f"  NEW : {stored_files}")

                setattr(user, field, ",".join(stored_files))

            # SINGLE FILE
            else:
                old_value = getattr(user, field)
                new_value = save_file(file_data, user_id, field)

                print(f"\nFILE FIELD: {field}")
                print(f"  OLD : {old_value}")
                print(f"  NEW : {new_value}")

                setattr(user, field, new_value)

        # -------- COMMIT --------
        print("\n========== COMMITTING ==========")
        # Preserve old status/comments for notification
        import copy
        old_status = user.status
        old_comments = user.comments
        new_data = {}
        section_map = {
                "Basic Info": ["username","first_name","last_name","gender","contact_phone",
                               "emergency_mobile","email","personal_email"],
                "Address": ["current_address","permanent_address",
                            "current_address_proof","permanent_address_proof"],
                "Bank Account": ["bank_name","branch_name","account_number","ifsc_code",
                                 "account_holder_name","account_type","cancelled_cheque"],
                "Identity Proof": ["aadhaar","pan","driving_license","passport",
                                   "aadhaar_file","pan_file","driving_license_file","passport_file"]
            }

        # 🔥 STEP 1: decide allowed fields
        allowed_fields = set()

        if status_basic_info and status_basic_info.lower() in ["approved", "changes requested"]:
            allowed_fields.update(section_map["Basic Info"])

        if status_address and status_address.lower() in ["approved", "changes requested"]:
            allowed_fields.update(section_map["Address"])

        if status_identity_proof and status_identity_proof.lower() in ["approved", "changes requested"]:
            allowed_fields.update(section_map["Identity Proof"])

        if status_bank and status_bank.lower() in ["approved", "changes requested"]:
            allowed_fields.update(section_map["Bank Account"])


        # 🔥 STEP 2: filter fields BEFORE building changes
        for k, v in fields.items():
            if v is None:
                continue

            if allowed_fields and k not in allowed_fields:
                continue

            new_data[k] = v

        # Add date fields
        for k, v in date_fields.items():
            if v is None:
                continue

            if len(allowed_fields) > 0 and k not in allowed_fields:
                continue

            new_data[k] = to_date(v)
        # 1️⃣ Get existing from DB
        row = db.execute(
            text("SELECT changed_fields FROM users WHERE user_id = :uid"),
            {"uid": user_id}
        ).fetchone()

        existing_changes = []

        if row and row[0]:
            try:
                data = row[0] if isinstance(row[0], dict) else json.loads(row[0])
                existing_changes = data.get("changed_fields", [])
            except:
                existing_changes = []

        # 2️⃣ Build new structured changes
        changed_fields = build_changed_fields(old_user, new_data, existing_changes)

        # 3️⃣ Merge (replace same fields, not append blindly)
        final_map = {item["field"]: item for item in existing_changes}

        for item in changed_fields:
            final_map[item["field"]] = item

        final_changes = list(final_map.values())
                           # Detect changed sections based on incoming fields and file uploads
        section_map = {
                "Basic Info": ["username","first_name","last_name","gender","contact_phone",
                               "emergency_mobile","email","personal_email"],
                "Address": ["current_address","permanent_address",
                            "current_address_proof","permanent_address_proof"],
                "Bank Account": ["bank_name","branch_name","account_number","ifsc_code",
                                 "account_holder_name","account_type","cancelled_cheque"],
                "Identity Proof": ["aadhaar","pan","driving_license","passport",
                                   "aadhaar_file","pan_file","driving_license_file","passport_file"]
            }
        # -------------------------------

        # 4️⃣ Save
        db.execute(text("""
        UPDATE users
        SET changed_fields = :fields
        WHERE user_id = :uid
        """), {
            "fields": json.dumps({
                "changed_fields": final_changes
            }),
            "uid": user_id
        })

        print("🔥 Changed fields:", changed_fields)
        db.commit()
        db.refresh(user)

        print("\n========== FINAL VALUES ==========")
        for field in fields.keys():
            print(f"{field}: {getattr(user, field)!r}")
        for field in date_fields.keys():
            print(f"{field}: {getattr(user, field)}")

        print("========== UPDATE DEBUG END ==========")

        # -------------------------------------------------
        # TRIGGER NOTIFICATIONS (same behaviour as old implementation)
        # -------------------------------------------------
        try:
            new_status = user.status
            new_comments = user.comments

            # Detect changed sections based on incoming fields and file uploads
            section_map = {
                "Basic Info": ["username","first_name","last_name","gender","contact_phone",
                               "emergency_mobile","email","personal_email"],
                "Address": ["current_address","permanent_address",
                            "current_address_proof","permanent_address_proof"],
                "Bank Account": ["bank_name","branch_name","account_number","ifsc_code",
                                 "account_holder_name","account_type","cancelled_cheque"],
                "Identity Proof": ["aadhaar","pan","driving_license","passport",
                                   "aadhaar_file","pan_file","driving_license_file","passport_file"]
            }

            changed_sections = []

            # `fields` contains incoming scalar values (None if not provided)
            # `file_fields` contains uploaded files (empty/None if not provided)
            for sec, sec_fields in section_map.items():
                for f in sec_fields:
                    if f in fields and fields.get(f) is not None:
                        changed_sections.append(sec)
                        break
                    if f in file_fields and file_fields.get(f):
                        changed_sections.append(sec)
                        break
        
            notification_changed_fields = get_only_changed_fields(old_user, new_data)

            print("🔥 ONLY DIFF:", notification_changed_fields)

            employee_username = user.username

 # -------- BASIC INFO NOTIFICATION --------
            if status_basic_info and status_basic_info.lower() == "pending approval":
 
                await handle_employee_update_notifications(
                    db=db,
                    old_status=old_status,
                    new_status=status_basic_info,
                    old_comments=old_comments,
                    new_comments=None,
                    employee_username=employee_username,
                    changed_sections=["Basic Info"],
                    changed_fields=notification_changed_fields,
                    reference_id=str(user_id),
                    redirect_url=f"/profile/profile-info/{str(user_id)}/review",
                    bg=background_tasks
                )
 
            elif status_basic_info and status_basic_info.lower() in ["approved", "changes requested"]:
 
                hr = get_all_hr_usernames(db)
                hr_username = hr[0] if hr else "HR"
 
                await notify_employee_on_status_change(
                    db=db,
                    employee_username=employee_username,
                    hr_username=hr_username,
                    new_status=status_basic_info,
                    comments=None,
                    changed_sections="Basic Info",
                    reference_id=str(user_id),
                    redirect_url=f"/profile/{str(user_id)}",
                    bg=background_tasks
                )
 
            # -------- ADDRESS NOTIFICATION --------
            if status_address and status_address.lower() == "pending approval":
 
                await handle_employee_update_notifications(
                    db=db,
                    old_status=old_status,
                    new_status=status_address,
                    old_comments=old_comments,
                    new_comments=None,
                    employee_username=employee_username,
                    changed_sections=["Address"],
                    changed_fields=notification_changed_fields,
                    reference_id=str(user_id),
                    redirect_url=f"/profile/profile-info/{str(user_id)}/review",
                    bg=background_tasks
                )
 
            elif status_address and status_address.lower() in ["approved", "changes requested"]:
 
                hr = get_all_hr_usernames(db)
                hr_username = hr[0] if hr else "HR"
 
                await notify_employee_on_status_change(
                    db=db,
                    employee_username=employee_username,
                    hr_username=hr_username,
                    new_status=status_address,
                    comments=None,
                    changed_sections="Address info",
                    reference_id=str(user_id),
                    redirect_url=f"/profile/{str(user_id)}",
                    bg=background_tasks
                )
 
            # -------- BANK NOTIFICATION --------
            # if status_bank and status_bank.lower() == "pending approval":
 
            #     await handle_employee_update_notifications(
            #         db=db,
            #         old_status=old_status,
            #         new_status=status_bank,
            #         old_comments=old_comments,
            #         new_comments=None,
            #         employee_username=employee_username,
            #         changed_sections=["Bank"],
            #         changed_fields=changed_fields,
            #         reference_id=str(user_id),
            #         redirect_url=f"/profile/{user_id}",
            #         bg=background_tasks
            #     )
 
            # elif status_bank and status_bank.lower() in ["approved", "changes requested"]:
 
            #     hr = get_all_hr_usernames(db)
            #     hr_username = hr[0] if hr else "HR"
 
            #     await notify_employee_on_status_change(
            #         db=db,
            #         employee_username=employee_username,
            #         hr_username=hr_username,
            #         new_status=status_bank,
            #         comments=None,
            #         changed_sections="Bank info",
            #         reference_id=str(user_id),
            #         redirect_url=f"/profile/{user_id}",
            #         bg=background_tasks
            #     )
 
            # -------- IDENTITY PROOF NOTIFICATION --------
            if status_identity_proof and status_identity_proof.lower() == "pending approval":
 
                await handle_employee_update_notifications(
                    db=db,
                    old_status=old_status,
                    new_status=status_identity_proof,
                    old_comments=old_comments,
                    new_comments=None,
                    employee_username=employee_username,
                    changed_sections=["Identity Proof"],
                    changed_fields=notification_changed_fields, 
                    reference_id=str(user_id),
                    redirect_url=f"/profile/profile-info/{str(user_id)}/review", 
                    bg=background_tasks
                )
 
            elif status_identity_proof and status_identity_proof.lower() in ["approved", "changes requested"]:
 
                hr = get_all_hr_usernames(db)
                hr_username = hr[0] if hr else "HR"
 
                await notify_employee_on_status_change(
                    db=db,
                    employee_username=employee_username,
                    hr_username=hr_username,
                    new_status=status_identity_proof,
                    comments=None,
                    changed_sections="Identity Proof info",
                    reference_id=str(user_id),
                    redirect_url=f"/profile/{str(user_id)}",
                    bg=background_tasks
                )
 
            return {
                    "status": True,
                    "message": "User updated successfully",
                    "data": {
                         "user_id": user.user_id,
                        "username": user.username,
                     },
                    "changes": {
                        "changed_fields": final_changes,
                        "changed_sections": changed_sections
                    }
}
 
        except HTTPException:
            raise
 
    except Exception:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(500, "Internal server error")


def clean(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value if value != "" else None
    return value  # bool, int, etc.


def to_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def save_file(file: UploadFile, user_id: int, field: str):
    ext = os.path.splitext(file.filename)[1]
    name = f"{field}_{user_id}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_FOLDER, "users", name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path.replace("\\", "/")


#====================== ENDPOINT ========================#



def get_station_name(db: Session, station_id: int | None):
    if not station_id:
        return None
    station = db.query(Station).filter(Station.station_id == station_id).first()
    return station.station_name if station else None


def get_supervisor_name(db: Session, supervisor_id: int | None):
    if not supervisor_id:
        return None
    supervisor = db.query(User).filter(User.user_id == supervisor_id).first()
    if supervisor:
        return f"{supervisor.first_name} {supervisor.last_name}".strip()
    return None



# @router.get("/{user_id}")
# def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
#     user = (
#         db.query(User)
#         .filter(User.user_id == user_id, User.is_deleted == False)
#         .first()
#     )

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # ---------------- FILE HELPERS ----------------
#     def file_link(path):
#         return make_download_url(path) if path else None

#     def multiple_file_links(paths_string):
#         if not paths_string:
#             return []
#         paths = [p.strip() for p in paths_string.split(',') if p.strip()]
#         return [make_download_url(path) for path in paths]

#     # ---------------- EXTRA FIELDS ----------------
#     station_name = get_station_name(db, user.station_id)
#     supervisor_name = get_supervisor_name(db, user.supervisor_id)
#     education_details = get_educations_by_user_id(db, user_id)

#     # ================= PROCESS EDUCATION DETAILS =================
#     education_details_processed = []
#     for edu in education_details:
#         e = dict(edu) if isinstance(edu, dict) else {k: v for k, v in edu.__dict__.items() if not k.startswith('_')}
#         e["education_document"] = file_link(e.get("education_document"))
#         education_details_processed.append(e)

#     education_global_status = next(
#         (e.get("status") for e in reversed(education_details) if e.get("status")),
#         None
#     )

#     family_global_status = next(
#         (f.status for f in reversed(user.family_members or []) if f.status),
#         None
#     )

#     vehicle_global_status = next(
#         (v.status for v in reversed(user.vehicles or []) if v.status),
#         None
#     )

#     # ================= SUBMISSION DETAILS =================
#     submission_rows = db.execute(
#         text("""
#             SELECT submission_id, user_id, status, hr_comment, created_at
#             FROM submission
#             WHERE user_id = :uid
#             ORDER BY created_at DESC
#         """),
#         {"uid": user_id}
#     ).fetchall()

#     # ================= FAMILY STATUS DETAILS =================
#     family_rows = db.execute(
#         text("""
#             SELECT DISTINCT s.submission_id, s.user_id, s.status, s.hr_comment, s.created_at
#             FROM submission s
#             JOIN employee_family ef
#             ON s.submission_id = ef.submission_id
#             WHERE ef.user_id = :uid
#             ORDER BY s.created_at DESC
#         """),
#         {"uid": user_id}
#     ).fetchall()

#     family_status_details = [dict(r._mapping) for r in family_rows]

#     # ================= EDUCATION STATUS DETAILS =================
#     education_submission_rows = db.execute(
#         text("""
#             SELECT DISTINCT s.submission_id, s.user_id, s.status, s.hr_comment, s.created_at
#             FROM submission s
#             JOIN user_education ue
#             ON s.submission_id = ue.submission_id
#             WHERE ue.user_id = :uid
#             ORDER BY s.created_at DESC
#         """),
#         {"uid": user_id}
#     ).fetchall()

#     education_status_details = [dict(r._mapping) for r in education_submission_rows]

#     # ================= BANK DETAILS =================
#     import json

#     bank_rows = db.execute(
#         text("""
#             SELECT 
#                 id,
#                 user_id,
#                 bank_name,
#                 branch_name,
#                 account_number,
#                 ifsc_code,
#                 account_holder_name,
#                 account_type,
#                 cancelled_cheque,
#                 document_details,
#                 comment,
#                 document_name,
#                 is_active,
#                 status,
#                 remarks
#             FROM employee_bank
#             WHERE user_id = :uid
#             ORDER BY id DESC
#         """),
#         {"uid": user_id}
#     ).fetchall()

#     def parse_document_links(document_name_field):
#         if not document_name_field:
#             return []
#         try:
#             paths = json.loads(document_name_field)
#             if isinstance(paths, list):
#                 return [make_download_url(p.strip()) for p in paths if p.strip()]
#         except (json.JSONDecodeError, TypeError):
#             pass
#         paths = [p.strip() for p in document_name_field.split(',') if p.strip()]
#         return [make_download_url(p) for p in paths]

#     bank_details = []
#     for r in bank_rows:
#         row = dict(r._mapping)
#         row["cancelled_cheque"] = file_link(row.get("cancelled_cheque"))
#         row["document_links"] = parse_document_links(row.get("document_name"))
#         bank_details.append(row)

#     # ================= PROCESS FAMILY MEMBERS =================
#     family_members_processed = []
#     for member in (user.family_members or []):
#         m = {k: v for k, v in member.__dict__.items() if not k.startswith('_')}
#         m["document"] = file_link(m.get("document"))
#         family_members_processed.append(m)

#     # ================= PROCESS ASSET DECLARATION =================
#     asset_declaration_processed = []
#     for asset in (user.asset_declaration or []):
#         a = {k: v for k, v in asset.__dict__.items() if not k.startswith('_')}
#         a["document"] = file_link(a.get("document"))
#         a["signature"] = file_link(a.get("signature"))
#         asset_declaration_processed.append(a)

#     # ================= PROCESS FORM 12C =================
#     form_12c_processed = None
#     if user.form_12c:
#         form_12c_processed = {k: v for k, v in user.form_12c.__dict__.items() if not k.startswith('_')}
#         form_12c_processed["upload_document"] = file_link(form_12c_processed.get("upload_document"))
#         form_12c_processed["signature"] = file_link(form_12c_processed.get("signature"))

#     # ================= PROCESS VEHICLES =================
#     vehicles_processed = []
#     for vehicle in (user.vehicles or []):
#         v = {k: v for k, v in vehicle.__dict__.items() if not k.startswith('_')}
#         v["document_upload"] = file_link(v.get("document_upload"))
#         vehicles_processed.append(v)

#     # ---------------- RESPONSE ----------------
#     payload =  {
#         "user_id": user.user_id,
#         "username": user.username,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "gender": user.gender,
#         "contact_phone": user.contact_phone,
#         "emergency_mobile": user.emergency_mobile,
#         "personal_email": user.personal_email,
#         "employee_code": user.employee_code,
#         "email": user.email,
#         "is_employee": user.is_employee,
#         "education_status": education_global_status,
#         "family_status": family_global_status,
#         "vehicle_status": vehicle_global_status,

#         "designation": user.designation,
#         "station_id": user.station_id,
#         "station_name": station_name,
#         "supervisor_id": user.supervisor_id,
#         "supervisor_name": supervisor_name,

#         "grade": user.grade,
#         "sap_location_code": user.sap_location_code,
#         "employee_vendor_code": user.employee_vendor_code,
#         "employment_type": user.employment_type,

#         "date_of_joining": user.date_of_joining,
#         "dob": user.dob,
#         "blood_group": user.blood_group,
#         "probation_from": user.probation_from,
#         "probation_to": user.probation_to,
#         "permanent_from": user.permanent_from,

#         "current_address": user.current_address,
#         "current_address_proof": file_link(user.current_address_proof),
#         "permanent_address": user.permanent_address,
#         "permanent_address_proof": file_link(user.permanent_address_proof),

#         "status": user.status,
#         "aadhaar": user.aadhaar,
#         "aadhaar_file": file_link(user.aadhaar_file),
#         "pan": user.pan,
#         "pan_file": file_link(user.pan_file),

#         "driving_license": user.driving_license,
#         "driving_license_file": file_link(user.driving_license_file),
#         "passport": user.passport,
#         "passport_file": file_link(user.passport_file),

#         "bank_name": user.bank_name,
#         "branch_name": user.branch_name,
#         "account_number": user.account_number,
#         "ifsc_code": user.ifsc_code,
#         "account_holder_name": user.account_holder_name,
#         "account_type": user.account_type,
#         "cancelled_cheque": file_link(user.cancelled_cheque),
#         "basic_document_details": user.basic_document_details,
#         "basic_comment": user.basic_comment,
#         "pr_address_document_details": user.pr_address_document_details,
#         "cr_address_document_details": user.cr_address_document_details,
#         "address_document_details": user.address_document_details,
#         "address_comment": user.address_comment,
#         "identity_document_details": user.identity_document_details,
#         "identity_comment": user.identity_comment,
#         "profile_pic": file_link(user.profile_pic),
#         "upload_document": multiple_file_links(user.upload_document),

#         "education_details": education_details_processed,
#         "finance": user.finance,
#         "asset_declaration": asset_declaration_processed,

#         "family_members": family_members_processed,

#         "form_12c": form_12c_processed,
#         "vehicles": vehicles_processed,

#         "role": user.role,
#         "data_card_number": user.data_card_number,
#         "status_basic_info": user.status_basic_info,
#         "status_address": user.status_address,
#         "status_bank": user.status_bank,
#         "status_identity_proof": user.status_identity_proof,

#         "family_status_details": family_status_details,
#         "education_status_details": education_status_details,

#         "bank_details": bank_details,
#     }
#     return JSONResponse(
#         content=jsonable_encoder(
#             payload,
#             custom_encoder={float: lambda v: None if math.isnan(v) else v}
#         )
#     )

@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.user_id == user_id, User.is_deleted == False)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ---------------- FILE HELPERS ----------------
    def file_link(path):
        return make_download_url(path) if path else None

    def multiple_file_links(paths_string):
        if not paths_string:
            return []
        paths = [p.strip() for p in paths_string.split(',') if p.strip()]
        return [make_download_url(path) for path in paths]

    # ---------------- EXTRA FIELDS ----------------
    station_name = get_station_name(db, user.station_id)
    supervisor_name = get_supervisor_name(db, user.supervisor_id)
    education_details = get_educations_by_user_id(db, user_id)

    # ================= PROCESS EDUCATION DETAILS =================
    education_details_processed = []
    for edu in education_details:
        e = dict(edu) if isinstance(edu, dict) else {k: v for k, v in edu.__dict__.items() if not k.startswith('_')}
        e["education_document"] = file_link(e.get("education_document"))
        education_details_processed.append(e)

    education_global_status = next(
        (e.get("status") for e in reversed(education_details) if e.get("status")),
        None
    )

    family_global_status = next(
        (f.status for f in reversed(user.family_members or []) if f.status),
        None
    )

    vehicle_global_status = next(
        (v.status for v in reversed(user.vehicles or []) if v.status),
        None
    )

    # ================= SUBMISSION DETAILS =================
    submission_rows = db.execute(
        text("""
            SELECT submission_id, user_id, status, hr_comment, created_at
            FROM submission
            WHERE user_id = :uid
            ORDER BY created_at DESC
        """),
        {"uid": user_id}
    ).fetchall()

    # ================= FAMILY STATUS DETAILS =================
    family_rows = db.execute(
        text("""
            SELECT DISTINCT s.submission_id, s.user_id, s.status, s.hr_comment, s.created_at
            FROM submission s
            JOIN employee_family ef
            ON s.submission_id = ef.submission_id
            WHERE ef.user_id = :uid
            ORDER BY s.created_at DESC
        """),
        {"uid": user_id}
    ).fetchall()

    family_status_details = [dict(r._mapping) for r in family_rows]

    # ================= EDUCATION STATUS DETAILS =================
    education_submission_rows = db.execute(
        text("""
            SELECT DISTINCT s.submission_id, s.user_id, s.status, s.hr_comment, s.created_at
            FROM submission s
            JOIN user_education ue
            ON s.submission_id = ue.submission_id
            WHERE ue.user_id = :uid
            ORDER BY s.created_at DESC
        """),
        {"uid": user_id}
    ).fetchall()

    education_status_details = [dict(r._mapping) for r in education_submission_rows]

    # ================= BANK DETAILS =================
    import json

    bank_rows = db.execute(
        text("""
            SELECT 
                id,
                user_id,
                bank_name,
                branch_name,
                account_number,
                ifsc_code,
                account_holder_name,
                account_type,
                cancelled_cheque,
                document_details,
                comment,
                document_name,
                is_active,
                status,
                remarks
            FROM employee_bank
            WHERE user_id = :uid
            ORDER BY id DESC
        """),
        {"uid": user_id}
    ).fetchall()

    def parse_document_links(document_name_field):
        if not document_name_field:
            return []
        try:
            paths = json.loads(document_name_field)
            if isinstance(paths, list):
                return [make_download_url(p.strip()) for p in paths if p.strip()]
        except (json.JSONDecodeError, TypeError):
            pass
        paths = [p.strip() for p in document_name_field.split(',') if p.strip()]
        return [make_download_url(p) for p in paths]

    bank_details = []
    for r in bank_rows:
        row = dict(r._mapping)
        row["cancelled_cheque"] = file_link(row.get("cancelled_cheque"))
        row["document_links"] = parse_document_links(row.get("document_name"))
        bank_details.append(row)

    # ================= PROCESS FAMILY MEMBERS =================
    family_members_processed = []
    for member in (user.family_members or []):
        m = {k: v for k, v in member.__dict__.items() if not k.startswith('_')}
        m["document"] = file_link(m.get("document"))
        family_members_processed.append(m)

    # ================= PROCESS ASSET DECLARATION =================
    asset_declaration_processed = []
    for asset in (user.asset_declaration or []):
        a = {k: v for k, v in asset.__dict__.items() if not k.startswith('_')}
        a["document"] = file_link(a.get("document"))
        a["signature"] = file_link(a.get("signature"))
        asset_declaration_processed.append(a)

    # ================= PROCESS FORM 12C =================
    form_12c_processed = None
    if user.form_12c:
        form_12c_processed = {k: v for k, v in user.form_12c.__dict__.items() if not k.startswith('_')}
        form_12c_processed["upload_document"] = file_link(form_12c_processed.get("upload_document"))
        form_12c_processed["signature"] = file_link(form_12c_processed.get("signature"))

    # ================= PROCESS VEHICLES =================
    vehicles_processed = []
    for vehicle in (user.vehicles or []):
        v = {k: v for k, v in vehicle.__dict__.items() if not k.startswith('_')}
        v["document_upload"] = file_link(v.get("document_upload"))
        vehicles_processed.append(v)

    # ================= FINANCE DETAILS =================
    finance_rows = db.execute(
        text("""
            SELECT
                user_finance_id,
                user_id,
                date,
                financial_year,
                opting_for_concessional_rate,
                residing_in_rented_house,
                monthly_rent,
                landlord_name,
                temporary_address,
                pension_plan,
                lic_premium,
                ppf,
                ulip,
                tuition_fees,
                nsc,
                nsc_interest,
                housing_loan_repayment,
                other_investments,
                medical_insurance_80d,
                interest_housing_24b,
                infrastructure_bond,
                educational_loan_interest,
                contribution_to_nps,
                upload_document,
                declaration_text,
                signature_name,
                status
            FROM user_finance
            WHERE user_id = :uid
            ORDER BY user_finance_id DESC
        """),
        {"uid": user_id}
    ).fetchall()

    finance_list = []
    for r in finance_rows:
        row = dict(r._mapping)
        row["upload_document"] = file_link(row.get("upload_document"))
        row["signature_name"] = file_link(row.get("signature_name"))
        finance_list.append(row)

    # ---------------- RESPONSE ----------------
    payload = {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender": user.gender,
        "contact_phone": user.contact_phone,
        "emergency_mobile": user.emergency_mobile,
        "personal_email": user.personal_email,
        "employee_code": user.employee_code,
        "email": user.email,
        "is_employee": user.is_employee,
        "education_status": education_global_status,
        "family_status": family_global_status,
        "vehicle_status": vehicle_global_status,

        "designation": user.designation,
        "station_id": user.station_id,
        "station_name": station_name,
        "supervisor_id": user.supervisor_id,
        "supervisor_name": supervisor_name,

        "grade": user.grade,
        "sap_location_code": user.sap_location_code,
        "employee_vendor_code": user.employee_vendor_code,
        "employment_type": user.employment_type,

        "date_of_joining": user.date_of_joining,
        "dob": user.dob,
        "blood_group": user.blood_group,
        "probation_from": user.probation_from,
        "probation_to": user.probation_to,
        "permanent_from": user.permanent_from,

        "current_address": user.current_address,
        "current_address_proof": file_link(user.current_address_proof),
        "permanent_address": user.permanent_address,
        "permanent_address_proof": file_link(user.permanent_address_proof),

        "status": user.status,
        "aadhaar": user.aadhaar,
        "aadhaar_file": file_link(user.aadhaar_file),
        "pan": user.pan,
        "pan_file": file_link(user.pan_file),

        "driving_license": user.driving_license,
        "driving_license_file": file_link(user.driving_license_file),
        "passport": user.passport,
        "passport_file": file_link(user.passport_file),

        "bank_name": user.bank_name,
        "branch_name": user.branch_name,
        "account_number": user.account_number,
        "ifsc_code": user.ifsc_code,
        "account_holder_name": user.account_holder_name,
        "account_type": user.account_type,
        "cancelled_cheque": file_link(user.cancelled_cheque),
        "basic_document_details": user.basic_document_details,
        "basic_comment": user.basic_comment,
        "pr_address_document_details": user.pr_address_document_details,
        "cr_address_document_details": user.cr_address_document_details,
        "address_document_details": user.address_document_details,
        "address_comment": user.address_comment,
        "identity_document_details": user.identity_document_details,
        "identity_comment": user.identity_comment,
        "profile_pic": file_link(user.profile_pic),
        "upload_document": multiple_file_links(user.upload_document),

        "education_details": education_details_processed,
        "finance": finance_list,                          # ← now a list of all records
        "asset_declaration": asset_declaration_processed,

        "family_members": family_members_processed,

        "form_12c": form_12c_processed,
        "vehicles": vehicles_processed,

        "role": user.role,
        "data_card_number": user.data_card_number,
        "status_basic_info": user.status_basic_info,
        "status_address": user.status_address,
        "status_bank": user.status_bank,
        "status_identity_proof": user.status_identity_proof,

        "family_status_details": family_status_details,
        "education_status_details": education_status_details,

        "bank_details": bank_details,
        "changed_fields": (
    user.changed_fields.get("changed_fields", [])
    if isinstance(user.changed_fields, dict)
    else json.loads(user.changed_fields).get("changed_fields", [])
    if user.changed_fields
    else []
),
    }
    return JSONResponse(
        content=jsonable_encoder(
            payload,
            custom_encoder={float: lambda v: None if math.isnan(v) else v}
        )
    )





import math
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from fastapi.responses import JSONResponse
class NanSafeEncoder(json.JSONEncoder):
    def iterencode(self, o, _one_shot=False):
        return super().iterencode(self._clean(o), _one_shot)

    def _clean(self, obj):
        if isinstance(obj, float) and math.isnan(obj):
            return None
        if isinstance(obj, dict):
            return {k: self._clean(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._clean(i) for i in obj]
        return obj

# @router.get("")
# def get_all_users(db: Session = Depends(get_db)):
    
#     # ── 1. Fetch all users sorted at DB level ──────────────────────────────
#     users = (
#         db.query(User)
#         .filter(User.is_deleted == False)
#         .options(
#             selectinload(User.family_members),
#             selectinload(User.vehicles),
#             selectinload(User.finance),
#             selectinload(User.asset_declaration),
#             selectinload(User.form_12c),
#         )
#         .order_by(User.date_of_joining.desc())
#         .all()
#     )

#     if not users:
#         return []

#     user_ids = [u.user_id for u in users]

#     # ── 2. Bulk-fetch station names ────────────────────────────────────────
#     station_ids = list({u.station_id for u in users if u.station_id})
#     stations_map = {}
#     if station_ids:
#         stations = db.query(Station.station_id, Station.station_name).filter(
#             Station.station_id.in_(station_ids)
#         ).all()
#         stations_map = {s.station_id: s.station_name for s in stations}

#     # ── 3. Bulk-fetch supervisor names ─────────────────────────────────────
#     supervisor_ids = list({u.supervisor_id for u in users if u.supervisor_id})
#     supervisors_map = {}
#     if supervisor_ids:
#         supervisors = db.query(User.user_id, User.first_name, User.last_name).filter(
#             User.user_id.in_(supervisor_ids)
#         ).all()
#         supervisors_map = {
#             s.user_id: f"{s.first_name} {s.last_name}".strip()
#             for s in supervisors
#         }

#     # ── 4. Bulk-fetch education details ────────────────────────────────────
#     education_rows = db.execute(
#         text("""
#             SELECT ue.user_id, ue.*, s.status as status
#             FROM user_education ue
#             LEFT JOIN submission s ON ue.submission_id = s.submission_id
#             WHERE ue.user_id = ANY(:uids)
#         """),
#         {"uids": user_ids}
#     ).fetchall()

#     education_map = {}
#     for row in education_rows:
#         d = dict(row._mapping)
#         education_map.setdefault(d["user_id"], []).append(d)

#     # ── 5. Bulk-fetch family status details ───────────────────────────────
#     family_rows = db.execute(
#         text("""
#             SELECT DISTINCT ON (s.submission_id)
#                 ef.user_id, s.submission_id, s.status, s.hr_comment, s.created_at
#             FROM submission s
#             JOIN employee_family ef ON s.submission_id = ef.submission_id
#             WHERE ef.user_id = ANY(:uids)
#             ORDER BY s.submission_id, s.created_at DESC
#         """),
#         {"uids": user_ids}
#     ).fetchall()

#     family_status_map = {}
#     for row in family_rows:
#         d = dict(row._mapping)
#         family_status_map.setdefault(d["user_id"], []).append(d)

#     # ── 6. Bulk-fetch education status details ────────────────────────────
#     edu_submission_rows = db.execute(
#         text("""
#             SELECT DISTINCT ON (s.submission_id)
#                 ue.user_id, s.submission_id, s.status, s.hr_comment, s.created_at
#             FROM submission s
#             JOIN user_education ue ON s.submission_id = ue.submission_id
#             WHERE ue.user_id = ANY(:uids)
#             ORDER BY s.submission_id, s.created_at DESC
#         """),
#         {"uids": user_ids}
#     ).fetchall()

#     edu_status_map = {}
#     for row in edu_submission_rows:
#         d = dict(row._mapping)
#         edu_status_map.setdefault(d["user_id"], []).append(d)

#     # ── 7. Bulk-fetch bank details ────────────────────────────────────────
#     bank_rows = db.execute(
#         text("""
#             SELECT
#                 id, user_id, bank_name, branch_name, account_number,
#                 ifsc_code, account_holder_name, account_type,
#                 cancelled_cheque, document_details, comment,
#                 document_name, is_active, status, remarks
#             FROM employee_bank
#             WHERE user_id = ANY(:uids)
#             ORDER BY id DESC
#         """),
#         {"uids": user_ids}
#     ).fetchall()

#     bank_map = {}
#     for row in bank_rows:
#         d = dict(row._mapping)
#         bank_map.setdefault(d["user_id"], []).append(d)

#     # ── 8. File helpers ───────────────────────────────────────────────────
#     def file_link(path):
#         return make_download_url(path) if path else None

#     def multiple_file_links(paths_string):
#         if not paths_string:
#             return []
#         return [make_download_url(p.strip()) for p in paths_string.split(',') if p.strip()]

#     # ── 9. Build response ─────────────────────────────────────────────────
#     result = []
#     for user in users:
#         uid = user.user_id
#         edu_details = education_map.get(uid, [])
#         family_members = user.family_members or []
#         vehicles = user.vehicles or []

#         result.append({
#             "user_id": uid,
#             "username": user.username,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "gender": user.gender,
#             "contact_phone": user.contact_phone,
#             "emergency_mobile": user.emergency_mobile,
#             "personal_email": user.personal_email,
#             "employee_code": user.employee_code,
#             "email": user.email,

#             "education_status": next(
#                 (e.get("status") for e in reversed(edu_details) if e.get("status")), None
#             ),
#             "family_status": next(
#                 (f.status for f in reversed(family_members) if f.status), None
#             ),
#             "vehicle_status": next(
#                 (v.status for v in reversed(vehicles) if v.status), None
#             ),

#             "designation": user.designation,
#             "station_id": user.station_id,
#             "station_name": stations_map.get(user.station_id),
#             "supervisor_id": user.supervisor_id,
#             "supervisor_name": supervisors_map.get(user.supervisor_id),

#             "grade": user.grade,
#             "sap_location_code": user.sap_location_code,
#             "employee_vendor_code": user.employee_vendor_code,
#             "employment_type": user.employment_type,

#             "date_of_joining": user.date_of_joining,
#             "dob": user.dob,
#             "blood_group": user.blood_group,
#             "probation_from": user.probation_from,
#             "probation_to": user.probation_to,
#             "permanent_from": user.permanent_from,

#             "current_address": user.current_address,
#             "current_address_proof": file_link(user.current_address_proof),
#             "permanent_address": user.permanent_address,
#             "permanent_address_proof": file_link(user.permanent_address_proof),

#             "status": user.status,
#             "aadhaar": user.aadhaar,
#             "aadhaar_file": file_link(user.aadhaar_file),
#             "pan": user.pan,
#             "pan_file": file_link(user.pan_file),
#             "is_employee": user.is_employee,
#             "driving_license": user.driving_license,
#             "driving_license_file": file_link(user.driving_license_file),
#             "passport": user.passport,
#             "passport_file": file_link(user.passport_file),

#             "bank_name": user.bank_name,
#             "branch_name": user.branch_name,
#             "account_number": user.account_number,
#             "ifsc_code": user.ifsc_code,
#             "account_holder_name": user.account_holder_name,
#             "account_type": user.account_type,
#             "cancelled_cheque": file_link(user.cancelled_cheque),

#             "profile_pic": file_link(user.profile_pic),
#             "upload_document": multiple_file_links(user.upload_document),

#             "education_details": edu_details,
#             "finance": user.finance,
#             "asset_declaration": user.asset_declaration,
#             "family_members": family_members,
#             "form_12c": user.form_12c,
#             "vehicles": vehicles,

#             "role": user.role,
#             "data_card_number": user.data_card_number,
#             "status_basic_info": user.status_basic_info,
#             "status_address": user.status_address,
#             "status_bank": user.status_bank,
#             "status_identity_proof": user.status_identity_proof,

#             "family_status_details": family_status_map.get(uid, []),
#             "education_status_details": edu_status_map.get(uid, []),
#             "bank_details": bank_map.get(uid, []),
#         })

#     return JSONResponse(content=jsonable_encoder(result, custom_encoder={float: lambda v: None if math.isnan(v) else v}))


@router.get("")
def get_all_users(db: Session = Depends(get_db)):
    
    # ── 1. Fetch all users sorted at DB level ──────────────────────────────
    users = (
        db.query(User)
        .filter(User.is_deleted == False)
        .options(
            selectinload(User.family_members),
            selectinload(User.vehicles),
            selectinload(User.finance),
            selectinload(User.asset_declaration),
            selectinload(User.form_12c),
        )
        .order_by(User.date_of_joining.desc())
        .all()
    )

    if not users:
        return []

    user_ids = [u.user_id for u in users]

    # ── 2. Bulk-fetch station names ────────────────────────────────────────
    station_ids = list({u.station_id for u in users if u.station_id})
    stations_map = {}
    if station_ids:
        stations = db.query(Station.station_id, Station.station_name).filter(
            Station.station_id.in_(station_ids)
        ).all()
        stations_map = {s.station_id: s.station_name for s in stations}

    # ── 3. Bulk-fetch supervisor names ─────────────────────────────────────
    supervisor_ids = list({u.supervisor_id for u in users if u.supervisor_id})
    supervisors_map = {}
    if supervisor_ids:
        supervisors = db.query(User.user_id, User.first_name, User.last_name).filter(
            User.user_id.in_(supervisor_ids)
        ).all()
        supervisors_map = {
            s.user_id: f"{s.first_name} {s.last_name}".strip()
            for s in supervisors
        }

    # ── 4. Bulk-fetch education details ────────────────────────────────────
    education_rows = db.execute(
        text("""
            SELECT ue.user_id, ue.*, s.status as status
            FROM user_education ue
            LEFT JOIN submission s ON ue.submission_id = s.submission_id
            WHERE ue.user_id = ANY(:uids)
        """),
        {"uids": user_ids}
    ).fetchall()

    education_map = {}
    for row in education_rows:
        d = dict(row._mapping)
        education_map.setdefault(d["user_id"], []).append(d)

    # ── 5. Bulk-fetch family status details ───────────────────────────────
    family_rows = db.execute(
        text("""
            SELECT DISTINCT ON (s.submission_id)
                ef.user_id, s.submission_id, s.status, s.hr_comment, s.created_at
            FROM submission s
            JOIN employee_family ef ON s.submission_id = ef.submission_id
            WHERE ef.user_id = ANY(:uids)
            ORDER BY s.submission_id, s.created_at DESC
        """),
        {"uids": user_ids}
    ).fetchall()

    family_status_map = {}
    for row in family_rows:
        d = dict(row._mapping)
        family_status_map.setdefault(d["user_id"], []).append(d)

    # ── 6. Bulk-fetch education status details ────────────────────────────
    edu_submission_rows = db.execute(
        text("""
            SELECT DISTINCT ON (s.submission_id)
                ue.user_id, s.submission_id, s.status, s.hr_comment, s.created_at
            FROM submission s
            JOIN user_education ue ON s.submission_id = ue.submission_id
            WHERE ue.user_id = ANY(:uids)
            ORDER BY s.submission_id, s.created_at DESC
        """),
        {"uids": user_ids}
    ).fetchall()

    edu_status_map = {}
    for row in edu_submission_rows:
        d = dict(row._mapping)
        edu_status_map.setdefault(d["user_id"], []).append(d)

    # ── 7. Bulk-fetch bank details ────────────────────────────────────────
    bank_rows = db.execute(
        text("""
            SELECT
                id, user_id, bank_name, branch_name, account_number,
                ifsc_code, account_holder_name, account_type,
                cancelled_cheque, document_details, comment,
                document_name, is_active, status, remarks
            FROM employee_bank
            WHERE user_id = ANY(:uids)
            ORDER BY id DESC
        """),
        {"uids": user_ids}
    ).fetchall()

    bank_map = {}
    for row in bank_rows:
        d = dict(row._mapping)
        bank_map.setdefault(d["user_id"], []).append(d)

    # ── 8. File helpers ───────────────────────────────────────────────────
    def file_link(path):
        return make_download_url(path) if path else None

    def multiple_file_links(paths_string):
        if not paths_string:
            return []
        return [make_download_url(p.strip()) for p in paths_string.split(',') if p.strip()]

    # ── 9. Build response ─────────────────────────────────────────────────
    result = []
    for user in users:
        uid = user.user_id
        edu_details = education_map.get(uid, [])
        family_members = user.family_members or []
        vehicles = user.vehicles or []

        result.append({
            "user_id": uid,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender,
            "contact_phone": user.contact_phone,
            "emergency_mobile": user.emergency_mobile,
            "personal_email": user.personal_email,
            "employee_code": user.employee_code,
            "email": user.email,

            "education_status": next(
                (e.get("status") for e in reversed(edu_details) if e.get("status")), None
            ),
            "family_status": next(
                (f.status for f in reversed(family_members) if f.status), None
            ),
            "vehicle_status": next(
                (v.status for v in reversed(vehicles) if v.status), None
            ),

            "designation": user.designation,
            "station_id": user.station_id,
            "station_name": stations_map.get(user.station_id),
            "supervisor_id": user.supervisor_id,
            "supervisor_name": supervisors_map.get(user.supervisor_id),

            "grade": user.grade,
            "sap_location_code": user.sap_location_code,
            "employee_vendor_code": user.employee_vendor_code,
            "employment_type": user.employment_type,

            "date_of_joining": user.date_of_joining,
            "dob": user.dob,
            "blood_group": user.blood_group,
            "probation_from": user.probation_from,
            "probation_to": user.probation_to,
            "permanent_from": user.permanent_from,

            "current_address": user.current_address,
            "current_address_proof": file_link(user.current_address_proof),
            "permanent_address": user.permanent_address,
            "permanent_address_proof": file_link(user.permanent_address_proof),

            "status": user.status,
            "aadhaar": user.aadhaar,
            "aadhaar_file": file_link(user.aadhaar_file),
            "pan": user.pan,
            "pan_file": file_link(user.pan_file),
            "is_employee": user.is_employee,
            "driving_license": user.driving_license,
            "driving_license_file": file_link(user.driving_license_file),
            "passport": user.passport,
            "passport_file": file_link(user.passport_file),

            "bank_name": user.bank_name,
            "branch_name": user.branch_name,
            "account_number": user.account_number,
            "ifsc_code": user.ifsc_code,
            "account_holder_name": user.account_holder_name,
            "account_type": user.account_type,
            "cancelled_cheque": file_link(user.cancelled_cheque),

            "profile_pic": file_link(user.profile_pic),
            "upload_document": multiple_file_links(user.upload_document),

            "education_details": edu_details,
            "finance": user.finance,
            "asset_declaration": user.asset_declaration,
            "family_members": family_members,
            "form_12c": user.form_12c,
            "vehicles": vehicles,

            "role": user.role,
            "data_card_number": user.data_card_number,
            "status_basic_info": user.status_basic_info,
            "status_address": user.status_address,
            "status_bank": user.status_bank,
            "status_identity_proof": user.status_identity_proof,

            "family_status_details": family_status_map.get(uid, []),
            "education_status_details": edu_status_map.get(uid, []),
            "bank_details": bank_map.get(uid, []),
        })

    # ── 10. Sort: any 'pending' status floats to top ──────────────────────
    # ── 10. Sort: any 'pending' status floats to top ──────────────────────
    def has_pending(u):
        PENDING = "pending"

        # Check all flat status fields
        flat_status_fields = [
            u.get("education_status"),
            u.get("family_status"),
            u.get("vehicle_status"),
            u.get("status_basic_info"),
            u.get("status_address"),
            u.get("status_bank"),
            u.get("status_identity_proof"),
            u.get("status"),
        ]
        if any(PENDING in str(s).lower() for s in flat_status_fields if s is not None):
            return True

        # Check nested bank_details list (dicts from raw SQL)
        if any(
            PENDING in str(b.get("status", "")).lower()
            for b in u.get("bank_details", [])
            if b.get("status")
        ):
            return True

        # Check nested family_status_details list (dicts from raw SQL)
        if any(
            PENDING in str(f.get("status", "")).lower()
            for f in u.get("family_status_details", [])
            if f.get("status")
        ):
            return True

        # Check nested education_status_details list (dicts from raw SQL)
        if any(
            PENDING in str(e.get("status", "")).lower()
            for e in u.get("education_status_details", [])
            if e.get("status")
        ):
            return True

        # Check nested education_details list (dicts from raw SQL)
        if any(
            PENDING in str(e.get("status", "")).lower()
            for e in u.get("education_details", [])
            if e.get("status")
        ):
            return True

        # Check nested family_members list (SQLAlchemy ORM objects - use getattr)
        for f in u.get("family_members", []):
            status = getattr(f, "status", None) if not isinstance(f, dict) else f.get("status")
            if status and PENDING in str(status).lower():
                return True

        # Check nested vehicles list (SQLAlchemy ORM objects - use getattr)
        for v in u.get("vehicles", []):
            status = getattr(v, "status", None) if not isinstance(v, dict) else v.get("status")
            if status and PENDING in str(status).lower():
                return True

        # Check nested asset_declaration list (SQLAlchemy ORM objects - use getattr)
        for a in u.get("asset_declaration", []):
            status = getattr(a, "status", None) if not isinstance(a, dict) else a.get("status")
            if status and PENDING in str(status).lower():
                return True

        return False

    result.sort(key=lambda u: (0 if has_pending(u) else 1))

    return JSONResponse(content=jsonable_encoder(result, custom_encoder={float: lambda v: None if math.isnan(v) else v}))


@router.put("/profile-pic/{user_id}")
def update_profile_pic(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1️⃣ Validate image type
    if file.content_type not in (
        "image/jpeg",
        "image/png",
        "image/jpg"
    ):
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG images are allowed"
        )

    # 2️⃣ Ensure directory exists
    upload_dir = "files/employee_dp"
    os.makedirs(upload_dir, exist_ok=True)

    # 3️⃣ Generate unique file name
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = f"{upload_dir}/{file_name}"

    # 4️⃣ Save file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # 5️⃣ Update DB (PURE SQL)
    result = db.execute(
        text("""
            UPDATE users
            SET profile_pic = :profile_pic
            WHERE user_id = :user_id
            RETURNING user_id, profile_pic
        """),
        {
            "profile_pic": file_path,
            "user_id": user_id
        }
    ).mappings().first()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.commit()

    return {
        "success": True,
        "message": "Profile picture updated successfully",
        "data": result
    }
