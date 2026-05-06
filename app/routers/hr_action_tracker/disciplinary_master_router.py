from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import shutil
 
from app.database import get_db
from app.crud.hr_action_tracker import disciplinary_master_crud, hr_action_notification_crud
from app.schemas.hr_action_tracker.disciplinary_master_schema import AcknowledgeDisciplinaryRequest, DisciplinaryIncidentCreate, DisciplinaryIncidentResponse
from app.schemas.hr_action_tracker.promotion_master_schema import CommonFilterRequest
 
router = APIRouter(
    prefix="/disciplinary-master",
    tags=["Disciplinary Incidents"]
)
 
# 1. CREATE Incident
@router.post("/")
def create_incident_endpoint(
    # incident_in: DisciplinaryIncidentCreate,
    # background_tasks: BackgroundTasks,
    user_id: int = Form(...),
    incident_date: str = Form(...),
    severity: str = Form(...),
    incident_details: str = Form(...),
    investigation_finding: Optional[str] = Form(None),
    measures_taken: Optional[str] = Form(None),
    enable_suspension: Optional[bool] = Form(False),
    enable_termination: Optional[bool] = Form(False),
    suspension_effective_from: Optional[str] = Form(None),
    suspension_effective_to: Optional[str] = Form(None),
    termination_effective_from: Optional[str] = Form(None),
    outcome: Optional[str] = Form(None),
    created_by: Optional[int] = Form(None),
    files: List[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    try:
        def parse_dt(dt_str):
            if not dt_str or dt_str == "string": return None
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

        incident_in = DisciplinaryIncidentCreate(
            user_id=user_id,
            incident_date=parse_dt(incident_date),
            severity=severity,
            incident_details=incident_details,
            investigation_finding=investigation_finding,
            measures_taken=measures_taken,
            enable_suspension=enable_suspension,
            enable_termination=enable_termination,
            suspension_effective_from=parse_dt(suspension_effective_from),
            suspension_effective_to=parse_dt(suspension_effective_to),
            termination_effective_from=parse_dt(termination_effective_from),
            outcome=outcome,
            created_by=created_by
        )

        db_incident = disciplinary_master_crud.create_incident(db, incident_in=incident_in)
        incident_id = db_incident['disciplinary_id']

        if files:
            UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "disciplinary_incidents")
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)

            for file in files:
                if file.filename:
                    unique_filename = f"{incident_id}_{int(datetime.now().timestamp())}_{file.filename}"
                    file_path = os.path.join(UPLOAD_DIR, unique_filename)

                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    relative_path = os.path.join("uploads", "disciplinary_incidents", unique_filename)
                    disciplinary_master_crud.create_document(
                        db,
                        disciplinary_id=incident_id,
                        file_name=file.filename,
                        file_path=relative_path
                    )
       
        # Trigger Notifications
        background_tasks.add_task(
            hr_action_notification_crud.send_hr_action_notification,
            db,
            user_id=user_id,
            action_type="Disciplinary Incident",
            action_details=incident_details,
            from_user_id=created_by,
            background_tasks=background_tasks
        )
        return {"message": "Disciplinary Incident created successfully", "id": incident_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# 2. GET ALL Incidents
@router.get("/")
def get_all_incidents(db: Session = Depends(get_db)):
    items, total = disciplinary_master_crud.get_all_incidents(db)
    return {"items": items, "total": total}
 
# 3. GET Incident BY ID
@router.get("/{id}", response_model=DisciplinaryIncidentResponse)
def get_incident(id: int, db: Session = Depends(get_db)):
    db_incident = disciplinary_master_crud.get_incident_by_id(db, incident_id=id)
    if not db_incident:
        raise HTTPException(status_code=404, detail="Disciplinary Incident not found")
    return db_incident
 
# 4. DELETE Incident
@router.delete("/{id}")
def delete_incident_endpoint(id: int, db: Session = Depends(get_db)):
    success = disciplinary_master_crud.delete_incident(db, incident_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Disciplinary Incident not found")
    return {"message": "Disciplinary Incident deleted successfully"}

#get disciplinary by userid
@router.get("/get-by-user-disciplinary/{user_id}", summary="get disciplinary by userid for employee")
def get_by_user_disciplinary(user_id: int, db: Session = Depends(get_db)):
    return disciplinary_master_crud.get_by_user_disciplinary_incident(db, user_id=user_id)

# @router.put("/acknowledge-disciplinary/{disciplinary_id}/{user_id}")
# def acknowledge_disciplinary(
#     disciplinary_id: int,
#     payload: AcknowledgeDisciplinaryRequest,
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     return disciplinary_master_crud.acknowledge_hr_disciplinary(db, disciplinary_id, user_id, payload.dict())
@router.put("/acknowledge-disciplinary/{disciplinary_id}/{user_id}")
def acknowledge_disciplinary(
    disciplinary_id: int,
    payload: AcknowledgeDisciplinaryRequest,
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    result = disciplinary_master_crud.acknowledge_hr_disciplinary(db, disciplinary_id, user_id, payload.dict())
   
    if result.get("status"):
        background_tasks.add_task(
            hr_action_notification_crud.send_hr_acknowledgement_notification,
            db,
            user_id=user_id,
            action_id=disciplinary_id,
            background_tasks=background_tasks,
            module_type="DISCIPLINARY"
        )
       
    return result

@router.post("/employee-activity-filter-disciplinary/{user_id}")
def employee_activity_filter_disciplinary(
    request: CommonFilterRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    return disciplinary_master_crud.get_employee_activity_disciplinary(db, request, user_id)