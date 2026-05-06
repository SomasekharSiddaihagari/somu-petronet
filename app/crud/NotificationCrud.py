from sqlalchemy.orm import Session
from datetime import datetime
from app.core.Websocket import manager
from app.schemas.NotificationSchema import NotificationCreate
from app.models.MOC.MocRequestModel import MoCRequest
from app.models.MOC.HiraModel import HIRAEntry
from app.models.UserModel import User
from app.utils.EmailUtils import send_email
from app.models.MOC.StationModel import Station
from app.models.NotificationModel import Notification


# ─── Safe Helpers ─────────────────────────────────────────────────────────────

def safe_username(u) -> str:
    """Returns a non-None string identifier for a User object."""
    if u is None:
        return ""
    return u.username or u.email or str(u.user_id)


def get_display_name(user) -> str:
    """Return full name if available, otherwise username or email."""
    if not user:
        return "User"
    full_name = " ".join(
        part for part in [user.first_name, user.last_name] if part
    ).strip()
    return full_name if full_name else (user.username or user.email or str(user.user_id))


# ─── DB CRUD ──────────────────────────────────────────────────────────────────

def create_notification(db: Session, data: NotificationCreate):
    obj = Notification(
        type=data.type,
        title=data.title,
        description=data.description,
        from_user=data.from_user,
        to_user=data.to_user,
        module_name=data.module_name,
        module_status=data.module_status,
        date=datetime.now(),
        is_read=False
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


from app.schemas.NotificationSchema import NotificationUpdate

def update_notification(db: Session, notification_id: int, data: NotificationUpdate):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(notif, field, value)
    db.commit()
    db.refresh(notif)
    return notif


# ─── Core Send ────────────────────────────────────────────────────────────────

async def _send_and_save(db: Session, to_user: str, msg: NotificationCreate):
    try:
        saved = create_notification(db, msg)
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
    except Exception as e:
        print(f"⚠️ _send_and_save failed for '{to_user}': {e}")
        # WebSocket failure is non-fatal — notification is already saved in DB


async def send_email_notification(
    background_tasks,
    subject,
    body,
    recipient,
    sender_name: str = "Management of Change (MOC)"
):
    background_tasks.add_task(send_email, recipient, subject, body, sender_name)


# ─── Notification Helpers ─────────────────────────────────────────────────────

# 1. HIRA Reviewer Notification
async def notify_hira_reviewer(db, moc, reviewer, initiator, background_tasks):
    reviewer_name = get_display_name(reviewer)
    initiator_name = get_display_name(initiator)

    msg = NotificationCreate(
        type="Review",
        title="New MOC Assigned for HIRA Review",
        description=f"MoC {moc.moc_request_no} requires HIRA review.",
        from_user=safe_username(initiator),   # ✅ fixed
        to_user=safe_username(reviewer),      # ✅ fixed
        module_name="moc",
        module_status="Pending HIRA Review",
    )

    await _send_and_save(db, safe_username(reviewer), msg)

    subject = f"New HIRA Review Assigned - {moc.moc_request_no}"
    body = f"""
Dear {reviewer_name},

You have been assigned a new HIRA review for {moc.moc_request_no}.

Please login to the MOC system to review it.

Regards,
{initiator_name}
"""
    await send_email_notification(background_tasks, subject, body, reviewer.email)


# 2. SIC Reviewer Notification
async def notify_sic_reviewer(db, moc, sic, updated_by_user, background_tasks):
    sic_name = get_display_name(sic)
    sender_name = get_display_name(updated_by_user)

    msg = NotificationCreate(
        type="Review",
        title="HIRA Review Completed",
        description=f"HIRA review completed. MoC {moc.moc_request_no} needs your SIC review.",
        from_user=safe_username(updated_by_user),  # ✅ fixed
        to_user=safe_username(sic),                # ✅ fixed
        module_name="moc",
        module_status="Pending Review",
    )

    await _send_and_save(db, safe_username(sic), msg)

    subject = f"SIC Review Required - {moc.moc_request_no}"
    body = f"""
Dear {sic_name},

MoC {moc.moc_request_no} requires your SIC review.

Regards,
{sender_name}
"""
    await send_email_notification(background_tasks, subject, body, sic.email)


# 3. Final Approver Notification
async def notify_final_approver(db, moc, approver, user, background_tasks):
    approver_name = get_display_name(approver)
    sender_name = get_display_name(user)

    msg = NotificationCreate(
        type="Approval",
        title="MOC Sent for Final Approval",
        description=f"MOC {moc.moc_request_no} requires final approval.",
        from_user=safe_username(user),      # ✅ fixed
        to_user=safe_username(approver),    # ✅ fixed
        module_name="moc",
        module_status="Pending Approval",
    )

    await _send_and_save(db, safe_username(approver), msg)

    subject = f"Final Approval Required - {moc.moc_request_no}"
    body = f"""
Dear {approver_name},

MoC {moc.moc_request_no} is ready for your final approval.

Regards,
{sender_name}
"""
    await send_email_notification(background_tasks, subject, body, approver.email)


# 4. Notify Initiator
async def notify_initiator(db, moc, initiator, status, user, background_tasks):
    initiator_name = get_display_name(initiator)
    sender_name = get_display_name(user)

    msg = NotificationCreate(
        type="Approval",
        title=f"MOC {status.capitalize()}",
        description=f"MOC {moc.moc_request_no} has been {status} by {sender_name}",
        from_user=safe_username(user),       # ✅ fixed
        to_user=safe_username(initiator),    # ✅ fixed
        module_name="moc",
        module_status=status.capitalize(),
    )

    await _send_and_save(db, safe_username(initiator), msg)

    subject = f"MOC {status.capitalize()} - {moc.moc_request_no}"
    body = f"""
Dear {initiator_name},

Your MOC {moc.moc_request_no} has been {status} by {sender_name}.

Regards,
MOC System
"""
    await send_email_notification(background_tasks, subject, body, initiator.email)


# 5. Notify Return (Rejected / Changes Requested)
async def notify_return(db, moc, receiver, user, background_tasks, status="Rejected"):
    status_text = status.lower().strip()

    if "change" in status_text:
        action_phrase = "requested for changes"
        title_text = "MOC Changes Requested"
    elif "reject" in status_text:
        action_phrase = "rejected"
        title_text = "MOC Rejected"
    else:
        action_phrase = "returned"
        title_text = "MOC Returned"

    receiver_name = get_display_name(receiver)
    sender_name = get_display_name(user)

    msg = NotificationCreate(
        type="Return",
        title=title_text,
        description=f"MOC {moc.moc_request_no} has been {action_phrase} by {sender_name}",
        from_user=safe_username(user),      # ✅ fixed
        to_user=safe_username(receiver),    # ✅ fixed
        module_name="moc",
        module_status=status.capitalize(),
    )

    await _send_and_save(db, safe_username(receiver), msg)

    subject = f"{title_text} - {moc.moc_request_no}"
    body = f"""
Dear {receiver_name},

MOC {moc.moc_request_no} has been {action_phrase} by {sender_name}.

Please check and update.

Regards,
MOC System
"""
    await send_email_notification(background_tasks, subject, body, receiver.email)


# ─── Handle MOC Create ────────────────────────────────────────────────────────

async def handle_moc_create_notifications(db, request, result, background_tasks):
    print("🔔 SIMPLE NOTIFICATION MODE ENABLED")

    reviewer: User = db.query(User).filter(User.user_id == request.hira_reviewer_id).first()
    if not reviewer:
        print("❌ Reviewer not found for user_id:", request.hira_reviewer_id)
        return
    print("✅ Reviewer fetched:", safe_username(reviewer), reviewer.first_name)

    initiator: User = db.query(User).filter(User.username == request.created_by).first()
    if not initiator:
        print("❌ Initiator not found for username:", request.created_by)
        return
    print("✅ Initiator fetched:", safe_username(initiator), initiator.first_name)

    class MocObj:
        pass

    moc = MocObj()
    moc.moc_request_no = request.moc_request_no or "Unknown"

    await notify_hira_reviewer(db=db, moc=moc, reviewer=reviewer, initiator=initiator, background_tasks=background_tasks)
    print("✅ Notification successfully sent to:", safe_username(reviewer))


# ─── Handle MOC Status Change ─────────────────────────────────────────────────

async def handle_moc_status_notifications(db, request, updated_by, background_tasks):
    try:
        # Step 1: Resolve the user who made the update
        updated_by_username = None
        updated_by_user_id = None

        if isinstance(updated_by, dict):
            updated_by_username = updated_by.get("username")
            updated_by_user_id = updated_by.get("user_id")
        else:
            updated_by_username = updated_by

        user = None
        if updated_by_username and str(updated_by_username).isdigit():
            user = db.query(User).filter(User.user_id == int(updated_by_username)).first()
        elif updated_by_user_id:
            user = db.query(User).filter(User.user_id == int(updated_by_user_id)).first()
        else:
            user = db.query(User).filter(User.username == updated_by_username).first()

        if not user:
            raise Exception(f"User not found: {updated_by_username}")

        sender_identifier = safe_username(user)   # ✅ never None
        sender_name = get_display_name(user)

        # Step 2: Fetch MOC record
        moc = db.query(MoCRequest).filter(MoCRequest.moc_request_no == request.moc_request_no).first()
        if not moc:
            raise Exception(f"No MOC found for {request.moc_request_no}")

        # Step 3: Fetch related users
        initiator = db.query(User).filter(User.username == moc.created_by).first()

        hira_entry = (
            db.query(HIRAEntry)
            .filter(HIRAEntry.moc_request_id == moc.moc_request_id)
            .order_by(HIRAEntry.hira_id.desc())
            .first()
        )

        hira_reviewer = None
        if hira_entry and hira_entry.hira_reviewer_id:
            hira_reviewer = db.query(User).filter(User.user_id == hira_entry.hira_reviewer_id).first()
            print(f"✅ HIRA reviewer: {safe_username(hira_reviewer)} (ID={hira_reviewer.user_id})")
        else:
            print(f"⚠️ No HIRAEntry reviewer for MOC ID={moc.moc_request_id}")

        from app.models.RolePermissionModel import RolePermission

        sic_reviewer = (
            db.query(User)
            .join(RolePermission, RolePermission.user_id == User.user_id)
            .filter(RolePermission.role_id == 2, RolePermission.submenu_id == 2)
            .order_by(User.user_id.asc())
            .first()
        )

        if not sic_reviewer:
            print("❌ No SIC reviewer found")
        else:
            print(f"✅ SIC reviewer: {safe_username(sic_reviewer)} (ID={sic_reviewer.user_id})")

        final_reviewer = db.query(User).filter(User.role_id == 3).first()

        # Step 4: Route by status
        status = request.status.strip() if request.status else ""
        print(f"🔔 Status notification triggered: {moc.moc_request_no} => {status}")

        # ── Forward Workflow ───────────────────────────────────────────────────
        if status.lower() == "pending review":
            if sic_reviewer:
                await notify_sic_reviewer(db, moc, sic_reviewer, user, background_tasks)
                print(f"✅ Notified SIC Reviewer: {safe_username(sic_reviewer)}")
            if initiator:
                await notify_initiator(db, moc, initiator, "sent for SIC review", user, background_tasks)
                print("✅ Notified Initiator: MOC sent to SIC")

        elif status.lower() == "pending approval":
            if final_reviewer:
                await notify_final_approver(db, moc, final_reviewer, user, background_tasks)
                print(f"✅ Notified Final Reviewer: {safe_username(final_reviewer)}")
            if initiator:
                await notify_initiator(db, moc, initiator, "sent for final approval", user, background_tasks)
                print("✅ Notified Initiator: MOC sent for final approval")

        elif status.lower() == "approved":
            for receiver in [initiator, hira_reviewer, final_reviewer]:
                if not receiver:
                    continue
                receiver_name = get_display_name(receiver)
                receiver_identifier = safe_username(receiver)   # ✅ fixed

                msg = NotificationCreate(
                    type="Approval",
                    title="MOC Approved",
                    description=f"MOC {moc.moc_request_no} has been approved by {sender_name}.",
                    from_user=sender_identifier,      # ✅ fixed
                    to_user=receiver_identifier,      # ✅ fixed
                    module_name="moc",
                    module_status=status.capitalize(),
                )
                await _send_and_save(db, receiver_identifier, msg)

                subject = f"MOC Approved - {moc.moc_request_no}"
                body = f"""
Dear {receiver_name},

MOC {moc.moc_request_no} has been approved by {sender_name}.

Regards,
MOC System
"""
                await send_email_notification(background_tasks, subject, body, receiver.email)

            print("✅ Approval notifications sent to all parties.")

        # ── Reverse Workflow ───────────────────────────────────────────────────
        elif status.lower() in ["rejected", "changes request"]:
            user_role_id = user.role_id

            if user_role_id == 1:
                if initiator:
                    await notify_initiator(db, moc, initiator, status, user, background_tasks)

            elif user_role_id == 2:
                for receiver in [hira_reviewer, initiator]:
                    if receiver:
                        await notify_return(db, moc, receiver, user, background_tasks, status)

            elif user_role_id == 3:
                for receiver in [final_reviewer, hira_reviewer, initiator]:
                    if receiver:
                        await notify_return(db, moc, receiver, user, background_tasks, status)
        elif status.lower() == "pending hira review":
            print("🚀 Triggering HIRA notification flow")

            if hira_reviewer:
                await notify_hira_reviewer(
                    db=db,
                    moc=moc,
                    reviewer=hira_reviewer,   # ✅ FIXED
                    initiator=initiator,
                    background_tasks=background_tasks
                )
                print(f"✅ Notification sent to HIRA Reviewer: {hira_reviewer.username}")
            else:
                print("❌ HIRA reviewer not found")

            # Optional but recommended: notify initiator also
            if initiator:
                await notify_initiator(
                    db=db,
                    moc=moc,
                    initiator=initiator,
                    status="Pending HIRA Review",
                    user=user,
                    background_tasks=background_tasks
                )
                print("✅ Initiator notified")
        elif status.lower() == "closure approved":
            print("🚀 Triggering CLOSURE notification flow")

            # call your closure function
            await notify_closure_completed(
                db=db,
                moc_closure=None,      # if you have closure table, pass it
                moc_request=moc,
                user=user,
                background_tasks=background_tasks
            )

            print(f"✅ Closure notifications sent for {moc.moc_request_no}")
        else:
            print(f"⚠️ Unhandled status: {status}")

    except Exception as e:
        print(f"❌ handle_moc_status_notifications failed: {e}")
        raise


# ─── Closure Notification ─────────────────────────────────────────────────────

async def notify_closure_completed(db, moc_closure, moc_request, user, background_tasks):
    try:
        sender_name = get_display_name(user) if user else "Initiator"
        sender_identifier = safe_username(user) if user else "unknown"   # ✅ fixed

        hira_entry = (
            db.query(HIRAEntry)
            .filter(HIRAEntry.moc_request_id == moc_request.moc_request_id)
            .order_by(HIRAEntry.hira_id.desc())
            .first()
        )
        print(f"HIRA entry for MOC {moc_request.moc_request_id}: {hira_entry.hira_id if hira_entry else 'None'}")

        hira_reviewer = None
        if hira_entry and hira_entry.hira_reviewer_id:
            hira_reviewer = db.query(User).filter(User.user_id == hira_entry.hira_reviewer_id).first()
            print(f"HIRA reviewer: {safe_username(hira_reviewer)}")

        station = db.query(Station).filter(Station.station_name == moc_request.station_name).first()
        if not station:
            print(f"❌ No station found for MOC {moc_request.moc_request_no}")
            return

        sic_reviewer = db.query(User).filter(User.role_id == 2, User.station_id == station.station_id).first()
        approver = db.query(User).filter(User.role_id == 3).first()

        print(
            f"Notifying: HIRA={safe_username(hira_reviewer)}, "
            f"SIC={safe_username(sic_reviewer)}, "
            f"Approver={safe_username(approver)}"
        )

        for receiver in [hira_reviewer, sic_reviewer, approver]:
            if not receiver:
                continue

            receiver_name = get_display_name(receiver)
            receiver_identifier = safe_username(receiver)   # ✅ fixed

            msg = NotificationCreate(
                type="Closure",
                title="MOC Closed",
                description=f"MOC {moc_request.moc_request_no} has been closed by {sender_name}.",
                from_user=sender_identifier,      # ✅ fixed
                to_user=receiver_identifier,      # ✅ fixed
                module_name="moc",
                module_status="Closed",
            )

            await _send_and_save(db, receiver_identifier, msg)

            subject = f"MOC Closed - {moc_request.moc_request_no}"
            body = f"""
Dear {receiver_name},

MOC {moc_request.moc_request_no} has been closed by {sender_name}.

Please review the closure details in the MOC system.

Regards,
{sender_name}
"""
            await send_email_notification(background_tasks, subject, body, receiver.email)

        print(f"✅ Closure notifications sent for {moc_request.moc_request_no}")

    except Exception as e:
        print(f"❌ notify_closure_completed failed: {str(e)}")