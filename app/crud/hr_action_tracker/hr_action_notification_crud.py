from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from app.models.hr_action_tracker.disciplinary_incidents import DisciplinaryIncident
from app.models.hr_action_tracker.employee_transfers import EmployeeTransfer
from app.models.hr_action_tracker.hr_action import HRAction
from app.models.hr_action_tracker.promotions import Promotion
from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User
from app.models.NotificationModel import Notification
 
def create_hr_notification(db: Session, notification: NotificationCreate):
    try:
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
        return db_notif
    except Exception as e:
        db.rollback()
        print("❌ HR NOTIFICATION DB ERROR:", e)
        raise
 
async def send_hr_action_notification(
    db: Session,
    *,
    user_id: int,
    action_type: str,
    action_details: str,
    from_user_id: int,
    background_tasks: BackgroundTasks
):
    """
    Sends notification to:
    1. The target Employee (user_id)
    2. The Employee's Supervisor (if supervisor_id exists)
    """
   
    # 1. Fetch Target Employee
    employee = db.query(User).filter(User.user_id == user_id).first()
    if not employee:
        print(f"❌ Employee with user_id {user_id} not found.")
        return
 
    # 2. Fetch Creator (From User)
    creator = db.query(User).filter(User.user_id == from_user_id).first()
    from_username = creator.username if creator else "System"
 
    # 3. Fetch Supervisor
    supervisor = None
    if employee.supervisor_id:
        supervisor = db.query(User).filter(User.user_id == employee.supervisor_id).first()
 
    # 4. Define Notifications
    recipients = [employee]
    if supervisor:
        recipients.append(supervisor)
 
    for recipient in recipients:
        if not recipient.username:
            continue
 
        is_supervisor = (recipient.user_id == employee.supervisor_id)
       
        title = f"HR Action: {action_type}"
       
        if is_supervisor:
            description = f"A new {action_type} has been recorded for your subordinate {employee.first_name or ''} {employee.last_name or ''}."
            email_body = (
                f"Dear {recipient.first_name or recipient.username},\n\n"
                f"This is to inform you that a new HR Action ({action_type}) has been recorded for your subordinate:\n\n"
                f"Employee: {employee.first_name or ''} {employee.last_name or ''} ({employee.employee_code or 'N/A'})\n"
                f"Details: {action_details}\n\n"
                f"Regards,\nPetronet Team"
            )
        else:
            description = f"A new {action_type} has been recorded for you."
            email_body = (
                f"Dear {employee.first_name or employee.username},\n\n"
                f"This is to inform you that a new HR Action ({action_type}) has been recorded in your profile.\n\n"
                f"Details: {action_details}\n\n"
                f"Regards,\nPetronet Team"
            )
 
        # A. Save to Database
        notif_data = NotificationCreate(
            type="HR Action",
            title=title,
            description=description,
            from_user=from_username,
            to_user=recipient.username,
            module_name="HR Action Tracker",
            module_status="Created"
        )
        db_notif = create_hr_notification(db, notif_data)
 
        # B. WebSocket push
        try:
            await manager.send_personal_message(recipient.username, {
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
            pass
 
        # C. Email
        if recipient.email:
            background_tasks.add_task(
                send_email,
                recipient.email,
                title,
                email_body,
                "HR Action Notification"
            )
 
    return True

async def send_hr_acknowledgement_notification(
    db: Session,
    *,
    user_id: int,
    action_id: int,
    background_tasks: BackgroundTasks,
    module_type: str = "HR_ACTION"
):
    """
    Sends notification to:
    1. The Action Creator (HR)
    2. The Employee's Supervisor
    """
   
    # 1. Fetch Acknowledging Employee
    employee = db.query(User).filter(User.user_id == user_id).first()
    if not employee:
        print(f"❌ Notification Error: Employee {user_id} not found")
        return
   
    emp_name = f"{employee.first_name or ''} {employee.last_name or ''}".strip() or employee.username
 
    # 2. Fetch Module Record and Identify Action Type
    record = None
    action_type = "HR Action"
 
    if module_type == "HR_ACTION":
        record = db.query(HRAction).filter(HRAction.id == action_id).first()
        action_type = record.action_type if record else "HR Action"
    elif module_type == "DISCIPLINARY":
        record = db.query(DisciplinaryIncident).filter(DisciplinaryIncident.disciplinary_id == action_id).first()
        action_type = "Disciplinary Incident"
    elif module_type == "TRANSFER":
        record = db.query(EmployeeTransfer).filter(EmployeeTransfer.id == action_id).first()
        action_type = "Employee Transfer"
    elif module_type == "PROMOTION":
        record = db.query(Promotion).filter(Promotion.id == action_id).first()
        action_type = "Promotion"
 
    if not record:
        print(f"❌ Notification Error: {module_type} record {action_id} not found")
        return
 
    # 3. Fetch Supervisor
    supervisor = None
    if employee.supervisor_id:
        supervisor = db.query(User).filter(User.user_id == employee.supervisor_id).first()
        if not supervisor:
            print(f"⚠️ Notification: Supervisor {employee.supervisor_id} not found for employee {user_id}")
 
    # 4. Fetch HR Creator
    hr_creator = None
    if record.created_by:
        hr_creator = db.query(User).filter(User.user_id == record.created_by).first()
        if not hr_creator:
            print(f"⚠️ Notification: HR Creator {record.created_by} not found for {module_type} {action_id}")
 
    # 5. Define Recipients (Unique set of users: Supervisor + HR Creator)
    recipients_map = {}
    if supervisor:
        recipients_map[supervisor.user_id] = supervisor
   
    if hr_creator:
        recipients_map[hr_creator.user_id] = hr_creator
 
    print(f" Total recipients for notification: {len(recipients_map)}")
 
    title = f"HR Action Acknowledged: {action_type}"
    description = f"Employee {emp_name} has acknowledged the HR Action ({action_type})."
 
    for recipient_id, recipient in recipients_map.items():
        if not recipient.username:
            continue
 
        email_body = (
            f"Dear {recipient.first_name or recipient.username},\n\n"
            f"This is to inform you that the HR Action ({action_type}) has been acknowledged by the employee:\n\n"
            f"Employee: {emp_name} ({employee.employee_code or 'N/A'})\n"
            f"Action ID: {action_id}\n\n"
            f"Regards,\nPetronet Team"
        )
 
        # A. Save to Database
        notif_data = NotificationCreate(
            type="HR Action Acknowledge",
            title=title,
            description=description,
            from_user=employee.username,
            to_user=recipient.username,
            module_name="HR Action Tracker",
            module_status="Acknowledged"
        )
        db_notif = create_hr_notification(db, notif_data)
 
        # B. WebSocket push
        try:
            await manager.send_personal_message(recipient.username, {
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
            pass
 
        # C. Email
        if recipient.email:
            background_tasks.add_task(
                send_email,
                recipient.email,
                title,
                email_body,
                "HR Action Acknowledgement"
            )
 
    return True