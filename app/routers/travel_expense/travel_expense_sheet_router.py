# from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.crud.travel_expense.travel_expense_notification_crud import notify_next_tc_approver, notify_supervisor_on_tc_create, notify_tc_approved, notify_tc_rejected, notify_tc_send_back, send_travel_expense_notification 
# from app.database import get_db

# from app.models.RolePermissionModel import RolePermission
# from app.models.UserModel import User
# from app.models.travel_expense.travel_expense_sheet import TravelExpenseSheet
# from app.schemas.travel_expense.travel_expense_schema import (
#     TravelExpenseSheetCreate,
#     TravelExpenseSheetUpdate,
# )

# from app.crud.travel_expense.travel_expense_sheet_crud import (
#     create_travel_expense_sheet,
#     update_travel_expense_sheet,
# )

# router = APIRouter(prefix="/api/expense-sheet", tags=["Travel Expense Sheet"])


# # -------------------------------
# # POST → Create + history insert
# # -------------------------------
# @router.post("/create")
# async def create_expense_sheet(
#     data: TravelExpenseSheetCreate,
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db)
# ):
    

#     sheet = create_travel_expense_sheet(db, data)

    


#     await notify_supervisor_on_tc_create(
#         db=db,
#         sheet=sheet,
#         background_tasks=background_tasks
#     )


#     return sheet

# # -------------------------------
# # PUT → Update only main table
# # -------------------------------
# # @router.put("/update/{tes_id}")
# # async def update_expense_sheet(
# #     tes_id: int,
# #     data: TravelExpenseSheetUpdate,
# #     background_tasks: BackgroundTasks,
# #     db: Session = Depends(get_db)
# # ):
   

# #     sheet = update_travel_expense_sheet(db, tes_id, data)
# #     if not sheet:
    
# #         raise HTTPException(status_code=404, detail="Travel Expense Sheet not found")



# #     role_name = getattr(data, "role_name", None)
# #     action_type = getattr(data, "action_type", None)
# #     acted_by = getattr(data, "acted_by_username", "System")



# #     # ================================
# #     # APPROVE FLOW
# #     # ================================
# #     if action_type == "approve":
      

# #         await notify_next_tc_approver(
# #             db=db,
# #             sheet=sheet,
# #             role_name=role_name,
# #             acted_by_username=acted_by,
# #             background_tasks=background_tasks
# #         )

  

# #     # ================================
# #     # REJECT FLOW
# #     # ================================
# #     elif action_type == "reject":
       

# #         await notify_tc_rejected(
# #             db=db,
# #             sheet=sheet,
# #             rejected_by_role=role_name,
# #             rejected_by_username=acted_by,
# #             background_tasks=background_tasks
# #         )

# #     # ================================
# #     # SEND BACK FLOW
# #     # ================================
# #     elif action_type == "send_back":
   

# #         await notify_tc_send_back(
# #             db=db,
# #             sheet=sheet,
# #             role_name=role_name,
# #             acted_by_username=acted_by,
# #             background_tasks=background_tasks
# #         )

# #         print("✅ [TC UPDATE] Send-back notification sent")

# #     else:
# #         print("⚠️ [TC UPDATE] No notification action taken")

# #     return sheet

# # @router.put("/update/{tes_id}")
# # async def update_expense_sheet(
# #     tes_id: int,
# #     data: TravelExpenseSheetUpdate,
# #     background_tasks: BackgroundTasks,
# #     db: Session = Depends(get_db)
# # ):
# #     sheet = update_travel_expense_sheet(db, tes_id, data)
# #     if not sheet:
# #         raise HTTPException(status_code=404, detail="Travel Expense Sheet not found")

# #     status = (data.status or "").strip()
# #     status_lower = status.lower()

# #     print("🔍 [TC STATUS RECEIVED]:", status)

# #     # ======================================================
# #     # DERIVE ACTED BY USER FROM STATUS
# #     # ======================================================
# #     acted_by = "System"

# #     if status_lower.endswith("- supervisor"):
# #         acted_by = data.updated_by_supervisor_name or "Supervisor"
# #     elif status_lower.endswith("- hr"):
# #         acted_by = data.updated_by_hr_name or "HR"
# #     elif status_lower.endswith("- md"):
# #         acted_by = data.updated_by_md_name or "MD"
# #     elif status_lower.endswith("- finance"):
# #         acted_by = data.updated_by_finance_name or "Finance"

# #     # ======================================================
# #     # STATUS → CURRENT ROLE MAPPING
# #     # ======================================================

# #     # Supervisor approved → HR pending
# #     if status_lower == "tc pending - hr":
# #         print("➡️ Supervisor approved → Notify HR")

# #         await notify_next_tc_approver(
# #             db=db,
# #             sheet=sheet,
# #             role_name="Supervisor",
# #             acted_by_username=acted_by,
# #             background_tasks=background_tasks
# #         )

# #         print("✅ HR notification sent")

# #     # HR approved → MD pending
# #     elif status_lower == "tc pending - md":
# #         print("➡️ HR approved → Notify MD")

# #         await notify_next_tc_approver(
# #             db=db,
# #             sheet=sheet,
# #             role_name="HR",
# #             acted_by_username=acted_by,
# #             background_tasks=background_tasks
# #         )

# #         print("✅ MD notification sent")

# #     # MD approved → Finance pending
# #     elif status_lower == "tc pending - finance":
# #         print("➡️ MD approved → Notify Finance")

# #         await notify_next_tc_approver(
# #             db=db,
# #             sheet=sheet,
# #             role_name="MD",
# #             acted_by_username=acted_by,
# #             background_tasks=background_tasks
# #         )

# #         print("✅ Finance notification sent")

# #     # Finance approved → Final approval
# #     elif status_lower == "travel claim approved":
# #         print("🎉 Finance approved → Notify Employee")

# #         await notify_tc_approved(
# #             db=db,
# #             sheet=sheet,
# #             approved_by=acted_by,
# #             background_tasks=background_tasks
# #         )

# #         print("✅ Employee notified")

# #     # Rejection (any level)
# #     elif "rejected" in status_lower:
# #         print("❌ Claim rejected")

# #         await notify_tc_rejected(
# #             db=db,
# #             sheet=sheet,
# #             rejected_by_role="System",
# #             rejected_by_username=acted_by,
# #             background_tasks=background_tasks
# #         )

# #         print("❌ Rejection notification sent")

# #     # Send back (role specific)
# #     elif status_lower.startswith("tc changes request"):
# #         print("↩️ Claim sent back")

# #         # Extract role from status
# #         role_name = status.replace("TC Changes Request -", "").strip()

# #         await notify_tc_send_back(
# #             db=db,
# #             sheet=sheet,
# #             role_name=role_name,
# #             acted_by_username=acted_by,
# #             background_tasks=background_tasks
# #         )

# #         print("↩️ Send-back notification sent")

# #     return sheet


# @router.put("/update/{tes_id}")
# async def update_expense_sheet(
#     tes_id: int,
#     data: TravelExpenseSheetUpdate,
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db)
# ):
#     # --------------------------------------
#     # Update sheet
#     # --------------------------------------
#     update_travel_expense_sheet(db, tes_id, data)

#     # 🔥 FORCE FULL ORM LOAD
#     sheet = db.query(TravelExpenseSheet).filter(
#         TravelExpenseSheet.tes_id == tes_id
#     ).first()

#     if not sheet:
#         raise HTTPException(status_code=404, detail="Travel Expense Sheet not found")

#     status = (sheet.status or "").strip()
#     status_lower = status.lower()

#     print("🔍 [TC STATUS RECEIVED]:", status)
#     print("🧪 sheet.user_id =", sheet.user_id)

#     # --------------------------------------
#     # Determine actor username
#     # --------------------------------------
#     # --------------------------------------
#     # Determine actor ROLE (CRITICAL FIX)
#     # --------------------------------------
#     acted_by = "system"

#     if sheet.updated_by_finance_name:
#         acted_by = "finance"
#     elif sheet.updated_by_md_name:
#         acted_by = "md"
#     elif sheet.updated_by_hr_name:
#         acted_by = "hr"
#     elif sheet.updated_by_head_tech_name:
#         acted_by = "head_tech"
#     elif sheet.updated_by_supervisor_name:
#         acted_by = "supervisor"

#     print("🧑 Action performed by:", acted_by)


#     # ======================================================
#     # 1️⃣ USER SUBMISSION / RE-SUBMISSION → SUPERVISOR
#     # ======================================================
#     if status_lower == "tc pending - supervisor":
#         print("➡️ User submitted → Notify Supervisor")

#         # 1️⃣ Notify Supervisor
#         await notify_supervisor_on_tc_create(
#             db=db,
#             sheet=sheet,
#             background_tasks=background_tasks
#         )

#         # 2️⃣ Notify USER (confirmation)
#         await send_travel_expense_notification(
#             db=db,
#             title="Travel Expense Submitted",
#             description="Your travel expense claim has been submitted successfully and sent to your supervisor for approval.",
#             from_user=sheet.employee_name or "system",
#             to_user=db.query(User).filter(User.user_id == sheet.user_id).first().username,
#             module_status="TC Pending - Supervisor",
#             background_tasks=background_tasks
#         )

#         print("✅ Supervisor + User notified")

#         return sheet


#     # ======================================================
#     # 2️⃣ SEND BACK (Supervisor / HR / MD / Finance)
#     # ======================================================
#     if status_lower.startswith("tc changes request"):
#         role_name = status.replace("TC Changes Request -", "").strip()

#         print("↩️ Claim sent back by:", role_name)

#         await notify_tc_send_back(
#             db=db,
#             sheet=sheet,
#             role_name=role_name,
#             acted_by_username=acted_by,
#             background_tasks=background_tasks
#         )

#         print("↩️ Send-back notifications sent")
#         return sheet

#     # ======================================================
#     # 3️⃣ APPROVAL FLOW
#     # ======================================================
#     if status_lower == "tc pending - hr":
#         await notify_next_tc_approver(
#             db=db,
#             sheet=sheet,
#             role_name="Supervisor",
#             acted_by_username=acted_by,
#             background_tasks=background_tasks
#         )

#     elif status_lower == "tc pending - md":
#         await notify_next_tc_approver(
#             db=db,
#             sheet=sheet,
#             role_name="HR",
#             acted_by_username=acted_by,
#             background_tasks=background_tasks
#         )

#     elif status_lower == "tc pending - finance":
#         await notify_next_tc_approver(
#             db=db,
#             sheet=sheet,
#             role_name="MD",
#             acted_by_username=acted_by,
#             background_tasks=background_tasks
#         )

#     # ======================================================
#     # 4️⃣ FINAL APPROVAL
#     # ======================================================
#     elif status_lower == "travel claim approved":
#         await notify_tc_approved(
#             db=db,
#             sheet=sheet,
#             approved_by=acted_by,
#             background_tasks=background_tasks
#         )

#     # ======================================================
#     # 5️⃣ REJECTION
#     # ======================================================
#     elif "rejected" in status_lower:
#         await notify_tc_rejected(
#             db=db,
#             sheet=sheet,
#             rejected_by_role="System",
#             rejected_by_username=acted_by,
#             background_tasks=background_tasks
#         )

#     return {
#     "tes_id": sheet.tes_id,
#     "user_id": sheet.user_id,
#     "status": sheet.status,
#     "updated_at": sheet.updated_at
# }





from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models.UserModel import User
from app.models.travel_expense.travel_expense_sheet import TravelExpenseSheet

from app.schemas.travel_expense.travel_expense_schema import (
    TravelExpenseSheetCreate,
    TravelExpenseSheetUpdate,
)

from app.crud.travel_expense.travel_expense_sheet_crud import (
    create_travel_expense_sheet,
    update_travel_expense_sheet,
)

from app.crud.travel_expense.travel_expense_notification_crud import (
    notify_next_tc_approver,
    notify_supervisor_on_tc_create,
    notify_tc_approved,
    notify_tc_rejected,
    notify_tc_send_back,
    send_travel_expense_notification
)

router = APIRouter(prefix="/api/expense-sheet", tags=["Travel Expense Sheet"])

logger = logging.getLogger("travel_expense_router")


# ============================================================
# CREATE EXPENSE SHEET
# ============================================================

@router.post("/create")
async def create_expense_sheet(
    data: TravelExpenseSheetCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logger.info("======== CREATE EXPENSE SHEET ========")

    sheet = create_travel_expense_sheet(db, data)

    if not sheet:
        raise HTTPException(status_code=400, detail="Failed to create sheet")

    # Stage 1 → Notify Supervisor
    await notify_supervisor_on_tc_create(
        db=db,
        sheet=sheet,
        background_tasks=background_tasks
    )

    return sheet


# ============================================================
# UPDATE EXPENSE SHEET (MAIN FLOW CONTROLLER)
# ============================================================

@router.put("/update/{tes_id}")
async def update_expense_sheet(
    tes_id: int,
    data: TravelExpenseSheetUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    logger.info(f"======== UPDATE EXPENSE SHEET → ID {tes_id} ========")

    # --------------------------------------
    # Update DB
    # --------------------------------------
    update_travel_expense_sheet(db, tes_id, data)

    # Reload full sheet
    sheet = db.query(TravelExpenseSheet).filter(
        TravelExpenseSheet.tes_id == tes_id
    ).first()

    if not sheet:
        raise HTTPException(status_code=404, detail="Travel Expense Sheet not found")

    status = (sheet.status or "").strip()
    status_lower = status.lower()

    logger.info(f"[STATUS] {status}")

    # ======================================================
    # DETERMINE ACTED BY USER
    # ======================================================

    acted_by = "system"

    if status_lower == "tc pending - head tech":
        acted_by = sheet.updated_by_supervisor_name or "supervisor"

    elif status_lower == "tc pending - finance":
        acted_by = sheet.updated_by_head_tech_name or "head_tech"

    elif status_lower == "travel claim approved":
        acted_by = sheet.updated_by_finance_name or "finance"

    elif status_lower.startswith("tc rejected -"):
        if "supervisor" in status_lower:
            acted_by = sheet.updated_by_supervisor_name or "supervisor"
        elif "head tech" in status_lower:
            acted_by = sheet.updated_by_head_tech_name or "head_tech"
        elif "finance" in status_lower:
            acted_by = sheet.updated_by_finance_name or "finance"

    elif status_lower.startswith("tc changes request -"):
        if "supervisor" in status_lower:
            acted_by = sheet.updated_by_supervisor_name or "supervisor"
        elif "head tech" in status_lower:
            acted_by = sheet.updated_by_head_tech_name or "head_tech"
        elif "finance" in status_lower:
            acted_by = sheet.updated_by_finance_name or "finance"

    logger.info(f"[ACTION BY] {acted_by}")

    # ======================================================
    # 1️⃣ USER SUBMISSION → SUPERVISOR
    # ======================================================

    if status_lower == "tc pending - supervisor":

        logger.info("FLOW → USER SUBMISSION")

        await notify_supervisor_on_tc_create(
            db=db,
            sheet=sheet,
            background_tasks=background_tasks
        )

        # Notify employee confirmation
        employee = db.query(User).filter(
            User.user_id == sheet.user_id
        ).first()

        if employee:
            await send_travel_expense_notification(
                db=db,
                title="Travel Expense Submitted",
                description="Your travel expense claim has been submitted and sent to your supervisor for approval.",
                from_user=sheet.employee_name or "system",
                to_user_id=employee.user_id,
                module_status="TC Pending - Supervisor",
                background_tasks=background_tasks
            )

        return sheet


    # ======================================================
    # 2️⃣ SEND BACK FLOW
    # ======================================================

    if status_lower.startswith("tc changes request -"):

        logger.info("FLOW → SEND BACK")

        role_name = status.replace("TC Changes Request -", "").strip()

        await notify_tc_send_back(
            db=db,
            sheet=sheet,
            role_name=role_name,
            acted_by_username=acted_by,
            background_tasks=background_tasks
        )

        return sheet


    # ======================================================
    # 3️⃣ APPROVAL FLOW
    # ======================================================

    # Supervisor Approved → Head Tech
    if status_lower == "tc pending - head tech":

        logger.info("FLOW → SUPERVISOR APPROVED")

        await notify_next_tc_approver(
            db=db,
            sheet=sheet,
            role_name="Supervisor",
            acted_by_username=acted_by,
            background_tasks=background_tasks
        )


    # Head Tech Approved → Finance
    elif status_lower == "tc pending - finance":

        logger.info("FLOW → HEAD TECH APPROVED")

        await notify_next_tc_approver(
            db=db,
            sheet=sheet,
            role_name="Head Tech",
            acted_by_username=acted_by,
            background_tasks=background_tasks
        )


    # Finance Approved → Final
    elif status_lower == "travel claim approved":

        logger.info("FLOW → FINANCE APPROVED (FINAL)")

        await notify_tc_approved(
            db=db,
            sheet=sheet,
            approved_by=acted_by,
            background_tasks=background_tasks
        )


    # ======================================================
    # 4️⃣ REJECTION FLOW
    # ======================================================

    elif "rejected" in status_lower:

        logger.info("FLOW → REJECTION")

        role_name = status.replace("TC Rejected -", "").strip()

        await notify_tc_rejected(
            db=db,
            sheet=sheet,
            rejected_by_role=role_name,
            rejected_by_username=acted_by,
            background_tasks=background_tasks
        )

    # --------------------------------------
    # Final Response
    # --------------------------------------

    return {
        "tes_id": sheet.tes_id,
        "user_id": sheet.user_id,
        "status": sheet.status,
        "updated_at": sheet.updated_at
    }