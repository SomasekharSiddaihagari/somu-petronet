# from sqlalchemy.orm import Session
# from datetime import datetime
# from fastapi import BackgroundTasks
# from app.schemas.NotificationSchema import NotificationCreate
# from app.core.Websocket import manager
# from app.utils.EmailUtils import send_email
# from app.models.UserModel import User
# from app.models.NotificationModel import Notification
# import hashlib
# import time

# # Global cache to track recent notification requests (in-memory)
# # Key: hash of (employee_username, sections, new_status, timestamp_minute)
# # Value: timestamp when processed
# _notification_cache = {}
# _CACHE_EXPIRY_SECONDS = 60  # Prevent duplicate notifications within 60 seconds


# # -------------------------
# # Create + save notification (DB)
# # -------------------------
# def create_employee_notification(db: Session, notification: NotificationCreate):
#     try:
#         db_notif = Notification(
#             type=notification.type,
#             title=notification.title,
#             description=notification.description,
#             from_user=notification.from_user,
#             to_user=notification.to_user,
#             module_name=notification.module_name,
#             module_status=notification.module_status,
#             date=datetime.now(),
#             is_read=False
#         )
#         db.add(db_notif)
#         db.commit()
#         db.refresh(db_notif)
#         #print("✅ Notification saved with ID:", db_notif.id)
#         return db_notif
#     except Exception as e:
#         db.rollback()
#         #print("❌ NOTIFICATION DB ERROR:", e)
#         raise


# # -------------------------
# # Generic sender (DB + WS + Email)
# # -------------------------
# async def send_employee_notification(
#     db: Session,
#     *,
#     type: str,
#     title: str,
#     email_body: str,
#     notif_description: str | None,
#     from_user: str,
#     to_user: str,
#     module_name: str = "Employee Personal Information",
#     module_status: str | None = None,
#     background_tasks: BackgroundTasks
# ):
#     # Use notif_description for DB notification; fallback to short slice of email_body
#     desc_for_db = notif_description or (email_body[:200] + ("..." if len(email_body) > 200 else ""))

#     data = NotificationCreate(
#         type=type,
#         title=title,
#         description=desc_for_db,
#         from_user=from_user,
#         to_user=to_user,
#         module_name=module_name,
#         module_status=module_status
#     )

#     db_notif = create_employee_notification(db, data)

#     # WS push
#     try:
#         await manager.send_personal_message(to_user, {
#             "id": db_notif.id,
#             "type": db_notif.type,
#             "title": db_notif.title,
#             "description": db_notif.description,
#             "from_user": db_notif.from_user,
#             "to_user": db_notif.to_user,
#             "module_name": db_notif.module_name,
#             "module_status": db_notif.module_status,
#             "date": str(db_notif.date),
#         })
#     except Exception:
#         pass

#     # Email
#     try:
#         user = db.query(User).filter(User.username == to_user).first()
#         if user and user.email:
#             if background_tasks:
#                 background_tasks.add_task(
#                     send_email,
#                     user.email,
#                     title,
#                     email_body,
#                     "Employee Personal Updates"
#                 )
#             else:
#                 send_email(
#                     user.email,
#                     title,
#                     email_body,
#                     "Employee Personal Updates"
#                 )
#     except Exception:
#         pass

#     return db_notif


#     # -------------------------
#     # Helper functions
#     # -------------------------
# def _full_name_of_user(db: Session, username: str) -> str:
#     u = db.query(User).filter(User.username == username).first()
#     if not u:
#         return username
#     return f"{(u.first_name or '').strip()} {(u.last_name or '').strip()}".strip()


# def get_all_hr_usernames(db: Session) -> list[str]:
#     from app.models.RolePermissionModel import RolePermission

#     rps = (
#         db.query(RolePermission)
#         .filter(
#             RolePermission.submenu_id == 6,
#             RolePermission.role_id == 7
#         )
#         .all()
#     )

#     return list({
#         rp.user.username
#         for rp in rps
#         if rp.user
#     })


# def _clean_cache():
#     """Remove expired entries from cache"""
#     global _notification_cache
#     current_time = time.time()
#     expired_keys = [
#         k for k, v in _notification_cache.items()
#         if current_time - v > _CACHE_EXPIRY_SECONDS
#     ]
#     for k in expired_keys:
#         del _notification_cache[k]


# def _get_request_hash(employee_username: str, sections: list[str], new_status: str) -> str:
#     """Generate a hash for this notification request"""
#     # Use minute-level timestamp to allow same request after 1 minute
#     timestamp_minute = int(time.time() / 60)
#     key_data = f"{employee_username}:{','.join(sorted(sections))}:{new_status}:{timestamp_minute}"
#     return hashlib.md5(key_data.encode()).hexdigest()


# def _is_duplicate_request(employee_username: str, sections: list[str], new_status: str) -> bool:
#     """Check if this notification request was recently processed"""
#     _clean_cache()
#     request_hash = _get_request_hash(employee_username, sections, new_status)
    
#     if request_hash in _notification_cache:
#         #print(f"⚠️ DUPLICATE REQUEST DETECTED - Skipping (hash: {request_hash})")
#         return True
    
#     _notification_cache[request_hash] = time.time()
#     return False


# # -------------------------
# # HR notifications
# # -------------------------
# async def notify_hr_first_time_update(db: Session, employee_username: str, hr_username: str, sections: list[str], bg: BackgroundTasks):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "Review Employee Updated Details"
#     notif_description = f"{emp_full} has submitted {', '.join(sections or [])}."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted {', '.join(sections or [])}.\n\n"
#         f"Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Employee Personal Information",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_status="Pending Approval",
#         background_tasks=bg
#     )


# async def notify_hr_section_update(db: Session, employee_username: str, hr_username: str, section: str, bg: BackgroundTasks,changed_fields: list[str] = None):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#        # ---------- FORMAT CHANGED FIELDS ----------
#     def format_changed_fields(changes):
#         if not changes:
#             return "No field changes"

#         lines = []
#         for c in changes:
#             field_name = c["field"].replace("_", " ").title()
#             lines.append(f"- {field_name}: {c['old']} → {c['new']}")

#         return "\n".join(lines)

#     changes_text = format_changed_fields(changed_fields)

#     # ---------- TITLE ----------
#     title = f"Review {section} Updated"

#     # ✅ UPDATED NOTIFICATION DESCRIPTION (THIS IS WHAT YOU WANT)
#     notif_description = (
#         f"{emp_full} updated {section}: "
#         + ", ".join([
#             f"{c['field'].replace('_',' ').title()} ({c['old']} → {c['new']})"
#             for c in (changed_fields or [])
#         ])
#     )
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has updated {section}.\n\n"
#         f"Changed Fields:\n{changes_text}\n\n"
#         f"Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Employee Personal Information",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_status=f"Pending Approval {section}",
#         background_tasks=bg
#     )


# async def notify_employee_on_status_change(db: Session, employee_username: str, hr_username: str, new_status: str, comments: str,changed_sections: str | None, bg: BackgroundTasks):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     status_clean = new_status.capitalize()
#     title = f"Employee Details {status_clean}"
#     status = new_status.strip().lower().replace("_", " ")
 
#     if status == "changes requested":
#         notif_description = f"{emp_full}, your {changed_sections} was changes requested by Hr."
#         reason_text = f"\n\nReason: {comments}" if comments else ""
#         #print(notif_description + "1")
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your {changed_sections} was changes requested by Hr."
#             f"{reason_text}\n\n"
#             f"Regards,\nHR System"
#         )
#     elif status == "approved":
#         notif_description = f" {emp_full}, your {changed_sections} was approved by Hr."
#         #print(notif_description + "1")
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your {changed_sections} has been Approved by {hr_full}.\n\n"
#             f"Regards,\nHR System"
#         )
 

#     await send_employee_notification(
#         db=db,
#         type="Employee Personal Information",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=hr_username,
#         to_user=employee_username,
#         module_status=new_status,
#         background_tasks=bg
#     )


# # -------------------------
# # MASTER handler
# # -------------------------
# async def handle_employee_update_notifications(
#     db: Session,
#     *,
#     old_status: str | None,
#     new_status: str | None,
#     old_comments: str | None,
#     new_comments: str | None,
#     employee_username: str,
#     changed_sections: list[str] | None,
#     changed_fields:list[dict] | None,
#     bg: BackgroundTasks
# ):
#     """
#     Centralized notification handler with duplicate request prevention.
#     """
    
#     #print(f"\n{'='*60}")
#     #print(f"🔔 NOTIFICATION HANDLER CALLED")
#     #print(f"   Employee: {employee_username}")
#     #print(f"   Sections: {changed_sections}")
#     #print(f"   Old Status: {old_status}")
#     #print(f"   New Status: {new_status}")
#     #print(f"{'='*60}")

#     # ✅ Skip if no field changes
#     if not changed_fields and old_status is not None:
#         return
#     # DUPLICATE REQUEST PREVENTION
#     if _is_duplicate_request(employee_username, changed_sections, new_status or ""):
#         #print(f"🛑 SKIPPING - This exact request was processed within the last {_CACHE_EXPIRY_SECONDS} seconds")
#         #print(f"{'='*60}\n")
#         return

#     old_s = (old_status or "").strip().lower()
#     new_s = (new_status or "").strip().lower()

#     # Fetch all HR usernames (deduplicated)
#     hr_usernames = list(set(get_all_hr_usernames(db)))

#     if not hr_usernames:
#         #print("⚠️ No HR users found, skipping notifications")
#         #print(f"{'='*60}\n")
#         return
    
#     #print(f"📋 Found {len(hr_usernames)} unique HR users: {hr_usernames}")

#     # helper to extract a section from "pending approval <section>"
#     def parse_pending_section(s: str) -> str | None:
#         prefix = "pending approval"
#         if not s:
#             return None
#         if s.startswith(prefix):
#             sec = s[len(prefix):].strip()
#             return sec if sec else None
#         return None

#     pending_section = parse_pending_section(new_s)

#     # -------------------------
#     # 1) new_status indicates pending approval explicitly
#     # -------------------------
#     if new_s.startswith("pending approval"):
#         #print("📌 Case 1: Pending approval")

#         # 🆕 FIRST TIME CREATE
#         if old_status is None:
#             #print("🆕 First-time create → NO changed fields")

#             for hr_username in hr_usernames:
#                 await notify_hr_first_time_update(
#                     db,
#                     employee_username,
#                     hr_username,
#                     changed_sections or [],
#                     bg
#                 )

#             return

#         # 🔄 UPDATE CASE
#         #print("🔄 Update → WITH changed fields")

#         for hr_username in hr_usernames:
#             for sec in (changed_sections or []):
#                 await notify_hr_section_update(
#                     db,
#                     employee_username,
#                     hr_username,
#                     sec,
#                     bg,
#                     changed_fields
#                 )

        
#         #print(f"✅ Sent to {len(hr_usernames)} HR users")
#         #print(f"{'='*60}\n")
#         return

#     # -------------------------
#     # Case 2: First-time update
#     # -------------------------
#     if old_s in ("", "null", "none") and changed_sections:
#         #print("📌 Case 2: First-time update")

#         for hr_username in hr_usernames:
#             await notify_hr_first_time_update(
#                 db,
#                 employee_username,
#                 hr_username,
#                 changed_sections,
#                 bg
#             )

#         #print(f"✅ Sent to {len(hr_usernames)} HR users")
#         #print(f"{'='*60}\n")
#         return

#     # -------------------------
#     # Case 3: Resubmit after changes requested
#     # -------------------------
#     if old_s == "changes requested" and changed_sections:
#         #print("📌 Case 3: Resubmit after changes requested")

#         for hr_username in hr_usernames:
#             for sec in changed_sections:
#                 await notify_hr_section_update(
#                     db,
#                     employee_username,
#                     hr_username,
#                     sec,
#                     bg,
#                     changed_fields
#                 )

#         #print(f"✅ Sent after changes requested update")
#         #print(f"{'='*60}\n")
#         return

#     # -------------------------
#     # Case 4: Update after approval
#     # -------------------------
#     if old_s == "approved" and changed_sections:
#         #print("📌 Case 4: Update after approval")

#         for hr_username in hr_usernames:
#             for sec in changed_sections:
#                 await notify_hr_section_update(
#                     db,
#                     employee_username,
#                     hr_username,
#                     sec,
#                     bg,
#                     changed_fields
#                 )

#         #print(f"✅ Sent after approval update")
#         #print(f"{'='*60}\n")
#         return

#     # -------------------------
#     # Case 5: HR decision
#     # -------------------------
#     if new_s and old_s != new_s:
#         if new_s in ("approved", "changes requested"):
#             #print(f"📌 Case 5: HR decision - {new_s}")

#             hr_username = hr_usernames[0]

#             await notify_employee_on_status_change(
#                 db,
#                 employee_username,
#                 hr_username,
#                 new_s,
#                 comments=new_comments,
#                 changed_sections=", ".join(changed_sections),
#                 bg=bg
#             )

#             #print("✅ Employee notified")
#             #print(f"{'='*60}\n")
#             return

#     #print("⚠️ No matching condition")
#     #print(f"{'='*60}\n")
#     return


# async def notify_hr_finance_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "New Investment Declaration Submitted"
#     notif_description = f"{emp_full} has submitted Investment Declaration."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted Investment Declaration. Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Investment Declaration",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name="Investment Declaration",
#         module_status="Pending Approval",
#         background_tasks=bg
#     )


# async def notify_hr_form12c_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "New Form 12C Submitted"
#     notif_description = f"{emp_full} has submitted Form 12C."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted Form 12C. Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Form 12C",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name="Form 12C",
#         module_status="Pending Approval",
#         background_tasks=bg
#     )


# async def notify_hr_asset_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "New Asset Declaration Submitted"
#     notif_description = f"{emp_full} has submitted Asset Declaration."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted Asset Declaration. Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Asset Declaration",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name="Asset Declaration",
#         module_status="Pending Approval",
#         background_tasks=bg
#     )


# async def handle_employee_form_submission(
#     db: Session,
#     *,
#     employee_username: str,
#     form_name: str,
#     status: str,
#     bg: BackgroundTasks
# ):
#     hr_usernames = list(set(get_all_hr_usernames(db)))

#     if not hr_usernames:
#         return

#     status_l = (status or "").strip().lower()

#     if status_l == "pending approval":
#         if form_name == "Asset Declaration":
#             for hr_username in hr_usernames:
#                 await notify_hr_asset_update(db, employee_username, hr_username, bg)

#         elif form_name == "Investment Declaration":
#             for hr_username in hr_usernames:
#                 await notify_hr_finance_update(db, employee_username, hr_username, bg)

#         elif form_name == "Form 12C":
#             for hr_username in hr_usernames:
#                 await notify_hr_form12c_update(db, employee_username, hr_username, bg)

#         return

#     if status_l == "approved":
#         emp_full = _full_name_of_user(db, employee_username)
#         hr_username = hr_usernames[0] if hr_usernames else "HR"
#         hr_full = _full_name_of_user(db, hr_username)

#         title = f"{form_name} Approved"
#         notif_description = (
#             f"Dear {emp_full}, your {form_name} has been approved by {hr_full}."
#         )
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your {form_name} has been reviewed and approved by {hr_full}.\n\n"
#             f"Regards,\nHR System"
#         )

#         await send_employee_notification(
#             db=db,
#             type=form_name,
#             title=title,
#             email_body=email_body,
#             notif_description=notif_description,
#             from_user=hr_username,
#             to_user=employee_username,
#             module_name=form_name,
#             module_status="Approved",
#             background_tasks=bg
#         )

# async def notify_hr_bank_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "Bank Details Submitted"
#     notif_description = f"{emp_full} has submitted/updated Bank Details."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted/updated Bank Details. Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Employee Bank",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name="Employee Bank",
#         module_status="Pending Approval",
#         background_tasks=bg
#     )
# async def notify_employee_bank_status_change(
#     db: Session,
#     employee_username: str,
#     hr_username: str,
#     new_status: str,
#     comments: str | None,
#     bg: BackgroundTasks
# ):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     status_clean = new_status.capitalize()
#     title = f"Bank Details {status_clean}"

#     if new_status.lower() == "changes requested":
#         notif_description = f"Dear {emp_full}, your Bank Details were rejected by {hr_full}."
#         reason_text = f"\n\nReason: {comments}" if comments else ""
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your Bank Details were changes requested by {hr_full}."
#             f"{reason_text}\n\n"
#             f"Regards,\nHR System"
#         )
#     else:
#         notif_description = f"Dear {emp_full}, your Bank Details were approved by {hr_full}."
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your Bank Details have been Approved by {hr_full}.\n\n"
#             f"Regards,\nHR System"
#         )

#     await send_employee_notification(
#         db=db,
#         type="Employee Bank",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=hr_username,
#         to_user=employee_username,
#         module_name="Employee Bank",
#         module_status=new_status,
#         background_tasks=bg
#     )


# async def handle_employee_bank_submission(
#     db: Session,
#     *,
#     employee_username: str,
#     status: str,
#     comments: str | None,
#     bg: BackgroundTasks
# ):
#     hr_usernames = list(set(get_all_hr_usernames(db)))

#     if not hr_usernames:
#         return

#     status_l = (status or "").strip().lower()

#     # -------------------------
#     # Pending approval → notify HR
#     # -------------------------
#     if status_l == "pending approval":
#         for hr_username in hr_usernames:
#             await notify_hr_bank_update(db, employee_username, hr_username, bg)
#         return

#     # -------------------------
#     # Approved / Rejected → notify employee
#     # -------------------------
#     if status_l in ("approved", "changes requested"):
#         hr_username = hr_usernames[0] if hr_usernames else "HR"

#         await notify_employee_bank_status_change(
#             db,
#             employee_username,
#             hr_username,
#             status_l,
#             comments,
#             bg
#         )





















# from sqlalchemy.orm import Session
# from datetime import datetime
# from fastapi import BackgroundTasks
# from app.schemas.NotificationSchema import NotificationCreate
# from app.core.Websocket import manager
# from app.utils.EmailUtils import send_email
# from app.models.UserModel import User
# from app.models.NotificationModel import Notification
# import hashlib
# import time

# # Global cache to track recent notification requests (in-memory)
# # Key: hash of (employee_username, sections, new_status, timestamp_minute)
# # Value: timestamp when processed
# _notification_cache = {}
# _CACHE_EXPIRY_SECONDS = 60  # Prevent duplicate notifications within 60 seconds


# # -------------------------
# # Create + save notification (DB)
# # -------------------------
# def create_employee_notification(db: Session, notification: NotificationCreate):
#     try:
#         db_notif = Notification(
#             type=notification.type,
#             title=notification.title,
#             description=notification.description,
#             from_user=notification.from_user,
#             to_user=notification.to_user,
#             module_name=notification.module_name,
#             module_status=notification.module_status,
#             date=datetime.now(),
#             is_read=False,
#             reference_id=notification.reference_id,
#             redirect_url=notification.redirect_url,
#         )
#         db.add(db_notif)
#         db.commit()
#         db.refresh(db_notif)
#         #print("✅ Notification saved with ID:", db_notif.id)
#         return db_notif
#     except Exception as e:
#         db.rollback()
#         #print("❌ NOTIFICATION DB ERROR:", e)
#         raise


# # -------------------------
# # Generic sender (DB + WS + Email)
# # -------------------------
# async def send_employee_notification(
#     db: Session,
#     *,
#     type: str,
#     title: str,
#     email_body: str,
#     notif_description: str | None,
#     from_user: str,
#     to_user: str,
#     module_name: str = "Employee Personal Information",
#     module_status: str | None = None,
#     reference_id: str | None = None,   # ⭐ NEW
#     redirect_url: str | None = None,   # ⭐ NEW
#     background_tasks: BackgroundTasks
# ):
#     # Use notif_description for DB notification; fallback to short slice of email_body
#     desc_for_db = notif_description or (email_body[:200] + ("..." if len(email_body) > 200 else ""))

#     data = NotificationCreate(
#         type=type,
#         title=title,
#         description=desc_for_db,
#         from_user=from_user,
#         to_user=to_user,
#         module_name=module_name,
#         module_status=module_status,
#         reference_id=reference_id,
#         redirect_url=redirect_url,
#     )

#     db_notif = create_employee_notification(db, data)

#     # WS push
#     try:
#         await manager.send_personal_message(to_user, {
#             "id": db_notif.id,
#             "type": db_notif.type,
#             "title": db_notif.title,
#             "description": db_notif.description,
#             "from_user": db_notif.from_user,
#             "to_user": db_notif.to_user,
#             "module_name": db_notif.module_name,
#             "module_status": db_notif.module_status,
#             "date": str(db_notif.date),
#             "reference_id": db_notif.reference_id,
#             "redirect_url": db_notif.redirect_url,
#         })
#     except Exception:
#         pass

#     # Email
#     try:
#         user = db.query(User).filter(User.username == to_user).first()
#         if user and user.email:
#             if background_tasks:
#                 background_tasks.add_task(
#                     send_email,
#                     user.email,
#                     title,
#                     email_body,
#                     "Employee Personal Updates"
#                 )
#             else:
#                 send_email(
#                     user.email,
#                     title,
#                     email_body,
#                     "Employee Personal Updates"
#                 )
#     except Exception:
#         pass

#     return db_notif


#     # -------------------------
#     # Helper functions
#     # -------------------------
# def _full_name_of_user(db: Session, username: str) -> str:
#     u = db.query(User).filter(User.username == username).first()
#     if not u:
#         return username
#     return f"{(u.first_name or '').strip()} {(u.last_name or '').strip()}".strip()


# def get_all_hr_usernames(db: Session) -> list[str]:
#     from app.models.RolePermissionModel import RolePermission

#     rps = (
#         db.query(RolePermission)
#         .filter(
#             RolePermission.submenu_id == 6,
#             RolePermission.role_id == 7
#         )
#         .all()
#     )

#     return list({
#         rp.user.username
#         for rp in rps
#         if rp.user
#     })


# def _clean_cache():
#     """Remove expired entries from cache"""
#     global _notification_cache
#     current_time = time.time()
#     expired_keys = [
#         k for k, v in _notification_cache.items()
#         if current_time - v > _CACHE_EXPIRY_SECONDS
#     ]
#     for k in expired_keys:
#         del _notification_cache[k]


# def _get_request_hash(employee_username: str, sections: list[str], new_status: str) -> str:
#     """Generate a hash for this notification request"""
#     # Use minute-level timestamp to allow same request after 1 minute
#     timestamp_minute = int(time.time() / 60)
#     key_data = f"{employee_username}:{','.join(sorted(sections))}:{new_status}:{timestamp_minute}"
#     return hashlib.md5(key_data.encode()).hexdigest()


# def _is_duplicate_request(employee_username: str, sections: list[str], new_status: str) -> bool:
#     """Check if this notification request was recently processed"""
#     _clean_cache()
#     request_hash = _get_request_hash(employee_username, sections, new_status)
    
#     if request_hash in _notification_cache:
#         #print(f"⚠️ DUPLICATE REQUEST DETECTED - Skipping (hash: {request_hash})")
#         return True
    
#     _notification_cache[request_hash] = time.time()
#     return False


# # -------------------------
# # HR notifications
# # -------------------------
# async def notify_hr_first_time_update(db: Session, employee_username: str, hr_username: str, sections: list[str], reference_id: str | None, redirect_url: str | None, bg: BackgroundTasks):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "Review Employee Updated Details"
#     notif_description = f"{emp_full} has submitted {', '.join(sections or [])}."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted {', '.join(sections or [])}.\n\n"
#         f"Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Employee Personal Information",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_status="Pending Approval",
#         reference_id=reference_id,
#         redirect_url=redirect_url,
#         background_tasks=bg
#     )


# async def notify_hr_section_update(
#     db: Session,
#     employee_username: str,
#     hr_username: str,
#     section: str,
#     bg: BackgroundTasks,
#     changed_fields: list[dict] = None ,  # ⭐ NEW
#     reference_id: str | None = None,
#     redirect_url: str | None = None
# ):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     # ---------- FORMAT CHANGED FIELDS ----------
#     def format_changed_fields(changes):
#         if not changes:
#             return "No field changes"

#         lines = []
#         for c in changes:
#             field_name = c["field"].replace("_", " ").title()
#             lines.append(f"- {field_name}: {c['old']} → {c['new']}")

#         return "\n".join(lines)

#     changes_text = format_changed_fields(changed_fields)

#     # ---------- TITLE ----------
#     title = f"Review {section} Updated"

#     # ✅ UPDATED NOTIFICATION DESCRIPTION (THIS IS WHAT YOU WANT)
#     notif_description = (
#         f"{emp_full} updated {section}: "
#         + ", ".join([
#             f"{c['field'].replace('_',' ').title()} ({c['old']} → {c['new']})"
#             for c in (changed_fields or [])
#         ])
#     )

#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has updated {section}.\n\n"
#         f"Changed Fields:\n{changes_text}\n\n"
#         f"Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Employee Personal Information",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_status=f"Pending Approval {section}",
#         reference_id=reference_id,
#         redirect_url=redirect_url,
#         background_tasks=bg
#     )


# async def notify_employee_on_status_change(db: Session, employee_username: str, hr_username: str, new_status: str, comments: str,changed_sections: str | None, reference_id: str | None, redirect_url: str | None, bg: BackgroundTasks):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     status_clean = new_status.capitalize()
#     title = f"Employee Details {status_clean}"
#     status = new_status.strip().lower().replace("_", " ")
 
#     if status == "changes requested":
#         notif_description = f"{emp_full}, your {changed_sections} was changes requested by Hr."
#         reason_text = f"\n\nReason: {comments}" if comments else ""
#         #print(notif_description + "1")
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your {changed_sections} was changes requested by Hr."
#             f"{reason_text}\n\n"
#             f"Regards,\nHR System"
#         )
#     elif status == "approved":
#         notif_description = f" {emp_full}, your {changed_sections} was approved by Hr."
#         #print(notif_description + "1")
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your {changed_sections} has been Approved by {hr_full}.\n\n"
#             f"Regards,\nHR System"
#         )
 

#     await send_employee_notification(
#         db=db,
#         type="Employee Personal Information",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=hr_username,
#         to_user=employee_username,
#         module_status=new_status,
#         reference_id=reference_id,
#         redirect_url=redirect_url,
#         background_tasks=bg
#     )


# # -------------------------
# # MASTER handler
# # -------------------------
# async def handle_employee_update_notifications(
#     db: Session,
#     *,
#     old_status: str | None,
#     new_status: str | None,
#     old_comments: str | None,
#     new_comments: str | None,
#     employee_username: str,
#     changed_sections: list[str] | None,
#     changed_fields: list[dict] | None,   # ⭐ MUST EXIST
#     reference_id: str | None = None,     # ⭐ NEW
#     redirect_url: str | None = None,     # ⭐ NEW
#     bg: BackgroundTasks
# ):
#     """
#     Centralized notification handler with duplicate request prevention.
#     """

#     #print(f"\n{'='*60}")
#     #print(f"🔔 NOTIFICATION HANDLER CALLED")
#     #print(f"   Employee: {employee_username}")
#     #print(f"   Sections: {changed_sections}")
#     #print(f"   Old Status: {old_status}")
#     #print(f"   New Status: {new_status}")
#     #print(f"{'='*60}")

#     # ✅ Skip if no field changes
#     if not changed_fields and old_status is not None:
#         return

#     # ✅ Duplicate prevention
#     if _is_duplicate_request(employee_username, changed_sections, new_status or ""):
#         #print(f"🛑 DUPLICATE - Skipping")
#         #print(f"{'='*60}\n")
#         return

#     old_s = (old_status or "").strip().lower()
#     new_s = (new_status or "").strip().lower()

#     hr_usernames = list(set(get_all_hr_usernames(db)))

#     if not hr_usernames:
#         #print("⚠️ No HR users found")
#         #print(f"{'='*60}\n")
#         return

#     #print(f"📋 HR Users: {hr_usernames}")

#     # -------------------------
#     # Case 1: Pending Approval
#     # -------------------------
#     if new_s.startswith("pending approval"):
#         #print("📌 Case 1: Pending approval")

#         # 🆕 FIRST TIME CREATE
#         if old_status is None:
#             #print("🆕 First-time create → NO changed fields")

#             for hr_username in hr_usernames:
#                 await notify_hr_first_time_update(
#                     db,
#                     employee_username,
#                     hr_username,
#                     changed_sections or [],
#                     bg=bg,
#                     reference_id=reference_id,
#                     redirect_url=redirect_url
#                 )

#             return

#         # 🔄 UPDATE CASE
#         #print("🔄 Update → WITH changed fields")

#         for hr_username in hr_usernames:
#             for sec in (changed_sections or []):
#                 await notify_hr_section_update(
#                     db,
#                     employee_username,
#                     hr_username,
#                     sec,
#                     bg,
#                     changed_fields,
#                     reference_id,
#                     redirect_url
#                 )

        
#         #print(f"✅ Sent to {len(hr_usernames)} HR users")
#         #print(f"{'='*60}\n")
#         return

#     # -------------------------
#     # Case 2: First-time update
#     # -------------------------
#     if old_s in ("", "null", "none") and changed_sections:
#         #print("📌 Case 2: First-time update")

#         for hr_username in hr_usernames:
#             await notify_hr_first_time_update(
#                 db,
#                 employee_username,
#                 hr_username,
#                 changed_sections,
#                 bg
#             )

#         #print(f"✅ Sent to {len(hr_usernames)} HR users")
#         #print(f"{'='*60}\n")
#         return

#     # -------------------------
#     # Case 3: Resubmit after changes requested
#     # -------------------------
#     if old_s == "changes requested" and changed_sections:
#         #print("📌 Case 3: Resubmit after changes requested")

#         for hr_username in hr_usernames:
#             for sec in changed_sections:
#                 await notify_hr_section_update(
#                     db,
#                     employee_username,
#                     hr_username,
#                     sec,
#                     bg,
#                     changed_fields,
#                     reference_id,
#                     redirect_url
#                 )

#         #print(f"✅ Sent after changes requested update")
#         #print(f"{'='*60}\n")
#         return

#     # -------------------------
#     # Case 4: Update after approval
#     # -------------------------
#     if old_s == "approved" and changed_sections:
#         #print("📌 Case 4: Update after approval")

#         for hr_username in hr_usernames:
#             for sec in changed_sections:
#                 await notify_hr_section_update(
#                     db,
#                     employee_username,
#                     hr_username,
#                     sec,
#                     bg,
#                     changed_fields,
#                     reference_id,
#                     redirect_url
#                 )

#         #print(f"✅ Sent after approval update")
#         #print(f"{'='*60}\n")
#         return

#     # -------------------------
#     # Case 5: HR decision
#     # -------------------------
#     if new_s and old_s != new_s:
#         if new_s in ("approved", "changes requested"):
#             #print(f"📌 Case 5: HR decision - {new_s}")

#             hr_username = hr_usernames[0]

#             await notify_employee_on_status_change(
#                 db,
#                 employee_username,
#                 hr_username,
#                 new_s,
#                 comments=new_comments,
#                 changed_sections=", ".join(changed_sections),
#                 bg=bg,
#                 reference_id=reference_id,
#                 redirect_url=redirect_url
#             )

#             #print("✅ Employee notified")
#             #print(f"{'='*60}\n")
#             return

#     #print("⚠️ No matching condition")
#     #print(f"{'='*60}\n")
#     return


# async def notify_hr_finance_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks, reference_id: str, redirect_url: str):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "New Investment Declaration Submitted"
#     notif_description = f"{emp_full} has submitted Investment Declaration."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted Investment Declaration. Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Investment Declaration",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name="Investment Declaration",
#         module_status="Pending Approval",
#         reference_id=reference_id,
#         redirect_url=redirect_url,
#         background_tasks=bg
#     )


# async def notify_hr_form12c_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks, reference_id: str, redirect_url: str):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "New Form 12C Submitted"
#     notif_description = f"{emp_full} has submitted Form 12C."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted Form 12C. Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Form 12C",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name="Form 12C",
#         module_status="Pending Approval",
#         reference_id=reference_id,
#         redirect_url=redirect_url,
#         background_tasks=bg
#     )


# async def notify_hr_asset_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks, reference_id: str, redirect_url: str):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "New Asset Declaration Submitted"
#     notif_description = f"{emp_full} has submitted Asset Declaration."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted Asset Declaration. Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Asset Declaration",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name="Asset Declaration",
#         module_status="Pending Approval",
#         background_tasks=bg,
#         reference_id=reference_id,
#         redirect_url=redirect_url
#     )


# async def handle_employee_form_submission(
#     db: Session,
#     *,
#     employee_username: str,
#     form_name: str,
#     status: str,
#     bg: BackgroundTasks,
#     reference_id: str | None = None,
#     redirect_url: str | None = None
# ):
#     hr_usernames = list(set(get_all_hr_usernames(db)))

#     if not hr_usernames:
#         return

#     status_l = (status or "").strip().lower()

#     if status_l == "pending approval":
#         if form_name == "Asset Declaration":
#             for hr_username in hr_usernames:
#                 await notify_hr_asset_update(db, employee_username, hr_username, bg,reference_id=reference_id, redirect_url=redirect_url)

#         elif form_name == "Investment Declaration":
#             for hr_username in hr_usernames:
#                 await notify_hr_finance_update(db, employee_username, hr_username, bg, reference_id=reference_id, redirect_url=redirect_url)

#         elif form_name == "Form 12C":
#             for hr_username in hr_usernames:
#                 await notify_hr_form12c_update(db, employee_username, hr_username, bg,reference_id=reference_id, redirect_url=redirect_url)

#         return

#     if status_l == "approved":
#         emp_full = _full_name_of_user(db, employee_username)
#         hr_username = hr_usernames[0] if hr_usernames else "HR"
#         hr_full = _full_name_of_user(db, hr_username)

#         title = f"{form_name} Approved"
#         notif_description = (
#             f"Dear {emp_full}, your {form_name} has been approved by {hr_full}."
#         )
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your {form_name} has been reviewed and approved by {hr_full}.\n\n"
#             f"Regards,\nHR System"
#         )

#         await send_employee_notification(
#             db=db,
#             type=form_name,
#             title=title,
#             email_body=email_body,
#             notif_description=notif_description,
#             from_user=hr_username,
#             to_user=employee_username,
#             module_name=form_name,
#             module_status="Approved",
#             reference_id=reference_id,
#             redirect_url=redirect_url,
#             background_tasks=bg
#         )

# async def notify_hr_bank_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks, reference_id: str | None = None, redirect_url: str | None = None):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     title = "Bank Details Submitted"
#     notif_description = f"{emp_full} has submitted/updated Bank Details."
#     email_body = (
#         f"Dear {hr_full},\n\n"
#         f"{emp_full} has submitted/updated Bank Details. Please review.\n\n"
#         f"Regards,\nHR System"
#     )

#     await send_employee_notification(
#         db=db,
#         type="Employee Bank",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name="Employee Bank",
#         module_status="Pending Approval",
#         reference_id=reference_id,
#         redirect_url=redirect_url,
#         background_tasks=bg
#     )
# async def notify_employee_bank_status_change(
#     db: Session,
#     employee_username: str,
#     hr_username: str,
#     new_status: str,
#     comments: str | None,
#     reference_id: str | None ,
#     redirect_url: str | None ,
#     bg: BackgroundTasks
# ):
#     emp_full = _full_name_of_user(db, employee_username)
#     hr_full = _full_name_of_user(db, hr_username)

#     status_clean = new_status.capitalize()
#     title = f"Bank Details {status_clean}"

#     if new_status.lower() == "changes requested":
#         notif_description = f"Dear {emp_full}, your Bank Details were changes requested by {hr_full}."
#         reason_text = f"\n\nReason: {comments}" if comments else ""
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your Bank Details were Changes Requested by {hr_full}."
#             f"{reason_text}\n\n"
#             f"Regards,\nHR System"
#         )
#     else:
#         notif_description = f"Dear {emp_full}, your Bank Details were approved by {hr_full}."
#         email_body = (
#             f"Dear {emp_full},\n\n"
#             f"Your Bank Details have been Approved by {hr_full}.\n\n"
#             f"Regards,\nHR System"
#         )

#     await send_employee_notification(
#         db=db,
#         type="Employee Bank",
#         title=title,
#         email_body=email_body,
#         notif_description=notif_description,
#         from_user=hr_username,
#         to_user=employee_username,
#         module_name="Employee Bank",
#         module_status=new_status,
#         reference_id=reference_id,
#         redirect_url=redirect_url,
#         background_tasks=bg
#     )


# async def handle_employee_bank_submission(
#     db: Session,
#     *,
#     employee_username: str,
#     status: str,
#     comments: str | None,
#     reference_id: str | None = None,
#     redirect_url: str | None = None,
#     bg: BackgroundTasks
# ):
#     hr_usernames = list(set(get_all_hr_usernames(db)))

#     if not hr_usernames:
#         return

#     status_l = (status or "").strip().lower()

#     # -------------------------
#     # Pending approval → notify HR
#     # -------------------------
#     if status_l == "pending approval":
#         for hr_username in hr_usernames:
#             await notify_hr_bank_update(db, employee_username, hr_username, bg, reference_id, redirect_url)
#         return

#     # -------------------------
#     # Approved / Changes Requested → notify employee
#     # -------------------------
#     if status_l in ("approved", "changes requested"):
#         hr_username = hr_usernames[0] if hr_usernames else "HR"

#         await notify_employee_bank_status_change(
#             db,
#             employee_username,
#             hr_username,
#             status_l,
#             comments,
#             reference_id,
#             redirect_url,
#             bg
#         )








from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from app.schemas.NotificationSchema import NotificationCreate
from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User
from app.models.NotificationModel import Notification
import hashlib
import time

# Global cache to track recent notification requests (in-memory)
# Key: hash of (employee_username, sections, new_status, timestamp_minute)
# Value: timestamp when processed
_notification_cache = {}
_CACHE_EXPIRY_SECONDS = 60  # Prevent duplicate notifications within 60 seconds


# -------------------------
# Create + save notification (DB)
# -------------------------
def create_employee_notification(db: Session, notification: NotificationCreate):
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
            is_read=False,
            reference_id=notification.reference_id,
            redirect_url=notification.redirect_url,

        )
        db.add(db_notif)
        db.commit()
        db.refresh(db_notif)
        #print("✅ Notification saved with ID:", db_notif.id)
        return db_notif
    except Exception as e:
        db.rollback()
        #print("❌ NOTIFICATION DB ERROR:", e)
        raise


# -------------------------
# Generic sender (DB + WS + Email)
# -------------------------
async def send_employee_notification(
    db: Session,
    *,
    type: str,
    title: str,
    email_body: str,
    notif_description: str | None,
    from_user: str,
    to_user: str,
    module_name: str = "Employee Personal Information",
    module_status: str | None = None,
    reference_id: str | None = None,
    redirect_url: str | None = None,
    background_tasks: BackgroundTasks
):
    # Use notif_description for DB notification; fallback to short slice of email_body
    desc_for_db = notif_description or (email_body[:200] + ("..." if len(email_body) > 200 else ""))

    data = NotificationCreate(
        type=type,
        title=title,
        description=desc_for_db,
        from_user=from_user,
        to_user=to_user,
        module_name=module_name,
        module_status=module_status,
        reference_id=reference_id,
        redirect_url=redirect_url,
    )

    db_notif = create_employee_notification(db, data)

    # WS push
    try:
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
            "reference_id": db_notif.reference_id,
            "redirect_url": db_notif.redirect_url,
        })
    except Exception:
        pass

    # Email
    try:
        user = db.query(User).filter(User.username == to_user).first()
        if user and user.email:
            if background_tasks:
                background_tasks.add_task(
                    send_email,
                    user.email,
                    title,
                    email_body,
                    "Employee Personal Updates"
                )
            else:
                send_email(
                    user.email,
                    title,
                    email_body,
                    "Employee Personal Updates"
                )
    except Exception:
        pass

    return db_notif


    # -------------------------
    # Helper functions
    # -------------------------
def _full_name_of_user(db: Session, username: str) -> str:
    u = db.query(User).filter(User.username == username).first()
    if not u:
        return username
    return f"{(u.first_name or '').strip()} {(u.last_name or '').strip()}".strip()


def get_all_hr_usernames(db: Session) -> list[str]:
    from app.models.RolePermissionModel import RolePermission

    rps = (
        db.query(RolePermission)
        .filter(
            RolePermission.submenu_id == 6,
            RolePermission.role_id == 7
        )
        .all()
    )

    return list({
        rp.user.username
        for rp in rps
        if rp.user
    })


def _clean_cache():
    """Remove expired entries from cache"""
    global _notification_cache
    current_time = time.time()
    expired_keys = [
        k for k, v in _notification_cache.items()
        if current_time - v > _CACHE_EXPIRY_SECONDS
    ]
    for k in expired_keys:
        del _notification_cache[k]


def _get_request_hash(employee_username: str, sections: list[str], new_status: str, changed_fields: list) -> str:
    import json
    timestamp_minute = int(time.time() / 60)

    key_data = {
        "user": employee_username,
        "sections": sorted(sections or []),
        "status": new_status,
        "changes": changed_fields,   # 🔥 IMPORTANT FIX
        "time": timestamp_minute
    }

    return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()


def _is_duplicate_request(employee_username: str, sections: list[str], new_status: str, changed_fields: list) -> bool:
    """Check if this notification request was recently processed"""
    _clean_cache()
    request_hash = _get_request_hash(employee_username, sections, new_status, changed_fields)
    
    if request_hash in _notification_cache:
        #print(f"⚠️ DUPLICATE REQUEST DETECTED - Skipping (hash: {request_hash})")
        return True
    
    _notification_cache[request_hash] = time.time()
    return False


# -------------------------
# HR notifications
# -------------------------
async def notify_hr_first_time_update(db: Session, employee_username: str, hr_username: str, sections: list[str],reference_id: str | None, redirect_url: str | None , bg: BackgroundTasks):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "Review Employee Updated Details"
    notif_description = f"{emp_full} has submitted {', '.join(sections or [])}."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has submitted {', '.join(sections or [])}.\n\n"
        f"Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Employee Personal Information",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_status="Pending Approval",
        reference_id=reference_id,
        redirect_url=redirect_url,
        background_tasks=bg
    )


async def notify_hr_section_update(
    db: Session,
    employee_username: str,
    hr_username: str,
    section: str,
    bg: BackgroundTasks,
    changed_fields: list[dict] = None ,
    reference_id: str | None = None,
    redirect_url: str | None = None
      # ⭐ NEW
):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    # ---------- FORMAT CHANGED FIELDS ----------
    def format_changed_fields(changed_fields):
        formatted = []

        for item in changed_fields:
            field = item.get("field")
            old = item.get("old")
            new = item.get("new")

            if str(old) == str(new):
                continue

            # clean field name
            field_name = field.replace("_", " ").title()

            formatted.append(f"{field_name} ({old} → {new})")

        return ", ".join(formatted)

    changes_text = format_changed_fields(changed_fields)

    # ---------- TITLE ----------
    title = f"Review {section} Updated"

    # ✅ UPDATED NOTIFICATION DESCRIPTION (THIS IS WHAT YOU WANT)
    notif_description = (
        f"{emp_full} updated {section}: "
        + ", ".join([
            f"{c['field'].replace('_',' ').title()} ({c['old']} → {c['new']})"
            for c in (changed_fields or [])
        ])
    )

    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has updated {section}.\n\n"
        f"Changed Fields:\n{changes_text}\n\n"
        f"Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Employee Personal Information",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_status=f"Pending Approval {section}",
        reference_id=reference_id,
        redirect_url=redirect_url,
        background_tasks=bg
    )


async def notify_employee_on_status_change(db: Session, employee_username: str, hr_username: str, new_status: str, comments: str,changed_sections: str | None, reference_id: str | None, redirect_url: str | None, bg: BackgroundTasks):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    status_clean = new_status.capitalize()
    title = f"Employee Details {status_clean}"
    status = new_status.strip().lower().replace("_", " ")
 
    if status == "changes requested":
        notif_description = f"{emp_full}, your {changed_sections} was changes requested by Hr."
        reason_text = f"\n\nReason: {comments}" if comments else ""
        #print(notif_description + "1")
        email_body = (
            f"Dear {emp_full},\n\n"
            f"Your {changed_sections} was changes requested by Hr."
            f"{reason_text}\n\n"
            f"Regards,\nHR System"
        )
    elif status == "approved":
        notif_description = f" {emp_full}, your {changed_sections} was approved by Hr."
        #print(notif_description + "1")
        email_body = (
            f"Dear {emp_full},\n\n"
            f"Your {changed_sections} has been Approved by {hr_full}.\n\n"
            f"Regards,\nHR System"
        )
 

    await send_employee_notification(
        db=db,
        type="Employee Personal Information",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=hr_username,
        to_user=employee_username,
        module_status=new_status,
        reference_id=reference_id,
        redirect_url=redirect_url,
        background_tasks=bg
    )


# -------------------------
# MASTER handler
# -------------------------
async def handle_employee_update_notifications(
    db: Session,
    *,
    old_status: str | None,
    new_status: str | None,
    old_comments: str | None,
    new_comments: str | None,
    employee_username: str,
    changed_sections: list[str] | None,
    changed_fields: list[dict] | None,   # ⭐ MUST EXIST
    reference_id: str | None = None,
    redirect_url: str | None = None,
    bg: BackgroundTasks
):
    """
    Centralized notification handler with duplicate request prevention.
    """

    #print(f"\n{'='*60}")
    #print(f"🔔 NOTIFICATION HANDLER CALLED")
    #print(f"   Employee: {employee_username}")
    #print(f"   Sections: {changed_sections}")
    #print(f"   Old Status: {old_status}")
    #print(f"   New Status: {new_status}")
    #print(f"{'='*60}")

    # ✅ Skip if no field changes
    if not changed_fields and old_status is not None:
        return

    # ✅ Duplicate prevention
    if _is_duplicate_request(employee_username, changed_sections, new_status or "", changed_fields):
        #print(f"🛑 DUPLICATE - Skipping")
        #print(f"{'='*60}\n")
        return

    old_s = (old_status or "").strip().lower()
    new_s = (new_status or "").strip().lower()

    hr_usernames = list(set(get_all_hr_usernames(db)))

    if not hr_usernames:
        #print("⚠️ No HR users found")
        #print(f"{'='*60}\n")
        return

    ##print(f"📋 HR Users: {hr_usernames}")

    # -------------------------
    # Case 1: Pending Approval
    # -------------------------
    if new_s.startswith("pending approval"):
        ##print\("📌 Case 1: Pending approval")

        # 🆕 FIRST TIME CREATE
        if old_status is None:
            ##print("🆕 First-time create → NO changed fields")

            for hr_username in hr_usernames:
                await notify_hr_first_time_update(
                    db,
                    employee_username,
                    hr_username,
                    changed_sections or [],
                    bg=bg,
                    reference_id=reference_id,
                    redirect_url=redirect_url,
                    
                )

            return

        # 🔄 UPDATE CASE
        ##print("🔄 Update → WITH changed fields")

        for hr_username in hr_usernames:
            for sec in (changed_sections or []):
                await notify_hr_section_update(
                    db,
                    employee_username,
                    hr_username,
                    sec,
                    bg,
                    changed_fields,
                    reference_id,
                    redirect_url
                )

        
        ##print(f"✅ Sent to {len(hr_usernames)} HR users")
        ##print(f"{'='*60}\n")
        return

    # -------------------------
    # Case 2: First-time update
    # -------------------------
    if old_s in ("", "null", "none") and changed_sections:
        ##print("📌 Case 2: First-time update")

        for hr_username in hr_usernames:
            await notify_hr_first_time_update(
                db,
                employee_username,
                hr_username,
                changed_sections,   
                reference_id,
                redirect_url,
                bg
            )

        ##print(f"✅ Sent to {len(hr_usernames)} HR users")
        ##print(f"{'='*60}\n")
        return

    # -------------------------
    # Case 3: Resubmit after changes requested
    # -------------------------
    if old_s == "changes requested" and changed_sections:
        ##print("📌 Case 3: Resubmit after changes requested")

        for hr_username in hr_usernames:
            for sec in changed_sections:
                await notify_hr_section_update(
                    db,
                    employee_username,
                    hr_username,
                    sec,
                    bg,
                    changed_fields,
                    reference_id,
                    redirect_url
                )

        ##print(f"✅ Sent after changes requested update")
        ##print(f"{'='*60}\n")
        return

    # -------------------------
    # Case 4: Update after approval
    # -------------------------
    if old_s == "approved" and changed_sections:
        ##print("📌 Case 4: Update after approval")

        for hr_username in hr_usernames:
            for sec in changed_sections:
                await notify_hr_section_update(
                    db,
                    employee_username,
                    hr_username,
                    sec,
                    bg,
                    changed_fields,
                    reference_id,
                    redirect_url
                )

        ##print(f"✅ Sent after approval update")
        ##print(f"{'='*60}\n")
        return

    # -------------------------
    # Case 5: HR decision
    # -------------------------
    if new_s and old_s != new_s:
        if new_s in ("approved", "changes requested"):
            ##print(f"📌 Case 5: HR decision - {new_s}")

            hr_username = hr_usernames[0]

            await notify_employee_on_status_change(
                db,
                employee_username,
                hr_username,
                new_s,
                comments=new_comments,
                changed_sections=", ".join(changed_sections),
                bg=bg,
                reference_id=reference_id,
                redirect_url=redirect_url,
                

            )

            ##print("✅ Employee notified")
            ##print(f"{'='*60}\n")
            return

    ##print("⚠️ No matching condition")
    ##print(f"{'='*60}\n")
    return


async def notify_hr_finance_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks, reference_id: str = None, redirect_url: str = None):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "New Investment Declaration Submitted"
    notif_description = f"{emp_full} has submitted Investment Declaration."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has submitted Investment Declaration. Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Investment Declaration",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_name="Investment Declaration",
        module_status="Pending Approval",
        reference_id=reference_id,
        redirect_url=redirect_url,
        background_tasks=bg
    )


async def notify_hr_form12c_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks, reference_id: str = None, redirect_url: str = None):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "New Form 12C Submitted"
    notif_description = f"{emp_full} has submitted Form 12C."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has submitted Form 12C. Please review.\n\n"
        f"Regards,\nHR System"
    )   

    await send_employee_notification(
        db=db,
        type="Form 12C",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_name="Form 12C",
        module_status="Pending Approval",
        reference_id=reference_id,
        redirect_url=redirect_url,
        background_tasks=bg
    )


async def notify_hr_asset_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks, reference_id: str = None, redirect_url: str = None):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "New Asset Declaration Submitted"
    notif_description = f"{emp_full} has submitted Asset Declaration."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has submitted Asset Declaration. Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Asset Declaration",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_name="Asset Declaration",
        module_status="Pending Approval",
        background_tasks=bg,
        reference_id=reference_id,
        redirect_url=redirect_url

    )


async def handle_employee_form_submission(
    db: Session,
    *,
    employee_username: str,
    form_name: str,
    status: str,
    bg: BackgroundTasks,
    reference_id: str | None = None,
    redirect_url: str | None = None
):
    hr_usernames = list(set(get_all_hr_usernames(db)))

    if not hr_usernames:
        return

    status_l = (status or "").strip().lower()

    if status_l == "pending approval":
        if form_name == "Asset Declaration":
            for hr_username in hr_usernames:
                await notify_hr_asset_update(db, employee_username, hr_username, bg)

        elif form_name == "Investment Declaration":
            for hr_username in hr_usernames:
                await notify_hr_finance_update(db, employee_username, hr_username, bg)

        elif form_name == "Form 12C":
            for hr_username in hr_usernames:
                await notify_hr_form12c_update(db, employee_username, hr_username, bg)

        return

    if status_l == "approved":
        emp_full = _full_name_of_user(db, employee_username)
        hr_username = hr_usernames[0] if hr_usernames else "HR"
        hr_full = _full_name_of_user(db, hr_username)

        title = f"{form_name} Approved"
        notif_description = (
            f"Dear {emp_full}, your {form_name} has been approved by {hr_full}."
        )
        email_body = (
            f"Dear {emp_full},\n\n"
            f"Your {form_name} has been reviewed and approved by {hr_full}.\n\n"
            f"Regards,\nHR System"
        )

        await send_employee_notification(
            db=db,
            type=form_name,
            title=title,
            email_body=email_body,
            notif_description=notif_description,
            from_user=hr_username,
            to_user=employee_username,
            module_name=form_name,
            module_status="Approved",
            reference_id=reference_id,
            redirect_url=redirect_url,
            background_tasks=bg
        )

async def notify_hr_bank_update(db: Session, employee_username: str, hr_username: str, bg: BackgroundTasks, reference_id: str = None, redirect_url: str = None):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    title = "Bank Details Submitted"
    notif_description = f"{emp_full} has submitted/updated Bank Details."
    email_body = (
        f"Dear {hr_full},\n\n"
        f"{emp_full} has submitted/updated Bank Details. Please review.\n\n"
        f"Regards,\nHR System"
    )

    await send_employee_notification(
        db=db,
        type="Employee Bank",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=employee_username,
        to_user=hr_username,
        module_name="Employee Bank",
        module_status="Pending Approval",
        reference_id=reference_id,
        redirect_url=redirect_url,
        background_tasks=bg
    )
async def notify_employee_bank_status_change(
    db: Session,
    employee_username: str,
    hr_username: str,
    new_status: str,
    comments: str | None,
    reference_id: str | None,
    redirect_url: str | None,

    bg: BackgroundTasks
):
    emp_full = _full_name_of_user(db, employee_username)
    hr_full = _full_name_of_user(db, hr_username)

    status_clean = new_status.capitalize()
    title = f"Bank Details {status_clean}"

    if new_status.lower() == "changes requested":
        notif_description = f"Dear {emp_full}, your Bank Details were changes requested by {hr_full}."
        reason_text = f"\n\nReason: {comments}" if comments else ""
        email_body = (
            f"Dear {emp_full},\n\n"
            f"Your Bank Details were Changes Requested by {hr_full}."
            f"{reason_text}\n\n"
            f"Regards,\nHR System"
        )
    else:
        notif_description = f"Dear {emp_full}, your Bank Details were approved by {hr_full}."
        email_body = (
            f"Dear {emp_full},\n\n"
            f"Your Bank Details have been Approved by {hr_full}.\n\n"
            f"Regards,\nHR System"
        )

    await send_employee_notification(
        db=db,
        type="Employee Bank",
        title=title,
        email_body=email_body,
        notif_description=notif_description,
        from_user=hr_username,
        to_user=employee_username,
        module_name="Employee Bank",
        module_status=new_status,
        reference_id=reference_id,
        redirect_url=redirect_url,
        background_tasks=bg
    )


async def handle_employee_bank_submission(
    db: Session,
    *,
    employee_username: str,
    status: str,
    comments: str | None,
    reference_id: str | None = None,
    redirect_url: str | None = None,
    bg: BackgroundTasks
):
    hr_usernames = list(set(get_all_hr_usernames(db)))

    if not hr_usernames:
        return

    status_l = (status or "").strip().lower()

    # -------------------------
    # Pending approval → notify HR
    # -------------------------
    if status_l == "pending approval":
        for hr_username in hr_usernames:
            await notify_hr_bank_update(db, employee_username, hr_username, bg,reference_id,redirect_url)
        return

    # -------------------------
    # Approved / Changes Requested → notify employee
    # -------------------------
    if status_l in ("approved", "changes requested"):
        hr_username = hr_usernames[0] if hr_usernames else "HR"

        await notify_employee_bank_status_change(
            db,
            employee_username,
            hr_username,
            status_l,
            comments,
            reference_id,
            redirect_url,
            bg
        )















# from sqlalchemy.orm import Session
# from datetime import datetime
# from fastapi import BackgroundTasks
# from app.schemas.NotificationSchema import NotificationCreate
# from app.core.Websocket import manager
# from app.utils.EmailUtils import send_email
# from app.models.UserModel import User
# from app.models.NotificationModel import Notification
# import hashlib
# import time


# # ==============================
# # STANDARD STATUS CONSTANTS
# # ==============================

# STATUS_PENDING = "Pending Approval"
# STATUS_APPROVED = "Approved"
# STATUS_CHANGES_REQUESTED = "Changes Requested"
# STATUS_VERIFIED = "Approved"


# # ==============================
# # DUPLICATE CACHE
# # ==============================

# _notification_cache = {}
# _CACHE_EXPIRY_SECONDS = 60


# # ==============================
# # CREATE NOTIFICATION
# # ==============================

# def create_employee_notification(db: Session, notification: NotificationCreate):

#     ##print("\n========== CREATE NOTIFICATION ==========")
#     ##print("From:", notification.from_user)
#     ##print("To:", notification.to_user)
#     ##print("Module:", notification.module_name)
#     ##print("Status:", notification.module_status)

#     try:

#         db_notif = Notification(
#             type=notification.type,
#             title=notification.title,
#             description=notification.description,
#             from_user=notification.from_user,
#             to_user=notification.to_user,
#             module_name=notification.module_name,
#             module_status=notification.module_status,
#             date=datetime.now(),
#             is_read=False
#         )

#         db.add(db_notif)
#         db.commit()
#         db.refresh(db_notif)

#         ##print("✅ Notification Saved In DB -> ID:", db_notif.id)

#         return db_notif

#     except Exception as e:

#         db.rollback()
#         ##print("❌ Notification DB Error:", e)
#         raise


# # ==============================
# # SEND NOTIFICATION
# # ==============================

# async def send_employee_notification(
#     db: Session,
#     *,
#     type: str,
#     title: str,
#     email_body: str,
#     notif_description: str | None,
#     from_user: str,
#     to_user: str,
#     module_name: str,
#     module_status: str,
#     background_tasks: BackgroundTasks
# ):

#     ##print("\n========== SEND NOTIFICATION START ==========")
#     ##print("Type:", type)
#     ##print("Title:", title)
#     ##print("From:", from_user)
#     ##print("To:", to_user)
#     ##print("Module:", module_name)
#     ##print("Status:", module_status)

#     desc = notif_description or email_body[:200]

#     data = NotificationCreate(
#         type=type,
#         title=title,
#         description=desc,
#         from_user=from_user,
#         to_user=to_user,
#         module_name=module_name,
#         module_status=module_status
#     )

#     db_notif = create_employee_notification(db, data)

#     # -----------------------
#     # WebSocket Notification
#     # -----------------------

#     try:

#         ##print("📡 Sending WebSocket notification...")

#         await manager.send_personal_message(
#             to_user,
#             {
#                 "id": db_notif.id,
#                 "title": db_notif.title,
#                 "description": db_notif.description,
#                 "module_status": db_notif.module_status,
#                 "date": str(db_notif.date),
#             },
#         )

#         ##print("✅ WebSocket Sent Successfully")

#     except Exception as e:
#         ##print("⚠️ WebSocket Failed:", e)

#     # -----------------------
#     # Email Notification
#     # -----------------------

#     try:

#         ##print("📧 Fetching email for:", to_user)

#         user = db.query(User).filter(User.username == to_user).first()

#         if user and user.email:

#             ##print("📧 Email Found:", user.email)
#             ##print("📧 Sending Email...")

#             if background_tasks:

#                 background_tasks.add_task(
#                     send_email,
#                     user.email,
#                     title,
#                     email_body,
#                     "Employee Workflow Notification"
#                 )

#                 ##print("✅ Email task added to BackgroundTasks")

#             else:

#                 send_email(
#                     user.email,
#                     title,
#                     email_body,
#                     "Employee Workflow Notification"
#                 )

#                 ##print("✅ Email Sent Directly")

#         else:
#             ##print("⚠️ No email found for user")

#     except Exception as e:
#         ##print("❌ Email Sending Error:", e)

#     ##print("========== SEND NOTIFICATION END ==========\n")

#     return db_notif


# # ==============================
# # HELPER FUNCTIONS
# # ==============================

# def _full_name_of_user(db: Session, username: str):

#     ##print("🔍 Fetching full name for:", username)

#     u = db.query(User).filter(User.username == username).first()

#     if not u:
#         ##print("⚠️ User not found")
#         return username

#     full_name = f"{(u.first_name or '').strip()} {(u.last_name or '').strip()}".strip()

#     ##print("✅ Full Name:", full_name)

#     return full_name


# def get_all_hr_usernames(db: Session):

#     ##print("\n🔎 Fetching HR users...")

#     from app.models.RolePermissionModel import RolePermission

#     rps = (
#         db.query(RolePermission)
#         .filter(
#             RolePermission.submenu_id == 6,
#             RolePermission.role_id == 7
#         )
#         .all()
#     )

#     hr_users = list({rp.user.username for rp in rps if rp.user})

#     ##print("👥 HR Users Found:", hr_users)

#     return hr_users


# # ==============================
# # DUPLICATE CHECK
# # ==============================

# def _is_duplicate_request(employee_username, section, status):

#     key = f"{employee_username}:{section}:{status}:{int(time.time()/60)}"
#     h = hashlib.md5(key.encode()).hexdigest()

#     if h in _notification_cache:

#         ##print("⚠️ Duplicate Notification Skipped ->", employee_username, section)
#         return True

#     _notification_cache[h] = time.time()

#     return False


# # ==============================
# # HR NOTIFICATION
# # ==============================

# async def notify_hr_section_update(db, employee_username, hr_username, section, bg):

#     ##print("\n🔔 HR Notification Triggered")
#     ##print("Employee:", employee_username)
#     ##print("HR:", hr_username)
#     ##print("Section:", section)

#     if _is_duplicate_request(employee_username, section, STATUS_PENDING):
#         return

#     emp = _full_name_of_user(db, employee_username)
#     hr = _full_name_of_user(db, hr_username)

#     title = f"{section} Submitted"

#     email_body = f"""
# Dear {hr},

# {emp} has submitted {section}.

# Please review and approve.

# Regards
# HR System
# """

#     await send_employee_notification(
#         db=db,
#         type=section,
#         title=title,
#         email_body=email_body,
#         notif_description=f"{emp} submitted {section}",
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name=section,
#         module_status=STATUS_PENDING,
#         background_tasks=bg
#     )


# # ==============================
# # EMPLOYEE STATUS CHANGE
# # ==============================

# async def notify_employee_on_status_change(
#     db,
#     employee_username,
#     hr_username,
#     new_status,
#     comments,
#     section,
#     bg
# ):

#     ##print("\n🔄 Employee Status Change Notification")
#     ##print("Employee:", employee_username)
#     ##print("HR:", hr_username)
#     ##print("Section:", section)
#     ##print("New Status:", new_status)

#     emp = _full_name_of_user(db, employee_username)
#     hr = _full_name_of_user(db, hr_username)

#     if new_status == STATUS_APPROVED:

#         title = f"{section} Approved"

#         email_body = f"""
# Dear {emp},

# Your {section} has been approved by {hr}.

# Regards
# HR System
# """

#     else:

#         title = f"{section} Changes Requested"

#         email_body = f"""
# Dear {emp},

# HR has requested changes in {section}.

# Comments:
# {comments}

# Please update and resubmit.

# Regards
# HR System
# """

#     await send_employee_notification(
#         db=db,
#         type=section,
#         title=title,
#         email_body=email_body,
#         notif_description=title,
#         from_user=hr_username,
#         to_user=employee_username,
#         module_name=section,
#         module_status=new_status,
#         background_tasks=bg
#     )


# # ==============================
# # MASTER UPDATE HANDLER
# # ==============================

# async def handle_employee_update_notifications(
#     db: Session,
#     *,
#     old_status,
#     new_status,
#     old_comments,
#     new_comments,
#     employee_username,
#     changed_sections,
#     bg: BackgroundTasks
# ):

#     ##print("\n🚀 MASTER WORKFLOW STARTED")
#     ##print("Employee:", employee_username)
#     ##print("Old Status:", old_status)
#     ##print("New Status:", new_status)
#     ##print("Sections:", changed_sections)

#     hr_users = get_all_hr_usernames(db)

#     if not hr_users:
#         ##print("⚠️ No HR users found")
#         return

#     for section in changed_sections:

#         if new_status == STATUS_PENDING:

#             for hr in hr_users:
#                 await notify_hr_section_update(db, employee_username, hr, section, bg)

#         elif new_status in [STATUS_APPROVED, STATUS_CHANGES_REQUESTED]:

#             hr = hr_users[0]

#             await notify_employee_on_status_change(
#                 db,
#                 employee_username,
#                 hr,
#                 new_status,
#                 new_comments,
#                 section,
#                 bg
#             )


# # ==============================
# # FORM SUBMISSION HANDLER
# # ==============================

# async def handle_employee_form_submission(
#     db,
#     *,
#     employee_username,
#     form_name,
#     status,
#     bg
# ):

#     ##print("\n📄 FORM SUBMISSION WORKFLOW")
#     ##print("Employee:", employee_username)
#     ##print("Form:", form_name)
#     ##print("Status:", status)

#     hr_users = get_all_hr_usernames(db)

#     if not hr_users:
#         ##print("⚠️ No HR users found")
#         return

#     if status == STATUS_PENDING:

#         ##print("➡️ Sending submission notification to HR")

#         for hr in hr_users:
#             await notify_hr_section_update(
#                 db,
#                 employee_username,
#                 hr,
#                 form_name,
#                 bg
#             )

#     elif status in [STATUS_APPROVED, STATUS_CHANGES_REQUESTED]:

#         ##print("➡️ Sending HR decision notification to Employee")

#         hr = hr_users[0]

#         await notify_employee_on_status_change(
#             db,
#             employee_username,
#             hr,
#             status,
#             None,
#             form_name,
#             bg
#         )


# # ==============================
# # BANK NOTIFICATIONS
# # ==============================

# async def notify_hr_bank_update(db, employee_username, hr_username, bg):

#     ##print("\n🏦 BANK SUBMISSION WORKFLOW")

#     await notify_hr_section_update(
#         db,
#         employee_username,
#         hr_username,
#         "Bank Details",
#         bg
#     )


# async def notify_employee_bank_status_change(
#     db,
#     employee_username,
#     hr_username,
#     new_status,
#     comments,
#     bg
# ):

#     ##print("\n🏦 BANK STATUS CHANGE WORKFLOW")

#     await notify_employee_on_status_change(
#         db,
#         employee_username,
#         hr_username,
#         new_status,
#         comments,
#         "Bank Details",
#         bg
#     )


# async def handle_employee_bank_submission(
#     db,
#     *,
#     employee_username,
#     status,
#     comments,
#     bg
# ):

#     ##print("\n🏦 BANK WORKFLOW STARTED")
#     ##print("Employee:", employee_username)
#     ##print("Status:", status)

#     hr_users = get_all_hr_usernames(db)

#     if not hr_users:
#         ##print("⚠️ No HR users found")
#         return

#     if status == STATUS_PENDING:

#         for hr in hr_users:
#             await notify_hr_bank_update(db, employee_username, hr, bg)

#     elif status in [STATUS_APPROVED, STATUS_CHANGES_REQUESTED]:

#         hr = hr_users[0]

#         await notify_employee_bank_status_change(
#             db,
#             employee_username,
#             hr,
#             status,
#             comments,
#             bg
#         )







# from sqlalchemy.orm import Session
# from datetime import datetime
# from fastapi import BackgroundTasks
# from app.schemas.NotificationSchema import NotificationCreate
# from app.core.Websocket import manager
# from app.utils.EmailUtils import send_email
# from app.models.UserModel import User
# from app.models.NotificationModel import Notification
# import hashlib
# import time


# # ==============================
# # STANDARD STATUS CONSTANTS
# # ==============================

# STATUS_PENDING = "Pending Approval"
# STATUS_APPROVED = "Approved"
# STATUS_CHANGES_REQUESTED = "Changes Requested"
# STATUS_VERIFIED = "Approved"


# # ==============================
# # DUPLICATE CACHE
# # ==============================

# _notification_cache = {}
# _CACHE_EXPIRY_SECONDS = 60


# # ==============================
# # CREATE NOTIFICATION
# # ==============================

# def create_employee_notification(db: Session, notification: NotificationCreate):

#     ##print("\n========== CREATE NOTIFICATION ==========")
#     ##print("From:", notification.from_user)
#     ##print("To:", notification.to_user)
#     ##print("Module:", notification.module_name)
#     ##print("Status:", notification.module_status)

#     try:

#         db_notif = Notification(
#             type=notification.type,
#             title=notification.title,
#             description=notification.description,
#             from_user=notification.from_user,
#             to_user=notification.to_user,
#             module_name=notification.module_name,
#             module_status=notification.module_status,
#             date=datetime.now(),
#             is_read=False
#         )

#         db.add(db_notif)
#         db.commit()
#         db.refresh(db_notif)

#         ##print("✅ Notification Saved In DB -> ID:", db_notif.id)

#         return db_notif

#     except Exception as e:

#         db.rollback()
#         ##print("❌ Notification DB Error:", e)
#         raise


# # ==============================
# # SEND NOTIFICATION
# # ==============================

# async def send_employee_notification(
#     db: Session,
#     *,
#     type: str,
#     title: str,
#     email_body: str,
#     notif_description: str | None,
#     from_user: str,
#     to_user: str,
#     module_name: str,
#     module_status: str,
#     background_tasks: BackgroundTasks
# ):

#     ##print("\n========== SEND NOTIFICATION START ==========")
#     ##print("Type:", type)
#     ##print("Title:", title)
#     ##print("From:", from_user)
#     ##print("To:", to_user)
#     ##print("Module:", module_name)
#     ##print("Status:", module_status)

#     desc = notif_description or email_body[:200]

#     data = NotificationCreate(
#         type=type,
#         title=title,
#         description=desc,
#         from_user=from_user,
#         to_user=to_user,
#         module_name=module_name,
#         module_status=module_status
#     )

#     db_notif = create_employee_notification(db, data)

#     # -----------------------
#     # WebSocket Notification
#     # -----------------------

#     try:

#         ##print("📡 Sending WebSocket notification...")

#         await manager.send_personal_message(
#             to_user,
#             {
#                 "id": db_notif.id,
#                 "title": db_notif.title,
#                 "description": db_notif.description,
#                 "module_status": db_notif.module_status,
#                 "date": str(db_notif.date),
#             },
#         )

#         ##print("✅ WebSocket Sent Successfully")

#     except Exception as e:
#         ##print("⚠️ WebSocket Failed:", e)

#     # -----------------------
#     # Email Notification
#     # -----------------------

#     try:

#         ##print("📧 Fetching email for:", to_user)

#         user = db.query(User).filter(User.username == to_user).first()

#         if user and user.email:

#             ##print("📧 Email Found:", user.email)
#             ##print("📧 Sending Email...")

#             if background_tasks:

#                 background_tasks.add_task(
#                     send_email,
#                     user.email,
#                     title,
#                     email_body,
#                     "Employee Workflow Notification"
#                 )

#                 ##print("✅ Email task added to BackgroundTasks")

#             else:

#                 send_email(
#                     user.email,
#                     title,
#                     email_body,
#                     "Employee Workflow Notification"
#                 )

#                 ##print("✅ Email Sent Directly")

#         else:
#             ##print("⚠️ No email found for user")

#     except Exception as e:
#         ##print("❌ Email Sending Error:", e)

#     ##print("========== SEND NOTIFICATION END ==========\n")

#     return db_notif


# # ==============================
# # HELPER FUNCTIONS
# # ==============================

# def _full_name_of_user(db: Session, username: str):

#     ##print("🔍 Fetching full name for:", username)

#     u = db.query(User).filter(User.username == username).first()

#     if not u:
#         ##print("⚠️ User not found")
#         return username

#     full_name = f"{(u.first_name or '').strip()} {(u.last_name or '').strip()}".strip()

#     ##print("✅ Full Name:", full_name)

#     return full_name


# def get_all_hr_usernames(db: Session):

#     ##print("\n🔎 Fetching HR users...")

#     from app.models.RolePermissionModel import RolePermission

#     rps = (
#         db.query(RolePermission)
#         .filter(
#             RolePermission.submenu_id == 6,
#             RolePermission.role_id == 7
#         )
#         .all()
#     )

#     hr_users = list({rp.user.username for rp in rps if rp.user})

#     ##print("👥 HR Users Found:", hr_users)

#     return hr_users


# # ==============================
# # DUPLICATE CHECK
# # ==============================

# def _is_duplicate_request(employee_username, section, status):

#     key = f"{employee_username}:{section}:{status}:{int(time.time()/60)}"
#     h = hashlib.md5(key.encode()).hexdigest()

#     if h in _notification_cache:

#         ##print("⚠️ Duplicate Notification Skipped ->", employee_username, section)
#         return True

#     _notification_cache[h] = time.time()

#     return False


# # ==============================
# # HR NOTIFICATION
# # ==============================

# async def notify_hr_section_update(db, employee_username, hr_username, section, bg):

#     ##print("\n🔔 HR Notification Triggered")
#     ##print("Employee:", employee_username)
#     ##print("HR:", hr_username)
#     ##print("Section:", section)

#     if _is_duplicate_request(employee_username, section, STATUS_PENDING):
#         return

#     emp = _full_name_of_user(db, employee_username)
#     hr = _full_name_of_user(db, hr_username)

#     title = f"{section} Submitted"

#     email_body = f"""
# Dear {hr},

# {emp} has submitted {section}.

# Please review and approve.

# Regards
# HR System
# """

#     await send_employee_notification(
#         db=db,
#         type=section,
#         title=title,
#         email_body=email_body,
#         notif_description=f"{emp} submitted {section}",
#         from_user=employee_username,
#         to_user=hr_username,
#         module_name=section,
#         module_status=STATUS_PENDING,
#         background_tasks=bg
#     )


# # ==============================
# # EMPLOYEE STATUS CHANGE
# # ==============================

# async def notify_employee_on_status_change(
#     db,
#     employee_username,
#     hr_username,
#     new_status,
#     comments,
#     section,
#     bg
# ):

#     ##print("\n🔄 Employee Status Change Notification")
#     ##print("Employee:", employee_username)
#     ##print("HR:", hr_username)
#     ##print("Section:", section)
#     ##print("New Status:", new_status)

#     emp = _full_name_of_user(db, employee_username)
#     hr = _full_name_of_user(db, hr_username)

#     if new_status == STATUS_APPROVED:

#         title = f"{section} Approved"

#         email_body = f"""
# Dear {emp},

# Your {section} has been approved by {hr}.

# Regards
# HR System
# """

#     else:

#         title = f"{section} Changes Requested"

#         email_body = f"""
# Dear {emp},

# HR has requested changes in {section}.

# Comments:
# {comments}

# Please update and resubmit.

# Regards
# HR System
# """

#     await send_employee_notification(
#         db=db,
#         type=section,
#         title=title,
#         email_body=email_body,
#         notif_description=title,
#         from_user=hr_username,
#         to_user=employee_username,
#         module_name=section,
#         module_status=new_status,
#         background_tasks=bg
#     )


# # ==============================
# # MASTER UPDATE HANDLER
# # ==============================

# async def handle_employee_update_notifications(
#     db: Session,
#     *,
#     old_status,
#     new_status,
#     old_comments,
#     new_comments,
#     employee_username,
#     changed_sections,
#     bg: BackgroundTasks
# ):

#     ##print("\n🚀 MASTER WORKFLOW STARTED")
#     ##print("Employee:", employee_username)
#     ##print("Old Status:", old_status)
#     ##print("New Status:", new_status)
#     ##print("Sections:", changed_sections)

#     hr_users = get_all_hr_usernames(db)

#     if not hr_users:
#         ##print("⚠️ No HR users found")
#         return

#     for section in changed_sections:

#         if new_status == STATUS_PENDING:

#             for hr in hr_users:
#                 await notify_hr_section_update(db, employee_username, hr, section, bg)

#         elif new_status in [STATUS_APPROVED, STATUS_CHANGES_REQUESTED]:

#             hr = hr_users[0]

#             await notify_employee_on_status_change(
#                 db,
#                 employee_username,
#                 hr,
#                 new_status,
#                 new_comments,
#                 section,
#                 bg
#             )


# # ==============================
# # FORM SUBMISSION HANDLER
# # ==============================

# async def handle_employee_form_submission(
#     db,
#     *,
#     employee_username,
#     form_name,
#     status,
#     bg
# ):

#     ##print("\n📄 FORM SUBMISSION WORKFLOW")
#     ##print("Employee:", employee_username)
#     ##print("Form:", form_name)
#     ##print("Status:", status)

#     hr_users = get_all_hr_usernames(db)

#     if not hr_users:
#         ##print("⚠️ No HR users found")
#         return

#     if status == STATUS_PENDING:

#         ##print("➡️ Sending submission notification to HR")

#         for hr in hr_users:
#             await notify_hr_section_update(
#                 db,
#                 employee_username,
#                 hr,
#                 form_name,
#                 bg
#             )

#     elif status in [STATUS_APPROVED, STATUS_CHANGES_REQUESTED]:

#         ##print("➡️ Sending HR decision notification to Employee")

#         hr = hr_users[0]

#         await notify_employee_on_status_change(
#             db,
#             employee_username,
#             hr,
#             status,
#             None,
#             form_name,
#             bg
#         )


# # ==============================
# # BANK NOTIFICATIONS
# # ==============================

# async def notify_hr_bank_update(db, employee_username, hr_username, bg):

#     ##print("\n🏦 BANK SUBMISSION WORKFLOW")

#     await notify_hr_section_update(
#         db,
#         employee_username,
#         hr_username,
#         "Bank Details",
#         bg
#     )


# async def notify_employee_bank_status_change(
#     db,
#     employee_username,
#     hr_username,
#     new_status,
#     comments,
#     bg
# ):

#     ##print("\n🏦 BANK STATUS CHANGE WORKFLOW")

#     await notify_employee_on_status_change(
#         db,
#         employee_username,
#         hr_username,
#         new_status,
#         comments,
#         "Bank Details",
#         bg
#     )


# async def handle_employee_bank_submission(
#     db,
#     *,
#     employee_username,
#     status,
#     comments,
#     bg
# ):

#     ##print("\n🏦 BANK WORKFLOW STARTED")
#     ##print("Employee:", employee_username)
#     ##print("Status:", status)

#     hr_users = get_all_hr_usernames(db)

#     if not hr_users:
#         ##print("⚠️ No HR users found")
#         return

#     if status == STATUS_PENDING:

#         for hr in hr_users:
#             await notify_hr_bank_update(db, employee_username, hr, bg)

#     elif status in [STATUS_APPROVED, STATUS_CHANGES_REQUESTED]:

#         hr = hr_users[0]

#         await notify_employee_bank_status_change(
#             db,
#             employee_username,
#             hr,
#             status,
#             comments,
#             bg
#         )



