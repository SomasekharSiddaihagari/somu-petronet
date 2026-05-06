import os
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from app.models.employees_info.employee_education import UserEducation
from sqlalchemy import text
from sqlalchemy.orm import Session
import json
from app.crud.employees_info.employee_education import create_education, get_all_educations, get_educations_by_user_id, update_education
from app.crud.employees_info.employee_notifications_crud import get_all_hr_usernames, handle_employee_update_notifications, notify_employee_on_status_change
from app.database import get_db
from app.models.UserModel import User
from app.schemas.employees_info.user_education import UserEducationCreate, UserEducationOut, UserEducationUpdate



router = APIRouter(prefix="/api/education", tags=["User Education"])
UPLOAD_DIR = "files/education"
os.makedirs(UPLOAD_DIR, exist_ok=True)







@router.get("", response_model=list[UserEducationOut])
def route_get_all(db: Session = Depends(get_db)):
    items = get_all_educations(db)

    for item in items:
        item["education_document"] = make_download_url(item.get("education_document"))

    return items




@router.get("/user/{user_id}", response_model=list[UserEducationOut])
def route_get_by_user(user_id: int, db: Session = Depends(get_db)):
    items = get_educations_by_user_id(db, user_id)

    for item in items:
        item["education_document"] = make_download_url(item.get("education_document"))

    return items

import urllib.parse

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



# @router.post("/", response_model=UserEducationOut)
# def route_create(
#     user_id: int = Form(...),                     # REQUIRED
#     qualification: str | None = Form(None),       # OPTIONAL
#     year_of_completion: str | None = Form(None),  # Comes as STRING, even if empty
#     document: UploadFile | str | None = File(None),
#     status: str | None= Form(None),
#     db: Session = Depends(get_db),
# ):

#     # ================================
#     # SANITIZE EMPTY FORM FIELDS
#     # ================================
#     if qualification == "":
#         qualification = None

#     if year_of_completion == "" or year_of_completion is None:
#         year_of_completion = None
#     else:
#         year_of_completion = int(year_of_completion)

#     # File fix: if frontend sends "", treat as None
#     if isinstance(document, str):
#         document = None

#     # ================================
#     # SAVE DOCUMENT IF PROVIDED
#     # ================================
#     file_path = None

#     if document:
#         ext = document.filename.split(".")[-1]
#         filename = f"edu_{user_id}_{uuid.uuid4()}.{ext}"
#         full_path = os.path.join(UPLOAD_DIR, filename)

#         with open(full_path, "wb") as f:
#             f.write(document.file.read())

#         file_path = full_path

#     # ================================
#     # INSERT SQL
#     # ================================
#     sql = text("""
#         INSERT INTO user_education
#         (user_id, qualification, year_of_completion, education_document, created_at, status)
#         VALUES (:user_id, :qualification, :year_of_completion, :education_document, NOW(), :status)
#         RETURNING *;
#     """)

#     result = db.execute(sql, {
#         "user_id": user_id,
#         "qualification": qualification,
#         "year_of_completion": year_of_completion,
#         "education_document": file_path,
#         "status": status
#     })

#     db.commit()
#     return result.fetchone()
from fastapi import BackgroundTasks

@router.post("/create", response_model=UserEducationOut)
async def route_create(
    user_id: int = Form(...),
    submission_id: int = Form(...),  # ⭐ NEW
    qualification: str | None = Form(None),
    year_of_completion: str | None = Form(None),
    document: UploadFile | str | None = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
):

    if year_of_completion in ("", None):
        year_of_completion = None
    else:
        year_of_completion = int(year_of_completion)

    if isinstance(document, str):
        document = None

    file_path = None
    if document:
        ext = document.filename.split(".")[-1]
        filename = f"edu_{user_id}_{uuid.uuid4()}.{ext}"
        full_path = os.path.join(UPLOAD_DIR, filename)
        with open(full_path, "wb") as f:
            f.write(document.file.read())
        file_path = full_path

    sql = text("""
        INSERT INTO user_education
        (user_id, submission_id, qualification, year_of_completion, education_document, created_at)
        VALUES (:user_id, :submission_id, :qualification, :year_of_completion, :education_document, NOW())
        RETURNING *;
    """)

    result = db.execute(sql, {
        "user_id": user_id,
        "submission_id": submission_id,
        "qualification": qualification,
        "year_of_completion": year_of_completion,
        "education_document": file_path
    })
    record = result.fetchone()
    db.commit()

    
    user_obj = db.query(User).filter(User.user_id == user_id).first()
    

    await handle_employee_update_notifications(
        db=db,
        old_status=None,
        new_status="Pending Approval",
        old_comments=None,
        new_comments=None,
        employee_username=user_obj.username,
        changed_sections=["Education"],
        changed_fields=[],
        reference_id=str(record.education_id),
        redirect_url=f"/profile/profile-info/{str(user_id)}/review",
        bg=background_tasks
    )
    return dict(record._mapping)




# education router - put endpoint
# @router.put("/{education_id}", response_model=UserEducationOut)
# async def update_education_record(
#     education_id: int,
#     user_id: int = Form(...),
#     qualification: str | None = Form(None),
#     year_of_completion: str | None = Form(None),
#     document: UploadFile | str | None = File(None),
#     status: str | None = Form(None),
#     background_tasks: BackgroundTasks=None,
#     db: Session = Depends(get_db),
# ):

#     # 1) user
#     user_obj = db.query(User).filter(User.user_id == user_id).first()
#     if not user_obj:
#         raise HTTPException(404, "User not found")
#     old_status = user_obj.status
#     old_comments = user_obj.comments

#     # 2) education exists
#     check = db.execute(
#         text("SELECT * FROM user_education WHERE education_id = :id"),
#         {"id": education_id}
#     ).fetchone()
#     if not check:
#         raise HTTPException(404, "Education record not found")

#     # 3) sanitize
#     if qualification == "":
#         qualification = None
#     if year_of_completion in ("", None):
#         year_of_completion = None
#     else:
#         year_of_completion = int(year_of_completion)
#     if isinstance(document, str):
#         document = None

#     # 4) file upload
#     file_path = check.education_document
#     if document:
#         ext = document.filename.split(".")[-1]
#         filename = f"edu_{education_id}_{uuid.uuid4()}.{ext}"
#         full_path = os.path.join(UPLOAD_DIR, filename)
#         with open(full_path, "wb") as f:
#             f.write(document.file.read())
#         file_path = full_path

#     # 5) update education table
#     sql = text("""
#         UPDATE user_education
#         SET 
#             user_id = :user_id,
#             qualification = COALESCE(:qualification, qualification),
#             year_of_completion = COALESCE(:year_of_completion, year_of_completion),
#             education_document = :education_document,
#             status = :status
#         WHERE education_id = :id
#         RETURNING *;
#     """)
#     result = db.execute(sql, {
#         "id": education_id,
#         "user_id": user_id,
#         "qualification": qualification,
#         "year_of_completion": year_of_completion,
#         "education_document": file_path,
#         "status": status
#     })
#     db.commit()
#     updated_record = result.fetchone()

#     # 6) update User.status so HR can review
#     new_status = "Pending Approval Education"
#     db.query(User).filter(User.user_id == user_id).update({
#         User.status: new_status,
#         User.comments: None,
#         User.modified_by: None
#     })
#     db.commit()

#     # 7) call notification handler
#     await handle_employee_update_notifications(
#         db=db,
#         old_status=old_status,
#         new_status=new_status,
#         old_comments=old_comments,
#         new_comments=None,
#         employee_username=user_obj.username,
#         changed_sections=["Education"],
#         bg=background_tasks
#     )

#     return updated_record

#     return updated_record
def get_notification_changes(old_record: dict, new_data: dict):
    import os

    changes = []

    for field, new_value in new_data.items():

        if new_value in ["", None, " ", "null"]:
            continue

        old_value = old_record.get(field)

        # normalize datetime
        if hasattr(old_value, "isoformat"):
            old_value = old_value.isoformat()
        if hasattr(new_value, "isoformat"):
            new_value = new_value.isoformat()

        # skip same values ✅ FIX
        if str(old_value) == str(new_value):
            continue

        # clean file path ✅ FIX
        if field == "education_document":
            old_value = os.path.basename(str(old_value)) if old_value else old_value
            new_value = os.path.basename(str(new_value)) if new_value else new_value

        changes.append({
            "field": field,
            "old": old_value,
            "new": new_value
        })

    return changes


def build_changed_fields(old_obj: dict, new_data: dict, existing_changes: list):
    result = []

    existing_map = {item["field"]: item for item in existing_changes}

    for field, new_value in new_data.items():

        if new_value in ["", None, " ", "null"]:
            continue

        old_value = old_obj.get(field)

        # normalize
        if hasattr(old_value, "isoformat"):
            old_value = old_value.isoformat()
        if hasattr(new_value, "isoformat"):
            new_value = new_value.isoformat()

        if field not in existing_map:
            result.append({
                "field": field,
                "old": old_value,
                "new": new_value
            })
        else:
            prev = existing_map[field]
            result.append({
                "field": field,
                "old": prev["new"],
                "new": new_value
            })

    return result

@router.put("/{education_id}", response_model=UserEducationOut)
async def update_education_record(
    education_id: int,
    user_id: int = Form(...),
    submission_id: int = Form(...),   # ⭐ NEW FIELD (ADDED ONLY)
    qualification: str | None = Form(None),
    year_of_completion: str | None = Form(None),
    document: UploadFile | str | None = File(None),
    status: str | None = Form(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
):

    # ---------------- USER CHECK ----------------
    user_obj = db.query(User).filter(User.user_id == user_id).first()
    if not user_obj:
        raise HTTPException(404, "User not found")

    old_status = user_obj.status
    old_comments = user_obj.comments

    # ---------------- EDUCATION EXISTS ----------------
    check = db.execute(
        text("SELECT * FROM user_education WHERE education_id = :id"),
        {"id": education_id}
    ).fetchone()

    if not check:
        raise HTTPException(404, "Education record not found")
    old_record = check._mapping
    # ---------------- SANITIZE ----------------
    if qualification == "":
        qualification = None

    if year_of_completion in ("", None):
        year_of_completion = None
    else:
        year_of_completion = int(year_of_completion)

    if isinstance(document, str):
        document = None

    # ---------------- FILE UPLOAD ----------------
    file_path = old_record.get("education_document")

    if document:
        ext = document.filename.split(".")[-1]
        filename = f"edu_{education_id}_{uuid.uuid4()}.{ext}"
        full_path = os.path.join(UPLOAD_DIR, filename)

        with open(full_path, "wb") as f:
            f.write(document.file.read())

        file_path = full_path
    
    new_data = {
        "qualification": qualification,
        "year_of_completion": year_of_completion,
        "education_document": file_path,
        "status": status
    }
        # ---------------- DETECT CHANGES ----------------
    # 🔥 GET EXISTING CHANGES
    existing_changes = []

    if old_record.get("changed_fields"):
        try:
            existing_changes = json.loads(old_record["changed_fields"]).get("changed_fields", [])
        except:
            existing_changes = []

    # 🔥 BUILD NEW CHANGES
    changed_fields = build_changed_fields(old_record, new_data, existing_changes)

    # 🔥 MERGE
    final_map = {item["field"]: item for item in existing_changes}

    for item in changed_fields:
        final_map[item["field"]] = item

    final_changes = list(final_map.values())
    # ---------------- UPDATE EDUCATION TABLE ----------------
    if not final_changes:
        print("⚠️ No changes detected, skipping notification")

    notification_changes = get_notification_changes(old_record, new_data)

    # ---------------- UPDATE EDUCATION TABLE ----------------
    sql = text("""
        UPDATE user_education
        SET 
            user_id = :user_id,
            submission_id = :submission_id,
            qualification = COALESCE(:qualification, qualification),
            year_of_completion = COALESCE(:year_of_completion, year_of_completion),
            education_document = :education_document,
            status = :status,
            changed_fields = :changed_fields 
        WHERE education_id = :id
        RETURNING *;
    """)

    # ---------------- UPDATE EDUCATION TABLE ----------------
    result = db.execute(sql, {
        "id": education_id,
        "user_id": user_id,
        "submission_id": submission_id,
        "qualification": qualification,
        "year_of_completion": year_of_completion,
        "education_document": file_path,
        "status": status,
        "changed_fields": json.dumps(final_changes),
    })

    if status:  # only update if status is provided
        db.execute(
            text("""
                UPDATE submission
                SET status = :status
                WHERE submission_id = :submission_id
            """),
            {
                "status": status,
                "submission_id": submission_id
            }
        )
 
    updated_record = result.fetchone()
    
 
    if not updated_record:
        raise HTTPException(status_code=404, detail="Education update failed")
 
    db.commit()   # ✅ correct place
 
    # 🔥 GET STATUS FROM SUBMISSION TABLE
    submission_row = db.execute(
        text("""
            SELECT status
            FROM submission
            WHERE submission_id = :submission_id
        """),
        {"submission_id": submission_id}
    ).fetchone()
 
    final_status = submission_row.status if submission_row else None
 
 
    # ---------------- NOTIFICATION LOGIC ----------------
 
    # 1️⃣ Employee → HR
    if final_status and final_status.lower() == "pending approval" and final_changes:
 
        await handle_employee_update_notifications(
            db=db,
            old_status=old_status,
            new_status=final_status,
            old_comments=old_comments,
            new_comments=None,
            employee_username=user_obj.username,
            changed_sections=["Education"],
            changed_fields=notification_changes,
            reference_id=str(user_id),
            redirect_url=f"/profile/profile-info/{str(user_id)}/review",
            bg=background_tasks
        )
 
    # 2️⃣ HR → Employee
    if final_status and final_status.lower() in ["approved", "changes requested"]:
 
        hr_usernames = get_all_hr_usernames(db)
        hr_username = hr_usernames[0] if hr_usernames else "HR"
 
        await notify_employee_on_status_change(
            db=db,
            employee_username=user_obj.username,
            hr_username=hr_username,
            new_status=final_status,
            comments=None,
            changed_sections="Education Details",
            reference_id=str(user_id),
            redirect_url=f"/profile/{str(user_id)}",
            bg=background_tasks
        )
 
    return dict(updated_record._mapping)



@router.get("/education_submission/{submission_id}")
def get_education_by_submission(submission_id: int, db: Session = Depends(get_db)):

    sql = text("""
        SELECT * FROM user_education
        WHERE submission_id = :sid
    """)

    rows = db.execute(sql, {"sid": submission_id}).fetchall()

    return [dict(r._mapping) for r in rows]



@router.delete("/delete-user-education/{education_id}")
def delete_user_education(education_id: int, db: Session = Depends(get_db)):

    education = db.query(UserEducation).filter(
        UserEducation.education_id == education_id
    ).first()

    if not education:
        raise HTTPException(status_code=404, detail="Education not found")

    db.delete(education)
    db.commit()

    return {"message": "User education deleted successfully"}






# import os
# import uuid
# import urllib.parse
# from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
# from app.models.employees_info.employee_education import UserEducation
# from sqlalchemy import text
# from sqlalchemy.orm import Session

# from app.crud.employees_info.employee_education import (
#     create_education,
#     get_all_educations,
#     get_educations_by_user_id,
#     update_education
# )

# from app.crud.employees_info.employee_notifications_crud import handle_employee_update_notifications
# from app.database import get_db
# from app.models.UserModel import User
# from app.schemas.employees_info.user_education import (
#     UserEducationCreate,
#     UserEducationOut,
#     UserEducationUpdate
# )

# router = APIRouter(prefix="/api/education", tags=["User Education"])

# UPLOAD_DIR = "files/education"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # ---------------- DOWNLOAD URL ----------------

# def make_download_url(path: str):

#     if not path:
#         return None

#     base_url = os.getenv("BackEndPath")

#     file_path = path.replace("\\", "/")

#     if ":" in file_path:
#         file_path = file_path.split(":", 1)[1]

#     if file_path.startswith("/Petronet"):
#         file_path = file_path.replace("/Petronet", "", 1)

#     file_path = "/" + file_path.lstrip("/")

#     encoded_path = urllib.parse.quote(file_path)

#     return f"{base_url}{encoded_path}"


# # ---------------- GET ALL ----------------

# @router.get("/all", response_model=list[UserEducationOut])
# def route_get_all(db: Session = Depends(get_db)):

#     items = get_all_educations(db)

#     for item in items:
#         item["education_document"] = make_download_url(item.get("education_document"))

#     return items


# # ---------------- GET BY USER ----------------

# @router.get("/user/{user_id}", response_model=list[UserEducationOut])
# def route_get_by_user(user_id: int, db: Session = Depends(get_db)):

#     items = get_educations_by_user_id(db, user_id)

#     for item in items:
#         item["education_document"] = make_download_url(item.get("education_document"))

#     return items


# # ---------------- CREATE EDUCATION ----------------

# @router.post("/create", response_model=UserEducationOut)
# def route_create(
#     user_id: int = Form(...),
#     submission_id: int = Form(...),
#     qualification: str | None = Form(None),
#     year_of_completion: str | None = Form(None),
#     document: UploadFile | str | None = File(None),
#     db: Session = Depends(get_db),
# ):

#     if year_of_completion in ("", None):
#         year_of_completion = None
#     else:
#         year_of_completion = int(year_of_completion)

#     if isinstance(document, str):
#         document = None

#     file_path = None

#     if document:

#         ext = document.filename.split(".")[-1]
#         filename = f"edu_{user_id}_{uuid.uuid4()}.{ext}"

#         full_path = os.path.join(UPLOAD_DIR, filename)

#         with open(full_path, "wb") as f:
#             f.write(document.file.read())

#         file_path = full_path

#     sql = text("""
#         INSERT INTO user_education
#         (user_id, submission_id, qualification, year_of_completion, education_document, created_at)
#         VALUES (:user_id, :submission_id, :qualification, :year_of_completion, :education_document, NOW())
#         RETURNING *;
#     """)

#     result = db.execute(sql, {
#         "user_id": user_id,
#         "submission_id": submission_id,
#         "qualification": qualification,
#         "year_of_completion": year_of_completion,
#         "education_document": file_path
#     })

#     db.commit()

#     record = dict(result.fetchone()._mapping)

#     record["education_document"] = make_download_url(record.get("education_document"))

#     return record


# # ---------------- UPDATE EDUCATION ----------------

# @router.put("/{education_id}", response_model=UserEducationOut)
# async def update_education_record(
#     education_id: int,
#     user_id: int = Form(...),
#     submission_id: int = Form(...),
#     qualification: str | None = Form(None),
#     year_of_completion: str | None = Form(None),
#     document: UploadFile | str | None = File(None),
#     status: str | None = Form(None),
#     background_tasks: BackgroundTasks = None,
#     db: Session = Depends(get_db),
# ):

#     # ---------------- USER CHECK ----------------

#     user_obj = db.query(User).filter(User.user_id == user_id).first()

#     if not user_obj:
#         raise HTTPException(404, "User not found")

#     old_status = user_obj.status
#     old_comments = user_obj.comments

#     # ---------------- EDUCATION EXISTS ----------------

#     check = db.execute(
#         text("SELECT * FROM user_education WHERE education_id = :id"),
#         {"id": education_id}
#     ).fetchone()

#     if not check:
#         raise HTTPException(404, "Education record not found")

#     # ---------------- SANITIZE ----------------

#     if qualification == "":
#         qualification = None

#     if year_of_completion in ("", None):
#         year_of_completion = None
#     else:
#         year_of_completion = int(year_of_completion)

#     if isinstance(document, str):
#         document = None

#     # ---------------- FILE UPLOAD ----------------

#     file_path = check.education_document

#     if document:

#         ext = document.filename.split(".")[-1]

#         filename = f"edu_{education_id}_{uuid.uuid4()}.{ext}"

#         full_path = os.path.join(UPLOAD_DIR, filename)

#         with open(full_path, "wb") as f:
#             f.write(document.file.read())

#         file_path = full_path

#     # ---------------- UPDATE TABLE ----------------

#     sql = text("""
#         UPDATE user_education
#         SET 
#             user_id = :user_id,
#             submission_id = :submission_id,
#             qualification = COALESCE(:qualification, qualification),
#             year_of_completion = COALESCE(:year_of_completion, year_of_completion),
#             education_document = :education_document,
#             status = :status
#         WHERE education_id = :id
#         RETURNING *;
#     """)

#     result = db.execute(sql, {
#         "id": education_id,
#         "user_id": user_id,
#         "submission_id": submission_id,
#         "qualification": qualification,
#         "year_of_completion": year_of_completion,
#         "education_document": file_path,
#         "status": status
#     })

#     db.commit()

#     updated_record = dict(result.fetchone()._mapping)

#     # ---------------- USER STATUS UPDATE ----------------

#     new_status = "Pending Approval"

#     db.query(User).filter(User.user_id == user_id).update({
#         User.status: new_status,
#         User.comments: None,
#         User.modified_by: None
#     })

#     db.commit()

#     # ---------------- NOTIFICATION ----------------

#     await handle_employee_update_notifications(
#         db=db,
#         old_status=old_status,
#         new_status=new_status,
#         old_comments=old_comments,
#         new_comments=None,
#         employee_username=user_obj.username,
#         changed_sections=["Education"],
#         bg=background_tasks
#     )

#     updated_record["education_document"] = make_download_url(updated_record.get("education_document"))

#     return updated_record


# # ---------------- GET BY SUBMISSION ----------------

# @router.get("/education_submission/{submission_id}")
# def get_education_by_submission(submission_id: int, db: Session = Depends(get_db)):

#     sql = text("""
#         SELECT * FROM user_education
#         WHERE submission_id = :sid
#     """)

#     rows = db.execute(sql, {"sid": submission_id}).fetchall()

#     return [dict(r._mapping) for r in rows]


# # ---------------- DELETE ----------------

# @router.delete("/delete-user-education/{education_id}")
# def delete_user_education(education_id: int, db: Session = Depends(get_db)):

#     education = db.query(UserEducation).filter(
#         UserEducation.education_id == education_id
#     ).first()

#     if not education:
#         raise HTTPException(status_code=404, detail="Education not found")

#     db.delete(education)
#     db.commit()

#     return {"message": "User education deleted successfully"}