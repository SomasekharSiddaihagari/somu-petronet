from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from datetime import datetime
from typing import List, Set

from app.models.NotificationModel import Notification
from app.models.UserModel import User
from app.models.circular_mangement.circular_user_activity import CircularUserActivity
from app.models.circular_mangement.group_master import GroupMaster
from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email


# ============================================================
# Create Notification Entry
# ============================================================

# def create_circular_notification(db: Session, data: NotificationCreate):
#     notif = Notification(
#         type="Circular",
#         title=data.title,
#         description=data.description,
#         from_user=data.from_user,
#         to_user=data.to_user,
#         module_name="circular",
#         module_status="Created",
#         date=datetime.utcnow(),
#         is_read=False
#     )
#     db.add(notif)
#     db.commit()
#     db.refresh(notif)
#     return notif


# # ============================================================
# # Notify Group Users (Optimized)
# # ============================================================

# async def notify_group_users_for_circular(
#     db: Session,
#     *,
#     group_ids: List[int],
#     circular_title: str,
#     created_by_user_id: int,
#     background_tasks: BackgroundTasks
# ):

#     # 🔹 Step 1: Fetch groups
#     groups = db.query(GroupMaster).filter(
#         GroupMaster.group_id.in_(group_ids),
#         GroupMaster.is_deleted == False
#     ).all()

#     if not groups:
#         return

#     # 🔹 Step 2: Collect all employee_ids
#     all_user_ids: Set[int] = set()

#     for group in groups:
#         if group.employee_ids:
#             all_user_ids.update(group.employee_ids)

#     if not all_user_ids:
#         return

#     # 🔹 Step 3: Fetch all users in one query
#     users = db.query(User).filter(
#         User.user_id.in_(list(all_user_ids)),
#         User.is_deleted == False
#     ).all()

#     if not users:
#         return

#     # 🔹 Get creator username
#     creator = db.query(User).filter(
#         User.user_id == created_by_user_id
#     ).first()

#     from_username = creator.username if creator else "system"

#     # 🔹 Step 4: Send notification
#     for user in users:

#         data = NotificationCreate(
#             type="Circular",
#             title="New Circular Published",
#             description=f"A new circular '{circular_title}' has been published for your group.",
#             from_user=from_username,
#             to_user=user.username,
#             module_name="circular",
#             module_status="Created"
#         )

#         notif = create_circular_notification(db, data)

#         # WebSocket
#         await manager.send_personal_message(user.username, {
#             "id": notif.id,
#             "title": notif.title,
#             "description": notif.description,
#             "module_status": notif.module_status,
#             "date": str(notif.date)
#         })

#         # Email
#         if user.email:
#             full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
#             background_tasks.add_task(
#                 send_email,
#                 user.email,
#                 "New Circular Published",
#                 f"Dear {full_name or user.username},\n\n"
#                 f"A new circular '{circular_title}' has been published for your group.\n\n"
#                 "Regards,\nPetronet",
#                 "Circular Notification"
#             )


# new code

def create_circular_notification(db: Session, data: NotificationCreate):
    notif = Notification(
        type="Circular",
        title=data.title,
        description=data.description,
        from_user=data.from_user,
        to_user=data.to_user,
        module_name="circular",
        module_status="Created",
        date=datetime.now(),
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


# ============================================================
# MAIN UNIVERSAL HANDLER
# ============================================================

async def notify_circular_target_audience(
    db: Session,
    *,
    target_audience: List[dict],
    circular_title: str,
    created_by_user_id: int,
    background_tasks: BackgroundTasks
):
    """
    Handles:
    - GROUP
    - INDIVIDUAL
    - STATION
    """

    all_user_ids: Set[int] = set()

    # ========================================================
    # LOOP THROUGH TARGET AUDIENCE
    # ========================================================

    for audience in target_audience:

        audience_type = audience.get("audience_type")
        ref_ids = audience.get("audience_ref_id", [])

        # ----------------------------------------------------
        # 🔵 GROUP
        # ----------------------------------------------------
        if audience_type == "GROUP":

            groups = db.query(GroupMaster).filter(
                GroupMaster.group_id.in_(ref_ids),
                GroupMaster.is_deleted == False
            ).all()

            for group in groups:
                if group.employee_ids:
                    all_user_ids.update(group.employee_ids)

        # ----------------------------------------------------
        # 🟢 INDIVIDUAL
        # ----------------------------------------------------
        elif audience_type == "INDIVIDUAL":

            # Here audience_ref_id already contains user_ids
            all_user_ids.update(ref_ids)

        # ----------------------------------------------------
        # 🟡 STATION
        # ----------------------------------------------------
        elif audience_type == "STATION":

            station_users = db.query(User).filter(
                User.station_id.in_(ref_ids),
                User.is_deleted == False
            ).all()

            for user in station_users:
                all_user_ids.add(user.user_id)

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    if not all_user_ids:
        return

    users = db.query(User).filter(
        User.user_id.in_(list(all_user_ids)),
        User.is_deleted == False
    ).all()

    if not users:
        return

    # Get creator username
    creator = db.query(User).filter(
        User.user_id == created_by_user_id
    ).first()

    from_username = creator.username if creator else "system"

    # ========================================================
    # SEND NOTIFICATIONS
    # ========================================================

    for user in users:

        if not user.username:
            continue

        data = NotificationCreate(
            type="Circular",
            title="New Circular Published",
            description=f"A new circular '{circular_title}' has been published.",
            from_user=from_username,
            to_user=user.username,
            module_name="circular",
            module_status="Created"
        )

        notif = create_circular_notification(db, data)

        # WebSocket
        await manager.send_personal_message(user.username, {
            "id": notif.id,
            "title": notif.title,
            "description": notif.description,
            "module_status": notif.module_status,
            "date": str(notif.date)
        })

        # Email
        if user.email:
            full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

            background_tasks.add_task(
                send_email,
                user.email,
                "New Circular Published",
                f"Dear {full_name or user.username},\n\n"
                f"A new circular '{circular_title}' has been published.\n\n"
                "Regards,\nPetronet",
                "Circular Notification"
            )


# ============================================================
# UPDATE CIRCULAR NOTIFICATION HANDLER
# ============================================================

async def notify_users_for_circular_update(
    db: Session,
    *,
    circular_id: int,
    target_audience: List[dict],
    circular_title: str,
    change_type: str,  
    updated_by_user_id: int,
    background_tasks: BackgroundTasks
):
    """
    Handles UPDATE notification for:
    - GROUP
    - INDIVIDUAL
    - STATION
    """

    all_user_ids: Set[int] = set()

    # ========================================================
    # Collect Users Based On Audience
    # ========================================================

    for audience in target_audience:

        audience_type = audience.get("audience_type")
        ref_ids = audience.get("audience_ref_id", [])

        # GROUP
        if audience_type == "GROUP":

            groups = db.query(GroupMaster).filter(
                GroupMaster.group_id.in_(ref_ids),
                GroupMaster.is_deleted == False
            ).all()

            for group in groups:
                if group.employee_ids:
                    all_user_ids.update(group.employee_ids)

        # INDIVIDUAL
        elif audience_type == "INDIVIDUAL":
            all_user_ids.update(ref_ids)

        # STATION
        elif audience_type == "STATION":

            station_users = db.query(User).filter(
                User.station_id.in_(ref_ids),
                User.is_deleted == False
            ).all()

            for user in station_users:
                all_user_ids.add(user.user_id)

    if not all_user_ids:
        return

    # ========================================================
    # Fetch Valid Users
    # ========================================================

    users = db.query(User).filter(
        User.user_id.in_(list(all_user_ids)),
        User.is_deleted == False,
        User.username.isnot(None)
    ).all()

    if not users:
        return

    # ========================================================
    # Get Updater Username
    # ========================================================

    updater = db.query(User).filter(
        User.user_id == updated_by_user_id
    ).first()

    from_username = updater.username if updater else "system"

    # ========================================================
    # SEND UPDATE NOTIFICATION
    # ========================================================

    for user in users:

        data = NotificationCreate(
            type="Circular",
            title="Circular Updated",
            description=(
                  f"Circular {circular_id} – '{circular_title}' "
                  f"has been updated to Version {change_type}. "
                  f"Please review the latest version."
            ),
            from_user=from_username,
            to_user=user.username,
            module_name="circular",
            module_status="Updated"
        )

        notif = create_circular_notification(db, data)

        # 🔔 WebSocket
        await manager.send_personal_message(user.username, {
            "id": notif.id,
            "title": notif.title,
            "description": notif.description,
            "module_status": notif.module_status,
            "date": str(notif.date)
        })

        # 📧 Email
        if user.email:
            full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

            background_tasks.add_task(
                send_email,
                user.email,
                "Circular Updated",
                 f"Dear {full_name or user.username},\n\n"
                 f"Circular {circular_id} – '{circular_title}' "
                 f"has been updated to Version {change_type}.\n\n"
                 f"Please review the latest version at your earliest convenience.\n\n"
                "Regards,\nPetronet",
                "Circular Notification"
            )

# send remainder to all users who didn't acknowledged

async def notify_pending_acknowledgement_users(
    db: Session,
    *,
    circular_id: int,
    circular_title: str,
    change_type: str,
    login_user_id: int,
    background_tasks: BackgroundTasks
):
    """
    Send reminder notification to users who:
    - Have read the circular
    - But have NOT acknowledged it
    """

    # ======================================================
    # Get Users Who Read But Not Acknowledged
    # ======================================================

    pending_users = db.query(CircularUserActivity).filter(
    CircularUserActivity.circular_id == circular_id,
    CircularUserActivity.is_read.is_(True),
    CircularUserActivity.is_acknowledged.isnot(True)
    ).all()

    if not pending_users:
        return

    user_ids = [u.user_id for u in pending_users]

    # ======================================================
    # Fetch User Details
    # ======================================================

    users = db.query(User).filter(
        User.user_id.in_(user_ids),
        User.is_deleted == False,
        User.username.isnot(None)
    ).all()

    if not users:
        return

    updater = db.query(User).filter(
        User.user_id == login_user_id
    ).first()

    from_username = updater.username if updater else "system"

    # ======================================================
    # Send Reminder Notification
    # ======================================================

    for user in users:

        # 🔔 Notification Message
        description = (
            f"Circular {circular_id} – '{circular_title}' "
            f"(Version {change_type}) has been read but not acknowledged. "
            f"Please complete the acknowledgement."
        )

        data = NotificationCreate(
            type="Circular",
            title="Acknowledgement Reminder",
            description=description,
            from_user=from_username,
            to_user=user.username,
            module_name="circular",
            module_status="Pending Acknowledgement",
            module_id=circular_id
        )

        notif = create_circular_notification(db, data)

        # 🔔 WebSocket Push
        await manager.send_personal_message(user.username, {
            "id": notif.id,
            "title": notif.title,
            "description": notif.description,
            "module_status": notif.module_status,
            "module_id": circular_id,
            "date": str(notif.date)
        })

        # 📧 Email Reminder
        if user.email:
            full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

            background_tasks.add_task(
                send_email,
                user.email,
                "Circular Acknowledgement Reminder",
                f"Dear {full_name or user.username},\n\n"
                f"Circular {circular_id} – '{circular_title}' "
                f"(Version {change_type}) has been read but not acknowledged.\n\n"
                f"Kindly log in and complete the acknowledgement at the earliest.\n\n"
                "Regards,\n"
                "Petronet Team",
                "Circular Reminder"
            )