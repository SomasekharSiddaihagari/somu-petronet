
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


def create_notification(db: Session, data: NotificationCreate):
    from app.models.NotificationModel import Notification

    obj = Notification(
        type=data.type,
        title=data.title,
        description=data.description,
        from_user=data.from_user,
        to_user=data.to_user,
        module_name=data.module_name,        # NEW
        module_status=data.module_status,    # NEW
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





# WebSocket + DB save
async def _send_and_save(db: Session, to_user: str, msg: NotificationCreate):
    saved = create_notification(db, msg)
    await manager.send_personal_message(to_user, {
    "id": saved.id,
    "type": saved.type,
    "title": saved.title,
    "description": saved.description,
    "from_user": saved.from_user,
    "to_user": saved.to_user,
    "module_name": saved.module_name,       # NEW
    "module_status": saved.module_status,   # NEW
    "date": str(saved.date)
})



#  EMAIL HELPER
async def send_email_notification(
    background_tasks,
    subject,
    body,
    recipient,
    sender_name: str = "Management of Change (MOC)"
):
    background_tasks.add_task(
        send_email,
        recipient,
        subject,
        body,
        sender_name   
    )




#  1. HIRA Reviewer Notification (after CreateMocRequest)
async def notify_hira_reviewer(db, moc, reviewer, initiator, background_tasks):

    reviewer_name = reviewer.first_name or reviewer.username
    initiator_name = initiator.first_name or initiator.username

    msg = NotificationCreate(
    type="Review",
    title="New MOC Assigned for HIRA Review",
    description=f"MoC {moc.moc_request_no} requires HIRA review.",
    from_user=initiator.username,
    to_user=reviewer.username,
    module_name="moc",
    module_status="Pending HIRA Review",
)


    await _send_and_save(db, reviewer.username, msg)

    subject = f"New HIRA Review Assigned - {moc.moc_request_no}"
    body = f"""
Dear {reviewer_name},

You have been assigned a new HIRA review for {moc.moc_request_no}.

Please login to the MOC system to review it.

Regards,
{initiator_name}
"""

    await send_email_notification(background_tasks, subject, body, reviewer.email)



#  2. SIC Reviewer Notification
async def notify_sic_reviewer(db, moc, sic, updated_by_user, background_tasks):
    msg = NotificationCreate(
        type="Review",
        title="HIRA Review Completed",
        description=f"HIRA review completed. MoC {moc.moc_request_no} needs your SIC review.",
        from_user=updated_by_user.username,
        to_user=sic.username,
        module_name="moc",
        module_status="Pending Review",

    )

    await _send_and_save(db, sic.username, msg)

    subject = f"SIC Review Required - {moc.moc_request_no}"
    body = f"""
Dear {sic.first_name},

MoC {moc.moc_request_no} requires your SIC review.

Regards,  
{updated_by_user.first_name}
"""

    await send_email_notification(background_tasks, subject, body, sic.email)



# 3. Final Approver Notification
async def notify_final_approver(db, moc, approver, user, background_tasks):

    msg = NotificationCreate(
        type="Approval",
        title="MOC Sent for Final Approval",
        description=f"MOC {moc.moc_request_no} requires final approval.",
        from_user=user.username,
        to_user=approver.username,
        module_name="moc",
        module_status="Pending Approval",

    )

    await _send_and_save(db, approver.username, msg)

    subject = f"Final Approval Required - {moc.moc_request_no}"
    body = f"""
Dear {approver.first_name},

MoC {moc.moc_request_no} is ready for your final approval.

Regards,  
{user.first_name}{user.last_name}
"""

    await send_email_notification(background_tasks, subject, body, approver.email)



#  4. Notify Initiator (Approved / Rejected)
async def notify_initiator(db, moc, initiator, status, user, background_tasks):

    msg = NotificationCreate(
        type="Approval",
        title=f"MOC {status.capitalize()}",
        description=f"MOC {moc.moc_request_no} has been {status} by {user.username}",
        from_user=user.username,
        to_user=initiator.username,
        module_name="moc",
        module_status=status.capitalize(),

    )

    await _send_and_save(db, initiator.username, msg)

    subject = f"MOC {status.capitalize()} - {moc.moc_request_no}"
    body = f"""
Dear {initiator.first_name},

Your MOC {moc.moc_request_no} has been {status} by {user.first_name}.

Regards,  
MOC System
"""

    await send_email_notification(background_tasks, subject, body, initiator.email)



#  5. Notify Return to previous stage
async def notify_return(db, moc, receiver, user, background_tasks, status="Rejected"):
    """Notify users when MOC is returned, rejected, or change requested."""

    # Normalize status text
    status_text = status.lower().strip()

    # Choose title and message dynamically
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
        from_user=user.username,
        to_user=receiver.username,
        module_name="moc",
        module_status=status.capitalize(),

    )

    await _send_and_save(db, receiver.username, msg)

    subject = f"{title_text} - {moc.moc_request_no}"
    body = f"""
Dear {receiver_name},

MOC {moc.moc_request_no} has been {action_phrase} by {sender_name}.

Please check and update.

Regards,
MOC System
"""

    await send_email_notification(background_tasks, subject, body, receiver.email)



async def handle_moc_create_notifications(db, request, result, background_tasks):

    print(" SIMPLE NOTIFICATION MODE ENABLED")

    #  1. Get reviewer user using user_id (e.g. 18)
    reviewer: User = (
        db.query(User)
        .filter(User.user_id == request.hira_reviewer_id)
        .first()
    )
    if not reviewer:
        print(" Reviewer not found for user_id:", request.hira_reviewer_id)
        return

    print(" Reviewer fetched:", reviewer.username, reviewer.first_name)

    #  2. Get initiator user using username (e.g. Kiran)
    initiator: User = (
        db.query(User)
        .filter(User.username == request.created_by)
        .first()
    )
    if not initiator:
        print(" Initiator not found for username:", request.created_by)
        return

    print(" Initiator fetched:", initiator.username, initiator.first_name)

    #  3. Prepare MOC object (only storing request number)
    class MocObj:
        pass

    moc = MocObj()
    moc.moc_request_no = request.moc_request_no or "Unknown"
    print(" MOC Request No:", moc.moc_request_no)

    #  4. Notify HIRA Reviewer
    await notify_hira_reviewer(
        db=db,
        moc=moc,
        reviewer=reviewer,
        initiator=initiator,
        background_tasks=background_tasks
    )

    print(" Notification successfully sent to:", reviewer.username)



#  Safe helper to get a user's display name
def get_display_name(user):
    """Return full name if available, otherwise username."""
    if not user:
        return "User"
    full_name = " ".join(
        part for part in [user.first_name, user.last_name] if part
    ).strip()
    return full_name if full_name else user.username



# app/crud/notification_crud.py  (replace only this function)

async def handle_moc_status_notifications(db, request, updated_by, background_tasks):
    """
    Handles all notification + email workflows for MoC status changes.

    Forward flow:
        Initiator -> HIRA Reviewer (Engineer)       => Pending HIRA Review
        HIRA Reviewer -> SIC Reviewer               => Pending Review
        SIC Reviewer -> Head of Operations (Final)  => Pending Approval
        HOP (Approver) -> Closure                   => Closure Approved

    Reverse flow (Reject / Changes Request):
        HIRA Reviewer -> Initiator
        Final Reviewer -> HIRA Reviewer + Initiator
        Approver -> Final Reviewer + HIRA Reviewer + Initiator
    """

    try:
        #  Step 1: Identify who performed the update
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

        #  Step 2: Fetch the current MoC record
        moc = (
            db.query(MoCRequest)
            .filter(MoCRequest.moc_request_no == request.moc_request_no)
            .first()
        )
        if not moc:
            raise Exception(f"No MOC found for {request.moc_request_no}")

        #  Step 3: Get related users
        initiator = db.query(User).filter(User.username == moc.created_by).first()
        station = db.query(Station).filter(Station.station_name == moc.station_name).first()

        # HIRA Reviewer (Engineer)
        hira_entry = (
            db.query(HIRAEntry)
            .filter(HIRAEntry.moc_request_id == moc.moc_request_id)
            .order_by(HIRAEntry.hira_id.desc())  # latest HIRA
            .first()
        )

        hira_reviewer = None
        if hira_entry and hira_entry.hira_reviewer_id:
            hira_reviewer = (
                db.query(User)
                .filter(User.user_id == hira_entry.hira_reviewer_id)
                .first()
            )
            print(
                f"✅ Found HIRA reviewer from HIRAEntry: {hira_reviewer.username} "
                f"(ID={hira_reviewer.user_id}, Email={hira_reviewer.email})"
            )
        else:
            print(
                f"⚠️ No HIRAEntry with valid reviewer found for MOC ID={moc.moc_request_id}"
    )

        # SIC Reviewer (unique per station)
        sic_reviewer = (
            db.query(User)
            .filter(User.role_id == 2, User.station_id == station.station_id)
            .first()
        )

        if not sic_reviewer:
            print(f" No SIC reviewer found for station: {station.station_name}")
        else:
            print(f" Found SIC reviewer for station {station.station_name}: {sic_reviewer.username}")

        # Final Reviewer / Approver (Head of Operations)
        final_reviewer = (
            db.query(User)
            .filter(User.role_id == 3)
            .first()
        )

        #  Step 4: Determine current status
        status = request.status.strip() if request.status else ""
        print(f" handle_moc_status_notifications triggered for {moc.moc_request_no}, status={status}")

       # -------------------------------------------------------------------------
        # FORWARD WORKFLOW (with initiator notifications)
        # -------------------------------------------------------------------------
        if status.lower() == "pending review":
            # HIRA Reviewer -> SIC Reviewer
            if sic_reviewer:
                await notify_sic_reviewer(db, moc, sic_reviewer, user, background_tasks)
                print(f" Sent notification to SIC Reviewer: {sic_reviewer.username}")

            #  Also notify Initiator that MOC has been forwarded to SIC
            if initiator:
                msg_status = "sent for SIC review"
                await notify_initiator(db, moc, initiator, msg_status, user, background_tasks)
                print(f" Notified Initiator that MOC sent to SIC")

        elif status.lower() == "pending approval":
            # SIC Reviewer -> Final Reviewer (HOP)
            if final_reviewer:
                await notify_final_approver(db, moc, final_reviewer, user, background_tasks)
                print(f" Sent notification to Final Reviewer: {final_reviewer.username}")

            #  Also notify Initiator that MOC has been sent for approval
            if initiator:
                msg_status = "sent for final approval"
                await notify_initiator(db, moc, initiator, msg_status, user, background_tasks)
                print(f" Notified Initiator that MOC sent for final approval")

        elif status.lower() == "approved":
            # Approver -> All relevant users (Initiator, HIRA Reviewer, Final Reviewer)
            for receiver in [initiator, hira_reviewer, final_reviewer]:
                if not receiver:
                    continue

                receiver_name = get_display_name(receiver)
                sender_name = get_display_name(user)

                msg = NotificationCreate(
                    type="Approval",
                    title="MOC Approved",
                    description=f"MOC {moc.moc_request_no} has been approved by {sender_name}.",
                    from_user=user.username,
                    to_user=receiver.username,
                    module_name="moc",
                    module_status=status.capitalize(),
                )

                await _send_and_save(db, receiver.username, msg)

                subject = f"MOC Approved - {moc.moc_request_no}"
                body = f"""
        Dear {receiver_name},

        MOC {moc.moc_request_no} has been approved by {sender_name}.

        Regards,
        MOC System
        """
                await send_email_notification(background_tasks, subject, body, receiver.email)

            print(f"✅ Sent approval notifications to HIRA Reviewer, Final Reviewer, and Initiator.")



        # -------------------------------------------------------------------------
        #  REVERSE WORKFLOW (Reject / Changes Request)
        # -------------------------------------------------------------------------
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


        # -------------------------------------------------------------------------
        #  DEFAULT CATCH (if status doesn’t match known workflow)
        # -------------------------------------------------------------------------
        else:
            print(f" Unhandled status: {status}")

    except Exception as e:
        print(f" handle_moc_status_notifications failed: {e}")
        raise



async def notify_closure_completed(db, moc_closure, moc_request, user, background_tasks):
    """
    Notifies HIRA Reviewer, SIC Reviewer, and Approver when MOC is closed by Initiator.
    """
    try:
        from app.models.UserModel import User
        from app.models.MOC.StationModel import Station
        from app.models.MOC.HiraModel import HIRAEntry  # Add this import

        if not user:
            print(" Initiator user not provided. Skipping sender details.")
            sender_name = "Initiator"
            sender_username = "Unknown"
        else:
            sender_name = get_display_name(user)
            sender_username = user.username

        # Get the assigned HIRA reviewer from HIRAEntry
        hira_entry = (
            db.query(HIRAEntry)
            .filter(HIRAEntry.moc_request_id == moc_request.moc_request_id)
            .order_by(HIRAEntry.hira_id.desc())  # Get the latest entry
            .first()
        )

        print(f"Found HIRA entry for MOC {moc_request.moc_request_id}: {hira_entry.hira_id if hira_entry else 'None'}")

        # Get HIRA reviewer from the entry
        hira_reviewer = None
        if hira_entry and hira_entry.hira_reviewer_id:
            hira_reviewer = db.query(User).filter(User.user_id == hira_entry.hira_reviewer_id).first()
            print(f"Found HIRA reviewer: {hira_reviewer.username if hira_reviewer else 'None'}")

        # Fetch station for this MOC
        station = db.query(Station).filter(
            Station.station_name == moc_request.station_name
        ).first()

        if not station:
            print(f" No station found for MOC {moc_request.moc_request_no}")
            return

        # Get SIC Reviewer for this station
        sic_reviewer = (
            db.query(User)
            .filter(User.role_id == 2, User.station_id == station.station_id)
            .first()
        )

        # Get the approver (role_id = 3)
        approver = db.query(User).filter(User.role_id == 3).first()

        receivers = [hira_reviewer, sic_reviewer, approver]
        print(f"Sending notifications to: HIRA={hira_reviewer.username if hira_reviewer else 'None'}, "
              f"SIC={sic_reviewer.username if sic_reviewer else 'None'}, "
              f"Approver={approver.username if approver else 'None'}")

        for receiver in receivers:
            if not receiver:
                continue  # Skip missing users safely

            receiver_name = get_display_name(receiver)
            print(f"Sending notification to {receiver.username} ({receiver_name})")

            msg = NotificationCreate(
                type="Closure",
                title="MOC Closed",
                description=f"MOC {moc_request.moc_request_no} has been closed by {sender_name}.",
                from_user=sender_username,
                to_user=receiver.username,
                module_name="moc",
                module_status="Closed",
            )

            # Save + send notification
            await _send_and_save(db, receiver.username, msg)

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
        print(f" notify_closure_completed failed: {str(e)}")