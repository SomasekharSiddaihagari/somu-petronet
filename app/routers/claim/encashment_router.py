
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.crud.claim.claim_notifications_crud import handle_claim_notification
from app.database import get_db
from app.schemas.claim.encashment_schemas import (
    EncashmentMainCreate,
    EncashmentMainUpdate,
    EncashmentMainResponse,
    LeaveEncashmentCreate,
    LeaveEncashmentUpdate,
    LeaveEncashmentResponse,
)
from app.crud.claim.encashment_crud import (
    create_encashment_main,
    update_encashment_main,
    create_leave_encashment,
    update_leave_encashment,
)

router = APIRouter(prefix="/api/encashment", tags=["Encashment"])


# =================================================
# ENCASHMENT MAIN
# =================================================
@router.post("/claim/create", response_model=EncashmentMainResponse)
def create_encashment(
    data: EncashmentMainCreate,
    db: Session = Depends(get_db)
):
    encashment_id = create_encashment_main(db, data)
    return db.execute(
        text("SELECT * FROM encashment_main WHERE encashment_main_id = :id"),
        {"id": encashment_id},
    ).mappings().first()


@router.put("/claim/update/{encashment_main_id}", response_model=EncashmentMainResponse)
def update_encashment(
    encashment_main_id: int,
    data: EncashmentMainUpdate,
    db: Session = Depends(get_db)
):
    if not update_encashment_main(db, encashment_main_id, data):
        raise HTTPException(status_code=404, detail="Encashment not found")

    return db.execute(
        text("SELECT * FROM encashment_main WHERE encashment_main_id = :id"),
        {"id": encashment_main_id},
    ).mappings().first()


# =================================================
# LEAVE ENCASHMENT SUBMISSION
# =================================================
# @router.post("/submission/create", response_model=LeaveEncashmentResponse)
# def create_leave_encashment_api(
#     data: LeaveEncashmentCreate,
#     db: Session = Depends(get_db)
# ):
#     leave_id = create_leave_encashment(db, data)
#     return db.execute(
#         text("SELECT * FROM leave_encashment WHERE leave_encashment_id = :id"),
#         {"id": leave_id},
#     ).mappings().first()


# @router.put("/submission/update/{leave_encashment_id}", response_model=LeaveEncashmentResponse)
# def update_leave_encashment_api(
#     leave_encashment_id: int,
#     data: LeaveEncashmentUpdate,
#     db: Session = Depends(get_db)
# ):
#     if not update_leave_encashment(db, leave_encashment_id, data):
#         raise HTTPException(status_code=404, detail="Leave encashment not found")

#     return db.execute(
#         text("SELECT * FROM leave_encashment WHERE leave_encashment_id = :id"),
#         {"id": leave_encashment_id},
#     ).mappings().first()

@router.post("/submission/create", response_model=LeaveEncashmentResponse)
async def create_leave_encashment_api(
    data: LeaveEncashmentCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    leave_id = create_leave_encashment(db, data)

    encashment = db.execute(
        text("SELECT * FROM leave_encashment WHERE leave_encashment_id = :id"),
        {"id": leave_id},
    ).mappings().first()

    # 🔔 FIRST NOTIFICATION
    if encashment and encashment["status"] == "Pending Supervisor Approval":

        class DummySheet:
            def __init__(self, row):
                self.status = row["status"]
                self.user_id = row["created_by"]
                self.requisition_number = row["encashment_ref_id"]
                self.employee_name = row["employee_name"]
                self.employee_code = row["employee_code"]
                self.leave_type = row["leave_type"]
                self.encashment_date = row["encashment_date"]
                self.el_encashable = row["el_encashable"]
                self.encash_el = row["encash_el"]
                self.balance_as_on_date = row["balance_as_on_date"]
                self.amount_claimed = row["amount_claimed"]
                self.no_days_approved=row["no_days_approved"]
                self.request_text = row["request_text"]
                self.encashment_opening = row["encashment_opening"]
                self.non_encashment_opening = row["non_encashment_opening"]
                self.total_encashment_opening = row["total_encashment_opening"]

        sheet = DummySheet(encashment)

        await handle_claim_notification(
            db=db,
            module_key="encashment",
            sheet=sheet,
            background_tasks=background_tasks
        )

    return encashment

@router.put("/submission/update/{leave_encashment_id}", response_model=LeaveEncashmentResponse)
async def update_leave_encashment_api(
    leave_encashment_id: int,
    data: LeaveEncashmentUpdate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    if not update_leave_encashment(db, leave_encashment_id, data):
        raise HTTPException(status_code=404, detail="Leave encashment not found")

    encashment = db.execute(
        text("SELECT * FROM leave_encashment WHERE leave_encashment_id = :id"),
        {"id": leave_encashment_id},
    ).mappings().first()

    if encashment and encashment["status"]:

        class DummySheet:
            def __init__(self, row):
                self.status = row["status"]
                self.user_id = row["created_by"]

                # ✅ Use correct reference
                self.requisition_number = row["encashment_ref_id"]

                # ✅ Encashment-specific fields
                self.employee_name = row.get("employee_name")
                self.employee_code = row.get("employee_code")
                self.leave_type = row.get("leave_type")
                self.encashment_date = row.get("encashment_date")

                self.el_encashable = row.get("el_encashable")
                self.encash_el = row.get("encash_el")
                self.balance_as_on_date = row.get("balance_as_on_date")
                self.encashment_opening = row.get("encashment_opening")
                self.non_encashment_opening = row.get("non_encashment_opening")
                self.total_encashment_opening = row.get("total_encashment_opening")

                self.request_text = row.get("request_text")

                # ✅ Approval trail
                self.updated_by_supervisor = row.get("updated_by_supervisor")
                self.updated_by_supervisor_name = row.get("updated_by_supervisor_name")

                self.updated_by_hr = row.get("updated_by_hr")
                self.updated_by_hr_name = row.get("updated_by_hr_name")

                self.updated_by_finance = row.get("updated_by_finance")
                self.updated_by_finance_name = row.get("updated_by_finance_name")
                self.supervisor_comment = row.get("supervisor_comment")
                self.hr_comment = row.get("hr_comment")
                self.finance_comment = row.get("finance_comment")


        sheet = DummySheet(encashment)

        await handle_claim_notification(
            db=db,
            module_key="encashment",
            sheet=sheet,
            background_tasks=background_tasks
        )

    return encashment



