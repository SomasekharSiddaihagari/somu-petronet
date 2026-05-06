# from sqlalchemy.orm import Session
# from datetime import datetime
# from fastapi import BackgroundTasks
# from typing import Optional

# from app.models.RolePermissionModel import RolePermission
# from app.schemas.NotificationSchema import NotificationCreate
# from app.core.Websocket import manager
# from app.utils.EmailUtils import send_email
# from app.models.UserModel import User
# from app.models.NotificationModel import Notification


# # ============================================================
# # Helpers (DICT SAFE)
# # ============================================================

# def get_val(obj, key):
#     if isinstance(obj, dict):
#         return obj.get(key)
#     return getattr(obj, key, None)


# def get_full_name(user: User) -> str:
#     first = (user.first_name or "").strip()
#     last = (user.last_name or "").strip()
#     return f"{first} {last}".strip() or user.username


# # ============================================================
# # Create + save notification (DB)
# # ============================================================

# def create_travel_expense_notification(db: Session, notification: NotificationCreate):
#     notif = Notification(
#         type="TravelExpense",
#         title=notification.title,
#         description=notification.description,
#         from_user=notification.from_user,
#         to_user=notification.to_user,
#         module_name="travel_expense",
#         module_status=notification.module_status,
#         date=datetime.now(),
#         is_read=False
#     )
#     db.add(notif)
#     db.commit()
#     db.refresh(notif)
#     return notif


# # ============================================================
# # Generic sender (DB + WS + Email)
# # ============================================================

# async def send_travel_expense_notification(
#     db: Session,
#     *,
#     title: str,
#     description: str,
#     from_user: str,
#     to_user: str,
#     module_status: Optional[str],
#     background_tasks: BackgroundTasks
# ):
#     data = NotificationCreate(
#         type="TravelExpense",
#         title=title,
#         description=description,
#         from_user=from_user,
#         to_user=to_user,
#         module_name="travel_expense",
#         module_status=module_status or ""
#     )

#     db_notif = create_travel_expense_notification(db, data)

#     # WebSocket
#     await manager.send_personal_message(to_user, {
#         "id": db_notif.id,
#         "type": db_notif.type,
#         "title": db_notif.title,
#         "description": db_notif.description,
#         "from_user": db_notif.from_user,
#         "to_user": db_notif.to_user,
#         "module_name": db_notif.module_name,
#         "module_status": db_notif.module_status,
#         "date": str(db_notif.date)
#     })

#     # Email (safe)
#     user = db.query(User).filter(User.username == to_user).first()
#     if user and user.email and "@" in user.email:
#         full_name = get_full_name(user)
#         background_tasks.add_task(
#             send_email,
#             user.email,
#             title,
#             f"Dear {full_name},\n\n{description}\n\nRegards,\nPetronet Travel System",
#             "Travel Expense Claims"
#         )


# # ============================================================
# # NOTIFICATION TEXT RESOLVER (Violation Aware)
# # ============================================================

# def get_tc_notification_content(*, role: str, violation: str):
#     if violation == "YES":
#         if role == "Supervisor":
#             return ("Policy Limit Exceeded — Verify", "Submitted expense exceeds entitlement.")
#         if role == "HR":
#             return ("Policy Limit Exceeded — Verify", "Expense violates policy and needs HR verification.")
#         if role == "MD":
#             return ("MD Approval Required", "Policy threshold exceeded.")
#         if role == "Finance":
#             return ("Claim Requires Your Approval", "Entitlement threshold exceeded.")

#     return ("Travel Expense Pending Approval", "A travel expense claim requires your approval.")


# # ============================================================
# # 1️⃣ User creates Travel Expense → Notify Supervisor
# # ============================================================

# async def notify_supervisor_on_tc_create(
#     db: Session,
#     sheet: dict,
#     background_tasks: BackgroundTasks
# ):
#     user_id = get_val(sheet, "user_id")
#     status = get_val(sheet, "status")
#     violation = get_val(sheet, "violation")

#     if not user_id:
#         return

#     employee = db.query(User).filter(User.user_id == user_id).first()
#     if not employee or not employee.supervisor_id:
#         return

#     supervisor = db.query(User).filter(User.user_id == employee.supervisor_id).first()
#     if not supervisor:
#         return

#     title, description = get_tc_notification_content(
#         role="Supervisor",
#         violation=violation
#     )

#     await send_travel_expense_notification(
#         db=db,
#         title=title,
#         description=description,
#         from_user=employee.username,
#         to_user=supervisor.username,
#         module_status=status,
#         background_tasks=background_tasks
#     )


# # ============================================================
# # Approval Role Flow
# # ============================================================

# ROLE_FLOW = {
#     "Supervisor": ("TC Pending - HR", "HR", 7),
#     "HR": ("TC Pending - MD", "MD", 10),
#     "MD": ("TC Pending - Finance", "Finance", 11),
#     "Finance": ("Travel Claim Approved", None, None),
# }


# # ============================================================
# # 2️⃣ Approval → Next Approver / Final Approval
# # ============================================================

# async def notify_next_tc_approver(
#     db: Session,
#     *,
#     sheet: dict,
#     role_name: str,
#     acted_by_username: str,
#     background_tasks: BackgroundTasks
# ):
#     if role_name not in ROLE_FLOW:
#         return

#     status, next_role, next_role_id = ROLE_FLOW[role_name]
#     violation = get_val(sheet, "violation")

#     # FINAL APPROVAL
#     if not next_role:
#         await notify_tc_approved(
#             db=db,
#             sheet=sheet,
#             approved_by=acted_by_username,
#             background_tasks=background_tasks
#         )
#         return

#     # 🔥 FETCH ALL USERS FOR ROLE + SUBMENU (FIX)
#     role_permissions = (
#         db.query(RolePermission)
#         .filter(
#             RolePermission.role_id == next_role_id,
#             RolePermission.submenu_id == 11
#         )
#         .all()
#     )

#     if not role_permissions:
#         print(f"❌ No users found for role_id={next_role_id}, submenu_id=11")
#         return

#     title, description = get_tc_notification_content(
#         role=next_role,
#         violation=violation
#     )

#     for rp in role_permissions:
#         user = db.query(User).filter(User.user_id == rp.user_id).first()
#         if not user:
#             continue

#         print(f"📢 TC notification → {next_role}: {user.username}")

#         await send_travel_expense_notification(
#             db=db,
#             title=title,
#             description=description,
#             from_user=acted_by_username,
#             to_user=user.username,
#             module_status=status,
#             background_tasks=background_tasks
#         )


# # ============================================================
# # 3️⃣ Final Approval → Notify User
# # ============================================================

# # async def notify_tc_approved(

# #     db: Session,

# #     *,

# #     sheet,  # ORM TravelExpenseSheet

# #     approved_by: str,

# #     background_tasks: BackgroundTasks

# # ):

# #     print("🟢 [APPROVED] sheet.user_id =", sheet.user_id)
 
# #     if not sheet.user_id:

# #         print("🔴 notify_tc_approved: user_id is NULL")

# #         return
 
# #     user = db.query(User).filter(

# #         User.user_id == sheet.user_id

# #     ).first()
 
# #     if not user:

# #         print("🔴 notify_tc_approved: employee not found")

# #         return
 
# #     await send_travel_expense_notification(

# #         db=db,

# #         title="Approved Claim Ready for Processing",

# #         description="Your travel expense claim has been fully approved.",

# #         from_user=approved_by,

# #         to_user=user.username,

# #         module_status="Travel Claim Approved",

# #         background_tasks=background_tasks

# #     )
 
# #     print("✅ Approved notification sent to:", user.username)

 
# async def notify_tc_approved(
#     db: Session,
#     *,
#     sheet,
#     approved_by: str,
#     background_tasks: BackgroundTasks
# ):
#     print("🟢 [APPROVED] sheet.user_id =", sheet.user_id)
#     print("🟢 Approved by =", approved_by)

#     if not sheet.user_id:
#         print("🔴 notify_tc_approved: user_id is NULL")
#         return

#     employee = db.query(User).filter(
#         User.user_id == sheet.user_id
#     ).first()

#     if not employee:
#         print("🔴 notify_tc_approved: employee not found")
#         return

#     # ================================
#     # 1️⃣ USER (always)
#     # ================================
#     await send_travel_expense_notification(
#         db=db,
#         title="Travel Expense Approved",
#         description="Your travel expense claim has been approved.",
#         from_user=approved_by,
#         to_user=employee.username,
#         module_status="Travel Claim Approved",
#         background_tasks=background_tasks
#     )
#     print("✅ Approved → User")

#     # ================================
#     # 2️⃣ SUPERVISOR (Finance / HR / MD)
#     # ================================
#     if approved_by in ["finance", "hr", "md"] and employee.supervisor_id:
#         supervisor = db.query(User).filter(
#             User.user_id == employee.supervisor_id
#         ).first()

#         if supervisor:
#             await send_travel_expense_notification(
#                 db=db,
#                 title="Travel Expense Approved",
#                 description=f"Travel expense claim of {employee.username} has been approved.",
#                 from_user=approved_by,
#                 to_user=supervisor.username,
#                 module_status="Travel Claim Approved",
#                 background_tasks=background_tasks
#             )
#             print("✅ Approved → Supervisor")

#     # ================================
#     # 3️⃣ HR USERS (Finance / MD)
#     # ================================
#     if approved_by in ["finance", "md"]:
#         hr_users = (
#             db.query(RolePermission)
#             .filter(
#                 RolePermission.role_id == 7,
#                 RolePermission.submenu_id == 11
#             )
#             .all()
#         )

#         for rp in hr_users:
#             hr = db.query(User).filter(User.user_id == rp.user_id).first()
#             if not hr:
#                 continue

#             await send_travel_expense_notification(
#                 db=db,
#                 title="Travel Expense Approved",
#                 description=f"Travel expense claim of {employee.username} has been approved.",
#                 from_user=approved_by,
#                 to_user=hr.username,
#                 module_status="Travel Claim Approved",
#                 background_tasks=background_tasks
#             )
#             print("✅ Approved → HR:", hr.username)




# # ============================================================
# # 4️⃣ Rejection → Notify User
# # ============================================================

# async def notify_tc_rejected(

#     db: Session,

#     *,

#     sheet,  # ORM TravelExpenseSheet

#     rejected_by_role: str,

#     rejected_by_username: str,

#     background_tasks: BackgroundTasks

# ):

#     print("🔴 [REJECTED] sheet.user_id =", sheet.user_id)
 
#     if not sheet.user_id:

#         print("🔴 notify_tc_rejected: user_id is NULL")

#         return
 
#     user = db.query(User).filter(

#         User.user_id == sheet.user_id

#     ).first()
 
#     if not user:

#         print("🔴 notify_tc_rejected: employee not found")

#         return
 
#     await send_travel_expense_notification(

#         db=db,

#         title="Travel Expense Claim Rejected",

#         description=f"Your travel expense claim was rejected by {rejected_by_role}.",

#         from_user=rejected_by_username,

#         to_user=user.username,

#         module_status=f"TC Rejected - {rejected_by_role}",

#         background_tasks=background_tasks

#     )
 
#     print("❌ Rejection notification sent to:", user.username)

 
# # ============================================================
# # 5️⃣ Send Back → Notify User
# # ============================================================

# async def notify_tc_send_back(
#     db: Session,
#     *,
#     sheet,
#     role_name: str,
#     acted_by_username: str,
#     background_tasks: BackgroundTasks
# ):
#     print("🟡 SEND BACK user_id =", sheet.user_id)

#     if not sheet.user_id:
#         print("🔴 sheet.user_id is NULL")
#         return

#     employee = db.query(User).filter(
#         User.user_id == sheet.user_id
#     ).first()

#     if not employee:
#         print("🔴 Employee not found")
#         return

#     # 1️⃣ Employee (always)
#     await send_travel_expense_notification(
#         db=db,
#         title="Travel Expense Changes Requested",
#         description=f"Your travel expense claim was sent back by {role_name}.",
#         from_user=acted_by_username,
#         to_user=employee.username,
#         module_status=f"TC Changes Request - {role_name}",
#         background_tasks=background_tasks
#     )

#     # 2️⃣ Supervisor (HR / MD / Finance)
#     if role_name in ["HR", "MD", "Finance"] and employee.supervisor_id:
#         supervisor = db.query(User).filter(
#             User.user_id == employee.supervisor_id
#         ).first()

#         if supervisor:
#             await send_travel_expense_notification(
#                 db=db,
#                 title="Travel Expense Sent Back",
#                 description=f"Claim of {employee.username} was sent back by {role_name}.",
#                 from_user=acted_by_username,
#                 to_user=supervisor.username,
#                 module_status=f"TC Changes Request - {role_name}",
#                 background_tasks=background_tasks
#             )

#     # 3️⃣ HR USERS (MD / FINANCE)
#     if role_name in ["MD", "Finance"]:
#         hr_users = (
#             db.query(RolePermission)
#             .filter(
#                 RolePermission.role_id == 7,
#                 RolePermission.submenu_id == 11
#             )
#             .all()
#         )

#         for rp in hr_users:
#             hr = db.query(User).filter(User.user_id == rp.user_id).first()
#             if not hr:
#                 continue

#             await send_travel_expense_notification(
#                 db=db,
#                 title="Travel Expense Sent Back",
#                 description=f"Claim of {employee.username} was sent back by {role_name}.",
#                 from_user=acted_by_username,
#                 to_user=hr.username,
#                 module_status=f"TC Changes Request - {role_name}",
#                 background_tasks=background_tasks
#             )





from sqlalchemy.orm import Session       
from datetime import datetime
from fastapi import BackgroundTasks
from typing import Optional
import logging

from app.models.RolePermissionModel import RolePermission
from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User
from app.models.NotificationModel import Notification


# ============================================================
# 🔹 CENTRAL CONSTANTS (MERGED FROM tc_constants.py)
# ============================================================

# DB identifiers
TC_SUBMENU_ID = 11
ROLE_ID_HEAD_TECHNICAL = 15
ROLE_ID_FINANCE = 11

# Notification meta
TC_NOTIFICATION_TYPE = "TravelExpense"
TC_MODULE_NAME = "travel_expense"
TC_EMAIL_SUBJECT = "Travel Expense Claims"

# Role Labels
ROLE_LABEL_SUPERVISOR = "Supervisor"
ROLE_LABEL_HEAD_TECHNICAL = "Head Technical"
ROLE_LABEL_FINANCE = "Finance"

# Status Strings
STATUS_PENDING_SUPERVISOR = "TC Pending - Supervisor"
STATUS_PENDING_HEADTECH = "TC Pending - HeadTech"
STATUS_PENDING_FINANCE = "TC Pending - Finance"
STATUS_APPROVED = "Travel Claim Approved"
STATUS_PREFIX_CHANGES = "TC Changes Request -"
STATUS_PREFIX_REJECTED = "TC Rejected -"


# ============================================================
# LOGGER CONFIG
# ============================================================

logger = logging.getLogger("travel_expense_notifications")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


# ============================================================
# HELPERS
# ============================================================

def get_val(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def get_full_name(user: User) -> str:
    first = (user.first_name or "").strip()
    last = (user.last_name or "").strip()
    return f"{first} {last}".strip() or user.username


# ============================================================
# CREATE NOTIFICATION (DB SAVE)
# ============================================================

def create_travel_expense_notification(db: Session, notification: NotificationCreate):

    logger.info(f"[DB] Creating notification → To: {notification.to_user}")

    notif = Notification(
        type=TC_NOTIFICATION_TYPE,
        title=notification.title,
        description=notification.description,
        from_user=notification.from_user,
        to_user=notification.to_user,
        module_name=TC_MODULE_NAME,
        module_status=notification.module_status,
        date=datetime.now(),
        is_read=False
    )

    db.add(notif)
    db.commit()
    db.refresh(notif)

    logger.info(f"[DB] Notification saved successfully → ID: {notif.id}")

    return notif


# ============================================================
# GENERIC SENDER (DB + WS + EMAIL)
# ============================================================

async def send_travel_expense_notification(
    db: Session,
    *,
    title: str,
    description: str,
    from_user: str,
    to_user_id: int,
    module_status: Optional[str],
    background_tasks: BackgroundTasks
):

    logger.info(f"[NOTIFY] Preparing notification → To user_id={to_user_id}")

    user = db.query(User).filter(User.user_id == to_user_id).first()

    if not user:
        logger.error(f"[ERROR] User not found in DB → user_id={to_user_id}")
        return

    data = NotificationCreate(
        type=TC_NOTIFICATION_TYPE,
        title=title,
        description=description,
        from_user=from_user,
        to_user=user.username,
        module_name=TC_MODULE_NAME,
        module_status=module_status or ""
    )

    db_notif = create_travel_expense_notification(db, data)

    # WebSocket Push
    await manager.send_personal_message(user.username, {
        "id": db_notif.id,
        "title": db_notif.title,
        "description": db_notif.description,
        "from_user": db_notif.from_user,
        "module_status": db_notif.module_status,
        "date": str(db_notif.date)
    })

    # Email Sending
    if user.email and "@" in user.email:
        background_tasks.add_task(
            send_email,
            user.email,
            title,
            f"Dear {get_full_name(user)},\n\n{description}\n\nRegards,\nPetronet Travel System",
            TC_EMAIL_SUBJECT
        )


# ============================================================
# 1️⃣ USER SUBMIT → SUPERVISOR
# ============================================================

async def notify_supervisor_on_tc_create(
    db: Session,
    sheet,
    background_tasks: BackgroundTasks
):

    employee = db.query(User).filter(
        User.user_id == get_val(sheet, "user_id")
    ).first()

    if not employee or not employee.supervisor_id:
        return

    await send_travel_expense_notification(
        db=db,
        title="Travel Expense Pending Approval",
        description="Claim requires Supervisor approval.",
        from_user=employee.username,
        to_user_id=employee.supervisor_id,
        module_status=STATUS_PENDING_SUPERVISOR,
        background_tasks=background_tasks
    )


# ============================================================
# 2️⃣ APPROVAL FLOW
# ============================================================

async def notify_next_tc_approver(
    db: Session,
    *,
    sheet,
    role_name: str,
    acted_by_username: str,
    background_tasks: BackgroundTasks
):

    # Supervisor → Head Tech
    if role_name == ROLE_LABEL_SUPERVISOR:

        head_tech_roles = db.query(RolePermission).filter(
            RolePermission.role_id == ROLE_ID_HEAD_TECHNICAL,
            RolePermission.submenu_id == TC_SUBMENU_ID
        ).all()

        for rp in head_tech_roles:
            await send_travel_expense_notification(
                db=db,
                title="Travel Expense Pending Approval",
                description="Claim requires Head Tech approval.",
                from_user=acted_by_username,
                to_user_id=rp.user_id,
                module_status=STATUS_PENDING_HEADTECH,
                background_tasks=background_tasks
            )
        return

    # Head Tech → Finance
    if role_name == ROLE_LABEL_HEAD_TECHNICAL:

        finance_roles = db.query(RolePermission).filter(
            RolePermission.role_id == ROLE_ID_FINANCE,
            RolePermission.submenu_id == TC_SUBMENU_ID
        ).all()

        for rp in finance_roles:
            await send_travel_expense_notification(
                db=db,
                title="Travel Expense Pending Approval",
                description="Claim requires Finance approval.",
                from_user=acted_by_username,
                to_user_id=rp.user_id,
                module_status=STATUS_PENDING_FINANCE,
                background_tasks=background_tasks
            )
        return

    # Finance → Final
    if role_name == ROLE_LABEL_FINANCE:
        await notify_tc_approved(
            db=db,
            sheet=sheet,
            approved_by=acted_by_username,
            background_tasks=background_tasks
        )


# ============================================================
# 3️⃣ FINAL APPROVAL
# ============================================================

async def notify_tc_approved(
    db: Session,
    *,
    sheet,
    approved_by: str,
    background_tasks: BackgroundTasks
):

    employee = db.query(User).filter(
        User.user_id == get_val(sheet, "user_id")
    ).first()

    if not employee:
        return

    # Employee
    await send_travel_expense_notification(
        db=db,
        title="Travel Expense Approved",
        description="Your travel expense claim has been approved.",
        from_user=approved_by,
        to_user_id=employee.user_id,
        module_status=STATUS_APPROVED,
        background_tasks=background_tasks
    )

    # Supervisor
    if employee.supervisor_id:
        await send_travel_expense_notification(
            db=db,
            title="Travel Expense Approved",
            description=f"{employee.username}'s claim has been approved.",
            from_user=approved_by,
            to_user_id=employee.supervisor_id,
            module_status=STATUS_APPROVED,
            background_tasks=background_tasks
        )


# ============================================================
# REJECTION
# ============================================================

async def notify_tc_rejected(
    db: Session,
    *,
    sheet,
    rejected_by_role: str,
    rejected_by_username: str,
    background_tasks: BackgroundTasks
):

    employee = db.query(User).filter(
        User.user_id == get_val(sheet, "user_id")
    ).first()

    if not employee:
        return

    await send_travel_expense_notification(
        db=db,
        title="Travel Expense Claim Rejected",
        description=f"Your travel expense claim was rejected by {rejected_by_role}.",
        from_user=rejected_by_username,
        to_user_id=employee.user_id,
        module_status=f"{STATUS_PREFIX_REJECTED} {rejected_by_role}",
        background_tasks=background_tasks
    )


# ============================================================
# SEND BACK
# ============================================================

async def notify_tc_send_back(
    db: Session,
    *,
    sheet,
    role_name: str,
    acted_by_username: str,
    background_tasks: BackgroundTasks
):

    employee = db.query(User).filter(
        User.user_id == get_val(sheet, "user_id")
    ).first()

    if not employee:
        return

    await send_travel_expense_notification(
        db=db,
        title="Travel Expense Changes Requested",
        description=f"Your travel expense claim was sent back by {role_name}.",
        from_user=acted_by_username,
        to_user_id=employee.user_id,
        module_status=f"{STATUS_PREFIX_CHANGES} {role_name}",
        background_tasks=background_tasks
    )


