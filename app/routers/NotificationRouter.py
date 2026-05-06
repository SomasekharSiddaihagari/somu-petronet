from typing import Optional

from fastapi import APIRouter, HTTPException, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.Websocket import manager
from app.schemas.NotificationSchema import NotificationCreate, NotificationUpdate
from app.crud import NotificationCrud
from app.utils.time_utils import to_ist

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            await websocket.receive_text()  # just keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)

# @router.post("/create")
# async def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
#     db_notification = NotificationCrud.create_notification(db, notification)
#     await manager.send_personal_message(notification.to_user, {
#         "id": db_notification.id,
#         "type": db_notification.type,
#         "title": db_notification.title,
#         "description": db_notification.description,
#         "from_user": db_notification.from_user,
#         "to_user": db_notification.to_user,
#         "date": str(db_notification.date),
#     })

#     return {
#         "id": db_notification.id,
#         "type": db_notification.type,
#         "title": db_notification.title,
#         "description": db_notification.description,
#        "date": db_notification.date.strftime("%Y-%m-%d %H:%M:%S"),

    
#         }
@router.post("/create")
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    db_notification = NotificationCrud.create_notification(db, notification)

    formatted_date = db_notification.date.strftime("%Y-%m-%d %H:%M:%S")

    await manager.send_personal_message(
        notification.to_user,
        {
            "id": db_notification.id,
            "type": db_notification.type,
            "title": db_notification.title,
            "description": db_notification.description,
            "from_user": db_notification.from_user,
            "to_user": db_notification.to_user,
            "date": formatted_date,
        }
    )

    return {
        "id": db_notification.id,
        "type": db_notification.type,
        "title": db_notification.title,
        "description": db_notification.description,
        "date": formatted_date,
    }


@router.put("/update/{notification_id}")
def update_notification(
    notification_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db)
):
    updated = NotificationCrud.update_notification(db, notification_id, notification)

    if not updated:
        raise HTTPException(status_code=404, detail="Notification not found")

    return {
        "id": updated.id,
        "type": updated.type,
        "title": updated.title,
        "description": updated.description,
        "from_user": updated.from_user,
        "to_user": updated.to_user,
        "module_name": updated.module_name,
        "module_status": updated.module_status,
        "is_read": updated.is_read,
        "date": updated.date.strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Notification updated successfully"
    }







@router.get("/user/{username}")
def get_user_notifications(username: str, db: Session = Depends(get_db)):
    from app.models.NotificationModel import Notification

    notifications = (
        db.query(Notification)
        .filter(Notification.to_user == username)
        .order_by(Notification.date.desc())
        .all()
    )

    return [
        {
            "id": n.id,
            "type": n.type,
            "title": n.title,
            "description": n.description,
            "from_user": n.from_user,
            "to_user": n.to_user,
            "module_name": n.module_name,      
            "module_status": n.module_status,   
            "date": n.date,
            "is_read": n.is_read,
            "reference_id": n.reference_id,
            "redirect_url": n.redirect_url
        }
        for n in notifications
    ]


# @router.get("/user/{username}")
# def get_user_notifications(
#     username: str,
#     limit: int = 20,
#     cursor: Optional[int] = None,  # last seen notification id
#     db: Session = Depends(get_db)
# ):
#     from app.models.NotificationModel import Notification

#     query = (
#         db.query(Notification)
#         .filter(Notification.to_user == username)
#     )

#     # If cursor provided, fetch only older notifications
#     if cursor:
#         query = query.filter(Notification.id < cursor)

#     notifications = (
#         query
#         .order_by(Notification.date.desc())
#         .limit(limit)
#         .all()
#     )

#     results = [
#         {
#             "id": n.id,
#             "type": n.type,
#             "title": n.title,
#             "description": n.description,
#             "from_user": n.from_user,
#             "to_user": n.to_user,
#             "module_name": n.module_name,
#             "module_status": n.module_status,
#             "date": n.date,
#             "is_read": n.is_read
#         }
#         for n in notifications
#     ]

#     # next_cursor = smallest id in this batch (oldest one returned)
#     next_cursor = notifications[-1].id if len(notifications) == limit else None
#     print("Next cursor:", next_cursor)
#     return {
#         "data": results,
#         "next_cursor": next_cursor,  # send this back in the next request
#         "has_more": next_cursor is not None
#     } 