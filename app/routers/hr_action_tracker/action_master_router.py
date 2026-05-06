from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
 
from app.database import get_db
from app.crud.hr_action_tracker import action_master_crud, hr_action_notification_crud
from app.schemas.hr_action_tracker.action_master_schema import AcknowledgeActionRequest, HRActionCreate, HRActionUpdate
from app.schemas.hr_action_tracker.promotion_master_schema import CommonFilterRequest
 
router = APIRouter(
    prefix="/hr-action",
    tags=["HR Action"]
)
 
# 1. CREATE HR Action with optional files
@router.post("/")
def create(
    user_id: int = Form(...),
    action_type: str = Form(...),
    action_date: str = Form(...),
    justification: str = Form(...),
    created_by: int = Form(...),
    files: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    try:
        # Parse date
        action_dt = datetime.fromisoformat(action_date.replace("Z", "+00:00"))
       
        action_in = HRActionCreate(
            user_id=user_id,
            action_type=action_type,
            action_date=action_dt,
            justification=justification,
            created_by=created_by
        )
 
        db_action = action_master_crud.create_action(db, action_in=action_in)
 
        if files:
            UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "hr_action")
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)
 
            for file in files:
                if file.filename:
                    unique_filename = f"{db_action['id']}_{int(datetime.now().timestamp())}_{file.filename}"
                    file_path = os.path.join(UPLOAD_DIR, unique_filename)
 
                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)
 
                    relative_path = os.path.join("uploads", "hr_action", unique_filename)
                    action_master_crud.create_document(
                        db,
                        hr_action_id=db_action['id'],
                        file_name=file.filename,
                        file_path=relative_path
                    )
       
        # 3. Trigger Notifications (Async)
        background_tasks.add_task(
            hr_action_notification_crud.send_hr_action_notification,
            db,
            user_id=user_id,
            action_type=action_type,
            action_details=justification,
            from_user_id=created_by,
            background_tasks=background_tasks
        )
 
        return {"message": "HR Action created successfully", "id": db_action['id']}
 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 
# 2. GET ALL HR Actions
@router.get("/")
def get_all(db: Session = Depends(get_db)):
    items, total = action_master_crud.get_all_actions(db)
    return {"items": items, "total": total}
 
# 3. GET HR Action BY ID
@router.get("/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    db_action = action_master_crud.get_action_by_id(db, action_id=id)
    if not db_action:
        raise HTTPException(status_code=404, detail="HR Action not found")
    return db_action
 
# 4. GET HR Actions BY USER
@router.get("/user/{user_id}")
def get_by_user(user_id: int, db: Session = Depends(get_db)):
    return action_master_crud.get_actions_by_user(db, user_id=user_id)
 
# 5. DELETE HR Action
@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    success = action_master_crud.delete_action(db, action_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="HR Action not found")
    return {"message": "HR Action deleted successfully"}

# @router.put("/acknowledge-action/{id}/{user_id}")
# def acknowledge_action(
#     id: int,
#     payload: AcknowledgeActionRequest,
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     return action_master_crud.acknowledge_hr_action(db, id, user_id, payload.dict())
@router.put("/acknowledge-action/{id}/{user_id}")
def acknowledge_action(
    id: int,
    payload: AcknowledgeActionRequest,
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    result = action_master_crud.acknowledge_hr_action(db, id, user_id, payload.dict())
   
    if result.get("status"):
        background_tasks.add_task(
            hr_action_notification_crud.send_hr_acknowledgement_notification,
            db,
            user_id=user_id,
            action_id=id,
            background_tasks=background_tasks
        )
       
    return result

@router.post("/employee-activity-filter-actions/{user_id}")
def employee_activity_filter_actions(
    request: CommonFilterRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    return action_master_crud.get_employee_activity_actions(db, request, user_id)
