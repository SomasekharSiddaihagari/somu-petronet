from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from typing import Optional

from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User
from app.models.NotificationModel import Notification


# ============================================================
# Helper (DICT SAFE like Meal Allowance)
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
# Create + save notification (DB)
# ============================================================

def create_travel_notification(db: Session, notification: NotificationCreate):
    notif = Notification(
        type=notification.type,
        title=notification.title,
        description=notification.description,
        from_user=notification.from_user,
        to_user=notification.to_user,
        module_name="travel",
        module_status=notification.module_status,
        date=datetime.now(),
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


# ============================================================
# Generic sender (DB + WS + Email)
# ============================================================

async def send_travel_notification(
    db: Session,
    *,
    title: str,
    description: str,
    from_user: str,
    to_user: str,
    module_status: Optional[str],
    background_tasks: BackgroundTasks
):
    data = NotificationCreate(
        type="Travel",
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name="travel",
        module_status=module_status or ""
    )

    db_notif = create_travel_notification(db, data)

    # WebSocket
    await manager.send_personal_message(to_user, {
        "id": db_notif.id,
        "type": db_notif.type,
        "title": db_notif.title,
        "description": db_notif.description,
        "from_user": db_notif.from_user,
        "to_user": db_notif.to_user,
        "module_name": db_notif.module_name,
        "module_status": db_notif.module_status,
        "date": str(db_notif.date)
    })

    # Email
    user = db.query(User).filter(User.username == to_user).first()
    if user and user.email:
        full_name = get_full_name(user)
        background_tasks.add_task(
            send_email,
            user.email,
            title,
            f"Dear {full_name},\n\n{description}\n\nRegards,\nPetronet Travel System",
            "Travel Expense Claims"
        )


# ============================================================
# 1️⃣ User creates Travel Requisition
#    → Notify User + Supervisor
# ============================================================

async def notify_on_travel_create(
    db: Session,
    travel: dict,
    background_tasks: BackgroundTasks
):
    user_id = get_val(travel, "user_id")
    status = get_val(travel, "status")

    if not user_id:
        return

    employee = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not employee or not employee.supervisor_id:
        return

    supervisor = (
        db.query(User)
        .filter(User.user_id == employee.supervisor_id)
        .first()
    )

    if not supervisor:
        return

    # 🔔 Notify USER
    await send_travel_notification(
        db=db,
        title="Travel Requisition Submitted",
        description="Your Travel Requisition Form has been submitted successfully.",
        from_user=employee.username,
        to_user=employee.username,
        module_status=status,
        background_tasks=background_tasks
    )

    # 🔔 Notify SUPERVISOR
    await send_travel_notification(
        db=db,
        title="New Travel Requisition for Review",
        description="A new travel request requires your approval.",
        from_user=employee.username,
        to_user=supervisor.username,
        module_status=status,
        background_tasks=background_tasks
    )


# ============================================================
# 2️⃣ Supervisor Approved
#    → Notify User
# ============================================================

async def notify_on_travel_approved(
    db: Session,
    travel: dict,
    approved_by: str,
    background_tasks: BackgroundTasks
):
    user_id = get_val(travel, "user_id")
    status = get_val(travel, "status")

    if not user_id:
        return

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return

    await send_travel_notification(
        db=db,
        title="Travel Requisition Approved",
        description="Your Travel Requisition has been approved and moved to Travel Claim stage.",
        from_user=approved_by,
        to_user=user.username,
        module_status=status,
        background_tasks=background_tasks
    )


# ============================================================
# 3️⃣ Supervisor Rejected
#    → Notify User
# ============================================================

async def notify_on_travel_rejected(
    db: Session,
    travel: dict,
    rejected_by: str,
    background_tasks: BackgroundTasks
):
    user_id = get_val(travel, "user_id")
    status = get_val(travel, "status")

    if not user_id:
        return

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return

    await send_travel_notification(
        db=db,
        title="Travel Requisition Rejected",
        description="Your Travel Requisition has been rejected by the supervisor.",
        from_user=rejected_by,
        to_user=user.username,
        module_status=status,
        background_tasks=background_tasks
    )
