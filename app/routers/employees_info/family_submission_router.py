# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.schemas.employees_info.submission_schema import (
#     FamilySubmissionCreate,
#     FamilySubmissionUpdate
# )
# from app.crud.employees_info.submission_crud import (
#     create_submission,
#     update_submission
# )

# router = APIRouter(prefix="/family-submission", tags=["Family Submission"])


# # =========================
# # POST
# # =========================
# @router.post("/")
# def create_family_submission(
#     payload: FamilySubmissionCreate,
#     db: Session = Depends(get_db)
# ):
#     submission_id = create_submission(db, payload)

#     return {
#         "message": "Submission created successfully",
#         "submission_id": submission_id
#     }


# # =========================
# # PUT
# # =========================
# @router.put("/{submission_id}")
# def update_family_submission(
#     submission_id: int,
#     payload: FamilySubmissionUpdate,
#     db: Session = Depends(get_db)
# ):
#     result = update_submission(db, submission_id, payload)

#     if result == "Nothing to update":
#         raise HTTPException(status_code=400, detail=result)

#     return {"message": result}


from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db

from app.models.employees_info.submission import FamilySubmission
from app.schemas.employees_info.submission_schema import (
    FamilySubmissionCreate,
    FamilySubmissionUpdate
)

from app.crud.employees_info.submission_crud import (
    create_submission,
    update_submission
)

from app.crud.employees_info.employee_notifications_crud import (
    handle_employee_update_notifications
)

from app.models.UserModel import User

router = APIRouter(prefix="/family-submission", tags=["Family Submission"])


# =========================================================
# CREATE SUBMISSION (Employee submits family information)
# =========================================================
@router.post("/")
async def create_family_submission(
    payload: FamilySubmissionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    # Force status for employee submission
    status = payload.status if payload.status else "Pending Approval"

    submission_id = create_submission(db, payload)

    # -----------------------------
    # Get employee
    # -----------------------------
    user = db.query(User).filter(User.user_id == payload.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # -----------------------------
    # Notify HR
    # -----------------------------
    await handle_employee_update_notifications(
        db=db,
        old_status=None,
        new_status=status,
        old_comments=None,
        new_comments=None,
        employee_username=user.username,
        changed_sections=["Family"],
        changed_fields=[],
        reference_id=str(payload.user_id),
        redirect_url=f"/profile/profile-info/{str(payload.user_id)}/review",
        bg=background_tasks
    )

    return {
        "message": "Submission created successfully",
        "submission_id": submission_id,
        "status": status
    }


# =========================================================
# UPDATE SUBMISSION (HR review)
# =========================================================
# @router.put("/{submission_id}")
# async def update_family_submission(
#     submission_id: int,
#     payload: FamilySubmissionUpdate,
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db)
#     ):

#     # ---------------------------------
#     # Validate HR status
#     # ---------------------------------
#     if payload.status not in ["Approved", "Changes Requested"]:
#         raise HTTPException(
#             status_code=400,
#             detail="Status must be Approved or Changes Requested"
#         )

#     # ---------------------------------
#     # Update submission
#     # ---------------------------------
#     result = update_submission(db, submission_id, payload)

#     if result == "Nothing to update":
#         raise HTTPException(status_code=400, detail=result)

#     # ---------------------------------
#     # Get user_id from submission
#     # ---------------------------------
#     submission = db.execute(
#         text("SELECT user_id FROM submission WHERE submission_id = :sid"),
#         {"sid": submission_id}
#     ).fetchone()

#     if not submission:
#         raise HTTPException(status_code=404, detail="Submission not found")

#     # ---------------------------------
#     # Get employee
#     # ---------------------------------
#     user = db.query(User).filter(User.user_id == submission.user_id).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # ---------------------------------
#     # Notify employee
#     # ---------------------------------
#     await handle_employee_update_notifications(
#         db=db,
#         old_status=None,
#         new_status=payload.status,
#         old_comments=None,
#         new_comments=payload.hr_comment,
#         employee_username=user.username,
#         changed_sections=["Family"],
#         bg=background_tasks
#     )

#     return {
#         "message": result,
#         "status": payload.status
#     }



@router.put("/{submission_id}")
async def update_family_submission(
    submission_id: int,
    payload: FamilySubmissionUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # ---------------------------------
    # Validate HR status
    # ---------------------------------
    if payload.status not in ["Approved", "Changes Requested"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Approved or Changes Requested"
        )

    # ---------------------------------
    # DEBUG
    # ---------------------------------
    ##print(f"DEBUG 1: submission_id = {submission_id}, type = {type(submission_id)}")

    all_ids = db.execute(text("SELECT submission_id FROM submission")).fetchall()
    #print(f"DEBUG 2: All IDs in DB = {[r[0] for r in all_ids]}")

    raw = db.execute(
        text("SELECT * FROM submission WHERE submission_id = :sid"),
        {"sid": submission_id}
    ).fetchone()
    #print(f"DEBUG 3: Raw query result = {raw}")

    orm = db.query(FamilySubmission).filter(
        FamilySubmission.submission_id == submission_id
    ).first()
    #print(f"DEBUG 4: ORM query result = {orm}")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Submission {submission_id} not found. All IDs: {[r[0] for r in all_ids]}")

    # ---------------------------------
    # Fetch user
    # ---------------------------------
    user = db.query(User).filter(User.user_id == raw.user_id).first()
    #print(f"DEBUG 5: user = {user}")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ---------------------------------
    # Update submission
    # ---------------------------------
    result = update_submission(db, submission_id, payload)
    user_id = raw.user_id  # Get user_id before update, as update might change it
    if result == "Nothing to update":
        raise HTTPException(status_code=400, detail=result)

    # ---------------------------------
    # Notify employee
    # ---------------------------------
    await handle_employee_update_notifications(
        db=db,
        old_status=None,
        new_status=payload.status,
        old_comments=None,
        new_comments=payload.hr_comment,
        employee_username=user.username,
        changed_sections=["Family"],
        changed_fields=[],
        reference_id=str(user_id),
        redirect_url=f"/profile/profile-info/{str(user_id)}/review",
        bg=background_tasks
    )

    return {
        "message": result,
        "status": payload.status
    }








