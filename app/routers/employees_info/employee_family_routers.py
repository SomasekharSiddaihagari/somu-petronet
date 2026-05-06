from datetime import datetime
import os
import json
import shutil
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employees_info.employee_family import EmployeeFamily
from app.models.UserModel import User
from app.routers.UserAuthR2 import make_download_url
from app.crud.employees_info.employee_family_crud import (
    get_all_family_members,
    get_family_member_by_id,
    get_family_members_by_user_id
)
from app.models.UserModel import User
from app.crud.employees_info.employee_notifications_crud import get_all_hr_usernames, handle_employee_update_notifications, notify_employee_on_status_change
router = APIRouter(prefix="/api/employee-family", tags=["Employee Family"])

UPLOAD_DIR = "files/employee_family"
os.makedirs(UPLOAD_DIR, exist_ok=True)





# ================= SERIALIZER =================
def serialize_family(row):
    return {
        "ef_id": row.get("ef_id"),
        "submission_id": row.get("submission_id"),
        "relation": row.get("relation"),
        "full_name": row.get("full_name"),
        "dob": row.get("dob"),
        "document": row.get("document"),
        "user_id": row.get("user_id"),
        "gender": row.get("gender"),
        "place_of_birth": row.get("place_of_birth"),
        "date_of_marriage": row.get("date_of_marriage"),
        "status": row.get("status"),
        "document_details": row.get("document_details"),
        "comment": row.get("comment"),
        "changed_fields":row.get("changed_fields"),
    }



# ================= GET APIs =================
@router.get("/")
def route_get_all(db: Session = Depends(get_db)):
    rows = get_all_family_members(db)
    return [serialize_family(row) for row in rows]


@router.get("/{ef_id}")
def route_get_by_id(ef_id: int, db: Session = Depends(get_db)):
    row = get_family_member_by_id(db, ef_id)
    return serialize_family(row)


@router.get("/user/{user_id}")
def route_get_by_user(user_id: int, db: Session = Depends(get_db)):
    rows = get_family_members_by_user_id(db, user_id)
    return [serialize_family(row) for row in rows]


# ================= FAMILY CRUD =================
# @router.post("/crud")
# async def employee_family_crud(
#     ef_id: str | None = Form(None),
#     user_id: int = Form(...),
#     submission_id: int = Form(...),
#     relation: str | None = Form(None),
#     full_name: str | None = Form(None),
#     dob: str | None = Form(None),
#     gender: str | None = Form(None),
#     place_of_birth: str | None = Form(None),
#     date_of_marriage: str | None = Form(None),
#     status: str | None = Form(None),
#     file: UploadFile | None = File(None),
#     document_details: str | None = Form(None),
#     comment: str | None = Form(None),
#     background_tasks: BackgroundTasks = None,
#     db: Session = Depends(get_db)
# ):

#     if ef_id:
#         ef_id = int(ef_id)

#     dob_value = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
#     dom_value = datetime.strptime(date_of_marriage, "%Y-%m-%d").date() if date_of_marriage else None

#     file_path = None
#     if file:
#         file_path = os.path.join(UPLOAD_DIR, file.filename)
#         with open(file_path, "wb") as f:
#             shutil.copyfileobj(file.file, f)

#     payload = {
#         "user_id": user_id,
#         "submission_id": submission_id,
#         "relation": relation,
#         "full_name": full_name,
#         "dob": dob_value,
#         "gender": gender,
#         "place_of_birth": place_of_birth,
#         "date_of_marriage": dom_value,
#         "document_details": document_details,
#         "comment": comment,
#         "status": status
#     }

#     if file_path:
#         payload["document"] = file_path

#     payload_clean = {k: v for k, v in payload.items() if v is not None}

#     # ---------- UPDATE ----------
#     if ef_id:
#         payload_clean["ef_id"] = ef_id

#         sql = text(f"""
#             UPDATE employee_family
#             SET {", ".join([f"{k} = :{k}" for k in payload_clean if k != "ef_id"])}
#             WHERE ef_id = :ef_id
#             RETURNING *;
#         """)

#         row = db.execute(sql, payload_clean).fetchone()
#         db.commit()

#         if not row:
#             return {
#                 "status": "error",
#                 "message": "No record found to update"
#             }

#         return dict(row._mapping)

#     # ---------- INSERT ----------
#     sql = text(f"""
#         INSERT INTO employee_family ({", ".join(payload_clean.keys())})
#         VALUES ({", ".join([f":{k}" for k in payload_clean])})
#         RETURNING *;
#     """)

#     row = db.execute(sql, payload_clean).fetchone()
#     db.commit()

#     if not row:
#         return {
#             "status": "error",
#             "message": "Insert failed"
#         }

#     return dict(row._mapping)
def build_changed_fields(old_row, new_data: dict, existing_changes: list):
    result = []

    existing_map = {item["field"]: item for item in existing_changes}

    for field, new_value in new_data.items():

        if new_value in ["", None, " ", "null"]:
            continue

        old_value = old_row.get(field)

        # normalize date
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

@router.post("/crud")
async def employee_family_crud(
    ef_id: str | None = Form(None),
    user_id: int = Form(...),
    submission_id: int = Form(...),
    relation: str | None = Form(None),
    full_name: str | None = Form(None),
    dob: str | None = Form(None),
    gender: str | None = Form(None),
    place_of_birth: str | None = Form(None),
    date_of_marriage: str | None = Form(None),
    status: str | None = Form(None),
    file: UploadFile | None = File(None),
    document_details: str | None = Form(None),
    comment: str | None = Form(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):

    if ef_id:
        ef_id = int(ef_id)

    dob_value = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
    dom_value = datetime.strptime(date_of_marriage, "%Y-%m-%d").date() if date_of_marriage else None

    file_path = None
    if file:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    payload = {
        "user_id": user_id,
        "submission_id": submission_id,
        "relation": relation,
        "full_name": full_name,
        "dob": dob_value,
        "gender": gender,
        "place_of_birth": place_of_birth,
        "date_of_marriage": dom_value,
        "document_details": document_details,
        "comment": comment,
        "status": status    
    }

    if file_path:
        payload["document"] = file_path


    payload_clean = {k: v for k, v in payload.items() if v is not None}

    # ---------- UPDATE ----------
    if ef_id:
        payload_clean["ef_id"] = ef_id

        # 🔥 1. FETCH OLD DATA
        old_row = db.execute(
            text("SELECT * FROM employee_family WHERE ef_id = :id"),
            {"id": ef_id}
        ).fetchone()

        old_data = dict(old_row._mapping) if old_row else {}

        # 🔥 2. GET EXISTING changed_fields
        existing_changes = []
        if old_data.get("changed_fields"):
            try:
                existing_changes = json.loads(old_data["changed_fields"]).get("changed_fields", [])
            except:
                existing_changes = []

        # 🔥 3. BUILD NEW CHANGES
        changed_fields = build_changed_fields(old_data, payload_clean, existing_changes)

        # 🔥 4. MERGE (NO DUPLICATE)
        final_map = {item["field"]: item for item in existing_changes}
        for item in changed_fields:
            final_map[item["field"]] = item

        final_changes = list(final_map.values())

        # 🔥 5. SAVE UPDATE + changed_fields
        payload_clean["changed_fields"] = json.dumps({
            "changed_fields": final_changes
        })

        sql = text(f"""
            UPDATE employee_family
            SET {", ".join([f"{k} = :{k}" for k in payload_clean if k != "ef_id"])}
            WHERE ef_id = :ef_id
            RETURNING *;
        """)

        row = db.execute(sql, payload_clean).fetchone()
        db.commit()

        if not row:
            return {"status": "error", "message": "No record found to update"}

    else:
                # 🔥 FIRST TIME → old = new
        initial_changes = []

        for k, v in payload_clean.items():
            if v is None:
                continue

            initial_changes.append({
                "field": k,
                "old": v,
                "new": v
            })

        payload_clean["changed_fields"] = json.dumps({
            "changed_fields": initial_changes
        })
        
        # ---------- INSERT ----------
        sql = text(f"""
            INSERT INTO employee_family ({", ".join(payload_clean.keys())})
            VALUES ({", ".join([f":{k}" for k in payload_clean])})
            RETURNING *;
        """)

        row = db.execute(sql, payload_clean).fetchone()
        db.commit()

        if not row:
            return {"status": "error", "message": "Insert failed"}

    # ---------- NOTIFICATION ----------
    employee = db.query(User).filter(User.user_id == user_id).first()
    employee_username = employee.username if employee else None

    #print("🚀 FAMILY NOTIFICATION TRIGGER")
    #print("Employee:", employee_username)
    #print("Status:", status)

    await handle_employee_update_notifications(
        db=db,
        old_status=None,
        new_status=status,
        old_comments=None,
        new_comments=comment,
        employee_username=employee_username,
        changed_sections=["Family Details"],
        changed_fields=[],
        reference_id=str(user_id),
        redirect_url=f"/profile/profile-info/{str(user_id)}/review",
        bg=background_tasks
    )
    result = dict(row._mapping)

    return result





@router.delete("/delete-employee-family/{ef_id}")
def delete_employee_family(ef_id: int, db: Session = Depends(get_db)):
    family = db.query(EmployeeFamily).filter(EmployeeFamily.ef_id == ef_id).first()

    if not family:
        raise HTTPException(status_code=404, detail="Family record not found")

    db.delete(family)
    db.commit()

    return {"message": "Employee family deleted successfully"}


# ================= SUBMISSION APIs =================
@router.post("/submission/create")
def create_submission(user_id: int = Form(...), db: Session = Depends(get_db)):
    sql = text("""
        INSERT INTO submission (user_id, status)
        VALUES (:user_id, '')
        RETURNING *;
    """)
    row = db.execute(sql, {"user_id": user_id}).fetchone()
    db.commit()
    return dict(row._mapping)


@router.delete("/delete-employee-family/{ef_id}")
def delete_employee_family(ef_id: int, db: Session = Depends(get_db)):
    family = db.query(EmployeeFamily).filter(EmployeeFamily.ef_id == ef_id).first()

    if not family:
        raise HTTPException(status_code=404, detail="Family record not found")

    db.delete(family)
    db.commit()

    return {"message": "Employee family deleted successfully"}


# ================= SUBMISSION APIs =================
# @router.post("/submission/create")
# def create_submission(user_id: int = Form(...), db: Session = Depends(get_db)):
#     sql = text("""
#         INSERT INTO submission (user_id, status)
#         VALUES (:user_id, '')
#         RETURNING *;
#     """)
#     row = db.execute(sql, {"user_id": user_id}).fetchone()
#     db.commit()
#     return dict(row._mapping)


# @router.put("/submission/{submission_id}")
# def update_submission(
#     submission_id: int,
#     status: str = Form(None),
#     hr_comment: str = Form(None),   
#     db: Session = Depends(get_db)
# ):

#     sql = text("""
#         UPDATE submission
#         SET status = COALESCE(:status, status),
#             hr_comment = COALESCE(:hr_comment, hr_comment)
#         WHERE submission_id = :sid
#         RETURNING *;
#     """)

#     row = db.execute(sql, {
#         "sid": submission_id,
#         "status": status,
#         "hr_comment": hr_comment  
#     }).fetchone()

#     db.commit()

#     if not row:
#         raise HTTPException(404, "Submission not found")

#     return dict(row._mapping)


# @router.put("/submission/{submission_id}")
# async def update_submission(
#     submission_id: int,
#     status: str = Form(None),
#     hr_comment: str = Form(None),
#     background_tasks: BackgroundTasks = None,
#     db: Session = Depends(get_db)
# ):
#     # ---------------------------------
#     # Fetch from submission table directly
#     # ---------------------------------
#     submission = db.execute(
#         text("""
#             SELECT s.*, u.username
#             FROM submission s
#             JOIN users u ON s.user_id = u.user_id
#             WHERE s.submission_id = :sid
#         """),
#         {"sid": submission_id}
#     ).fetchone()

#     if not submission:
#         raise HTTPException(404, "Submission not found")

#     old_status = submission.status
#     employee_username = submission.username

#     # ---------------------------------
#     # Update submission table
#     # ---------------------------------
#     row = db.execute(
#         text("""
#             UPDATE submission
#             SET status = COALESCE(:status, status),
#                 hr_comment = COALESCE(:hr_comment, hr_comment)
#             WHERE submission_id = :sid
#             RETURNING *;
#         """),
#         {
#             "sid": submission_id,
#             "status": status,
#             "hr_comment": hr_comment
#         }
#     ).fetchone()

#     db.commit()


#     new_status = row.status

#     print("🔔 HR FAMILY REVIEW")
#     print("Employee:", employee_username)
#     print("Old Status:", old_status)
#     print("New Status:", new_status)

#     # ---------------------------------
#     # Trigger notification
#     # ---------------------------------
#     await handle_employee_update_notifications(
#         db=db,
#         old_status=old_status,
#         new_status=new_status,
#         old_comments=None,
#         new_comments=hr_comment,
#         employee_username=employee_username,
#         changed_sections=["Family Details"],
#         bg=background_tasks
#     )

#     return dict(row._mapping)

#==================================
# this is change in 17/03/2026
#===================================

@router.put("/submission/{submission_id}")
async def update_submission(
    submission_id: int,
    status: str = Form(None),
    hr_comment: str = Form(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
 
    submission = db.execute(
        text("""
            SELECT s.*, u.username
            FROM submission s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.submission_id = :sid
        """),
        {"sid": submission_id}
    ).fetchone()
    user_id = submission.user_id if submission else None
    if not submission:
        raise HTTPException(404, "Submission not found")
 
    old_status = submission.status
    old_comments = submission.hr_comment
    employee_username = submission.username
 
    # ---------------------------------
    # Update ONLY comment (NOT status from API)
    # ---------------------------------
    # UPDATE
    row = db.execute(
        text("""
            UPDATE submission
            SET hr_comment = COALESCE(:hr_comment, hr_comment),
            status = COALESCE(:status, status)
            WHERE submission_id = :sid
            RETURNING *;
        """),
        {
            "sid": submission_id,
            "hr_comment": hr_comment,
            "status": status
        }
    ).fetchone()
 
 
    if not row:
        raise HTTPException(404, "Update failed")
 
    db.commit()
 
 
    # GET STATUS FROM DB
    submission_row = db.execute(
        text("""
            SELECT status
            FROM submission
            WHERE submission_id = :sid
        """),
        {"sid": submission_id}
    ).fetchone()
 
    final_status = (
        submission_row.status.strip().lower()
        if submission_row and submission_row.status
        else None
    )
 
 
    # NOTIFICATION
    if final_status == "pending approval":
 
        await handle_employee_update_notifications(
            db=db,
            old_status=old_status,
            new_status=final_status,
            old_comments=old_comments,
            new_comments=None,
            employee_username=employee_username,
            changed_sections=["Family"],
            changed_fields=[],
            reference_id=str(user_id),
            redirect_url=f"/profile/profile-info/{str(user_id)}/review",
            bg=background_tasks
        )
 
    elif final_status in ["approved", "changes requested"]:
 
        hr_usernames = get_all_hr_usernames(db)
        hr_username = hr_usernames[0] if hr_usernames else "HR"
 
        await notify_employee_on_status_change(
            db=db,
            employee_username=employee_username,
            hr_username=hr_username,
            new_status=final_status,
            comments=hr_comment,
            changed_sections="Family",
            reference_id=str(user_id),
            redirect_url=f"/profile/{str(user_id)}",
            bg=background_tasks
        )
 
 
    return dict(row._mapping)

@router.get("/submission-info/{submission_id}")
def get_submission_info(submission_id: int, db: Session = Depends(get_db)):
    sql = text("SELECT * FROM submission WHERE submission_id = :sid")
    row = db.execute(sql, {"sid": submission_id}).fetchone()

    if not row:
        raise HTTPException(404, "Submission not found")

    return dict(row._mapping)


@router.get("/submission/{submission_id}/members")
def get_family_by_submission(submission_id: int, db: Session = Depends(get_db)):
    sql = text("SELECT * FROM employee_family WHERE submission_id = :sid")
    rows = db.execute(sql, {"sid": submission_id}).fetchall()
    return [serialize_family(dict(r._mapping)) for r in rows]



# from datetime import datetime
# import os
# import shutil
# from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
# from sqlalchemy import text
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.employees_info.employee_family import EmployeeFamily
# from app.models.UserModel import User
# from app.routers.UserAuthR2 import make_download_url

# # NEW IMPORT (notification workflow)
# from app.crud.employees_info.employee_notifications_crud import handle_employee_update_notifications

# from app.crud.employees_info.employee_family_crud import (
#     get_all_family_members,
#     get_family_member_by_id,
#     get_family_members_by_user_id
# )

# router = APIRouter(prefix="/api/employee-family", tags=["Employee Family"])

# UPLOAD_DIR = "files/employee_family"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # ================= SERIALIZER =================
# def serialize_family(row):
#     return {
#         "ef_id": row.get("ef_id"),
#         "submission_id": row.get("submission_id"),
#         "relation": row.get("relation"),
#         "full_name": row.get("full_name"),
#         "dob": row.get("dob"),
#         "document": row.get("document"),
#         "user_id": row.get("user_id"),
#         "gender": row.get("gender"),
#         "place_of_birth": row.get("place_of_birth"),
#         "date_of_marriage": row.get("date_of_marriage"),
#         "status": row.get("status"),
#         "document_details": row.get("document_details"),
#         "comment": row.get("comment"),
#     }


# # ================= GET APIs =================
# @router.get("/all")
# def route_get_all(db: Session = Depends(get_db)):
#     rows = get_all_family_members(db)
#     return [serialize_family(row) for row in rows]


# @router.get("/{ef_id}")
# def route_get_by_id(ef_id: int, db: Session = Depends(get_db)):
#     row = get_family_member_by_id(db, ef_id)
#     return serialize_family(row)


# @router.get("/user/{user_id}")
# def route_get_by_user(user_id: int, db: Session = Depends(get_db)):
#     rows = get_family_members_by_user_id(db, user_id)
#     return [serialize_family(row) for row in rows]


# # ================= FAMILY CRUD =================
# @router.post("/crud")
# async def employee_family_crud(
#     ef_id: str | None = Form(None),
#     user_id: int = Form(...),
#     submission_id: int = Form(...),
#     relation: str | None = Form(None),
#     full_name: str | None = Form(None),
#     dob: str | None = Form(None),
#     gender: str | None = Form(None),
#     place_of_birth: str | None = Form(None),
#     date_of_marriage: str | None = Form(None),
#     status: str | None = Form(None),
#     file: UploadFile | None = File(None),
#     document_details: str | None = Form(None),
#     comment: str | None = Form(None),
#     background_tasks: BackgroundTasks = None,
#     db: Session = Depends(get_db)
# ):

#     if ef_id:
#         ef_id = int(ef_id)

#     user_obj = db.query(User).filter(User.user_id == user_id).first()

#     if not user_obj:
#         raise HTTPException(404, "User not found")

#     old_status = None

#     dob_value = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
#     dom_value = datetime.strptime(date_of_marriage, "%Y-%m-%d").date() if date_of_marriage else None

#     file_path = None
#     if file:
#         file_path = os.path.join(UPLOAD_DIR, file.filename)
#         with open(file_path, "wb") as f:
#             shutil.copyfileobj(file.file, f)

#     # FORCE STATUS FOR EMPLOYEE ACTION
#     # status = ""

#     payload = {
#         "user_id": user_id,
#         "submission_id": submission_id,
#         "relation": relation,
#         "full_name": full_name,
#         "dob": dob_value,
#         "gender": gender,
#         "place_of_birth": place_of_birth,
#         "date_of_marriage": dom_value,
#         "document_details": document_details,
#         "comment": comment,
#         # "status": status
#     }

#     if file_path:
#         payload["document"] = file_path

#     payload_clean = {k: v for k, v in payload.items() if v is not None}

#     # ---------- UPDATE ----------
#     if ef_id:

#         payload_clean["ef_id"] = ef_id

#         sql = text(f"""
#             UPDATE employee_family
#             SET {", ".join([f"{k} = :{k}" for k in payload_clean if k != "ef_id"])}
#             WHERE ef_id = :ef_id
#             RETURNING *;
#         """)

#         row = db.execute(sql, payload_clean).fetchone()
#         db.commit()

#         if not row:
#             return {
#                 "status": "error",
#                 "message": "No record found to update"
#             }

#         # 🔔 Notify HR
#         await handle_employee_update_notifications(
#             db=db,
#             old_status=old_status,
#             new_status=status,
#             old_comments=None,
#             new_comments=None,
#             employee_username=user_obj.username,
#             changed_sections=["Family Information"],
#             bg=background_tasks
#         )

#         return dict(row._mapping)

#     # ---------- INSERT ----------
#     sql = text(f"""
#         INSERT INTO employee_family ({", ".join(payload_clean.keys())})
#         VALUES ({", ".join([f":{k}" for k in payload_clean])})
#         RETURNING *;
#     """)

#     row = db.execute(sql, payload_clean).fetchone()
#     db.commit()

#     if not row:
#         return {
#             "status": "error",
#             "message": "Insert failed"
#         }

#     # 🔔 Notify HR
#     await handle_employee_update_notifications(
#         db=db,
#         old_status=old_status,
#         new_status=status,
#         old_comments=None,
#         new_comments=None,
#         employee_username=user_obj.username,
#         changed_sections=["Family Information"],
#         bg=background_tasks
#     )

#     return dict(row._mapping)


# @router.delete("/delete-employee-family/{ef_id}")
# def delete_employee_family(ef_id: int, db: Session = Depends(get_db)):
#     family = db.query(EmployeeFamily).filter(EmployeeFamily.ef_id == ef_id).first()

#     if not family:
#         raise HTTPException(status_code=404, detail="Family record not found")

#     db.delete(family)
#     db.commit()

#     return {"message": "Employee family deleted successfully"}


# # ================= SUBMISSION APIs =================
# @router.post("/submission/create")
# def create_submission(user_id: int = Form(...), db: Session = Depends(get_db)):

#     sql = text("""
#         INSERT INTO submission (user_id, status)
#         VALUES (:user_id, '')
#         RETURNING *;
#     """)

#     row = db.execute(sql, {"user_id": user_id}).fetchone()
#     db.commit()

#     return dict(row._mapping)


# @router.put("/submission/{submission_id}")
# async def update_submission(
#     submission_id: int,
#     status: str = Form(None),
#     hr_comment: str = Form(None),
#     background_tasks: BackgroundTasks = None,
#     db: Session = Depends(get_db)
# ):

#     sql = text("""
#         UPDATE submission
#         SET status = COALESCE(:status, status),
#             hr_comment = COALESCE(:hr_comment, hr_comment)
#         WHERE submission_id = :sid
#         RETURNING *;
#     """)

#     row = db.execute(sql, {
#         "sid": submission_id,
#         "status": status,
#         "hr_comment": hr_comment
#     }).fetchone()

#     db.commit()

#     if not row:
#         raise HTTPException(404, "Submission not found")

#     user_id = row.user_id
#     user_obj = db.query(User).filter(User.user_id == user_id).first()

#     # 🔔 HR decision → notify employee
#     await handle_employee_update_notifications(
#         db=db,
#         old_status=None,
#         new_status=status,
#         old_comments=None,
#         new_comments=hr_comment,
#         employee_username=user_obj.username,
#         changed_sections=["Family Information"],
#         bg=background_tasks
#     )

#     return dict(row._mapping)


# @router.get("/submission-info/{submission_id}")
# def get_submission_info(submission_id: int, db: Session = Depends(get_db)):
#     sql = text("SELECT * FROM submission WHERE submission_id = :sid")
#     row = db.execute(sql, {"sid": submission_id}).fetchone()

#     if not row:
#         raise HTTPException(404, "Submission not found")

#     return dict(row._mapping)


# @router.get("/submission/{submission_id}/members")
# def get_family_by_submission(submission_id: int, db: Session = Depends(get_db)):
#     sql = text("SELECT * FROM employee_family WHERE submission_id = :sid")
#     rows = db.execute(sql, {"sid": submission_id}).fetchall()
#     return [serialize_family(dict(r._mapping)) for r in rows]