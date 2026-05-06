from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from typing import List

from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User
from app.models.NotificationModel import Notification
from app.models.RolePermissionModel import RolePermission


# ============================================================
# Helpers (DICT + ORM SAFE)
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
# STATUS PARSER
# ============================================================

def parse_status(status: str):
    if not status:
        return None, None

    status = status.strip()

    if status.startswith("MA Pending"):
        return "pending", status.split("-")[-1].strip()

    if status.startswith("Rejected"):
        return "reject", status.split("-")[-1].strip()

    if status.startswith("Changes Request"):
        return "send_back", status.split("-")[-1].strip()

    if status == "Meal Allowance Approved":
        return "final_approve", "Finance"

    return None, None


# ============================================================
# Create + save notification
# ============================================================

def create_meal_allowance_notification(db: Session, data: NotificationCreate):
    notif = Notification(
        type="MealAllowance",
        title=data.title,
        description=data.description,
        from_user=data.from_user,
        to_user=data.to_user,
        module_name="meal_allowance",
        module_status=data.module_status,
        date=datetime.now(),
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


# ============================================================
# Generic sender
# ============================================================

async def send_meal_allowance_notification(
    db: Session,
    *,
    title: str,
    description: str,
    from_user: str,
    to_user: str,
    module_status: str,
    background_tasks: BackgroundTasks
):
    data = NotificationCreate(
        type="MealAllowance",
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name="meal_allowance",
        module_status=module_status
    )

    notif = create_meal_allowance_notification(db, data)

    await manager.send_personal_message(to_user, {
        "id": notif.id,
        "title": notif.title,
        "description": notif.description,
        "module_status": notif.module_status,
        "date": str(notif.date)
    })

    user = db.query(User).filter(User.username == to_user).first()
    if user and user.email:
        background_tasks.add_task(
            send_email,
            user.email,
            title,
            f"Dear {get_full_name(user)},\n\n{description}\n\nRegards,\nPetronet Travel System",
            "Travel Expense Claims"
        )


# ============================================================
# BULK NOTIFY
# ============================================================

async def notify_users_bulk(
    db: Session,
    *,
    users: List[User],
    title: str,
    description: str,
    from_user: str,
    module_status: str,
    background_tasks: BackgroundTasks
):
    sent = set()

    for u in users:
        if not u or u.username in sent:
            continue

        sent.add(u.username)

        await send_meal_allowance_notification(
            db=db,
            title=title,
            description=description,
            from_user=from_user,
            to_user=u.username,
            module_status=module_status,
            background_tasks=background_tasks
        )


# ============================================================
# CREATE → ONLY SUPERVISOR
# ============================================================

async def notify_supervisor_on_ma_create(
    db: Session,
    sheet,
    background_tasks: BackgroundTasks
):
    user_id = get_val(sheet, "user_id")
    status = get_val(sheet, "status")

    employee = db.query(User).filter(User.user_id == user_id).first()
    if not employee or not employee.supervisor_id:
        return

    supervisor = db.query(User).filter(
        User.user_id == employee.supervisor_id
    ).first()

    if not supervisor:
        return

    await send_meal_allowance_notification(
        db=db,
        title="Meal Allowance Pending Approval",
        description="A Meal Allowance request is awaiting your approval.",
        from_user=employee.username,
        to_user=supervisor.username,
        module_status=status,
        background_tasks=background_tasks
    )


# ============================================================
# UPDATE → HANDLE STATUS CHANGE
# ============================================================

PREVIOUS_ROLE_MAP = {
    "HR": "Supervisor",
    "Finance": "HR",
}


async def handle_meal_allowance_status_change(
    db: Session,
    *,
    sheet,
    background_tasks: BackgroundTasks
):
    status = get_val(sheet, "status")
    user_id = get_val(sheet, "user_id")
    req_no = get_val(sheet, "requisition_number")

    action_type, role_name = parse_status(status)
    if not action_type:
        return

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return

    # Who acted
    acted_by = None
    if role_name == "Supervisor":
        acted_by = get_val(sheet, "updated_by_supervisor_name")
    elif role_name == "HR":
        acted_by = get_val(sheet, "updated_by_hr_name")
    elif role_name == "Finance":
        acted_by = get_val(sheet, "updated_by_finance_name")

    # ========================================================
    # 🔵 PENDING → USER + NEXT APPROVER ONLY
    # ========================================================
    if action_type == "pending":
        users_to_notify = [user]

        approved_by_role = PREVIOUS_ROLE_MAP.get(role_name, "System")
        forwarded_to = role_name

        if role_name == "HR":
            hr_users = (
                db.query(User)
                .join(RolePermission, RolePermission.user_id == User.user_id)
                .filter(
                    RolePermission.role_id == 7,
                    RolePermission.submenu_id == 11
                )
                .all()
            )
            users_to_notify.extend(hr_users)

        elif role_name == "Finance":
            finance_users = (
                db.query(User)
                .join(RolePermission, RolePermission.user_id == User.user_id)
                .filter(
                    RolePermission.role_id == 11,
                    RolePermission.submenu_id == 11
                )
                .all()
            )
            users_to_notify.extend(finance_users)

        await notify_users_bulk(
            db=db,
            users=users_to_notify,
            title="Meal Allowance Pending Approval",
            description=(
                f"Meal Allowance {req_no} approved by "
                f"{approved_by_role} and forwarded to {forwarded_to}."
            ),
            from_user=acted_by or "system",
            module_status=status,
            background_tasks=background_tasks
        )
        return

    # ========================================================
    # 🔴 REJECT / SEND BACK → UPSTREAM ONLY
    # ========================================================
    if action_type in ("reject", "send_back"):
        users_to_notify = [user]

        if role_name == "HR" or role_name == "Finance":
            if user.supervisor_id:
                sup = db.query(User).filter(
                    User.user_id == user.supervisor_id
                ).first()
                if sup:
                    users_to_notify.append(sup)

        if role_name == "Finance":
            hr_users = (
                db.query(User)
                .join(RolePermission, RolePermission.user_id == User.user_id)
                .filter(
                    RolePermission.role_id == 7,
                    RolePermission.submenu_id == 9
                )
                .all()
            )
            users_to_notify.extend(hr_users)

        title = (
            "Meal Allowance Rejected"
            if action_type == "reject"
            else "Changes Requested in Meal Allowance"
        )

        description = (
            f"Meal Allowance {req_no} has been "
            f"{'Rejected' if action_type == 'reject' else 'sent back'} by {role_name}."
        )

        await notify_users_bulk(
            db=db,
            users=users_to_notify,
            title=title,
            description=description,
            from_user=acted_by or "system",
            module_status=status,
            background_tasks=background_tasks
        )
        return

    # ========================================================
    # 🟢 FINAL APPROVAL → USER + SUPERVISOR + HR  (NEW)
    # ========================================================
    if action_type == "final_approve":
        users_to_notify = [user]

        if user.supervisor_id:
            sup = db.query(User).filter(
                User.user_id == user.supervisor_id
            ).first()
            if sup:
                users_to_notify.append(sup)

        hr_users = (
            db.query(User)
            .join(RolePermission, RolePermission.user_id == User.user_id)
            .filter(
                RolePermission.role_id == 7,
                RolePermission.submenu_id == 11
            )
            .all()
        )
        users_to_notify.extend(hr_users)

        await notify_users_bulk(
            db=db,
            users=users_to_notify,
            title="Meal Allowance Approved",
            description=(
                f"Meal Allowance {req_no} has been approved by Finance."
            ),
            from_user=acted_by or "system",
            module_status=status,
            background_tasks=background_tasks
        )
        return
