from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import BackgroundTasks

from app.models.NotificationModel import Notification
from app.models.UserModel import User

from app.utils.EmailUtils import send_email
from app.core.Websocket import manager



# ============================================================
# GET SIC BY STATION (DYNAMIC – NO HARDCODE)
# ============================================================

def get_sic_by_station(db: Session, station_id: int):
    print(f"🔎 Looking for SIC at station_id={station_id}")

    # Debug: list all roles in the DB
    all_roles = db.execute(text("SELECT role_id, role_name FROM roles")).mappings().all()
    print(f"📋 Available roles in DB: {[dict(r) for r in all_roles]}")

    # Case-insensitive match, no hardcoded submenu_id
    sql = text("""
        SELECT 
            u.user_id,
            u.username,
            u.email,
            r.role_name
        FROM users u
        JOIN role_permissions rp ON rp.user_id = u.user_id
        JOIN roles r ON r.role_id = rp.role_id
        WHERE u.station_id = :station_id
        AND LOWER(TRIM(r.role_name)) = 'sic'
        AND u.is_deleted = FALSE
        LIMIT 1
    """)
    result = db.execute(sql, {"station_id": station_id}).mappings().first()

    if result:
        print(f"✅ SIC found: user_id={result['user_id']}, username={result['username']}, email={result.get('email')}")
    else:
        # Debug: check what users exist at this station
        station_users = db.execute(
            text("""
                SELECT u.user_id, u.username, u.station_id, r.role_name
                FROM users u
                LEFT JOIN role_permissions rp ON rp.user_id = u.user_id
                LEFT JOIN roles r ON r.role_id = rp.role_id
                WHERE u.station_id = :station_id
                AND u.is_deleted = FALSE
            """),
            {"station_id": station_id}
        ).mappings().all()
        print(f"❌ No SIC found. Users at station {station_id}: {[dict(u) for u in station_users]}")

    return result


# ============================================================
# GET HSE HEAD (DYNAMIC)
# ============================================================

def get_hse_heads(db: Session):
    print("🔎 Looking for HSE HEADs...")
    sql = text("""
        SELECT 
            u.user_id,
            u.username,
            u.email
        FROM users u
        JOIN role_permissions rp ON rp.user_id = u.user_id
        JOIN roles r ON r.role_id = rp.role_id
        WHERE LOWER(TRIM(r.role_name)) = 'hse head'
        AND u.is_deleted = FALSE
    """)
    heads = db.execute(sql).mappings().all()
    print(f"📋 HSE HEADs found: {[dict(h) for h in heads]}")
    return heads


# ============================================================
# CREATE NOTIFICATION
# ============================================================

def create_notification(
    db: Session,
    *,
    title: str,
    description: str,
    from_user: str,
    to_user: str,
    module_name: str,
    module_status: str,
    type: str = "prevention",
):
    try:
        notification = Notification(
            title=title,
            description=description,
            from_user=from_user,
            to_user=to_user,
            module_name=module_name,
            module_status=module_status,
            type=type,
            date=datetime.now(),
            is_read=False,
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        print(f"✅ NOTIFICATION SAVED: id={notification.id}, to={to_user}, title={title}")
        return notification

    except Exception as e:
        db.rollback()
        print("❌ NOTIFICATION DB ERROR:", e)
        return None


# ============================================================
# SEND NOTIFICATION (DB + WS + EMAIL)
# ============================================================

async def send_notification(
    db: Session,
    *,
    title: str,
    description: str,
    from_user: str,
    to_user: str,
    module_name: str,
    module_status: str,
    background_tasks: BackgroundTasks,
):

    notification = create_notification(
        db=db,
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name=module_name,
        module_status=module_status,
    )

    if not notification:
        print(f"❌ Notification NOT saved for {to_user}, skipping WS + email")
        return

    # WebSocket
    try:
        await manager.send_personal_message(
            to_user,
            {
                "title": title,
                "description": description,
                "status": module_status,
            },
        )
        print(f"✅ WebSocket sent to {to_user}")
    except Exception as e:
        print(f"❌ WebSocket Error for {to_user}:", e)

    # Email
    user = db.query(User).filter(User.username == to_user).first()

    if user and user.email:
        current_date = datetime.now().strftime("%d-%m-%Y %H:%M")

        subject = f"{title} | HSE Management System"

        body = f"""
Dear {user.first_name or user.username},

--------------------------------------------------
Incident Prevention Workflow Notification
--------------------------------------------------
Title       : {title}
Description : {description}
Status      : {module_status}
Date & Time : {current_date}
Module      : {module_name}
--------------------------------------------------

Please login to the HSE Management System for action.

Regards,
HSE Management Team
"""

        background_tasks.add_task(
            send_email,
            user.email,
            subject,
            body,
            module_name,
        )
        print(f"📧 Email queued for {to_user} ({user.email})")
    else:
        print(f"⚠️ No email for {to_user} — user={'not found' if not user else 'no email set'}")


# ============================================================
# HELPER: Get user by ID safely
# ============================================================

def get_user_by_id(db: Session, user_id):
    if not user_id:
        return None
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(db: Session, username):
    if not username:
        return None
    return db.query(User).filter(User.username == username).first()


# ============================================================
# PREVENTION WORKFLOW HANDLER
# ============================================================

async def handle_prevention_notification(
    db: Session,
    *,
    prevention,
    background_tasks: BackgroundTasks,
):

    print("=" * 60)
    print("🔎 PREVENTION NOTIFICATION HANDLER CALLED")
    print("=" * 60)

    # ---- Extract fields (dict or ORM safe) ----
    if isinstance(prevention, dict):
        status       = prevention.get("status")
        created_by   = prevention.get("created_by")
        incident_id  = prevention.get("incident_id")
        category     = prevention.get("category")
        engineer_id  = prevention.get("minor_allotted_engineer_id")
        ip_id        = prevention.get("ip_id")
        sic_name     = prevention.get("minor_sic_name")
    else:
        status       = getattr(prevention, "status", None)
        created_by   = getattr(prevention, "created_by", None)
        incident_id  = getattr(prevention, "incident_id", None)
        category     = getattr(prevention, "category", None)
        engineer_id  = getattr(prevention, "minor_allotted_engineer_id", None)
        ip_id        = getattr(prevention, "ip_id", None)
        sic_name     = getattr(prevention, "minor_sic_name", None)

    print(f"📋 Parsed → status={status}, category={category}, created_by={created_by}")
    print(f"📋         incident_id={incident_id}, ip_id={ip_id}")
    print(f"📋         engineer_id={engineer_id}, sic_name={sic_name}")

    # ---- Validate ----
    if not status or not category:
        print(f"❌ EARLY RETURN: status={status}, category={category} — one is missing!")
        return

    if category.lower() != "minor":
        print(f"ℹ️ Skipping: category is '{category}', not MINOR")
        return

    # status = status.strip().upper()
    sent = set()

    print(f"🚀 Processing status: '{status}'")

    # ============================================================
    # OPEN → AUTO ASSIGN SIC → Notify SIC
    # ============================================================

    if status == "Open":

        print(f"🔎 OPEN — looking up creator user_id={created_by}")
        creator = get_user_by_id(db, created_by)
        if not creator:
            print(f"❌ Creator with user_id={created_by} NOT FOUND in users table")
            return

        print(f"✅ Creator: username={creator.username}, station_id={creator.station_id}")

        if not creator.station_id:
            print(f"❌ Creator has NO station_id assigned!")
            return

        sic_data = get_sic_by_station(db, creator.station_id)
        if not sic_data:
            print(f"❌ No SIC found for station_id={creator.station_id}")
            return

        sic_user_id  = sic_data["user_id"]
        sic_username = sic_data["username"]

        # Auto assign SIC name if not already set
        if not sic_name:
            try:
                db.execute(
                    text("""
                        UPDATE incident_prevention
                        SET minor_sic_name = :sic_name
                        WHERE ip_id = :ip_id
                    """),
                    {"sic_name": sic_username, "ip_id": ip_id},
                )
                db.commit()
                print(f"✅ Auto-assigned SIC '{sic_username}' to ip_id={ip_id}")
            except Exception as e:
                db.rollback()
                print(f"❌ Failed to auto-assign SIC: {e}")

        # Notify SIC
        if sic_username not in sent:
            sent.add(sic_username)
            print(f"📤 Sending OPEN notification to SIC: {sic_username}")
            await send_notification(
                db=db,
                title="Minor Incident Submitted",
                description=f"Incident ID {incident_id} has been submitted. Please review and assign an engineer.",
                from_user="system",
                to_user=sic_username,
                module_name="incident_prevention",
                module_status=status,
                background_tasks=background_tasks,
            )

    # ============================================================
    # IN PROCESS → SIC assigned Engineer → Notify Engineer
    # ============================================================

    elif status == "In-Progress":

        print(f"🔎 IN PROCESS — engineer_id={engineer_id}")

        if not engineer_id:
            print("❌ IN PROCESS but no engineer_id found! Cannot notify engineer.")
            return

        engineer = get_user_by_id(db, engineer_id)
        if not engineer:
            print(f"❌ Engineer with user_id={engineer_id} NOT FOUND in users table")
            return

        print(f"✅ Engineer found: username={engineer.username}, email={engineer.email}")

        if engineer.username not in sent:
            sent.add(engineer.username)
            print(f"📤 Sending IN PROCESS notification to Engineer: {engineer.username}")
            await send_notification(
                db=db,
                title="Minor Incident Assigned To You",
                description=f"You have been assigned Incident ID {incident_id} by SIC. Please take corrective action.",
                from_user="system",
                to_user=engineer.username,
                module_name="incident_prevention",
                module_status=status,
                background_tasks=background_tasks,
            )

        # Also notify the creator that engineer has been assigned
        creator = get_user_by_id(db, created_by)
        if creator and creator.username not in sent:
            sent.add(creator.username)
            print(f"📤 Sending IN PROCESS notification to Creator: {creator.username}")
            await send_notification(
                db=db,
                title="Engineer Assigned to Your Incident",
                description=f"An engineer has been assigned to Incident ID {incident_id}. Status: In Process.",
                from_user="system",
                to_user=creator.username,
                module_name="incident_prevention",
                module_status=status,
                background_tasks=background_tasks,
            )

    # ============================================================
    # CLOSURE SUBMITTED → Notify SIC + HSE HEAD
    # ============================================================

    elif status == "Closure Submitted":

        print(f"🔎 CLOSURE SUBMITTED — sic_name={sic_name}, engineer_id={engineer_id}")

        # Notify SIC (stored as username in minor_sic_name)
        if sic_name:
            sic_user = get_user_by_username(db, sic_name)
            if sic_user and sic_user.username not in sent:
                sent.add(sic_user.username)
                print(f"📤 Sending CLOSURE SUBMITTED notification to SIC: {sic_user.username}")
                await send_notification(
                    db=db,
                    title="Closure Submitted for Review",
                    description=f"Incident ID {incident_id} closure has been submitted by the engineer. Please review.",
                    from_user="system",
                    to_user=sic_user.username,
                    module_name="incident_prevention",
                    module_status=status,
                    background_tasks=background_tasks,
                )
        else:
            print("⚠️ No SIC name found in minor_sic_name — can't notify SIC")

        # Notify all HSE HEADs
        hse_heads = get_hse_heads(db)

        for head in hse_heads:
            if head["username"] not in sent:
                sent.add(head["username"])
                print(f"📤 Sending CLOSURE SUBMITTED notification to HSE HEAD: {head['username']}")
                await send_notification(
                    db=db,
                    title="Incident Closure Requires HSE Approval",
                    description=f"Incident ID {incident_id} closure submitted. Requires your approval.",
                    from_user="system",
                    to_user=head["username"],
                    module_name="incident_prevention",
                    module_status=status,
                    background_tasks=background_tasks,
                )

    # ============================================================
    # CLOSED → Notify Engineer + Creator + SIC
    # ============================================================

    elif status == "Closed":

        print(f"🔎 CLOSED — engineer_id={engineer_id}, created_by={created_by}, sic_name={sic_name}")

        # Notify Engineer
        if engineer_id:
            engineer = get_user_by_id(db, engineer_id)
            if engineer and engineer.username not in sent:
                sent.add(engineer.username)
                print(f"📤 Sending CLOSED notification to Engineer: {engineer.username}")
                await send_notification(
                    db=db,
                    title="Incident Closed",
                    description=f"Incident ID {incident_id} has been approved and closed.",
                    from_user="system",
                    to_user=engineer.username,
                    module_name="incident_prevention",
                    module_status=status,
                    background_tasks=background_tasks,
                )
        else:
            print("⚠️ No engineer_id — can't notify engineer for CLOSED")

        # Notify Creator
        creator = get_user_by_id(db, created_by)
        if creator and creator.username not in sent:
            sent.add(creator.username)
            print(f"📤 Sending CLOSED notification to Creator: {creator.username}")
            await send_notification(
                db=db,
                title="Your Incident Has Been Closed",
                description=f"Incident ID {incident_id} has been approved and closed by HSE.",
                from_user="system",
                to_user=creator.username,
                module_name="incident_prevention",
                module_status=status,
                background_tasks=background_tasks,
            )

        # Notify SIC
        if sic_name:
            sic_user = get_user_by_username(db, sic_name)
            if sic_user and sic_user.username not in sent:
                sent.add(sic_user.username)
                print(f"📤 Sending CLOSED notification to SIC: {sic_user.username}")
                await send_notification(
                    db=db,
                    title="Incident Closed",
                    description=f"Incident ID {incident_id} has been approved and closed by HSE.",
                    from_user="system",
                    to_user=sic_user.username,
                    module_name="incident_prevention",
                    module_status=status,
                    background_tasks=background_tasks,
                )

    # ============================================================
    # SENT BACK → Notify Engineer + SIC
    # ============================================================

    elif status == "changes Request":

        print(f"🔎 SENT BACK — engineer_id={engineer_id}, sic_name={sic_name}")

        # Notify Engineer
        if engineer_id:
            engineer = get_user_by_id(db, engineer_id)
            if engineer and engineer.username not in sent:
                sent.add(engineer.username)
                print(f"📤 Sending SENT BACK notification to Engineer: {engineer.username}")
                await send_notification(
                    db=db,
                    title="Incident Sent Back for Correction",
                    description=f"Incident ID {incident_id} has been sent back. Please review and resubmit.",
                    from_user="system",
                    to_user=engineer.username,
                    module_name="incident_prevention",
                    module_status=status,
                    background_tasks=background_tasks,
                )
        else:
            print("⚠️ No engineer_id — can't notify engineer for SENT BACK")

        # Notify SIC
        if sic_name:
            sic_user = get_user_by_username(db, sic_name)
            if sic_user and sic_user.username not in sent:
                sent.add(sic_user.username)
                print(f"📤 Sending SENT BACK notification to SIC: {sic_user.username}")
                await send_notification(
                    db=db,
                    title="Incident Sent Back",
                    description=f"Incident ID {incident_id} has been sent back for correction.",
                    from_user="system",
                    to_user=sic_user.username,
                    module_name="incident_prevention",
                    module_status=status,
                    background_tasks=background_tasks,
                )

    else:
        print(f"⚠️ Unhandled status: '{status}' — no notification sent")

    print(f"✅ Notification handler complete. Sent to: {sent}")
    print("=" * 60)





# from datetime import datetime, timedelta, time
# from sqlalchemy.orm import Session
# from sqlalchemy import text
# # from app.core.scheduler import scheduler
# from app.database import SessionLocal
# from app.schemas.NotificationSchema import NotificationCreate
# from app.crud.NotificationCrud import create_notification
# from app.core.Websocket import manager
# import asyncio
# # (send_notification is defined in this same file — no self-import needed)
# from fastapi import BackgroundTasks
# # from app.core.scheduler import scheduler
# from datetime import datetime
# from app.utils.EmailUtils import send_email
# from app.core.Websocket import manager
# from app.schemas.NotificationSchema import NotificationCreate
# from app.crud.NotificationCrud import create_notification
# from app.models.UserModel import User


# async def send_meeting_notification(
#     db,
#     *,
#     title: str,
#     message: str,
#     to_user: str,
#     email: str,
#     meeting_no: str = None,
#     meeting_date: datetime = None,
#     meeting_time: str = None,
#     location: str = None,
# ):
#     try:
#         # ===============================
#         # ✅ FORMAT DATE & TIME
#         # ===============================
#         if meeting_date:
#             formatted_date = meeting_date.strftime("%d-%m-%Y")
#         else:
#             formatted_date = "N/A"

#         formatted_time = meeting_time if meeting_time else "N/A"

#         # ===============================
#         # ✅ FORMAT DESCRIPTION (CLEAN)
#         # ===============================
#         description = f"""
# 📢 Safety Committee Meeting

# • Meeting No   : {meeting_no or 'N/A'}
# • Message      : {message}
# • Date         : {formatted_date}
# • Time         : {formatted_time}
# • Location     : {location or 'N/A'}

# Please ensure your availability.
# """

#         # ===============================
#         # ✅ SAVE NOTIFICATION (DB)
#         # ===============================
#         notif = NotificationCreate(
#             type="meeting",
#             title=title,
#             description=description,
#             from_user="system",
#             to_user=to_user,
#             module_name="meeting",
#             module_status="info"
#         )

#         notification = create_notification(db, notif)

#         if not notification:
#             print(f"❌ Notification NOT saved for {to_user}")
#             return

#         # ===============================
#         # ✅ WEBSOCKET
#         # ===============================
#         try:
#             await manager.send_personal_message(
#                 to_user,
#                 {
#                     "title": title,
#                     "description": description,
#                 },
#             )
#             print(f"✅ WebSocket sent to {to_user}")
#         except Exception as e:
#             print(f"❌ WebSocket Error for {to_user}:", e)

#         # ===============================
#         # ✅ EMAIL (PROFESSIONAL FORMAT)
#         # ===============================
#         if email:
#             subject = f"{title} | HSE Meeting System"

#             body = f"""
# Dear {to_user},

# --------------------------------------------------
# 📢 Safety Committee Meeting Notification
# --------------------------------------------------

# 🔹 Meeting No : {meeting_no or 'N/A'}
# 🔹 Message    : {message}
# 🔹 Date       : {formatted_date}
# 🔹 Time       : {formatted_time}
# 🔹 Location   : {location or 'N/A'}

# --------------------------------------------------

# You are requested to attend the meeting.

# Regards,  
# HSE Management Team
# """

#             send_email(email, subject, body, "meeting")
#             print(f"📧 Email sent to {email}")

#         else:
#             print(f"⚠️ No email for {to_user}")

#     except Exception as e:
#         print("❌ Error in meeting notification:", e)

# # =====================================================
# # 🔥 ASYNC FUNCTION (ACTUAL LOGIC)
# # =====================================================
# # async def send_meeting_reminder(minutes_id: int, meeting_datetime: datetime):
# #     db: Session = SessionLocal()

# #     try:
# #         now = datetime.now()
# #         days_left = (meeting_datetime.date() - now.date()).days

# #         # ===============================
# #         # DYNAMIC MESSAGE
# #         # ===============================
# #         if days_left > 1:
# #             message = f"Meeting schedule in  {days_left} days."
# #         elif days_left == 1:
# #             message = "Meeting schedule tomorrow."
# #         elif days_left == 0:
# #             message = "Meeting schedule is today."
# #         else:
# #             message = "Meeting already scheduled."

# #         # ===============================
# #         # FETCH MEMBERS (FIXED)
# #         # ===============================
# #         members = db.execute(
# #             text("""
# #                 SELECT DISTINCT name
# #                 FROM safety_committee_members
# #                 WHERE is_active = true
# #                 AND name IS NOT NULL
# #             """),
# #             {"mid": minutes_id}
# #         ).fetchall()

# #         if not members:
# #             print("❌ No members found")
# #             return

# #         # ===============================
# #         # SEND NOTIFICATION
# #         # ===============================
# #         for row in members:
# #             username = row[0]

# #             if not username:
# #                 continue

# #             notif = NotificationCreate(
# #                 type="Meeting",
# #                 title="Meeting Reminder",
# #                 description=message,
# #                 from_user="system",
# #                 to_user=username,
# #                 module_name="meeting",
# #                 module_status="Reminder"
# #             )

# #             saved = create_notification(db, notif)

# #             await manager.send_personal_message(username, {
# #                 "id": saved.id,
# #                 "title": saved.title,
# #                 "description": saved.description,
# #                 "date": str(saved.date)
# #             })

# #         print("✅ Notification sent")

# #     except Exception as e:
# #         print("❌ Error:", e)

# #     finally:
# #         db.close()
# async def send_meeting_reminder(minutes_id: int, meeting_datetime: datetime):
#     db: Session = SessionLocal()

#     try:
#         now = datetime.now()
#         if isinstance(meeting_datetime, datetime):
#             meeting_date_only = meeting_datetime.date()
#         else:
#             meeting_date_only = meeting_datetime

#         days_left = (meeting_date_only - now.date()).days
        

#         if days_left > 1:
#             message = f"Meeting schedule in {days_left} days."
#         elif days_left == 1:
#             message = "Meeting schedule tomorrow."
#         elif days_left == 0:
#             message = "Meeting schedule is today."
#         else:
#             message = "Meeting already scheduled."

#         # ✅ FIXED: use user_id join
#         # members = db.execute(
#         #     text("""
#         #         SELECT DISTINCT u.user_id, u.username, u.email
#         #         FROM safety_committee_members scm
#         #         JOIN users u ON u.user_id = scm.user_id
#         #         WHERE scm.scm_id = :mid
#         #         AND scm.is_active = true
#         #         AND u.is_deleted = false
#         #     """),
#         #     {"mid": minutes_id}
#         # ).mappings().all()
#         members = db.execute(
#             text("""
#                 SELECT DISTINCT 
#                     u.user_id,
#                     u.username,
#                     u.email,
#                     scm.designation

#                 FROM safety_committee_members scm
#                 JOIN users u ON u.user_id = scm.user_id
#                 WHERE scm.is_active = true
#                 AND u.is_deleted = false
#             """)
#         ).mappings().all()

#         if not members:
#             print("❌ No members found")
#             return
#         meeting = db.execute(
#             text("""
#                 SELECT meeting_no, meeting_date, location, meeting_time
#                 FROM safety_committee_quarterly_meetings
#                 WHERE scm_id = :mid
#             """),
#             {"mid": minutes_id}
#         ).mappings().first()

#         if not meeting:
#             print("❌ Meeting not found")
#             return

#        # 🔥 STEP 1: Separate CSO & members
#         cso = None
#         normal_members = []

#         for row in members:
#             if (row["designation"] or "").strip().lower() == "chief safety officer":
#                 cso = row
#             else:
#                 normal_members.append(row)

#         # 🔥 STEP 2: Send based on days_left

#         if days_left == 7:
#             # ✅ ONLY CSO
#             if cso:
#                 await send_meeting_notification(
#                     db=db,
#                     title="Meeting Reminder (CSO)",
#                     message="Meeting is scheduled in 7 days.",
#                     to_user=cso["username"],
#                     email=cso["email"],
#                     meeting_no=meeting["meeting_no"],
#                     meeting_date=meeting["meeting_date"],
#                     meeting_time=str(meeting_datetime.time()),
#                     location=meeting["location"]
#                 )

#         elif days_left <= 1:
#             # ✅ ALL MEMBERS
#             for m in normal_members:
#                 await send_meeting_notification(
#                     db=db,
#                     title="Meeting Reminder",
#                     message=message,
#                     to_user=m["username"],
#                     email=m["email"],
#                     meeting_no=meeting["meeting_no"],
#                     meeting_date=meeting["meeting_date"],
#                     meeting_time=str(meeting_datetime.time()),
#                     location=meeting["location"]
#                 )

#         print("✅ Reminder sent")

#     except Exception as e:
#         print("❌ Error:", e)

#     finally:
#         db.close()
# # =====================================================
# # 🔥 WRAPPER (VERY IMPORTANT FIX)
# # =====================================================
# import asyncio

# def run_meeting_reminder(minutes_id, meeting_datetime):
#     import asyncio
#     try:
#         loop = asyncio.get_running_loop()
#         loop.create_task(send_meeting_reminder(minutes_id, meeting_datetime))
#     except RuntimeError:
#         asyncio.run(send_meeting_reminder(minutes_id, meeting_datetime))


# # =====================================================
# # ⏰ SCHEDULER FUNCTION (FINAL)
# # =====================================================
# def schedule_meeting_notification(minutes_id: int, meeting_date, meeting_time=None):

#     if isinstance(meeting_date, datetime):
#         meeting_datetime = meeting_date
#     else:
#         if meeting_time:
#             meeting_datetime = datetime.combine(meeting_date, meeting_time)
#         else:
#             meeting_datetime = datetime.combine(meeting_date, time.min)

#     from zoneinfo import ZoneInfo

#     IST = ZoneInfo("Asia/Kolkata")

#     meeting_datetime = meeting_datetime.replace(tzinfo=IST)
#     now = datetime.now(IST)

#     # 🔥 7 DAYS BEFORE → CSO
#     # scheduler.add_job(
#     #     run_meeting_reminder,
#     #     "date",
#     #     run_date=meeting_datetime - timedelta(days=7),
#     #     args=[minutes_id, meeting_datetime],
#     #     id=f"meeting_cso_{minutes_id}",
#     #     replace_existing=True
#     # )

#     # # 🔥 1 DAY BEFORE → ALL MEMBERS
#     # scheduler.add_job(
#     #     run_meeting_reminder,
#     #     "date",
#     #     run_date=meeting_datetime - timedelta(days=1),
#     #     args=[minutes_id, meeting_datetime],
#     #     id=f"meeting_members_{minutes_id}",
#     #     replace_existing=True
#     # )

#     print("✅ Scheduled for CSO + Members")

#     print("📅 Meeting:", meeting_datetime)
    

# # async def notify_meeting_creation(minutes_id: int, db: Session):
# #     try:
# #         print("🔥 Sending meeting creation notifications")

# #         # ===============================
# #         # 1. GET MEMBERS
# #         # ===============================
# #         members = db.execute(
# #             text("""
# #                 SELECT DISTINCT name
# #                 FROM safety_committee_members
# #                 WHERE is_active = true
# #                 AND name IS NOT NULL
# #             """),
# #             {"mid": minutes_id}
# #         ).fetchall()

# #         # ===============================
# #         # 2. NOTIFY MEMBERS
# #         # ===============================
# #         for row in members:
# #             username = row[0]

# #             notif = NotificationCreate(
# #                 type="Meeting",
# #                 title="New Meeting Scheduled",
# #                 description="You are part of a safety committee meeting.",
# #                 from_user="system",
# #                 to_user=username,
# #                 module_name="meeting",
# #                 module_status="Created"
# #             )

# #             saved = create_notification(db, notif)

# #             await manager.send_personal_message(username, {
# #                 "id": saved.id,
# #                 "title": saved.title,
# #                 "description": saved.description,
# #                 "date": str(saved.date)
# #             })

# #         # ===============================
# #         # 3. NOTIFY SAFETY INCHARGE
# #         # ===============================
# #         safety_incharge = db.execute(
# #             text("""
# #                 SELECT name
# #                 FROM safety_committee_members
# #                 WHERE designation = 'Chief Safety Officer'
# #                 AND is_active = true
# #                 LIMIT 1
# #             """)
# #         ).fetchone()
# #         print(f"🔎 Safety Incharge query result: {safety_incharge}")
# #         if safety_incharge:
# #             username = safety_incharge[0]
# #             print(f"📤 Notifying Safety Incharge: {username}")

# #             notif = NotificationCreate(
# #                 type="Meeting",
# #                 title="Meeting Scheduled",
# #                 description="A new safety committee meeting has been scheduled.",
# #                 from_user="system",
# #                 to_user=username,
# #                 module_name="meeting",
# #                 module_status="Created"
# #             )

# #             saved = create_notification(db, notif)

# #             await manager.send_personal_message(username, {
# #                 "id": saved.id,
# #                 "title": saved.title,
# #                 "description": saved.description,
# #                 "date": str(saved.date)
# #             })

# #         print("✅ Creation notifications sent")

# #     except Exception as e:
# #         print("❌ Error in creation notification:", e)

# async def notify_meeting_creation(minutes_id: int, meeting_time: datetime, db: Session):
#     try:
#         print("🔥 Sending meeting creation notifications")


#         # ✅ Get meeting details FIRST (from safety_committee_minutes)
#         meeting = db.execute(
#             text("""
#                 SELECT meeting_no, meeting_date, location
#                 FROM safety_committee_minutes
#                 WHERE scmm_id = :mid
#             """),
#             {"mid": minutes_id}
#         ).mappings().first()

#         if not meeting:
#             print("❌ Meeting not found")
#             return
#         now = datetime.now()
        
        
#         meeting_date = meeting["meeting_date"]

#         if isinstance(meeting_date, datetime):
#             meeting_date_only = meeting_date.date()
#         else:
#             meeting_date_only = meeting_date

#         days_left = (meeting_date_only - now.date()).days

        
#         # ✅ Get members
#         members = db.execute(
#             text("""
#                 SELECT DISTINCT 
#                     u.user_id,
#                     u.username,
#                     u.email,
#                     scm.designation

#                 FROM safety_committee_members scm
#                 JOIN users u ON u.user_id = scm.user_id
#                 WHERE scm.is_active = true
#                 AND u.is_deleted = false
#             """)
#         ).mappings().all()

#         # ✅ Notify members
#         # 🔥 Separate CSO & members
#         cso = None
#         normal_members = []

#         for row in members:
#             if (row["designation"] or "").strip().lower() == "chief safety officer":
#                 cso = row
#             else:
#                 normal_members.append(row)

#         # 🔥 Apply logic
# # ✅ ALWAYS notify ALL members when meeting is created
# # 🔥 Notify ONLY normal members
#         for row in normal_members:
#             await send_meeting_notification(
#                 db=db,
#                 title="New Meeting Scheduled",
#                 message="You are part of a safety committee meeting.",
#                 to_user=row["username"],
#                 email=row["email"],
#                 meeting_no=meeting["meeting_no"],
#                 meeting_date=meeting["meeting_date"],
#                         meeting_time=(
#                         meeting_time.strftime("%H:%M") if meeting_time else "N/A"
#                         ),
#                 location=meeting["location"]
#             )

#         # ✅ Safety Incharge
#         safety_incharge = db.execute(
#             text("""
#                 SELECT 
#                     u.user_id,
#                     u.username,
#                     u.email,
#                     scm.designation

#                 FROM safety_committee_members scm
#                 JOIN users u 
#                     ON u.user_id = scm.user_id

#                 WHERE scm.is_active = true
#                 AND u.is_deleted = false
#                 AND LOWER(TRIM(scm.designation)) = 'chief safety officer'

#                 LIMIT 1
#             """)
#         ).mappings().first()

#         if safety_incharge:
#             await send_meeting_notification(
#                 db=db,
#                 title="Meeting Scheduled (CSO)",
#                 message="A new safety committee meeting has been scheduled.",
#                 to_user=safety_incharge["username"],
#                 email=safety_incharge["email"],
#                 meeting_no=meeting["meeting_no"],
#                 meeting_date=meeting["meeting_date"],
#                 meeting_time=(
#                     meeting_time.strftime("%H:%M") if meeting_time else "N/A"
#                     ),
#                 location=meeting["location"]
#             )

#         print("✅ Creation notifications sent")

#     except Exception as e:
#         print("❌ Error:", e)
# # ============================================================
# # SAFE PLACEHOLDER
# # ============================================================
# def run_notify_meeting_creation(minutes_id, meeting_time, db):
#     import asyncio
#     try:
#         loop = asyncio.get_running_loop()
#         loop.create_task(notify_meeting_creation(minutes_id,meeting_time, db))
#     except RuntimeError:
#         asyncio.run(notify_meeting_creation(minutes_id, meeting_time, db))



# async def notify_discussion_to_members(
#     db,
#     *,
#     discussion,
#     background_tasks: BackgroundTasks
# ):
#     try:
#         print("🔥 Sending discussion notification to action_by user...")

#         # ===============================
#         # ✅ Step 1: Get action_by username from the discussion row
#         # The `action_by` column stores the username of who is responsible
#         # ===============================
#         action_by_username = discussion.get("action_by")

#         if not action_by_username:
#             print("⚠️ No action_by set on this discussion. Skipping notification.")
#             return

#         # ===============================
#         # ✅ Step 2: Fetch that user from DB to get email + display name
#         # ===============================
#         action_user = db.execute(
#             text("""
#                 SELECT user_id, username, first_name, last_name, email
#                 FROM users
#                 WHERE username = :username
#                 AND is_deleted = false
#             """),
#             {"username": action_by_username}
#         ).mappings().first()

#         if not action_user:
#             print(f"⚠️ action_by user '{action_by_username}' not found in users table. Skipping.")
#             return

#         # ===============================
#         # ✅ Step 3: Get creator (who created this discussion row)
#         # ===============================
#         creator = db.execute(
#             text("""
#                 SELECT username, first_name, last_name
#                 FROM users
#                 WHERE user_id = :uid
#             """),
#             {"uid": discussion["user_id"]}
#         ).mappings().first()

#         creator_name = (
#             f"{creator['first_name']} {creator['last_name']}".strip()
#             if creator and creator["first_name"]
#             else (creator["username"] if creator else "System")
#         )

#         action_by_display = (
#             f"{action_user['first_name']} {action_user['last_name']}".strip()
#             if action_user["first_name"]
#             else action_user["username"]
#         )

#         to_user = action_user["username"]
#         to_email = action_user["email"]

#         # ===============================
#         # ✅ Step 4: Build notification content
#         # ===============================
#         title = "New Discussion Action Assigned to You"

#         description = f"""
# 📢 Safety Committee Discussion — Action Assigned

# 🔹 Description  : {discussion.get('description_of_discussion') or 'N/A'}
# 🔹 Issues       : {discussion.get('issues_discussed') or 'N/A'}
# 🔹 Action Taken : {discussion.get('action_taken') or 'N/A'}
# 🔹 Target Date  : {discussion.get('target_date') or 'N/A'}
# 🔹 Completed On : {discussion.get('completed_on') or 'N/A'}
# 🔹 Assigned By  : {creator_name}

# You have been assigned as the action owner for this discussion.
# """

#         # ===============================
#         # ✅ Step 5: Save notification to DB
#         # ===============================
#         db.execute(
#             text("""
#                 INSERT INTO notifications
#                 (type, title, description, from_user, to_user, module_name, module_status, date, is_read)
#                 VALUES
#                 (:type, :title, :description, :from_user, :to_user, :module_name, :module_status, :date, false)
#             """),
#             {
#                 "type": "discussion",
#                 "title": title,
#                 "description": description,
#                 "from_user": creator["username"] if creator else "system",
#                 "to_user": to_user,
#                 "module_name": "discussion",
#                 "module_status": "Assigned",
#                 "date": datetime.now()
#             }
#         )
#         db.commit()
#         print(f"✅ Notification saved for: {to_user}")

#         # ===============================
#         # ✅ Step 6: WebSocket (non-fatal)
#         # ===============================
#         try:
#             await manager.send_personal_message(
#                 to_user,
#                 {
#                     "title": title,
#                     "description": description,
#                 }
#             )
#             print(f"✅ WebSocket sent to: {to_user}")
#         except Exception as e:
#             print(f"⚠️ WebSocket error for {to_user}: {e}")

#         # ===============================
#         # ✅ Step 7: Email (background)
#         # ===============================
#         if to_email:
#             subject = f"{title} | HSE System"
#             body = f"""
# Dear {action_by_display},

# --------------------------------------------------
# Safety Committee Discussion — Action Assigned to You
# --------------------------------------------------

# Description  : {discussion.get('description_of_discussion') or 'N/A'}
# Issues       : {discussion.get('issues_discussed') or 'N/A'}
# Action Taken : {discussion.get('action_taken') or 'N/A'}
# Target Date  : {discussion.get('target_date') or 'N/A'}
# Completed On : {discussion.get('completed_on') or 'N/A'}
# Assigned By  : {creator_name}

# --------------------------------------------------

# You have been assigned as the action owner. Please review and act accordingly.

# Regards,
# HSE Team
# """
#             background_tasks.add_task(
#                 send_email,
#                 to_email,
#                 subject,
#                 body,
#                 "HSE Safety Committee"
#             )
#             print(f"📧 Email queued for: {to_email}")
#         else:
#             print(f"⚠️ No email address found for user: {to_user}")

#         print(f"✅ Discussion notification complete → sent to: {to_user}")

#     except Exception as e:
#         print(f"❌ Error in notify_discussion_to_members: {e}")


# async def handle_hse_notification(*args, **kwargs):
#     pass






# # ============================================================
# # SAFE PLACEHOLDER
# # ============================================================





# async def handle_hse_notification(*args, **kwargs):
#     pass