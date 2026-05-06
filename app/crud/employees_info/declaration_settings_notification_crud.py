# app/crud/employees_info/DeclarationSettingsNotificationCrud.py

from sqlalchemy.orm import Session
from fastapi import BackgroundTasks, HTTPException
from datetime import datetime

from app.models.employees_info.gloabal_setting_declaration import DeclarationSettings
from app.models.NotificationModel import Notification
from app.models.UserModel import User
from app.utils.EmailUtils import send_email
from app.core.Websocket import manager


# ---------------------------------------------------
# MAIN HANDLER
# ---------------------------------------------------
async def handle_declaration_setting(
    db: Session,
    *,
    data: dict,
    background_tasks: BackgroundTasks
):
    """
    Create OR Update declaration setting.
    If declaration.is_active == True → Broadcast to ALL users.
    """

    try:
        # ---------------------------------------------------
        # 1️⃣ CHECK IF DECLARATION TYPE ALREADY EXISTS
        # ---------------------------------------------------
        existing = db.query(DeclarationSettings).filter(
            DeclarationSettings.declaration_type == data["declaration_type"]
        ).first()

        if existing:
            # UPDATE existing declaration
            existing.opening_date = data.get("opening_date")
            existing.closing_date = data.get("closing_date")
            existing.is_active = data.get("is_active", False)
            declaration = existing
        else:
            # CREATE new declaration
            declaration = DeclarationSettings(**data)
            db.add(declaration)

        db.flush()  # Important to get ID before commit

        # ---------------------------------------------------
        # 2️⃣ BROADCAST ONLY IF ACTIVE
        # ---------------------------------------------------
        if declaration.is_active:

            users = db.query(User).all()

            if users:

                subject = "Declaration Window Open"
                notifications_bulk = []

                for user in users:

                    username = getattr(user, "username", None) or user.email
                    first_name = user.first_name or "User"

                    email_body = (
                        f"Dear {first_name},\n\n"
                        f"The declaration window for {declaration.declaration_type} is now open.\n\n"
                        f"Opening Date: {declaration.opening_date}\n"
                        f"Closing Date: {declaration.closing_date}\n\n"
                        f"Please login and fill the form before closing date.\n\n"
                        f"Regards,\nHR System"
                    )

                    notif_description = (
                        f"{declaration.declaration_type} window is now open."
                    )

                    notifications_bulk.append(
                        Notification(
                            type="Declaration",
                            title="Declaration Window Open",
                            description=notif_description,
                            from_user="Admin",
                            to_user=username,
                            module_name="Declaration",
                            module_status="Open",
                            date=datetime.now(),
                            is_read=False
                        )
                    )

                    if user.email:
                        background_tasks.add_task(
                            send_email,
                            user.email,
                            subject,
                            email_body,
                            "HR System"
                        )

                # Bulk insert notifications
                db.bulk_save_objects(notifications_bulk)

                # WebSocket Push
                for notif in notifications_bulk:
                    try:
                        await manager.send_personal_message(
                            notif.to_user,
                            {
                                "type": notif.type,
                                "title": notif.title,
                                "description": notif.description,
                                "from_user": notif.from_user,
                                "to_user": notif.to_user,
                                "module_name": notif.module_name,
                                "module_status": notif.module_status,
                                "date": str(notif.date),
                            }
                        )
                    except Exception:
                        pass

        # ---------------------------------------------------
        # 3️⃣ COMMIT EVERYTHING
        # ---------------------------------------------------
        db.commit()
        db.refresh(declaration)

        return declaration

    except Exception as e:
        db.rollback()
        print("❌ Declaration Notification Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to create/update declaration setting"
        )