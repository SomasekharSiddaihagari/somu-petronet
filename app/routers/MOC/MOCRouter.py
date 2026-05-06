from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.MOC.MOCSchema import (
    MOCRequest,
    MOCStatusCountRequest,
    MOCRequestDetail,
    MOCStatusCountRequestStation,
   
    UpdateMOCRequest,
    EngineerListResponse
)
from app.crud.MOC.MOCCrud import (
    get_all_station_summary,
    get_hira_approved_model,
    get_moc_status_summary_by_station,
    get_moc_status_summary_by_user,
    get_sic_approved_model,
    get_submitted_model,
    insert_moc_request_service,
    get_moc_request_by_no,
    update_moc_request_service,
    get_all_engineer_details,
    get_moc_requests_by_user
)
from app.database import get_db
from app.utils.UserAuthUtils import verify_access_token
from app.crud.NotificationCrud import handle_moc_create_notifications


router = APIRouter(prefix="/api/MOC", tags=["MOC"])


@router.post("/CreateMocRequest")
def create_moc_request(
    request: MOCRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_access_token)
):
    try:
        username = current_user.get("username") if isinstance(current_user, dict) else current_user
        request.updated_by = username
        result = insert_moc_request_service(db, request)
        background_tasks.add_task(handle_moc_create_notifications, db, request, result, background_tasks)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#  UPDATE MOC REQUEST

@router.put("/UpdateMocRequest", summary="Update MOC Request")
async def update_moc_request(
    request: UpdateMOCRequest,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None,
   current_user: str = Depends(verify_access_token)
):
    try:
        #  Your stored procedure call
        result = update_moc_request_service(db, request)

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        #  NEW: trigger workflow notifications
        from app.crud.NotificationCrud import handle_moc_status_notifications
        await handle_moc_status_notifications(
            db=db,
            request=request,
            updated_by=current_user,
            background_tasks=background_tasks
        )

        return {"status": "success", "data": result["message"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







#  GET MOC REQUEST BY NUMBER
@router.get(
    "/GetMocRequest",
    response_model=MOCRequestDetail,
    summary="Get MOC Request Details by Request Number",
)
def fetch_moc_request_by_no(
    moc_request_no: str = Query(..., description="MOC Request Number (e.g., Moc/MLR/2025-26/001)"),
    db: Session = Depends(get_db),background_tasks: BackgroundTasks = None,
#    current_user: str = Depends(verify_access_token)
):
    """
    Fetches a single MOC Request record by its request number.
    Returns 404 if no matching record is found.
    """
    moc_data = get_moc_request_by_no(db, moc_request_no)

    if moc_data is None:
        raise HTTPException(status_code=404, detail="No MOC Request found for this number.")

    return moc_data



#  GET TOTAL STATUS COUNT
@router.get("/TotalCount")
def get_moc_summary(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_access_token)
    ):
    req = MOCStatusCountRequest(user_id=user_id)
    data = get_moc_status_summary_by_user(db, req)
    return {"data": data}

@router.get("/Total/Summary_By_Station")
def get_moc_summary(
    station_name: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_access_token)
    ):
    req = MOCStatusCountRequestStation(station_name=station_name)
    data = get_moc_status_summary_by_station(db, req)
    return {"data": data}

@router.get("/TotalStationSummary")
def get_moc_summary(
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_access_token)
):
    
    data = get_all_station_summary(db)
    return {"data": data}

#  GET SIC APPROVED MOCS
@router.get("/SICApproved")
def get_sic_approved(
    db: Session = Depends(get_db),
    # current_user: str = Depends(verify_access_token)
    ):
    data = get_sic_approved_model(db)
    return {"data": data}



#  GET HIRA APPROVED MOCS
@router.get("/HiraApproved")
def get_hira_approved(
    db: Session = Depends(get_db),
    # current_user: str = Depends(verify_access_token)
):
    data = get_hira_approved_model(db)
    return {"data": data}



#  GET ALL SUBMITTED MOCS
@router.get("/GetAllSubmitted")
def get_submitted(
    db: Session = Depends(get_db),
    # current_user: str = Depends(verify_access_token)
):
    data = get_submitted_model(db)
    return {"data": data}

from sqlalchemy import text as sql_text



@router.get("/GetALlEngineersDD")
def fetch_all_engineers(
    user_id: int,
    db: Session = Depends(get_db),
    # current_user: str = Depends(verify_access_token)
):
    try:
        query = sql_text("""
            SELECT DISTINCT
                u.user_id,
                u.username,
                u.first_name,
                u.last_name,
                u.email,
                u.contact_phone,
                r.role_name
            FROM users u
            INNER JOIN role_permissions rp ON rp.user_id = u.user_id
            INNER JOIN roles r ON r.role_id = rp.role_id
            WHERE rp.submenu_id = :submenu_id
              AND rp.role_id = :role_id
              AND u.station_id = (
                  SELECT station_id
                  FROM users
                  WHERE user_id = :current_user_id
              )
        """)

        result = db.execute(
            query,
            {
                "submenu_id": 2,
                "role_id": 1,
                "current_user_id": user_id
            }
        ).fetchall()

        data = [
            {
                "user_id": row.user_id,
                "username": row.username,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "email": row.email,
                "contact_phone": row.contact_phone,
                "role_name": row.role_name
            }
            for row in result
        ]

        return {
            "statusCode": "0000",
            "statusMessage": "Success",
            "data": data
        }

    except Exception as e:
        print("ENGINEER DD ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail={
                "statusCode": "9999",
                "statusMessage": str(e),
                "data": []
            }
        )




#  GET MOC REQUESTS BY USER
@router.get("/GetByUser/{user_id}")
def get_moc_requests_by_user_router(
    user_id: int,
    db: Session = Depends(get_db),
    # current_user: str = Depends(verify_access_token)
):
    """
    Fetch all MOC Requests for a given user.
    Admins see all requests; others see only their station's.
    """
    data = get_moc_requests_by_user(db, user_id)
    return {"data": data}

