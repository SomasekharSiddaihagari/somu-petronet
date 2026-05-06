# from fastapi import APIRouter, BackgroundTasks
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil
from typing import List, Optional

from app.database import get_db

from app.crud.hr_action_tracker import hr_action_notification_crud
from app.crud.hr_action_tracker.promotion_master_crud import (
    acknowledge_hr_promotion, create_promotion, delete_promotion, 
    get_all_actions_hr, get_all_emp_disciplinary_hr, get_all_emp_hr, 
    get_all_emp_transfer_hr, get_all_performance_hr, get_all_promotions, 
    get_all_promotions_hr, get_by_user_promotions, get_employee_activity, 
    get_employee_activity_promotion, get_grade_designation, 
    get_promotion_based_promotionid
)
from app.schemas.hr_action_tracker.promotion_master_schema import (
    AcknowledgePromotionRequest, CommonFilterRequest, PromotionCreate
)



router = APIRouter(prefix="/promotions", tags=["Promotions"])

# get designation and grade by userid
@router.get("/{user_id}", summary="get previous designation and grade")
def get(user_id: int, db: Session = Depends(get_db)):
    result = get_grade_designation(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return dict(result._mapping)

# create promotion
# @router.post("/", summary="create promotion")
# def create(data: PromotionCreate, db: Session = Depends(get_db)):
#     id = create_promotion(db, data)
#     return {"message": "Promotion created", "id": id}
@router.post("/")
def create(
    user_id: int = Form(...),
    current_grade: str = Form(...),
    new_grade: str = Form(...),
    current_designation: str = Form(...),
    new_designation: str = Form(...),
    effective_date: str = Form(...),
    remarks: Optional[str] = Form(None),
    created_by: Optional[int] = Form(None),
    files: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    try:
        eff_dt = None
        if effective_date and effective_date != "string":
            eff_dt = datetime.fromisoformat(effective_date.replace("Z", "+00:00"))
        
        data = PromotionCreate(
            id=0, # auto-incremented
            user_id=user_id,
            current_grade=current_grade,
            new_grade=new_grade,
            current_designation=current_designation,
            new_designation=new_designation,
            effective_date=eff_dt,
            remarks=remarks,
            created_by=created_by
        )
        
        promotion_id = create_promotion(db, data)
       
        if files:
            UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "promotions")
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)

            for file in files:
                if file.filename:
                    unique_filename = f"{promotion_id}_{int(datetime.now().timestamp())}_{file.filename}"
                    file_path = os.path.join(UPLOAD_DIR, unique_filename)

                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    relative_path = os.path.join("uploads", "promotions", unique_filename)
                    # We need to import promotion_master_crud specifically or use it from the previous imports
                    from app.crud.hr_action_tracker import promotion_master_crud
                    promotion_master_crud.create_document(
                        db,
                        promotion_id=promotion_id,
                        file_name=file.filename,
                        file_path=relative_path
                    )
       
        # Trigger Notifications
        background_tasks.add_task(
            hr_action_notification_crud.send_hr_action_notification,
            db,
            user_id=user_id,
            action_type="Promotion",
            action_details=f"Grade: {current_grade} -> {new_grade}, Designation: {current_designation} -> {new_designation}",
            from_user_id=created_by,
            background_tasks=background_tasks
        )
 
        return {"message": "Promotion created successfully", "id": promotion_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get by promotion id
@router.get("get-promotion-by-id/{id}")
def get(id: int, db: Session = Depends(get_db)):
    result = get_promotion_based_promotionid(db, id=id)

    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return result

#get all promotions
@router.get("/", summary="get all promotion")
def get_all(db: Session = Depends(get_db)):
    results = get_all_promotions(db)
    return [dict(row._mapping) for row in results]

#get promotions by userid
@router.get("/get-by-user-promotion/{user_id}", summary="get promotion by userid for employee")
def get_by_user_promotion(user_id: int, db: Session = Depends(get_db)):
    return get_by_user_promotions(db, user_id=user_id)

#delete promotions
@router.delete("/delete/{id}")
def delete_promotion_api(
    id: int,
    db: Session = Depends(get_db)
):
    delete_promotion(db, id)
    return {
        "status": "success",
        "message": "Promotion deleted successfully"
    }

#api for promotion tab getall for hr and supervisor
@router.get("/get-all-promotions_hr/{user_id}", summary="promotion tab getall for hr and supervisor")
def get_all_promotion(user_id: int, db: Session = Depends(get_db)):
    return get_all_promotions_hr(db,user_id)

#api for allemployee tab  getall for hr and supervisor
@router.get("/get-all-emp_hr/{user_id}", summary="allemployee tab  getall for hr and supervisor")
def get_all_emp(user_id: int, db: Session = Depends(get_db)):
    return get_all_emp_hr(db,user_id)

#api for actions tab  getall for hr and supervisor
@router.get("/get-all-actions_hr/{user_id}", summary="actions tab  getall for hr and supervisor")
def get_all_actions(user_id: int, db: Session = Depends(get_db)):
    return get_all_actions_hr(db,user_id)

#api for transfer tab  getall for hr and supervisor
@router.get("/get-all-emp-transfer_hr/{user_id}", summary="transfers tab  getall for hr and supervisor")
def get_all_emp_trasfer(user_id: int, db: Session = Depends(get_db)):
    return get_all_emp_transfer_hr(db,user_id)

#api for disciplinary tab  getall for hr and supervisor
@router.get("/get-all-emp-disciplinary_hr/{user_id}", summary="disciplinary tab  getall for hr and supervisor")
def get_all_emp_disciplinary(user_id: int, db: Session = Depends(get_db)):
    return get_all_emp_disciplinary_hr(db,user_id)

@router.get("/get-all-performance_hr/{user_id}", summary="performance tab getall for hr and supervisor")
def get_all_performance(user_id: int, db: Session = Depends(get_db)):
    return get_all_performance_hr(db,user_id)
# @router.put("/acknowledge-promotion/{id}/{user_id}")
# def acknowledge_promotion(
#     id: int,
#     payload: AcknowledgePromotionRequest,
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     return acknowledge_hr_promotion(db, id, user_id, payload.dict())

@router.put("/acknowledge-promotion/{id}/{user_id}")
def acknowledge_promotion_endpoint(
    id: int,
    payload: AcknowledgePromotionRequest,
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    result = acknowledge_hr_promotion(db, id, user_id, payload.dict())
   
    if result.get("status"):
        background_tasks.add_task(
            hr_action_notification_crud.send_hr_acknowledgement_notification,
            db,
            user_id=user_id,
            action_id=id,
            background_tasks=background_tasks,
            module_type="PROMOTION"
        )
       
    return result

@router.post("/employee-activity-filter/{user_id}")
def employee_activity_filter(
    request: CommonFilterRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_employee_activity(db, request, user_id)

@router.post("/employee-activity-filter-promotion/{user_id}")
def employee_activity_filter_promotion(
    request: CommonFilterRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_employee_activity_promotion(db, request, user_id)