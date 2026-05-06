import os
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.crud.employees_info.employee_notifications_crud import get_all_hr_usernames, handle_employee_bank_submission, notify_employee_on_status_change,handle_employee_update_notifications

from app.database import get_db
from app.crud.employees_info.employee_bank_crud import (
    get_all_employee_banks,
    get_employee_bank_by_user_id,
    create_employee_bank,
    parse_document_field,
    update_employee_bank,
    delete_employee_bank
)
from app.models.UserModel import User
from app.schemas.employees_info.employee_bank import (
    EmployeeBankCreate,
    EmployeeBankOut,
    EmployeeBankUpdate
)

router = APIRouter(prefix="/api/employee-bank", tags=["Employee Bank"])

UPLOAD_DIR = "files/bank"
os.makedirs(UPLOAD_DIR, exist_ok=True)




def save_multiple_files(user_id, documents):
    file_paths = []

    if documents:
        for doc in documents:
            ext = doc.filename.split(".")[-1]
            filename = f"bank_{user_id}_{uuid.uuid4()}.{ext}"
            full_path = os.path.join(UPLOAD_DIR, filename)

            with open(full_path, "wb") as f:
                f.write(doc.file.read())

            file_paths.append(full_path)

    return file_paths

# -------------------------
# GET ALL
# -------------------------
@router.get("/", response_model=list[EmployeeBankOut])
def route_get_all(db: Session = Depends(get_db)):
    return get_all_employee_banks(db)


# -------------------------
# GET BY USER
# -------------------------
@router.get("/user/{user_id}", response_model=list[EmployeeBankOut])
def route_get_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_employee_bank_by_user_id(db, user_id)


# -------------------------
# CREATE
# -------------------------
from fastapi import APIRouter, Depends, Form, File, UploadFile
from typing import List
import os, uuid, json

UPLOAD_DIR = "files/bank"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/create", response_model=EmployeeBankOut)
async def route_create(
    user_id: int = Form(...),
    bank_name: str | None = Form(None),
    branch_name: str | None = Form(None),
    account_number: str | None = Form(None),
    ifsc_code: str | None = Form(None),
    account_holder_name: str | None = Form(None),
    account_type: str | None = Form(None),
    status: str | None = Form(None),
    document_details: str | None = Form(None),  
    documents: List[UploadFile] | None = File(None),
    is_active: bool = Form(False),
    background_tasks: BackgroundTasks=None,
    db: Session = Depends(get_db),
):

    # ============================
    # 1️⃣ USER CHECK
    # ============================
    user_obj = db.query(User).filter(User.user_id == user_id).first()
    if not user_obj:
        raise HTTPException(404, "User not found")

    old_status = user_obj.status
    old_comments = user_obj.comments

    # ============================
    # 2️⃣ FILE UPLOAD
    # ============================
    file_paths = []

    if documents:
        for doc in documents:
            ext = doc.filename.split(".")[-1]
            filename = f"bank_{user_id}_{uuid.uuid4()}.{ext}"
            full_path = os.path.join(UPLOAD_DIR, filename)

            with open(full_path, "wb") as f:
                f.write(doc.file.read())

            file_paths.append(full_path)

    document_json = json.dumps(file_paths) if file_paths else None

    # ============================
    # 3️⃣ INSERT
    # ============================
    sql = text("""
        INSERT INTO employee_bank
        (user_id, bank_name, branch_name, account_number,
         ifsc_code, account_holder_name, document_details,account_type,
         document_name,status, is_active)
        VALUES (:user_id, :bank_name, :branch_name, :account_number,
                :ifsc_code, :account_holder_name, :document_details,:account_type,
                :document_name, :status,:is_active)
        RETURNING *;
    """)

    result = db.execute(sql, {
        "user_id": user_id,
        "bank_name": bank_name,
        "branch_name": branch_name,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
        "account_holder_name": account_holder_name,
        "document_details": document_details,
        "account_type": account_type,
        "document_name": document_json,
        "is_active": is_active,
        "status": status
    })
    db.commit()
    created = result.mappings().first()

    # ============================
    # 4️⃣ UPDATE USER STATUS
    # ============================

    new_status = status if status else old_status

    db.query(User).filter(User.user_id == user_id).update({
        User.status: new_status,
        User.comments: None,
        User.modified_by: None
    })
    db.commit()

    # ============================
    # 5️⃣ CALL NOTIFICATION
    # ============================
    await handle_employee_bank_submission(
        db=db,
        employee_username=user_obj.username,
        status=new_status,
        comments=None,
        bg=background_tasks,
        reference_id=str(user_id),
        redirect_url=f"/profile/profile-info/{str(user_id)}/review"
       
    )

    return parse_document_field(created)

# -------------------------
# UPDATE
# -------------------------
from typing import List
from fastapi import Form, File, UploadFile
import json

def get_changed_fields_bank(old_obj, new_data: dict):
    changes = []

    IGNORE_FIELDS = ["status"]   # ✅ IGNORE status

    for field, new_value in new_data.items():

        if field in IGNORE_FIELDS:
            continue

        old_value = old_obj.get(field)

        # Normalize
        if new_value in ["", " ", None]:
            new_value = None
        if old_value in ["", " ", None]:
            old_value = None

        if str(old_value) != str(new_value):
            changes.append({
                "field": field,
                "old": old_value,
                "new": new_value
            })

    return changes

@router.put("/{bank_id}", response_model=EmployeeBankOut)
async def update_bank_record(
    bank_id: int,
    user_id: int = Form(...),
    bank_name: str | None = Form(None),
    branch_name: str | None = Form(None),
    account_number: str | None = Form(None),
    ifsc_code: str | None = Form(None),
    account_holder_name: str | None = Form(None),
    account_type: str | None = Form(None),
    document_details: str | None = Form(None),  # JSON string of existing documents
    comment: str | None = Form(None),
    documents: List[UploadFile] | None = File(None),
    status: str | None = Form(None),
    is_active: bool = Form(False),
    background_tasks: BackgroundTasks=None,
    db: Session = Depends(get_db),
):

    # ============================
    # 1️⃣ USER CHECK
    # ============================
    user_obj = db.query(User).filter(User.user_id == user_id).first()
    if not user_obj:
        raise HTTPException(404, "User not found")

    old_status = user_obj.status
    old_comments = user_obj.comments

    # ============================
    # 2️⃣ CHECK RECORD
    # ============================
    check = db.execute(
        text("SELECT * FROM employee_bank WHERE id = :id"),
        {"id": bank_id}
    ).mappings().first()

    if not check:
        raise HTTPException(404, "Bank record not found")
    
    import copy
    old_bank = copy.deepcopy(check)

    # ============================
    # 3️⃣ FILE UPLOAD
    # ============================
    file_paths = json.loads(check["document_name"]) if check["document_name"] else []

    if documents:
        for doc in documents:
            ext = doc.filename.split(".")[-1]
            filename = f"bank_{bank_id}_{uuid.uuid4()}.{ext}"
            full_path = os.path.join(UPLOAD_DIR, filename)

            with open(full_path, "wb") as f:
                f.write(doc.file.read())

            file_paths.append(full_path)

    document_json = json.dumps(file_paths)
    new_data = {
    "bank_name": bank_name,
    "branch_name": branch_name,
    "account_number": account_number,
    "ifsc_code": ifsc_code,
    "account_holder_name": account_holder_name,
    "account_type": account_type,
    "document_details": document_details,
    "comment": comment,
}

    changed_fields = get_changed_fields_bank(old_bank, new_data)

    # ✅ STOP IF NO CHANGE
    if not changed_fields and not documents:
        if not status:
            #print("⚠️ No changes → skipping")
            return parse_document_field(check)
    
    #print(f"Detected changes: {changed_fields}")
    # ============================
    # 4️⃣ UPDATE TABLE
    # ============================
    sql = text("""
        UPDATE employee_bank
        SET 
            bank_name = COALESCE(:bank_name, bank_name),
            branch_name = COALESCE(:branch_name, branch_name),
            account_number = COALESCE(:account_number, account_number),
            ifsc_code = COALESCE(:ifsc_code, ifsc_code),
            account_holder_name = COALESCE(:account_holder_name, account_holder_name),
            document_details = COALESCE(:document_details, document_details),
            comment = COALESCE(:comment, comment),
            account_type = COALESCE(:account_type, account_type),
            is_active = :is_active,
            document_name = :document_name,
            status = :status,
            changed_fields = :changed_fields
        WHERE id = :id
        RETURNING *;
    """)

    result = db.execute(sql, {
        "id": bank_id,
        "bank_name": bank_name,
        "branch_name": branch_name,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
        "account_holder_name": account_holder_name,
        "account_type": account_type,
        "document_details": document_details,
        "comment": comment,
        "document_name": document_json,
        "status": status,
        "is_active": is_active,
        "changed_fields": json.dumps(changed_fields)
    })
    db.commit()
    updated = result.fetchone()

    # ============================
    # 5️⃣ UPDATE USER STATUS
    # ============================
    new_status = status if status else old_status

    db.query(User).filter(User.user_id == user_id).update({
        User.status: new_status,
        User.comments: None,
        User.modified_by: None
    })
    db.commit()

    new_status = status if status else old_status
    if new_status and new_status.strip().lower().startswith("pending approval"):

        await handle_employee_update_notifications(
            db=db,
            old_status=old_status,
            new_status=new_status,
            old_comments=old_comments,
            new_comments=None,
            employee_username=user_obj.username,
            changed_sections=["Bank Details"],
            changed_fields=changed_fields,
            reference_id=str(user_id),
            redirect_url=f"/profile/profile-info/{str(user_id)}/review",
            bg=background_tasks
        )
        
    if new_status and new_status.lower() in ["approved", "changes requested"]:
    
        hr_usernames = get_all_hr_usernames(db)
        hr_username = hr_usernames[0] if hr_usernames else "HR"
    
        await notify_employee_on_status_change(
            db=db,
            employee_username=user_obj.username,
            hr_username=hr_username,
            new_status=new_status,
            comments=None,
            changed_sections="Bank Details",
            reference_id=str(user_id),
            redirect_url=f"/profile/{str(user_id)}",
            bg=background_tasks
        )
    
    return parse_document_field(updated)


# -------------------------
# DELETE
# -------------------------
@router.delete("/{bank_id}")
def route_delete(bank_id: int, db: Session = Depends(get_db)):
    delete_employee_bank(db, bank_id)
    return {"message": "Employee bank deleted successfully"}




# import os
 
# import uuid
 
# import json
 
# import logging
 
# from typing import List
 
# from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Form, File, UploadFile
 
# from sqlalchemy.orm import Session
 
# from sqlalchemy import text
 
# from app.database import get_db
 
# from app.models.UserModel import User
 
# from app.schemas.employees_info.employee_bank import EmployeeBankOut
 
# from app.crud.employees_info.employee_bank_crud import (
 
#     get_all_employee_banks,
 
#     get_employee_bank_by_user_id,
 
#     parse_document_field,
 
#     delete_employee_bank
 
# )
 
# from app.crud.employees_info.employee_notifications_crud import (
 
#     handle_employee_bank_submission,
 
#     notify_employee_bank_status_change
 
# )
 
# router = APIRouter(prefix="/api/employee-bank", tags=["Employee Bank"])
 
# UPLOAD_DIR = "files/bank"
 
# os.makedirs(UPLOAD_DIR, exist_ok=True)
 
# # ==============================================
 
# # LOGGER
 
# # ==============================================
 
# logging.basicConfig(level=logging.INFO)
 
# logger = logging.getLogger("employee_bank")
 
 
# # ==============================================
 
# # SAVE FILES
 
# # ==============================================
 
# def save_multiple_files(user_id, documents):
 
#     file_paths = []
 
#     if documents:
 
#         for doc in documents:
 
#             ext = doc.filename.split(".")[-1]
 
#             filename = f"bank_{user_id}_{uuid.uuid4()}.{ext}"
 
#             full_path = os.path.join(UPLOAD_DIR, filename)
 
#             with open(full_path, "wb") as f:
 
#                 f.write(doc.file.read())
 
#             logger.info(f"Saved file: {full_path}")
 
#             file_paths.append(full_path)
 
#     return file_paths
 
 
# # ==============================================
 
# # GET ALL
 
# # ==============================================
 
# @router.get("/all", response_model=list[EmployeeBankOut])
 
# def get_all_banks(db: Session = Depends(get_db)):
 
#     logger.info("Fetching all employee bank records")
 
#     return get_all_employee_banks(db)
 
 
# # ==============================================
 
# # GET USER BANKS
 
# # ==============================================
 
# @router.get("/user/{user_id}", response_model=list[EmployeeBankOut])
 
# def get_user_banks(user_id: int, db: Session = Depends(get_db)):
 
#     logger.info(f"Fetching bank records for user {user_id}")
 
#     return get_employee_bank_by_user_id(db, user_id)
 
 
# # ==============================================
 
# # CREATE BANK
 
# # ==============================================
 
# @router.post("/create", response_model=EmployeeBankOut)
 
# async def create_bank(
 
#     user_id: int = Form(...),
 
#     bank_name: str | None = Form(None),
 
#     branch_name: str | None = Form(None),
 
#     account_number: str | None = Form(None),
 
#     ifsc_code: str | None = Form(None),
 
#     account_holder_name: str | None = Form(None),
 
#     account_type: str | None = Form(None),
 
#     document_details: str | None = Form(None),
 
#     documents: List[UploadFile] | None = File(None),
 
#     is_active: bool = Form(False),
 
#     background_tasks: BackgroundTasks = None,
 
#     db: Session = Depends(get_db)
 
# ):
 
#     logger.info(f"Creating bank record for user {user_id}")
 
#     user_obj = db.query(User).filter(User.user_id == user_id).first()
 
#     if not user_obj:
 
#         raise HTTPException(404, "User not found")
 
#     file_paths = save_multiple_files(user_id, documents)
 
#     document_json = json.dumps(file_paths) if file_paths else None
 
#     status = "Pending Approval"
 
#     sql = text("""
 
#         INSERT INTO employee_bank
 
#         (user_id, bank_name, branch_name, account_number,
 
#          ifsc_code, account_holder_name, document_details,
 
#          account_type, document_name, status, is_active)
 
#         VALUES (:user_id, :bank_name, :branch_name, :account_number,
 
#                 :ifsc_code, :account_holder_name, :document_details,
 
#                 :account_type, :document_name, :status, :is_active)
 
#         RETURNING *;
 
#     """)
 
#     result = db.execute(sql, {
 
#         "user_id": user_id,
 
#         "bank_name": bank_name,
 
#         "branch_name": branch_name,
 
#         "account_number": account_number,
 
#         "ifsc_code": ifsc_code,
 
#         "account_holder_name": account_holder_name,
 
#         "document_details": document_details,
 
#         "account_type": account_type,
 
#         "document_name": document_json,
 
#         "status": status,
 
#         "is_active": is_active
 
#     })
 
#     db.commit()
 
#     created = result.fetchone()
 
#     logger.info(f"Bank created with status: {status}")
 
#     await handle_employee_bank_submission(
 
#         db=db,
 
#         employee_username=user_obj.username,
 
#         status=status,
 
#         comments=None,
 
#         bg=background_tasks
 
#     )
 
#     return parse_document_field(created)
 
 
# # ==============================================
 
# # UPDATE BANK (EMPLOYEE EDIT)
 
# # ==============================================
 
# @router.put("/{bank_id}", response_model=EmployeeBankOut)
 
# async def update_bank(
 
#     bank_id: int,
 
#     user_id: int = Form(...),
 
#     bank_name: str | None = Form(None),
 
#     branch_name: str | None = Form(None),
 
#     account_number: str | None = Form(None),
 
#     ifsc_code: str | None = Form(None),
 
#     account_holder_name: str | None = Form(None),
 
#     account_type: str | None = Form(None),
 
#     document_details: str | None = Form(None),
 
#     comment: str | None = Form(None),
 
#     documents: List[UploadFile] | None = File(None),
 
#     is_active: bool = Form(False),
 
#     background_tasks: BackgroundTasks = None,
 
#     db: Session = Depends(get_db)
 
# ):
 
#     logger.info(f"Updating bank record {bank_id}")
 
#     user_obj = db.query(User).filter(User.user_id == user_id).first()
 
#     if not user_obj:
 
#         raise HTTPException(404, "User not found")
 
#     record = db.execute(
 
#         text("SELECT * FROM employee_bank WHERE id=:id"),
 
#         {"id": bank_id}
 
#     ).fetchone()
 
#     if not record:
 
#         raise HTTPException(404, "Bank record not found")
 
#     file_paths = json.loads(record.document_name) if record.document_name else []
 
#     if documents:
 
#         for doc in documents:
 
#             ext = doc.filename.split(".")[-1]
 
#             filename = f"bank_{bank_id}_{uuid.uuid4()}.{ext}"
 
#             full_path = os.path.join(UPLOAD_DIR, filename)
 
#             with open(full_path, "wb") as f:
 
#                 f.write(doc.file.read())
 
#             logger.info(f"Updated file saved: {full_path}")
 
#             file_paths.append(full_path)
 
#     document_json = json.dumps(file_paths)
 
#     # IMPORTANT: employee editing resets status
 
#     status = "Pending Approval"
 
#     logger.info(f"Employee edit → resetting status to {status}")
 
#     sql = text("""
 
#         UPDATE employee_bank
 
#         SET
 
#             bank_name = COALESCE(:bank_name, bank_name),
 
#             branch_name = COALESCE(:branch_name, branch_name),
 
#             account_number = COALESCE(:account_number, account_number),
 
#             ifsc_code = COALESCE(:ifsc_code, ifsc_code),
 
#             account_holder_name = COALESCE(:account_holder_name, account_holder_name),
 
#             document_details = COALESCE(:document_details, document_details),
 
#             comment = COALESCE(:comment, comment),
 
#             account_type = COALESCE(:account_type, account_type),
 
#             document_name = :document_name,
 
#             status = :status,
 
#             is_active = :is_active
 
#         WHERE id = :id
 
#         RETURNING *;
 
#     """)
 
#     result = db.execute(sql, {
 
#         "id": bank_id,
 
#         "bank_name": bank_name,
 
#         "branch_name": branch_name,
 
#         "account_number": account_number,
 
#         "ifsc_code": ifsc_code,
 
#         "account_holder_name": account_holder_name,
 
#         "account_type": account_type,
 
#         "document_details": document_details,
 
#         "comment": comment,
 
#         "document_name": document_json,
 
#         "status": status,
 
#         "is_active": is_active
 
#     })
 
#     db.commit()
 
#     updated = result.fetchone()
 
#     logger.info(f"Bank record {bank_id} updated → status: {status}")
 
#     await handle_employee_bank_submission(
 
#         db=db,
 
#         employee_username=user_obj.username,
 
#         status=status,
 
#         comments=None,
 
#         bg=background_tasks
 
#     )
 
#     return parse_document_field(updated)
 
 
# # ==============================================
 
# # HR REVIEW
 
# # ==============================================
 
# @router.put("/hr-review/{bank_id}", response_model=EmployeeBankOut)
 
# async def hr_review_bank(
 
#     bank_id: int,
 
#     status: str = Form(...),
 
#     comment: str | None = Form(None),
 
#     background_tasks: BackgroundTasks = None,
 
#     db: Session = Depends(get_db)
 
# ):
 
#     logger.info(f"HR reviewing bank {bank_id} with status {status}")
 
#     if status not in ["Approved", "Changes Requested"]:
 
#         raise HTTPException(400, "Status must be Approved or Changes Requested")
 
#     record = db.execute(
 
#         text("SELECT * FROM employee_bank WHERE id=:id"),
 
#         {"id": bank_id}
 
#     ).fetchone()
 
#     if not record:
 
#         raise HTTPException(404, "Bank record not found")
 
#     result = db.execute(
 
#         text("""
 
#         UPDATE employee_bank
 
#         SET status=:status,
 
#             comment=:comment
 
#         WHERE id=:id
 
#         RETURNING *
 
#         """),
 
#         {
 
#             "status": status,
 
#             "comment": comment,
 
#             "id": bank_id
 
#         }
 
#     )
#     updated = result.fetchone()
#     db.commit()
 
#     #updated = result.fetchone()
 
#     logger.info(f"HR updated bank {bank_id} → new status: {status}")
 
#     user = db.query(User).filter(User.user_id == record.user_id).first()
 
#     await notify_employee_bank_status_change(
 
#         db=db,
 
#         employee_username=user.username,
 
#         hr_username="HR",
 
#         new_status=status,
 
#         comments=comment,
 
#         bg=background_tasks
 
#     )
 

   
 
#     return parse_document_field(updated)
 
 
# # ==============================================
 
# # DELETE
 
# # ==============================================
 
# @router.delete("/{bank_id}")
 
# def delete_bank(bank_id: int, db: Session = Depends(get_db)):
 
#     logger.info(f"Deleting bank record {bank_id}")
 
#     delete_employee_bank(db, bank_id)
 
#     return {"message": "Employee bank deleted successfully"}