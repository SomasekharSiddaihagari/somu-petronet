from pydoc import text
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session
from app.crud.circular_management.circular_notification_crud import notify_circular_target_audience, notify_pending_acknowledgement_users, notify_users_for_circular_update
from app.database import get_db
from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
import json

from app.models.circular_mangement.circular_model import CircularMaster
from app.schemas.circular_management.circular_master_schema import (
    CircularCreate,
    CircularUpdate
)
from app.crud.circular_management.circular_master_crud import (
    create_circular,
    update_circular,
    get_circular,
    get_all_circulars,
    get_circular_dashboard_counts_crud,
    delete_circular,
    get_all_archived_circulars,
    archived_circular,
    getall_version_history,
    get_employee_circulars,
    get_circular_dashboard_counts
)

router = APIRouter(prefix="/circular", tags=["Circular Master"])

# ---------------- Create Circular ----------------
@router.post("/create", summary="Create Circular with Files & Target Audience")
async def create_circular_api(
    title: str = Form(...),
    category_id: int = Form(...),
    # subcategory_id: int = Form(...),
    subcategory_id: int | None = Form(None),
    content: str = Form(...),
    change_type: str = Form(...),
    mandatory_status: bool = Form(...),
    status: str = Form(...),
    created_by: int = Form(...),
    tags: str = Form(...),
    target_audience: str = Form(...),
    files: list[UploadFile] = File([]),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):    
    # parse target_audience
    try:
        target_audience_list = json.loads(target_audience)
        if not isinstance(target_audience_list, list):
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail='target_audience must be a JSON array of objects')

    result = create_circular(
        db=db,
        payload={
            "title": title,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "content": content,
            "change_type": change_type,
            "mandatory_status": mandatory_status,
            "status": status,
            "created_by": created_by,
            "tags": tags
        },
        target_audience=target_audience_list,
        files=files
    )

    await notify_circular_target_audience(
            db=db,
            target_audience=target_audience_list,
            circular_title=title,
            created_by_user_id=created_by,
            background_tasks=background_tasks
    )

    return result


# ---------------- Update Circular ----------------
@router.put("/update/{circular_id}", summary="Update Circular with Files & Target Audience")
async def update_circular_api(
    circular_id: int,
    title: str = Form(None),
    category_id: int = Form(None),
    subcategory_id: int | None = Form(None),
    content: str = Form(None),
    change_type: str = Form(None),
    mandatory_status: bool = Form(None),
    status: str = Form(None),
    is_archived: bool = Form(None),
    updated_by: int = Form(...),
    tags: str = Form(None),
    target_audience: str = Form(None),
    removed_user: str = Form(None),
    files: list[UploadFile] = File([]),
    reason: str | None = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    
    # ---------- Parse target_audience ----------
    target_audience_list = []
    if target_audience:
        try:
            target_audience_list = json.loads(target_audience)
            if not isinstance(target_audience_list, list):
                raise ValueError
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="target_audience must be a JSON array of objects"
            )
        
    removed_users_list = []
    if removed_user:
        try:
            removed_users_list = json.loads(removed_user)
            if not isinstance(removed_users_list, list):
                raise ValueError
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="removed_user must be a JSON array"
            )
    
    for ta in target_audience_list:
        ta["removed_users"] = removed_users_list
        if "audience_ref_id" in ta and removed_users_list:
            ta["audience_ref_id"] = list(
            set(ta["audience_ref_id"]) - set(removed_users_list)
        )

    # ---------- Call CRUD ----------
    updated_circular = update_circular(
        db=db,
        circular_id=circular_id,
        payload={
            "title": title,
            "category_id": category_id,
            "subcategory_id": None if not subcategory_id else int(subcategory_id),
            "content": content,
            "change_type": change_type,
            "mandatory_status": mandatory_status,
            "status": status,
            "is_archived": is_archived,
            "updated_by": updated_by,
            "tags": tags,
            "reason": reason
        },
        target_audience=target_audience_list,
        files=files
    )
    
    if not updated_circular:
        raise HTTPException(status_code=404, detail="Circular not found")

    await notify_users_for_circular_update(
    db=db,
    circular_id=circular_id,
    target_audience=target_audience_list,
    circular_title=title,
    change_type=change_type,
    updated_by_user_id=updated_by,
    background_tasks=background_tasks
)

    return updated_circular


@router.get("/get/{circular_id}")
def get(circular_id: int, version: str, db: Session = Depends(get_db)):
    result = get_circular(db, circular_id, version)
    return {
        "status": "success",
        "data": result
    }

@router.get("/get-all/{user_id}", summary="Get All My Published")
def get_all(
        user_id: int,
        db: Session = Depends(get_db)
    ):
    result = get_all_circulars(db,user_id)
    return {
        "status": "success",
        "data": result
    }

@router.get("/dashboard-count/{user_id}", summary="Dashboard circular counts")
def get_circular_dashboard_counts_api(
    user_id: int,
    db: Session = Depends(get_db)
):
    result = get_circular_dashboard_counts_crud(db, user_id)
    return {
        "status": "success",
        "data": result
    }

@router.delete("/delete/{circular_id}")
def delete(circular_id: int, db: Session = Depends(get_db)):
    delete_circular(db, circular_id)
    return {
        "status": "success",
        "message": "Circular deleted successfully"
    }


@router.get("/get-all-archived/{user_id}", summary="Get All Archived Circular Admin / Publisher")
def get_all(
        user_id: int,
        db: Session = Depends(get_db)
    ):
    result = get_all_archived_circulars(db,user_id)
    return {
        "status": "success",
        "data": result
    }

@router.put("/archived/{circular_id}")
def put(
        circular_id: int, 
        status: bool,  
        db: Session = Depends(get_db)
        ):
    archived_circular(db, circular_id,status)
    return {
        "status": "success",
        "message": "Circular archive status changed successfully"
    }

@router.get("/get_version_history/{circular_id}/{version}")
def get(circular_id: int, version: str, db: Session = Depends(get_db)):
    result = getall_version_history(db, circular_id, version)
    return {
        "status": "success",
        "data": result
    }


#----------------
@router.get("/circulars", summary="Fetch All Circulars Admin / Publisher / Employee")
def fetch_employee_circulars(
    user_id: int = Query(..., description="Logged-in User ID"),
    db: Session = Depends(get_db)
):
    rows = get_employee_circulars(db, user_id)

    return {
        "status": "success",
        "message": "Circulars fetched successfully",
        "count": len(rows),
        "data": [
            {
                "circular_id": row.circular_id,
                "title": row.title,
                "document_no": row.document_no,
                "content":row.content,
                "category_id":row.category_id,
                 "category_name": row.category_name,
                "subcategory_id":row.subcategory_id,
                "subcategory_name": row.subcategory_name,
                "mandatory_status":row.mandatory_status,
                "status":row.status,
                "version":row.version,
                "published_date":row.published_date,
                "publisher_name":row.publisher_name,
                "created_by":row.created_by,
                "updated_date":row.updated_date,
                "tags":row.tags,
                "is_read":row.is_read,
                "is_acknowledged":row.is_acknowledged
            }
            for row in rows
        ]
    }


@router.get("/circulars/dashboard-counts")
def fetch_circular_dashboard_counts(
    user_id: int = Query(..., description="Logged-in User ID"),
    db: Session = Depends(get_db)
):
    counts = get_circular_dashboard_counts(db, user_id)

    return {
        "status": "success",
        "message": "Dashboard counts fetched successfully",
        "data": counts
    }

@router.post("/send-ack-reminder/{circular_id}/{login_user_id}", summary="Send Acknowledgement Reminder")
async def send_acknowledgement_reminder(
    circular_id: int,
    login_user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Get circular details
    circular = db.query(CircularMaster).filter(
        CircularMaster.circular_id == circular_id
    ).first()

    if not circular:
        raise HTTPException(status_code=404, detail="Circular not found")

    # Call reminder function
    await notify_pending_acknowledgement_users(
        db=db,
        circular_id=circular.circular_id,
        circular_title=circular.title,
        change_type=circular.change_type,
        login_user_id=login_user_id,
        background_tasks=background_tasks
    )

    return {"message": "Reminder sent successfully"}