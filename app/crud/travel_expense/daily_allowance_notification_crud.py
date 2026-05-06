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

def parse_da_status(status: str):
    if not status:
        return None, None

    status = status.strip()

    if status.startswith("DA Pending"):
        return "pending", status.split("-")[-1].strip()

    if status.startswith("DA Rejected"):
        return "reject", status.split("-")[-1].strip()

    if status.startswith("DA Changes Request"):
        return "send_back", status.split("-")[-1].strip()

    if status == "Daily Allowance Approved":
        return "final_approve", "Finance"

    return None, None


# ============================================================
# PREVIOUS ROLE MAP
# ============================================================

PREVIOUS_ROLE_MAP = {
    "Supervisor": "User",
    "HR": "Supervisor",
    "MD": "HR",
    "Finance": "MD",
}


# ============================================================
# MESSAGE BUILDER
# ============================================================

def get_da_message(*, action: str, role: str, violation: str, req_no: str):
    approved_by = PREVIOUS_ROLE_MAP.get(role, "System")

    # ---------------- PENDING ----------------
    if action == "pending":

        if role == "Supervisor":
            if violation == "YES":
                return (
                    "Policy Limit Exceeded — Verify",
                    f"Daily Allowance {req_no} exceeds entitlement and is awaiting your approval."
                )
            return (
                "Daily Allowance Pending Approval",
                f"Daily Allowance {req_no} has been submitted and is awaiting your approval."
            )

        if violation == "YES":
            return (
                "Policy Limit Exceeded — Verify",
                f"Daily Allowance {req_no} approved by {approved_by} and forwarded for review."
            )

        return (
            "Daily Allowance Pending Approval",
            f"Daily Allowance {req_no} approved by {approved_by} and forwarded for approval."
        )

    # ---------------- REJECT ----------------
    if action == "reject":
        return (
            "Daily Allowance Rejected",
            f"Daily Allowance {req_no} has been rejected by {role}."
        )

    # ---------------- SEND BACK ----------------
    if action == "send_back":
        return (
            "Changes Requested in Daily Allowance",
            f"Daily Allowance {req_no} has been sent back by {role}."
        )

    # ---------------- FINAL ----------------
    return (
        "Daily Allowance Approved",
        f"Daily Allowance {req_no} has been fully approved."
    )


# ============================================================
# CREATE + SAVE NOTIFICATION (DB ONLY)
# ============================================================

def create_da_notification(db: Session, data: NotificationCreate):
    notif = Notification(
        type="DailyAllowance",
        title=data.title,
        description=data.description,
        from_user=data.from_user,
        to_user=data.to_user,
        module_name="daily_allowance",
        module_status=data.module_status,
        date=datetime.now(),
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


# ============================================================
# GENERIC SENDER (SYNC + SAFE)
# ============================================================

def send_da_notification(
    db: Session,
    *,
    title: str,
    description: str,
    from_user: str,
    to_user: str,
    module_status: str,
    background_tasks: BackgroundTasks
):
    # -------------------------
    # DB INSERT (MUST BE INLINE)
    # -------------------------
    notif = Notification(
        type="DailyAllowance",
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name="daily_allowance",
        module_status=module_status,
        date=datetime.now(),
        is_read=False
    )
    
    db.add(notif)
    db.commit()
    db.refresh(notif)

    # -------------------------
    # WebSocket (Background)
    # -------------------------
    background_tasks.add_task(
        manager.send_personal_message,
        to_user,
        {
            "id": notif.id,
            "title": notif.title,
            "description": notif.description,
            "module_status": notif.module_status,
            "date": str(notif.date)
        }
    )

    # -------------------------
    # Email (Background)
    # -------------------------
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
# BULK NOTIFY (NO DUPLICATES)
# ============================================================

def notify_users_bulk(
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

        send_da_notification(
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

async def notify_supervisor_on_da_create(
    db: Session,
    sheet,
    background_tasks: BackgroundTasks
):
    user_id = get_val(sheet, "user_id")
    status = get_val(sheet, "status")
    violation = get_val(sheet, "violation")

    employee = db.query(User).filter(User.user_id == user_id).first()
    if not employee or not employee.supervisor_id:
        return

    supervisor = db.query(User).filter(
        User.user_id == employee.supervisor_id
    ).first()
    if not supervisor:
        return

    title, desc = get_da_message(
        action="pending",
        role="Supervisor",
        violation=violation,
        req_no=str(get_val(sheet, "da_sheet_id"))
    )

    send_da_notification(
        db=db,
        title=title,
        description=desc,
        from_user=employee.username,
        to_user=supervisor.username,
        module_status=status,
        background_tasks=background_tasks
    )


# ============================================================
# UPDATE → STATUS CHANGE HANDLER
# ============================================================

async def handle_daily_allowance_status_change(
    db: Session,
    *,
    sheet,
    background_tasks: BackgroundTasks
):
    status = get_val(sheet, "status")
    user_id = get_val(sheet, "user_id")
    violation = get_val(sheet, "violation")
    req_no = str(get_val(sheet, "da_sheet_id"))

    action, role = parse_da_status(status)
    if not action:
        return

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return

    acted_by = (
        get_val(sheet, "updated_by_supervisor_name")
        if role == "HR"
        else get_val(sheet, "updated_by_hr_name")
        if role == "MD"
        else get_val(sheet, "updated_by_md_name")
        if role == "Finance"
        else "system"
    )

    approved_by = PREVIOUS_ROLE_MAP.get(role, "System")

    # ---------------- PENDING ----------------
    if action == "pending":

        send_da_notification(
            db=db,
            title="Daily Allowance Pending Approval",
            description=(
                f"Daily Allowance {req_no} approved by {approved_by} "
                f"and is awaiting your approval."
            ),
            from_user=acted_by,
            to_user=user.username,
            module_status=status,
            background_tasks=background_tasks
        )

        approvers = []

        if role == "HR":
            approvers = (
                db.query(User)
                .join(RolePermission)
                .filter(RolePermission.role_id == 7, RolePermission.submenu_id == 11)
                .all()
            )

        elif role == "MD":
            approvers = (
                db.query(User)
                .join(RolePermission)
                .filter(RolePermission.role_id == 10)
                .all()
            )

        elif role == "Finance":
            approvers = (
                db.query(User)
                .join(RolePermission)
                .filter(RolePermission.role_id == 11, RolePermission.submenu_id == 11)
                .all()
            )

        title, desc = get_da_message(
            action="pending",
            role=role,
            violation=violation,
            req_no=req_no
        )

        notify_users_bulk(
            db=db,
            users=approvers,
            title=title,
            description=desc,
            from_user=acted_by,
            module_status=status,
            background_tasks=background_tasks
        )
