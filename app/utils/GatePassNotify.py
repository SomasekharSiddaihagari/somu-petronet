# app/utils/gatepass_notify.py

from app.schemas.NotificationSchema import NotificationCreate
from app.crud.gate_pass.GatePassNotificationCrud_old import create_gatepass_notification
from app.core.Websocket import manager


async def send_gatepass_notification(db, *, type, title, description, from_user, to_user, module_status):
    data = NotificationCreate(
        type=type,
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name="gatepass",
        module_status=module_status
    )
    db_notification = create_gatepass_notification(db, data)

    await manager.send_personal_message(to_user, {
        "id": db_notification.id,
        "type": db_notification.type,
        "title": db_notification.title,
        "description": db_notification.description,
        "from_user": db_notification.from_user,
        "to_user": db_notification.to_user,
        "module_name": db_notification.module_name,
        "module_status": db_notification.module_status,
        "date": str(db_notification.date),
    })
