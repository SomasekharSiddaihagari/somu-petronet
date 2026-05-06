from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File, Form
# from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
import uuid
from datetime import datetime
 
from app.database import get_db
from app.crud.hr_action_tracker import emp_transfer_master_crud, hr_action_notification_crud
from app.schemas.hr_action_tracker.emp_transfer_master_schema import AcknowledgeTransferRequest, EmployeeTransferCreate, EmployeeTransferResponse
from app.schemas.hr_action_tracker.promotion_master_schema import CommonFilterRequest
 
router = APIRouter(
    prefix="/emp-transfer",
    tags=["Employee Transfer"]
)
 
# 1. CREATE Transfer with optional files
@router.post("/")
def create_transfer_endpoint(
    user_id: int = Form(...),
    current_station: int = Form(...),
    new_station: int = Form(...),
    effective_date: str = Form(...),
    remarks: Optional[str] = Form(None),
    created_by: int = Form(...),
    office_order_number: Optional[str] = Form(...),
    files: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    try:
        # Convert string date to datetime
        eff_date = datetime.fromisoformat(effective_date)
       
        transfer_in = EmployeeTransferCreate(
            user_id=user_id,
            current_station=current_station,
            new_station=new_station,
            effective_date=eff_date,
            remarks=remarks,
            created_by=created_by,
            office_order_number = office_order_number
        )
       
        db_transfer = emp_transfer_master_crud.create_transfer(db, transfer_in=transfer_in)
 
        if files:
            UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "emp_transfer")
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)
 
            for file in files:
                if file.filename:
                    unique_filename = f"{db_transfer['id']}_{int(datetime.now().timestamp())}_{file.filename}"
                    file_path = os.path.join(UPLOAD_DIR, unique_filename)
 
                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)
 
                    relative_path = os.path.join("uploads", "emp_transfer", unique_filename)
                    emp_transfer_master_crud.create_document(
                        db,
                        transfer_id=db_transfer['id'],
                        file_name=file.filename,
                        file_path=relative_path
                    )
 
        # 3. Trigger Notifications
        background_tasks.add_task(
            hr_action_notification_crud.send_hr_action_notification,
            db,
            user_id=user_id,
            action_type="Employee Transfer",
            action_details=f"Transfer initiated to Station ID {new_station}. Remarks: {remarks or 'N/A'}",
            from_user_id=created_by,
            background_tasks=background_tasks
        )
 
        # Re-fetch to include attachments
        return {"message": "Employee Transfer created successfully", "id": db_transfer['id']}
 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 
# 2. GET ALL Transfers
@router.get("/")
def get_all_transfers(db: Session = Depends(get_db)):
    items, total = emp_transfer_master_crud.get_all_transfers(db)
    return {"items": items, "total": total}
 
# 3. GET Transfer by ID
@router.get("/{id}", response_model=EmployeeTransferResponse)
def get_transfer(id: int, db: Session = Depends(get_db)):
    db_transfer = emp_transfer_master_crud.get_transfer_by_id(db, transfer_id=id)
    if not db_transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return db_transfer
 
# 4. DELETE Transfer (Soft Delete)
@router.delete("/{id}")
def delete_transfer_endpoint(id: int, db: Session = Depends(get_db)):
    success = emp_transfer_master_crud.delete_transfer(db, transfer_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return {"message": "Employee Transfer deleted successfully"}

#get transfer by userid
@router.get("/get-by-user-transfer/{user_id}", summary="get transfer by userid for employee")
def get_by_user_transfer(user_id: int, db: Session = Depends(get_db)):
    return emp_transfer_master_crud.get_by_user_transfers(db, user_id=user_id)

# @router.put("/acknowledge-transfer/{id}/{user_id}")
# def acknowledge_transfer(
#     id: int,
#     payload: AcknowledgeTransferRequest,
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     return emp_transfer_master_crud.acknowledge_hr_transfer(db, id, user_id, payload.dict())
@router.put("/acknowledge-transfer/{id}/{user_id}")
def acknowledge_transfer(
    id: int,
    payload: AcknowledgeTransferRequest,
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    result = emp_transfer_master_crud.acknowledge_hr_transfer(db, id, user_id, payload.dict())
   
    if result.get("status"):
        background_tasks.add_task(
            hr_action_notification_crud.send_hr_acknowledgement_notification,
            db,
            user_id=user_id,
            action_id=id,
            background_tasks=background_tasks,
            module_type="TRANSFER"
        )
       
    return result

@router.post("/employee-activity-filter-transfer/{user_id}")
def employee_activity_filter_transfer(
    request: CommonFilterRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    return emp_transfer_master_crud.get_employee_activity_transfer(db, request, user_id)