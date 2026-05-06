from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.travel_expense.travel_requisition_notification_crud import notify_on_travel_approved, notify_on_travel_create, notify_on_travel_rejected
from app.database import get_db
from app.schemas.travel_expense.travel_requisition_schema import (
    TravelRequisitionCreate,
    TravelRequisitionFullResponse,
    TravelRequisitionUpdate,
    TravelRequisitionResponse,
)
from app.crud.travel_expense.travel_requisition_crud import (
    create_travel_requisition,
    get_travel_requisition_full,
    update_travel_requisition
)

router = APIRouter(prefix="/api/travel-requisition", tags=["Travel Requisition"])


# ---------------------- POST API --------------------------
@router.post("/create", response_model=TravelRequisitionResponse)
async def create_travel_req(
    data: TravelRequisitionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    travel = create_travel_requisition(db, data)

    await notify_on_travel_create(
        db=db,
        travel=travel, # type: ignore
        background_tasks=background_tasks
    )

    return travel

# ---------------------- PUT API --------------------------
@router.put("/update/{travel_id}", response_model=TravelRequisitionResponse)
async def update_travel_req(
    travel_id: int,
    data: TravelRequisitionUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    travel = update_travel_requisition(db, travel_id, data)
    if not travel:
        raise HTTPException(status_code=404, detail="Travel Requisition not found")

    status = travel.get("status")
    updated_by = getattr(data, "updated_by", None)

    # ✅ Supervisor Approved
    if status == "Travel Claim Pending":
        await notify_on_travel_approved(
            db=db,
            travel=travel,
            approved_by=updated_by or "System",
            background_tasks=background_tasks
        )

    # ❌ Supervisor Rejected
    elif status == "Travel Requisition Rejected":
        await notify_on_travel_rejected(
            db=db,
            travel=travel,
            rejected_by=updated_by or "System",
            background_tasks=background_tasks
        )

    return travel

@router.get("/{travel_id}", response_model=TravelRequisitionFullResponse)
def get_full_requisition(travel_id: int, db: Session = Depends(get_db)):

    data = get_travel_requisition_full(db, travel_id)

    if not data:
        raise HTTPException(status_code=404, detail="Requisition not found")

    return data