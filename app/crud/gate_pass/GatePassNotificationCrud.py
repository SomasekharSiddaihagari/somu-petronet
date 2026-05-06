import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from fastapi import BackgroundTasks
from app.models.gate_pass.inward_gate_pass import InwardGatePass
from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GatePassNotification")

ROLE_ID_SECURITY = 6
GATEPASS_SUBMENU_ID = 5


def extract_outward(outward_dict):

    logger.info("STEP 1: Extracting outward data")

    if not isinstance(outward_dict, dict):
        logger.warning("Outward data is not dictionary")
        return {}

    data = outward_dict.get("data")

    if isinstance(data, dict):
        logger.info("Nested outward data detected")
        return data.get("outward", outward_dict)

    return outward_dict


def create_gatepass_notification(db: Session, notification: NotificationCreate):

    from app.models.NotificationModel import Notification

    logger.info(f"STEP 2: Saving notification for user -> {notification.to_user}")

    db_notif = Notification(
        type=notification.type,
        title=notification.title,
        description=notification.description,
        from_user=notification.from_user,
        to_user=notification.to_user,
        module_name=notification.module_name,
        module_status=notification.module_status,
        date=datetime.now(),
        is_read=False
    )

    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)

    logger.info(f"Notification saved with ID -> {db_notif.id}")

    return db_notif


async def send_gatepass_notification(
    db: Session,
    *,
    type: str,
    title: str,
    description: str,
    from_user: str,
    to_user: str,
    module_status: str,
    background_tasks: BackgroundTasks
):

    logger.info(f"STEP 3: Preparing to send notification to -> {to_user}")

    if not to_user:
        logger.warning("Notification skipped: to_user empty")
        return

    data = NotificationCreate(
        type=type,
        title=title,
        description=description,
        from_user=from_user or "system",
        to_user=to_user,
        module_name="gatepass",
        module_status=module_status
    )

    db_notif = create_gatepass_notification(db, data)

    try:

        logger.info(f"STEP 4: Sending websocket notification to -> {to_user}")

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

        logger.info(f"Websocket sent successfully to {to_user}")

    except Exception as e:
        logger.error(f"Websocket failed for {to_user} -> {str(e)}")

    logger.info(f"STEP 5: Fetching user email for -> {to_user}")

    user = db.query(User).filter(User.username == to_user).first()

    if user and user.email and background_tasks:

        logger.info(f"Sending email notification to -> {user.email}")

        background_tasks.add_task(
            send_email,
            user.email,
            title,
            f"Dear {user.username},\n\n{description}\n\nRegards,\nGatePass System",
            "Gate Pass Management"
        )
    else:
        logger.info("Email not sent (user/email/background_tasks missing)")


# ================= INWARD FLOW =================


async def notify_inward_approver_on_create(
        db, inward_data, inward_id, background_tasks
    ):

    logger.info("INWARD FLOW STARTED -> notify approver")
    logger.info(f"Inward Data Received -> {inward_data}")
    logger.info(f"Inward ID -> {inward_id}")

    # Fetch gate pass
    inward = db.query(InwardGatePass).filter(
        InwardGatePass.inward_id == inward_id
    ).first()

    if not inward:
        logger.warning("Inward gate pass not found")
        return

    gate_pass_no = inward.gate_pass_no

    approver = db.query(User).filter(
        User.user_id == inward_data.get("approver_id")
    ).first()

    if not approver:
        logger.warning("Approver not found in DB")
        return

    logger.info(f"Approver found -> {approver.username}")

    await send_gatepass_notification(
        db=db,
        type="GatePass",
        title="Inward Gate Pass Pending Approval",
        description=f"Inward Gate Pass {gate_pass_no} requires your approval.",
        from_user=inward_data.get("created_by"),
        to_user=approver.username,
        module_status="Pending Approval",
        background_tasks=background_tasks
    )



async def notify_inward_initiator_on_status_change(
    db,
    inward_id,
    status,
    gate_pass_no,
    created_by,
    updated_by,
    background_tasks
):

    logger.info("INWARD STATUS UPDATE")
    logger.info(f"Status changed -> {status}")
    logger.info(f"Created by -> {created_by}")

    # ✅ Support both user_id (int/str) and username
    try:
        creator_id = int(created_by)
        initiator = db.query(User).filter(User.user_id == creator_id).first()
    except (ValueError, TypeError):
        initiator = db.query(User).filter(User.username == created_by).first()

    if not initiator:
        logger.warning("Initiator not found")
        return

    logger.info(f"Sending status notification to creator -> {initiator.username}")

    await send_gatepass_notification(
        db=db,
        type="GatePass",
        title=f"Inward Gate Pass {status}",
        description=f"Your Inward Gate Pass {gate_pass_no or inward_id} has been {status}.",
        from_user=updated_by,
        to_user=initiator.username,
        module_status=status,
        background_tasks=background_tasks
    )



# ================= OUTWARD FLOW =================


async def notify_approver_on_create(db, outward, background_tasks):

    logger.info("OUTWARD FLOW STARTED -> notify engineer")

    o = extract_outward(outward)

    logger.info(f"Outward data -> {o}")

    approver = db.query(User).filter(
        User.user_id == o.get("approver_id")
    ).first()

    if not approver:
        logger.warning("Approver not found")
        return

    logger.info(f"Engineer found -> {approver.username}")

    await send_gatepass_notification(
        db=db,
        type="GatePass",
        title="Outward Gate Pass Pending Engineer Review",
        description=f"Gate Pass {o.get('gate_pass_no')} requires your review.",
        from_user=o.get("created_by"),
        to_user=approver.username,
        module_status="Pending Engineer Review",
        background_tasks=background_tasks
    )


# ================= SECURITY NOTIFICATION =================

async def notify_initiator_on_rejection(db, outward, background_tasks):

    logger.info("OUTWARD -> Rejected Step")

    o = extract_outward(outward)

    created_by_id = o.get("created_by")
    gate_pass_no = o.get("gate_pass_no")

    creator = db.query(User).filter(User.user_id == created_by_id).first()

    if not creator:
        logger.warning("Creator not found")
        return

    logger.info(f"Sending rejection notification to -> {creator.username}")

    await send_gatepass_notification(
        db=db,
        type="GatePass",
        title="Outward Gate Pass Rejected",
        description=f"Your Gate Pass {gate_pass_no} has been rejected.",
        from_user=o.get("updated_by"),
        to_user=creator.username,
        module_status="Rejected",
        background_tasks=background_tasks
    )


async def notify_security_on_pending_verification(
        db,
        outward,
        background_tasks
):

    logger.info("OUTWARD -> Pending Verification Step")

    o = extract_outward(outward)

    created_by = (o.get("created_by") or "").strip()
    gate_pass_no = o.get("gate_pass_no", "")

    logger.info(f"Gate Pass -> {gate_pass_no}")
    logger.info(f"Created by -> {created_by}")

    # Try to get station_id from the gate pass data first
    station_name = o.get("station")
    station_id = None

    if station_name:
        from app.models.MOC.StationModel import Station
        station = db.query(Station).filter(Station.station_name.ilike(station_name.strip())).first()
        if station:
            station_id = station.station_id
            logger.info(f"Resolved station_id {station_id} from name '{station_name}'")

    # Fallback to creator's station if station_name didn't work
    if not station_id:
        creator = None
        try:
            creator_id = int(created_by)
            creator = db.query(User).filter(User.user_id == creator_id).first()
        except (ValueError, TypeError):
            creator = db.query(User).filter(User.username == created_by).first()

        if creator and creator.station_id:
            station_id = creator.station_id
            logger.info(f"Resolved station_id {station_id} from creator '{created_by}'")
        else:
            logger.warning(f"Could not resolve station for gate pass {gate_pass_no}")
            return

    logger.info(f"Fetching security users for station -> {station_id}")
    creator = db.query(User).filter(User.user_id == o.get("created_by")).first()

    if creator:

        logger.info(f"Sending acknowledgement to creator -> {creator.username}")

        await send_gatepass_notification(
            db=db,
            type="GatePass",
            title="Gate Pass Sent for Verification",
            description=f"Your Gate Pass {gate_pass_no} has been sent for security verification.",
            from_user=o.get("updated_by"),
            to_user=creator.username,
            module_status="Pending Verification",
            background_tasks=background_tasks
        )
    security_users = db.execute(
        text("""
            SELECT u.username, u.email
            FROM users u
            JOIN role_permissions rp ON rp.user_id = u.user_id
            WHERE rp.role_id = :role_id
              AND rp.submenu_id = :submenu_id
              AND u.station_id = :station_id
              AND u.is_deleted = false
        """),
        {
            "role_id": ROLE_ID_SECURITY,
            "submenu_id": GATEPASS_SUBMENU_ID,
            "station_id": station_id
        }
    ).fetchall()

    logger.info(f"Security users found -> {len(security_users)}")

    if not security_users:
        logger.warning("No security users available")
        return

    for security_user in security_users:

        logger.info(f"Sending verification notification to -> {security_user.username}")

        await send_gatepass_notification(
            db=db,
            type="GatePass",
            title="Gate Pass Pending Verification",
            description=f"Gate Pass {gate_pass_no} requires verification.",
            from_user=o.get("updated_by") or created_by,
            to_user=security_user.username,
            module_status="Pending Verification",
            background_tasks=background_tasks
        )




# ================= VERIFIED =================


async def notify_acknowledge_verified(db, outward, background_tasks):

    logger.info("OUTWARD -> Guard Verified Step")

    o = extract_outward(outward)

    gate_pass_no = o.get("gate_pass_no")

    created_by_id = o.get("created_by")
    approver_id = o.get("approver_id")

    users_to_notify = []

    # 1️⃣ Creator
    if created_by_id:
        creator = db.query(User).filter(User.user_id == created_by_id).first()

        if creator:
            users_to_notify.append(creator.username)
            logger.info(f"Creator found -> {creator.username}")
        else:
            logger.warning(f"Creator not found for ID -> {created_by_id}")

    # 2️⃣ Approver
    if approver_id:
        approver = db.query(User).filter(User.user_id == approver_id).first()

        if approver:
            users_to_notify.append(approver.username)
            logger.info(f"Approver found -> {approver.username}")
        else:
            logger.warning(f"Approver not found for ID -> {approver_id}")

    # Remove duplicates
    users_to_notify = list(set(users_to_notify))

    logger.info(f"Users to notify -> {users_to_notify}")

    for username in users_to_notify:

        await send_gatepass_notification(
            db=db,
            type="GatePass",
            title="Gate Pass Guard Verified",
            description=f"Gate Pass {gate_pass_no} has been verified by security.",
            from_user=o.get("updated_by"),
            to_user=username,
            module_status="Guard Verified",
            background_tasks=background_tasks
        )
# ================= RETURNABLE FLOW =================


async def notify_returnable_approver_on_create(
    db,
    outward_id,
    approver_name,
    created_by,
    background_tasks
):

    logger.info("RETURNABLE FLOW STARTED")

    logger.info(f"Outward ID -> {outward_id}")
    logger.info(f"Approver -> {approver_name}")

    approver = db.query(User).filter(
        User.username == approver_name
    ).first()

    if not approver:
        logger.warning("Returnable approver not found")
        return

    logger.info(f"Engineer found -> {approver.username}")

    await send_gatepass_notification(
        db=db,
        type="GatePass",
        title="Returnable Gate Pass Created",
        description=f"Returnable Gate Pass for Outward ID {outward_id} requires your review.",
        from_user=created_by,
        to_user=approver.username,
        module_status="Returnable",
        background_tasks=background_tasks
    )




async def notify_returnable_on_status_change(
    db,
    outward_id,
    status,
    updated_by,
    background_tasks
):

    logger.info("RETURNABLE STATUS CHANGE")

    rgp = db.execute(
        text("""
            SELECT created_by, reviewer_id, returnable_gate_pass_no
            FROM returnable_gate_pass
            WHERE outward_id = :id
        """),
        {"id": outward_id}
    ).fetchone()

    if not rgp:
        logger.warning("Returnable gate pass not found")
        return

    created_by = rgp[0]
    reviewer_id = rgp[1]
    returnable_gate_pass_no = rgp[2]

    logger.info(f"Creator -> {created_by}")
    logger.info(f"Reviewer -> {reviewer_id}")
    logger.info(f"Status -> {status}")

    # ===============================
    # CASE 1 → Send to Reviewer
    # ===============================
    if status == "Returnable":

        reviewer = db.query(User).filter(User.user_id == reviewer_id).first()

        if not reviewer:
            logger.warning("Reviewer not found")
            return

        await send_gatepass_notification(
            db=db,
            type="GatePass",
            title="Returnable Gate Pass Pending Approval",
            description=f"Returnable Gate Pass {returnable_gate_pass_no} requires your review.",
            from_user=updated_by,
            to_user=reviewer.username,
            module_status="Returnable",
            background_tasks=background_tasks
        )

    # ===============================
    # CASE 2 → Reviewer Decision
    # ===============================
    elif status in ["Approved", "Returnable Rejected"]:

        creator = db.query(User).filter(User.user_id == created_by).first()

        if not creator:
            logger.warning("Creator not found")
            return

        await send_gatepass_notification(
            db=db,
            type="GatePass",
            title=f"Returnable Gate Pass {status}",
            description=f"Returnable Gate Pass {returnable_gate_pass_no} has been {status}.",
            from_user=updated_by,
            to_user=creator.username,
            module_status=status,
            background_tasks=background_tasks
        )