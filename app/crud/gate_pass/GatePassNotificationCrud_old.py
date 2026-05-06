# app/crud/gate_pass/GatePassNotificationCrud.py

from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User


# ============================================================
# Helper: extract real outward from nested SQL JSON
# ============================================================

def extract_outward(outward_dict):
    try:
        return outward_dict["data"]["outward"]
    except:
        return outward_dict


# ============================================================
# Create + save notification (DB)
# ============================================================

def create_gatepass_notification(db: Session, notification: NotificationCreate):
    from app.models.NotificationModel import Notification

    db_notif = Notification(
        type=notification.type,
        title=notification.title,
        description=notification.description,
        from_user=notification.from_user,
        to_user=notification.to_user,
        module_name=notification.module_name,      # NEW
        module_status=notification.module_status,  # NEW
        date=datetime.now(),
        is_read=False
    )

    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif


# ============================================================
# Generic sender (DB + WS + background email)
# ============================================================

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
    """Send notification to DB + WebSocket + email (background)"""

    # Build NotificationCreate payload (set module_name explicitly)
    data = NotificationCreate(
        type=type,
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name="gatepass",       # ✅ explicit module name
        module_status=module_status   # ✅ actual GatePass status from record
    )

    # Save to DB
    db_notif = create_gatepass_notification(db, data)

    # WebSocket push (include module fields)
    await manager.send_personal_message(to_user, {
        "id": db_notif.id,
        "type": db_notif.type,
        "title": db_notif.title,
        "description": db_notif.description,
        "from_user": db_notif.from_user,
        "to_user": db_notif.to_user,
        "module_name": db_notif.module_name,          # NEW
        "module_status": db_notif.module_status,      # NEW
        "date": str(db_notif.date),
    })

    # Background email
    # Background email
    user = db.query(User).filter(User.username == to_user).first()  # type: ignore
    if user and user.email:  # type: ignore
        background_tasks.add_task(
            send_email,
            user.email,  # to_email
            title,       # subject
            f"Dear {user.username},\n\n{description}\n\nRegards,\nPetronet GatePass System",
            "Gate Pass Management"  
        )



# ============================================================
# 1️⃣ Notify Approver on CREATE
# ============================================================

async def notify_approver_on_create(db: Session, outward, background_tasks: BackgroundTasks):
    o = extract_outward(outward)

    approver = db.query(User).filter(User.user_id == o.get("approver_id")).first()

    if not approver:
        print("❌ Approver not found")
        return

    await send_gatepass_notification(
        db=db,
        type="GatePass",
        title="New Gate Pass Requires Approval",
        description=f"Gate Pass {o['gate_pass_no']} is awaiting your approval.",
        from_user=o.get("created_by"),
        to_user=approver.username,  # type: ignore
        module_status=o.get("status", "Pending Approval"),  # status from record
        background_tasks=background_tasks
    )


# ============================================================
# 2️⃣ Approver → Pending Verification → Notify Security
# ============================================================

async def notify_security_on_pending_verification(db: Session, outward, background_tasks: BackgroundTasks):
    o = extract_outward(outward)

    # Convert station name → station_id
    from app.models.MOC.StationModel import Station

    station = (
        db.query(Station)
        .filter(Station.station_name.ilike(o.get("station", "")))
        .first()
    )

    if not station:
        print(f"❌ No station found for name {o.get('station')}")
        return

    station_id = station.station_id

    # Fetch security user (role_id = 6)
    security_user = (
        db.query(User)
        .filter(User.role_id == 6)
        .filter(User.station_id == station_id)
        .first()
    )

    if not security_user:
        print(f"❌ No security user found for station_id {station_id}")
        return

    # Send notification
    await send_gatepass_notification(
        db=db,
        type="GatePass",
        title="Gate Pass Pending Verification",
        description=f"Gate Pass {o['gate_pass_no']} is ready for verification.",
        from_user=o.get("updated_by", o.get("created_by")),
        to_user=security_user.username,  # type: ignore
        module_status=o.get("status", "Pending Verification"),
        background_tasks=background_tasks
    )


# ============================================================
# 3️⃣ Approver → Rejected → Notify Initiator
# ============================================================

async def notify_initiator_on_rejection(db: Session, outward, background_tasks: BackgroundTasks):
    o = extract_outward(outward)

    initiator = db.query(User).filter(User.username == o.get("created_by")).first()

    if initiator:
        await send_gatepass_notification(
            db=db,
            type="GatePass",
            title="Gate Pass Rejected",
            description=f"Your Gate Pass {o['gate_pass_no']} has been rejected.",
            from_user=o.get("updated_by", o.get("created_by")),
            to_user=initiator.username,  # type: ignore
            module_status=o.get("status", "Rejected"),
            background_tasks=background_tasks
        )


# ============================================================
# 4️⃣ Security → Verified → Notify Approver + Initiator
# ============================================================

async def notify_acknowledge_verified(db: Session, outward, background_tasks: BackgroundTasks):
    o = extract_outward(outward)

    # Notify approver
    approver = db.query(User).filter(User.user_id == o.get("approver_id")).first()
    if approver:
        await send_gatepass_notification(
            db=db,
            type="GatePass",
            title="Gate Pass Verified",
            description=f"Gate Pass {o['gate_pass_no']} has been verified.",
            from_user=o.get("updated_by", o.get("created_by")),
            to_user=approver.username,  # type: ignore
            module_status=o.get("status", "Verified"),
            background_tasks=background_tasks
        )

    # Notify initiator
    initiator = db.query(User).filter(User.username == o.get("created_by")).first()
    if initiator:
        await send_gatepass_notification(
            db=db,
            type="GatePass",
            title="Your Gate Pass is Verified",
            description=f"Gate Pass {o['gate_pass_no']} is verified by security.",
            from_user=o.get("updated_by", o.get("created_by")),
            to_user=initiator.username,  # type: ignore
            module_status=o.get("status", "Verified"),
            background_tasks=background_tasks
        )
