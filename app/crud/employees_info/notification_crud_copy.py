# app/crud/employee/EmployeeNotificationCrud.py
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User
from app.models.NotificationModel import Notification  # used for overrides


# -------------------------
# Create + save notification (DB)
# -------------------------
def create_employee_notification(db: Session, notification: NotificationCreate):
    try:
        db_notif = Notification(
            type=notification.type,
            title=notification.title,
            description=notification.description,
            from_user=notification.from_user,
            to_user=notification.to_user,
            module_name=notification.module_name,
            module_status=notification.module_status,
            date=datetime.utcnow(),
            is_read=False
        )
        db.add(db_notif)
        db.commit()
        db.refresh(db_notif)
        #print("✅ Notification saved with ID:", db_notif.id)
        return db_notif
    except Exception as e:
        db.rollback()
        #print("❌ NOTIFICATION DB ERROR:", e)
        raise



# -------------------------
# Generic sender (DB + WS + Email)
# - Note: email_body is the full email text, notif_description is short message for notification
# - Returns db_notif
# -------------------------
async def send_employee_notification(
    db: Session,
    *,
    type: str,
    title: str,
    email_body: str,
    notif_description: str | None,
    from_user: str,
    to_user: str,
    module_name: str = "Employee Personal Information",
    module_status: str | None = None,
    background_tasks: BackgroundTasks
):
    # Use notif_description for DB notification; fallback to short slice of email_body
    desc_for_db = notif_description or (email_body[:200] + ("..." if len(email_body) > 200 else ""))

    data = NotificationCreate(
        type=type,
        title=title,
        description=desc_for_db,
        from_user=from_user,
        to_user=to_user,
        module_name=module_name,
        module_status=module_status
    )

    db_notif = create_employee_notification(db, data)

    # WS push (send the short description)
    try:
        await manager.send_personal_message(to_user, {
            "id": db_notif.id,
            "type": db_notif.type,
            "title": db_notif.title,
            "description": db_notif.description,
            "from_user": db_notif.from_user,
            "to_user": db_notif.to_user,
            "module_name": db_notif.module_name,
            "module_status": db_notif.module_status,
            "date": str(db_notif.date),
        })
    except Exception:
        # websocket failure should not break flow
        pass

    # Email: send the full email body (background)
    try:
        user = db.query(User).filter(User.username == to_user).first()
        if user and user.email: # type: ignore
            if background_tasks:
                background_tasks.add_task(
                    send_email,
                    user.email,  # type: ignore
                    title,
                    email_body,
                    "Employee Personal Updates"  # type: ignore
                )
            else:
                send_email(
                    user.email,
                    title,
                    email_body,
                    "Employee Personal Updates"
                )
    except Exception:
        pass

    return db_notif


# -------------------------
# Helper functions to build messages
# -------------------------
def _full_name_of_user(db: Session, username: str) -> str:
    u = db.query(User).filter(User.username == username).first()
    if not u:
        return username
    return f"{(u.first_name or '').strip()} {(u.last_name or '').strip()}".strip()


# -------------------------
# HR notifications
# -------------------------
async def notify_hr_first_time_update(db: Session, employee_username: str, hr_username: str, sections: list[str], bg: BackgroundTasks):
    # Build texts
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "Review Employee Updated Details"
    notif_description = f"{emp_full} has updated {', '.join(sections)}."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has updated {', '.join(sections)}. Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Employee Personal Information",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_status="Pending Approval",
        background_tasks=bg
    )


async def notify_hr_section_update(db: Session, employee_username: str, hr_username: str, section: str, bg: BackgroundTasks):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = f"Review {section} Updated"
    notif_description = f"{emp_full} has updated {section}."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has updated {section}. Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Employee Personal Information",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_status=f"Pending Approval {section}",
        background_tasks=bg
    )


# -------------------------
# Employee notifications on HR decision
# -------------------------
async def notify_employee_on_status_change(db: Session, employee_username: str, hr_username: str, new_status: str, comments: str | None, bg: BackgroundTasks):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    status_clean = new_status.capitalize()
    title = f"Employee Details {status_clean}"

    if new_status.lower() == "changes requested":
        # Notification: short, NO reason (as requested)
        notif_description = f"Dear {emp_full}, your profile update was rejected by {hr_full}."

        # Email: detailed with reason
        reason_text = f"\n\nReason: {comments}" if comments else ""
        email_body = (
            f"Dear {emp_full},\n\n"
            f"Your profile update was Rejected by {hr_full}."
            f"{reason_text}\n\n"
            f"Regards,\nHR System"
        )
    else:
        notif_description = f"Dear {emp_full}, your profile update was approved by {hr_full}."
        email_body = (
            f"Dear {emp_full},\n\n"
            f"Your profile update has been Approved by {hr_full}.\n\n"
            f"Regards,\nHR System"
        )

    await send_employee_notification(
        db=db,
        type="Employee Personal Information",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=hr_username,
        to_user=employee_username,
        module_status=new_status,
        background_tasks=bg
    )


# -------------------------
# MASTER handler
# -------------------------
async def handle_employee_update_notifications(
    db: Session,
    *,
    old_status: str | None,
    new_status: str | None,
    old_comments: str | None,
    new_comments: str | None,
    employee_username: str,
    changed_sections: list[str],
    bg: BackgroundTasks
):
    """
    Centralized notification handler.
    - Router provides changed_sections (list of strings; for education/family router pass ["Education"] / ["Family"])
    - old_status = user's status before the operation
    - new_status = user's status after operation (could be "Pending Approval", "Pending Approval Education", "approved", "rejected", etc.)
    - new_comments = user's current comments (new HR comments after HR action) - used when notifying employee on HR decision
    """

    old_s = (old_status or "").strip().lower()
    new_s = (new_status or "").strip().lower()

    # fetch HR (role_id == 7)
    # fetch HR (from role_permissions where submenu_id=6 and role_id=7)
    from app.models.RolePermissionModel import RolePermission

    rp = (
        db.query(RolePermission)
        .filter(
            RolePermission.submenu_id == 6,
            RolePermission.role_id == 7
        )
        .first()
    )

    if not rp or not rp.user:
        return

    hr_username = rp.user.username


    # helper to extract a section from "pending approval <section>"
    def parse_pending_section(s: str) -> str | None:
        prefix = "pending approval"
        if not s:
            return None
        if s.startswith(prefix):
            sec = s[len(prefix):].strip()
            return sec if sec else None
        return None

    pending_section = parse_pending_section(new_s)

    # -------------------------
    # 1) new_status indicates pending approval explicitly
    # -------------------------
    if new_s.startswith("pending approval"):
        if pending_section:
            # send notifications only for the explicit section
            for sec in changed_sections:
                if sec.lower() == pending_section.lower():
                    await notify_hr_section_update(db, employee_username, hr_username, sec, bg)
            # if changed_sections doesn't include requested section, still send one notif for it:
            if not any(s.lower() == pending_section.lower() for s in changed_sections):
                await notify_hr_section_update(db, employee_username, hr_username, pending_section, bg)
            return

        # generic "Pending Approval" with changed_sections present
        if changed_sections:
            if old_s in ("", "null", None):
                await notify_hr_first_time_update(db, employee_username, hr_username, changed_sections, bg)
                return
            for sec in changed_sections:
                await notify_hr_section_update(db, employee_username, hr_username, sec, bg)
            return

        # fallback: notify HR unified
        await notify_hr_first_time_update(db, employee_username, hr_username, [], bg)
        return

    # -------------------------
    # 2) First-time update (old status empty) & changed_sections exist
    # -------------------------
    if old_s in ("", "null", None) and changed_sections:
        await notify_hr_first_time_update(db, employee_username, hr_username, changed_sections, bg)
        return

    # -------------------------
    # 3) Resubmit after rejection & changed_sections exist
    # -------------------------
    if old_s == "rejected" and changed_sections:
        for sec in changed_sections:
            await notify_hr_section_update(db, employee_username, hr_username, sec, bg)
        return

    # -------------------------
    # 4) Update after approved
    # -------------------------
    if old_s == "approved" and changed_sections:
        for sec in changed_sections:
            await notify_hr_section_update(db, employee_username, hr_username, sec, bg)

    # -------------------------
    # 5) HR decision changed -> notify employee once (approved/rejected)
    # -------------------------
    if new_s and old_s != new_s:
        if new_s in ("approved", "rejected"):
            await notify_employee_on_status_change(
                db,
                employee_username,
                hr_username,
                new_s,
                comments=new_comments,
                bg=bg
            )
            return

    # Nothing to do
    return




async def notify_hr_finance_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "New Investment Declaration Submitted"

    notif_description = f"{emp_full} has submitted Investment Declaration."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has submitted Investment Declaration. Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Investment Declaration",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_name="Investment Declaration",
        module_status="Pending Approval",
        background_tasks=bg
    )


async def notify_hr_form12c_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "New Form 12C Submitted"

    notif_description = f"{emp_full} has submitted Form 12C."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has submitted Form 12C. Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Form 12C",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_name="Form 12C",
        module_status="Pending Approval",
        background_tasks=bg
    )


async def notify_hr_asset_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "New Asset Declaration Submitted"

    notif_description = f"{emp_full} has submitted Asset Declaration."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has submitted Asset Declaration. Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Asset Declaration",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_name="Asset Declaration",
        module_status="Pending Approval",
        background_tasks=bg
    )


# -------------------------
# MAIN handler for Asset / Finance / Form12C
# -------------------------
async def handle_employee_form_submission(
    db: Session,
    *,
    employee_username: str,
    form_name: str,              # "Asset Declaration" / "Investment Declaration" / "Form 12C"
    status: str,
    bg: BackgroundTasks
):
    # fetch HR (role_id == 7)
# fetch HR (from role_permissions where submenu_id=6 and role_id=7)
    from app.models.RolePermissionModel import RolePermission

    rp = (
        db.query(RolePermission)
        .filter(
            RolePermission.submenu_id == 6,
            RolePermission.role_id == 7
        )
        .first()
    )

    if not rp or not rp.user:
        return

    hr_username = rp.user.username


    status_l = (status or "").strip().lower()

    # -------------------------
    # SEND TO HR — Pending Approval
    # -------------------------
    if status_l == "pending approval":

        if form_name == "Asset Declaration":
            await notify_hr_asset_update(db, employee_username, hr_username, bg)

        elif form_name == "Investment Declaration":
            await notify_hr_finance_update(db, employee_username, hr_username, bg)

        elif form_name == "Form 12C":
            await notify_hr_form12c_update(db, employee_username, hr_username, bg)

        return

    # -------------------------
    # HR APPROVED — Notify Employee
    # -------------------------
    if status_l == "approved":
        emp_full = _full_name_of_user(db, employee_username)
        hr_full = _full_name_of_user(db, hr_username)

        title = f"{form_name} Approved"
        notif_description = (
            f"Dear {emp_full}, your {form_name} has been approved by {hr_full}."
        )
        email_body = (
            f"Dear {emp_full},\n\n"
            f"Your {form_name} has been reviewed and approved by {hr_full}.\n\n"
            f"Regards,\nHR System"
        )

        await send_employee_notification(
            db=db,
            type=form_name,
            title=title,
            email_body=email_body,
            notif_description=notif_description,
            from_user=hr_username,
            to_user=employee_username,
            module_name=form_name,
            module_status="Approved",
            background_tasks=bg
        )




