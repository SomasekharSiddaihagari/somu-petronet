# app/crud/leave/LeaveNotificationCrud.py

from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks

from app.models.leave.hr_leave_application import HRLeaveApplication
from app.schemas.NotificationSchema import NotificationCreate
from app.models.NotificationModel import Notification
from app.models.UserModel import User
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email


# =====================================================
# HELPERS
# =====================================================

def get_user(db: Session, user_id: int | None):
    if not user_id:
        return None
    return db.query(User).filter(User.user_id == user_id).first()


def get_username(db: Session, user_id: int | None):
    user = get_user(db, user_id)
    return user.username if user else None


# =====================================================
# SAVE NOTIFICATION
# =====================================================

def save_leave_notification(db: Session, data: NotificationCreate):
    notif = Notification(
        type=data.type,
        title=data.title,
        description=data.description,
        from_user=data.from_user,   # username
        to_user=data.to_user,       # username
        module_name="leave",
        module_status=data.module_status,
        date=datetime.now(),
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


# =====================================================
# GENERIC NOTIFICATION SENDER
# =====================================================

async def send_leave_notification(
    db: Session,
    *,
    type: str,
    title: str,
    description: str,
    from_user: str,     # username
    to_user: str,       # username
    module_status: str,
    background_tasks: BackgroundTasks
):
    data = NotificationCreate(
        type=type,
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name="leave",
        module_status=module_status
    )

    saved = save_leave_notification(db, data)

    # ---------------- WebSocket ----------------
    await manager.send_personal_message(to_user, {
        "id": saved.id,
        "type": saved.type,
        "title": saved.title,
        "description": saved.description,
        "from_user": saved.from_user,
        "to_user": saved.to_user,
        "module_name": saved.module_name,
        "module_status": saved.module_status,
        "date": str(saved.date)
    })

    # ---------------- Email ----------------
    user = db.query(User).filter(User.username == to_user).first()
    if user and user.email:
        full_name = f"{user.first_name} {user.last_name}".strip()

        email_body = (
            f"Dear {full_name},\n\n"
            f"{description}\n\n"
            f"Regards,\n"
            f"Petronet Leave System"
        )

        if background_tasks: 
            background_tasks.add_task(
            send_email,
            user.email,
            title,
            email_body,
            "Leave Management"
        )
        else:
            send_email(
                user.email,
                title,
                email_body,
                "Leave Management"
            )


# =====================================================
# NOTIFY SUPERVISOR ON APPLY
# =====================================================

async def notify_supervisor_on_apply(
    db: Session,
    leave_data: dict,
    background_tasks: BackgroundTasks
):
    supervisor_username = get_username(db, leave_data.get("supervisor_id"))
    applicant_username = get_username(db, leave_data.get("user_id"))

    if not supervisor_username or not applicant_username:
        print("❌ Username resolution failed (apply)")
        return

    await send_leave_notification(
        db=db,
        type="Leave",
        title=f"New Leave Request ({leave_data['leave_type']})",
        description=(
            f"{leave_data['user_name']} applied for {leave_data['leave_type']} "
            f"from {leave_data['from_date']} to {leave_data['to_date']}."
        ),
        from_user=applicant_username,
        to_user=supervisor_username,
        module_status="Pending Approval",
        background_tasks=background_tasks
    )


# =====================================================
# HANDLE ALL SUPERVISOR ACTIONS
# =====================================================

async def handle_supervisor_action(
    db: Session,
    row: dict,
    background_tasks: BackgroundTasks
):
    leave = db.query(HRLeaveApplication).filter(
        HRLeaveApplication.leave_id == row["leave_id"]
    ).first()

    if not leave:
        print("❌ Leave not found")
        return

    status = row["status"]

    # -------- usernames (FOR NOTIFICATIONS) --------
    user_username = get_username(db, leave.user_id)
    supervisor_username = get_username(db, leave.supervisor_id)

    if not user_username or not supervisor_username:
        print("❌ Username resolution failed")
        return

    # -------- display names (FOR MESSAGE TEXT) --------
    user_name = leave.user_name
    supervisor_name = leave.supervisor_name

    leave_type = leave.leave_type
    from_date = leave.from_date
    to_date = leave.to_date

    reversal_from = leave.reversal_from_date
    reversal_to = leave.reversal_to_date
    reversal_remarks = leave.reversal_remarks
    supervisor_remarks = leave.supervisor_remarks

    hr_list = db.query(User).filter(User.role_id == 7).all()

    # =================================================
    # WITHDRAW PENDING
    # =================================================
    if status == "Withdraw Pending":
        await send_leave_notification(
            db=db,
            type="Leave",
            title="Leave Withdrawal Request",
            description=(
                f"{user_name} requested withdrawal of leave "
                f"({leave_type}) from {from_date} to {to_date}."
            ),
            from_user=user_username,
            to_user=supervisor_username,
            module_status=status,
            background_tasks=background_tasks
        )
        return

    # =================================================
    # WITHDRAW APPROVED / REJECTED
    # =================================================
    if status in ["Withdraw Approved", "Withdraw Rejected"]:
        await send_leave_notification(
            db=db,
            type="Leave",
            title=f"Leave Withdrawal {status}",
            description=(
                f"Your leave withdrawal request ({leave_type}) "
                f"from {from_date} to {to_date} was {status.lower()} "
                f"by {supervisor_name}.\n"
                f"Remarks: {supervisor_remarks}"
            ),
            from_user=supervisor_username,
            to_user=user_username,
            module_status=status,
            background_tasks=background_tasks
        )

        for hr in hr_list:
            await send_leave_notification(
                db=db,
                type="Leave",
                title=f"Leave Withdrawal {status}",
                description=(
                    f"{supervisor_name} {status.lower()} withdrawal of "
                    f"{leave_type} for {user_name} "
                    f"({from_date} to {to_date})."
                ),
                from_user=supervisor_username,
                to_user=hr.username,
                module_status=status,
                background_tasks=background_tasks
            )
        return

    # =================================================
    # REVERSAL PENDING
    # =================================================
    if status == "Reversal Pending":
        await send_leave_notification(
            db=db,
            type="Leave",
            title="Leave Reversal Request",
            description=(
                f"{user_name} requested leave reversal "
                f"from {reversal_from} to {reversal_to}.\n"
                f"Remarks: {reversal_remarks}"
            ),
            from_user=user_username,
            to_user=supervisor_username,
            module_status=status,
            background_tasks=background_tasks
        )
        return

    # =================================================
    # REVERSAL APPROVED / REJECTED
    # =================================================
    if status in ["Reversal Approved", "Reversal Rejected"]:
        await send_leave_notification(
            db=db,
            type="Leave",
            title=f"Leave Reversal {status}",
            description=(
                f"Your leave reversal request "
                f"from {reversal_from} to {reversal_to} "
                f"was {status.lower()} by {supervisor_name}.\n"
                f"Remarks: {supervisor_remarks}"
            ),
            from_user=supervisor_username,
            to_user=user_username,
            module_status=status,
            background_tasks=background_tasks
        )

        for hr in hr_list:
            await send_leave_notification(
                db=db,
                type="Leave",
                title=f"Leave Reversal {status}",
                description=(
                    f"{supervisor_name} {status.lower()} leave reversal "
                    f"for {user_name} "
                    f"({reversal_from} to {reversal_to})."
                ),
                from_user=supervisor_username,
                to_user=hr.username,
                module_status=status,
                background_tasks=background_tasks
            )
        return
    status = (row["status"] or "").strip().lower()
    if status == "auto rejected":
        await send_leave_notification(
            db=db,
            type="Leave",
            title="Leave Auto Rejected",
            description=(
                f"Your leave request ({leave_type}) "
                f"from {from_date} to {to_date} was automatically rejected.\n"
                f"Reason: Approval time expired or no action was taken."
            ),
            from_user="System",   # or use supervisor_username if needed
            to_user=user_username,
            module_status=status,
            background_tasks=background_tasks
        )
        return
