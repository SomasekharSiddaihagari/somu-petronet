from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import shutil

from app.crud.hr_action_tracker.performance_master_crud import get_appraisal_dashboard, get_performance_by_user, get_performance_by_id, get_performance_list_filter, save_employee_performance, create_document, delete_performance, get_distinct_appraisal_years
from app.database import get_db
from app.schemas.hr_action_tracker.performance_master_schema import EmployeeAppraisalItem


router = APIRouter(
    prefix="/performance-master",
    tags=["Performance Master"]
)

@router.post("/save-appraisal/{login_user_id}")
def save_appraisal(
    login_user_id: int,
    user_id: int = Form(...),
    appraisal_start_date: str = Form(...),
    appraisal_end_date: str = Form(...),
    annual_appraisal_rating: Optional[str] = Form(None),
    annual_rating_score: Optional[str] = Form(None),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    
):
    try:
        # Convert strings to datetime
        start_dt = datetime.fromisoformat(appraisal_start_date.replace("Z", "+00:00")) if appraisal_start_date != "string" else None
        end_dt = datetime.fromisoformat(appraisal_end_date.replace("Z", "+00:00")) if appraisal_end_date != "string" else None

        item = EmployeeAppraisalItem(
            user_id=user_id,
            appraisal_start_date=start_dt,
            appraisal_end_date=end_dt,
            annual_appraisal_rating=annual_appraisal_rating,
            annual_rating_score=annual_rating_score
        )
        
        # save_employee_performance takes a list, so we pass [item]
        result = save_employee_performance(db, [item], login_user_id)
        
        # We need the performance_id to link files. 
        # Since it's an update/insert, let's fetch the ID
        from sqlalchemy import text
        # perf_id_query = text("SELECT performance_id FROM employee_performance WHERE user_id = :uid")
        # performance_id = db.execute(perf_id_query, {"uid": user_id}).scalar()

        perf_id_query = text("""
            SELECT performance_id FROM employee_performance 
            WHERE user_id = :uid 
            AND appraisal_start_date = :start_dt 
            AND appraisal_end_date = :end_dt
        """)
        performance_id = db.execute(perf_id_query, {
            "uid": user_id,
            "start_dt": start_dt,
            "end_dt": end_dt
        }).scalar()

        if files and performance_id:
            UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "performance")
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)

            for file in files:
                if file.filename:
                    unique_filename = f"{performance_id}_{int(datetime.now().timestamp())}_{file.filename}"
                    file_path = os.path.join(UPLOAD_DIR, unique_filename)

                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    relative_path = os.path.join("uploads", "performance", unique_filename)
                    create_document(db, performance_id, file.filename, relative_path)

        return {
            "status": True,
            "message": "Appraisal saved successfully",
            "performance_id": performance_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/get-appraisal-dashboard")
def get_appraisal_dashboard_router(
    year: Optional[str] = Query(None, description="Appraisal year range e.g. 2025-2026"),
    db: Session = Depends(get_db)
):
    return get_appraisal_dashboard(db, year)
 
@router.get("/get-appraisal-years")
def get_years(db: Session = Depends(get_db)):
    return get_distinct_appraisal_years(db)


@router.get("/get-performance/{user_id}")
def get_performance(
    user_id: int,
    db: Session = Depends(get_db)
):
    result = get_performance_by_user(db, user_id)

    # if not result:
    #     raise HTTPException(status_code=404, detail="No data found")

    return result

@router.get("/get-performance-by-id/{performance_id}")
def get_performance_id(
    performance_id: int,
    db: Session = Depends(get_db)
):
    result = get_performance_by_id(db, performance_id)

    if not result:
        raise HTTPException(status_code=404, detail="No data found for this performance ID")

    return result

@router.get("/performance-list")
def get_performance_list(
    year: str = None,   # format: "2008-2009"
    db: Session = Depends(get_db)
):
    return get_performance_list_filter(db, year)

@router.delete("/{performance_id}")
def delete_performance_endpoint(performance_id: int, db: Session = Depends(get_db)):
    success = delete_performance(db, performance_id=performance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Performance record not found")
    return {"message": "Performance record deleted successfully"}