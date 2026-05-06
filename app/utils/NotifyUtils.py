from app.crud import notification_crud
from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager

async def send_notification(db, *, type, title, description, from_user, to_user):
    data = NotificationCreate(
        type=type,
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user
    )
    db_notification = notification_crud.create_notification(db, data)
    await manager.send_personal_message(to_user, {
        "id": db_notification.id,
        "type": db_notification.type,
        "title": db_notification.title,
        "description": db_notification.description,
        "from_user": db_notification.from_user,
        "to_user": db_notification.to_user,
        "date": str(db_notification.date),
    })

