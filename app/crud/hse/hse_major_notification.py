from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from typing import Optional
from sqlalchemy import text
from app.models.NotificationModel import Notification
from app.models.hse.hse_incident_investigation_master import HSEIncidentInvestigationMaster
from app.models.hse.incident_prevention import IncidentPrevention
from app.schemas.NotificationSchema import NotificationCreate
from app.models.UserModel import User
from app.models.RolePermissionModel import RolePermission

from app.core.Websocket import manager
from app.utils.EmailUtils import send_email


# =====================================================
# EMAIL CONTEXT BUILDER
# =====================================================

def build_incident_email_context(prevention):

    if isinstance(prevention, dict):
        get = prevention.get
    else:
        get = lambda k: getattr(prevention, k, None)

    context = f"""
Incident Details
-------------------------
Prevention ID : {get("ip_id")}
Incident ID   : {get("incident_id")}
Category      : {get("category")}
Status        : {get("status")}
Prepared By   : {get("major_prepared_by_name") or get("minor_prepared_by_name")}
Created At    : {get("created_at")}

Immediate Actions :
{get("major_immediate_actions_taken")}

Recommendations :
{get("major_recommendations")}
"""
    return context


# =====================================================
# CREATE NOTIFICATION RECORD
# =====================================================

def create_incident_notification(db: Session, notification: NotificationCreate):
    notif = Notification(
        type="HSEIncident",
        title=notification.title,
        description=notification.description,
        from_user=notification.from_user,
        to_user=notification.to_user,
        module_name="incident_prevention",
        module_status=notification.module_status,
        date=datetime.now(),
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


# =====================================================
# SEND NOTIFICATION (DB + WS + EMAIL)
# =====================================================

async def send_incident_notification(
    db: Session,
    *,
    title: str,
    description: str,
    from_user: str,
    to_user: str,
    module_status: Optional[str],
    background_tasks: BackgroundTasks,
    prevention=None
):

    data = NotificationCreate(
        type="HSEIncident",
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name="incident_prevention",
        module_status=module_status or ""
    )

    db_notif = create_incident_notification(db, data)

    # Websocket
    await manager.send_personal_message(to_user, {
        "id": db_notif.id,
        "title": db_notif.title,
        "description": db_notif.description,
        "module_status": db_notif.module_status,
        "date": str(db_notif.date)
    })

    # Email
    user = db.query(User).filter(User.username == to_user).first()

    if user and user.email:

        email_body = description

        if prevention:
            email_body += "\n\n" + build_incident_email_context(prevention)

        background_tasks.add_task(
            send_email,
            user.email,
            title,
            email_body,
            "HSE Incident System"
        )


# =====================================================
# IN PROGRESS NOTIFICATION
# =====================================================

async def notify_in_progress(
    db: Session,
    *,
    prevention,
    acted_by_username: str,
    background_tasks: BackgroundTasks
):

    users = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id.in_([3, 12]),
            RolePermission.submenu_id == 3
        )
        .all()
    )

    for rp in users:
        user = db.query(User).filter(User.user_id == rp.user_id).first()
        if not user:
            continue

        await send_incident_notification(
            db=db,
            title="Incident Prevention In Progress",
            description="An incident prevention report is now under investigation.",
            from_user=acted_by_username,
            to_user=user.username,
            module_status="In-Progress",
            background_tasks=background_tasks,
            prevention=prevention
        )


# =====================================================
# HSE REVIEWED NOTIFICATION
# =====================================================

async def notify_hse_reviewed(
    db: Session,
    *,
    prevention,
    acted_by_username: str,
    background_tasks: BackgroundTasks
):

    prevention_id = prevention.get("ip_id") if isinstance(prevention, dict) else prevention.ip_id

    prevention_obj = db.query(IncidentPrevention).filter(
        IncidentPrevention.ip_id == prevention_id
    ).first()

    users = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == 10,
            RolePermission.submenu_id == 3
        )
        .all()
    )

    for rp in users:
        user = db.query(User).filter(User.user_id == rp.user_id).first()
        if not user:
            continue

        await send_incident_notification(
            db=db,
            title="HSE Review Completed",
            description="Incident prevention report reviewed by HSE. Awaiting MD review.",
            from_user=acted_by_username,
            to_user=user.username,
            module_status="HSE Reviewed",
            background_tasks=background_tasks,
            prevention=prevention_obj
        )


# =====================================================
# MAIN HANDLER
# =====================================================

async def handle_incident_notification(
    db: Session,
    *,
    prevention,
    acted_by_username: str,
    background_tasks: BackgroundTasks
):

    if isinstance(prevention, dict):
        category = prevention.get("category")
        status = prevention.get("status")
    else:
        category = getattr(prevention, "category", None)
        status = getattr(prevention, "status", None)

    print("DEBUG CATEGORY:", category)
    print("DEBUG STATUS:", status)

    if category.lower() != "major":
        return

    if status == "In-Progress":
        await notify_in_progress(
            db=db,
            prevention=prevention,
            acted_by_username=acted_by_username,
            background_tasks=background_tasks
        )

    elif status == "HSE Reviewed":
        await notify_hse_reviewed(
            db=db,
            prevention=prevention,
            acted_by_username=acted_by_username,
            background_tasks=background_tasks
        )
    elif status == "Team-Ack":
        await notify_team_acknowledged(
            db=db,
            prevention=prevention,
            acted_by_username=acted_by_username,
            background_tasks=background_tasks
        )
    elif status == "Inv-Approved-MD":
        await notify_md_approved_investigation(
            db=db,
            prevention=prevention,
            background_tasks=background_tasks
        )
    elif status == "Inv-Changes-Requested-MD":

        await notify_md_changes_requested(
            db=db,
            prevention=prevention,
            background_tasks=background_tasks
        )

# =====================================================
# INVESTIGATION TEAM NOTIFICATION
# =====================================================

# async def notify_investigation_team_member(
#     db: Session,
#     *,
#     team_member,
#     background_tasks: BackgroundTasks
# ):

#     if isinstance(team_member, dict):
#         user_id = team_member.get("user_id")
#         is_leader = team_member.get("is_leader")
#         is_member = team_member.get("is_member")
#         prevention_id = team_member.get("prevention_id")
#     else:
#         user_id = team_member.user_id
#         is_leader = team_member.is_leader
#         is_member = team_member.is_member
#         prevention_id = team_member.prevention_id

#     user = db.query(User).filter(User.user_id == user_id).first()

#     if not user:
#         print("❌ User not found")
#         return

#     if is_leader:
#         title = "Investigation Team Leader Assigned"
#         description = "You have been assigned as Investigation Team Leader."
#     elif is_member:
#         title = "Added to Investigation Team"
#         description = "You have been selected as an investigation team member."
#     else:
#         return

#     prevention_obj = db.query(IncidentPrevention).filter(
#         IncidentPrevention.ip_id == prevention_id
#     ).first()

#     print("📢 Sending investigation team notification to:", user.username)

#     await send_incident_notification(
#         db=db,
#         title=title,
#         description=description,
#         from_user="system",
#         to_user=user.username,
#         module_status="Investigation Team",
#         background_tasks=background_tasks,
#         prevention=prevention_obj
#     )


async def notify_investigation_team_member(
    db: Session,
    *,
    team_member,
    background_tasks: BackgroundTasks
):

    # ===============================
    # SAFE FIELD EXTRACTION
    # ===============================
    if isinstance(team_member, dict):
        user_id = team_member.get("user_id")
        is_leader = team_member.get("is_leader")
        is_member = team_member.get("is_member")
        prevention_id = team_member.get("prevention_id")
    else:
        user_id = team_member.user_id
        is_leader = team_member.is_leader
        is_member = team_member.is_member
        prevention_id = team_member.prevention_id

    print("DEBUG USER ID:", user_id)
    print("DEBUG PREVENTION ID:", prevention_id)

    # ===============================
    # FETCH USER
    # ===============================
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        print("❌ User not found")
        return

    # ===============================
    # MESSAGE BASED ON ROLE
    # ===============================
    if is_leader:
        title = "Investigation Team Leader Assigned"
        description = "You have been assigned as Investigation Team Leader."
    elif is_member:
        title = "Added to Investigation Team"
        description = "You have been selected as an investigation team member."
    else:
        return

    # ===============================
    # FETCH PREVENTION RECORD
    # ===============================
    prevention_obj = None

    if prevention_id:
        prevention_obj = db.query(IncidentPrevention).filter(
            IncidentPrevention.ip_id == prevention_id
        ).first()

    if not prevention_obj:
        print("⚠️ Prevention record not found for ID:", prevention_id)

    # ===============================
    # SEND NOTIFICATION
    # ===============================
    print("📢 Sending investigation team notification to:", user.username)

    await send_incident_notification(
        db=db,
        title=title,
        description=description,
        from_user="system",
        to_user=user.username,
        module_status="Investigation Team",
        background_tasks=background_tasks,
        prevention=prevention_obj
    )




async def notify_investigation_report_filled(
    db: Session,
    *,
    hiim,
    background_tasks: BackgroundTasks
):

    print("🔥 Investigation report filled notification triggered")

    # =====================================================
    # 🔍 SAFELY EXTRACT incident_id
    # =====================================================
    incident_id = getattr(hiim, "incident_id", None)

    if not incident_id:
        print("❌ No incident_id found")
        return

    # =====================================================
    # 🔍 FETCH PREVENTION RECORD
    # =====================================================
    prevention = db.query(IncidentPrevention).filter(
        IncidentPrevention.incident_id == incident_id
    ).first()

    if not prevention:
        print("❌ Prevention record not found")
        return

    print("✅ Prevention ID:", prevention.ip_id)

    # =====================================================
    # 🔍 FETCH TEAM MEMBERS (DISTINCT)
    # =====================================================
    team_rows = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM incident_investigation_team
            WHERE prevention_id = :pid
            AND user_id IS NOT NULL
        """),
        {"pid": prevention.ip_id}
    ).fetchall()

    if not team_rows:
        print("❌ No team members found")
        return

    # =====================================================
    # 🔥 DEDUPE USERS
    # =====================================================
    unique_user_ids = {row[0] for row in team_rows}

    print("👥 Unique users:", unique_user_ids)

    # =====================================================
    # 🚀 SEND NOTIFICATIONS
    # =====================================================
    for user_id in unique_user_ids:

        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            continue

        print("📢 Sending notification to:", user.username)

        await send_incident_notification(
            db=db,
            title="Investigation Report Submitted",
            description="Please acknowledge this investigation report.",
            from_user="system",
            to_user=user.username,
            module_status="Investigation Report Filled",
            background_tasks=background_tasks,
            prevention=prevention
        )


async def notify_team_acknowledged(
    db: Session,
    *,
    prevention,
    acted_by_username: str,
    background_tasks: BackgroundTasks
):

    print("🔥 TEAM ACKNOWLEDGED TRIGGERED")

    # =====================================================
    # 🔍 FETCH MD USERS (role_id = 10, submenu = 3)
    # =====================================================
    users = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == 10,
            RolePermission.submenu_id == 3
        )
        .all()
    )

    if not users:
        print("❌ No MD users found")
        return

    for rp in users:

        user = db.query(User).filter(User.user_id == rp.user_id).first()

        if not user:
            continue

        print("📢 Sending Team Ack notification to:", user.username)

        await send_incident_notification(
            db=db,
            title="Investigation Report Acknowledged",
            description="Investigation report has been acknowledged by team members.",
            from_user=acted_by_username,
            to_user=user.username,
            module_status="Team-Ack",
            background_tasks=background_tasks,
            prevention=prevention
        )

from sqlalchemy import text
from app.models.hse.incident_prevention import IncidentPrevention





async def notify_md_approved_investigation(
    db: Session,
    *,
    prevention,
    background_tasks: BackgroundTasks
):

    print("🔥 MD APPROVED INVESTIGATION TRIGGERED")

    # =====================================================
    # 🔍 HANDLE DICT OR ORM
    # =====================================================
    if isinstance(prevention, dict):
        ip_id = prevention.get("ip_id")
    else:
        ip_id = prevention.ip_id

    if not ip_id:
        print("❌ No ip_id")
        return

    # =====================================================
    # 🔍 FETCH REAL PREVENTION OBJECT
    # =====================================================
    prevention_obj = db.query(IncidentPrevention).filter(
        IncidentPrevention.ip_id == ip_id
    ).first()

    if not prevention_obj:
        print("❌ Prevention record not found")
        return

    print("✅ Prevention ID:", prevention_obj.ip_id)

    # =====================================================
    # 🔍 FETCH HIIM USING incident_id
    # =====================================================
    hiim = db.query(HSEIncidentInvestigationMaster).filter(
        HSEIncidentInvestigationMaster.incident_id == prevention_obj.incident_id
    ).first()

    if not hiim:
        print("❌ HIIM record not found")
        return

    # =====================================================
    # 🔍 TEAM MEMBERS
    # =====================================================
    team_rows = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM incident_investigation_team
            WHERE prevention_id = :pid
            AND user_id IS NOT NULL
        """),
        {"pid": prevention_obj.ip_id}
    ).fetchall()

    team_user_ids = {row[0] for row in team_rows}

    # =====================================================
    # 🔍 HSE HEAD
    # =====================================================
    hse_users = db.query(RolePermission).filter(
        RolePermission.role_id == 12,
        RolePermission.submenu_id == 3
    ).all()

    hse_ids = {u.user_id for u in hse_users}

    # =====================================================
    # 🔍 HOP
    # =====================================================
    hop_users = db.query(RolePermission).filter(
        RolePermission.role_id == 3,
        RolePermission.submenu_id == 3
    ).all()

    hop_ids = {u.user_id for u in hop_users}

    # =====================================================
    # 🔍 STATION INCHARGE
    # =====================================================
    creator = db.query(User).filter(
        User.user_id == prevention_obj.created_by
    ).first()

    station_ids = set()

    if creator and creator.station_id:

        station_users = db.query(RolePermission).join(User).filter(
            RolePermission.role_id == 2,
            User.station_id == creator.station_id
        ).all()

        station_ids = {u.user_id for u in station_users}

    # =====================================================
    # 🔥 MERGE USERS
    # =====================================================
    all_user_ids = team_user_ids | hse_ids | hop_ids | station_ids

    print("👤 All recipients:", all_user_ids)

    # =====================================================
    # 🚀 SEND NOTIFICATIONS
    # =====================================================
    for user_id in all_user_ids:

        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            continue

        print("📢 Sending MD approval notification to:", user.username)

        await send_incident_notification(
            db=db,
            title="Investigation Report Approved by MD",
            description="Investigation report has been approved by MD.",
            from_user="system",
            to_user=user.username,
            module_status="Inv-Approved-MD",
            background_tasks=background_tasks,
            prevention=prevention_obj
        )


async def notify_md_changes_requested(
    db: Session,
    *,
    prevention,
    background_tasks: BackgroundTasks
):

    print("🔥 MD CHANGES REQUESTED TRIGGERED")

    # =====================================================
    # 🔍 HANDLE DICT OR ORM
    # =====================================================
    if isinstance(prevention, dict):
        ip_id = prevention.get("ip_id")
    else:
        ip_id = prevention.ip_id

    if not ip_id:
        print("❌ No ip_id")
        return

    # =====================================================
    # 🔍 FETCH REAL PREVENTION
    # =====================================================
    prevention_obj = db.query(IncidentPrevention).filter(
        IncidentPrevention.ip_id == ip_id
    ).first()

    if not prevention_obj:
        print("❌ Prevention not found")
        return

    # =====================================================
    # 🔍 FETCH HIIM
    # =====================================================
    hiim = db.query(HSEIncidentInvestigationMaster).filter(
        HSEIncidentInvestigationMaster.incident_id == prevention_obj.incident_id
    ).first()

    if not hiim:
        print("❌ HIIM not found")
        return

    if not hiim.created_by:
        print("❌ No created_by in HIIM")
        return

    # =====================================================
    # 🔍 FETCH USER WHO CREATED REPORT
    # =====================================================
    creator_value = hiim.created_by

    user = None

    # If numeric → treat as user_id
    if str(creator_value).isdigit():
        user = db.query(User).filter(
            User.user_id == int(creator_value)
        ).first()
    else:
        # fallback username match
        user = db.query(User).filter(
            User.username == creator_value
        ).first()

    if not user:
        print("❌ Creator user not found")
        return

    print("📢 Sending MD change request to:", user.username)

    # =====================================================
    # 📧 EMAIL BODY
    # =====================================================
    email_body = f"""
MD has requested changes in the investigation report.

Report Number : {hiim.report_number}
Incident Date : {hiim.incident_date}
Location      : {hiim.location_details}
Reported By   : {hiim.reported_by}

MD Remarks:
{hiim.remarks_md}

Please review and update the investigation report.
"""

    # =====================================================
    # 🚀 SEND NOTIFICATION
    # =====================================================
    await send_incident_notification(
        db=db,
        title="Changes Requested by MD",
        description="MD has requested changes in the investigation report.",
        from_user="system",
        to_user=user.username,
        module_status="Inv-Changes-Requested-MD",
        background_tasks=background_tasks,
        prevention=prevention_obj
    )


async def notify_engineer_allotted(
    db: Session,
    *,
    hiim,
    background_tasks: BackgroundTasks
):

    print("🛠 ENGINEER ALLOTTED TRIGGERED")

    if not hiim.allotted_to_name:
        print("❌ No allotted_to_name")
        return

    # allotted_to_name is user_id
    user = db.query(User).filter(
        User.user_id == hiim.allotted_to_name
    ).first()

    if not user:
        print("❌ Engineer user not found")
        return

    print("📢 Sending engineer allotment notification to:", user.username)

    # =====================================================
    # EMAIL BODY
    # =====================================================
    email_body = f"""
    You have been allotted an investigation by Station Incharge.

    Report Number : {hiim.report_number}
    Incident Date : {hiim.incident_date}
    Location      : {hiim.location_details}
    Reported By   : {hiim.reported_by}

    Please review and proceed with investigation.
    """

    await send_incident_notification(
        db=db,
        title="Investigation Assigned",
        description="You have been allotted an investigation by Station Incharge.",
        from_user="system",
        to_user=user.username,
        module_status="Inv-Engineer-Allotted",
        background_tasks=background_tasks,
        prevention=None  # optional
    )


async def notify_capa_form_filled(
    db: Session,
    *,
    capa,
    background_tasks: BackgroundTasks
):

    print("📋 CAPA FORM FILLED TRIGGERED")

    if not capa.hse_head_id:
        print("❌ No HSE Head assigned")
        return

    # Fetch HSE Head
    user = db.query(User).filter(
        User.user_id == capa.hse_head_id
    ).first()

    if not user:
        print("❌ HSE Head user not found")
        return

    print("📢 Sending CAPA notification to:", user.username)

    email_body = f"""
CAPA Form has been filled by allotted engineer.

Report No     : {capa.report_no}
Department    : {capa.department}
Problem       : {capa.problem_description}
Root Cause    : {capa.root_cause_analysis}
Corrective    : {capa.corrective_action}
Preventive    : {capa.preventive_action}
Status        : {capa.status}

Please review the CAPA report.
"""

    await send_incident_notification(
        db=db,
        title="CAPA Form Submitted",
        description="Allotted engineer has filled CAPA form.",
        from_user="system",
        to_user=user.username,
        module_status="CAPA-Form-Filled",
        background_tasks=background_tasks,
        prevention=None
    )


async def notify_capa_approved(
    db: Session,
    *,
    capa,
    background_tasks: BackgroundTasks
):

    print("✅ CAPA APPROVED TRIGGERED")

    if not capa.created_by:
        print("❌ No creator found")
        return

    # created_by assumed username
    user = db.query(User).filter(
        User.user_id == capa.created_by
    ).first()

    if not user:
        print("❌ Creator user not found")
        return

    print("📢 Sending CAPA approved notification to:", user.username)

    email_body = f"""
Your CAPA report has been approved by HSE Head.

Report No     : {capa.report_no}
Department    : {capa.department}
Problem       : {capa.problem_description}
Root Cause    : {capa.root_cause_analysis}
Corrective    : {capa.corrective_action}
Preventive    : {capa.preventive_action}
Status        : {capa.status}

You may proceed with further actions.
"""

    await send_incident_notification(
        db=db,
        title="CAPA Approved",
        description="HSE Head has approved your CAPA report.",
        from_user="system",
        to_user=user.username,
        module_status="CAPA-Approved",
        background_tasks=background_tasks,
        prevention=None
    )


async def notify_capa_changes_requested(
    db: Session,
    *,
    capa,
    background_tasks: BackgroundTasks
):

    print("📋 CAPA CHANGES REQUESTED TRIGGERED")

    if not capa.created_by:
        print("❌ No creator found")
        return

    user = db.query(User).filter(
        User.user_id == capa.created_by
    ).first()

    if not user:
        print("❌ Creator user not found")
        return

    print("📢 Sending CAPA changes requested notification to:", user.username)

    email_body = f"""
HSE Head has requested changes in your CAPA report.

Remarks :
{capa.remarks}

Report No     : {capa.report_no}
Department    : {capa.department}
Problem       : {capa.problem_description}
Root Cause    : {capa.root_cause_analysis}
Corrective    : {capa.corrective_action}
Preventive    : {capa.preventive_action}
Status        : {capa.status}

Please review and update the CAPA accordingly.
"""

    await send_incident_notification(
        db=db,
        title="CAPA Changes Requested",
        description="HSE Head has requested changes in your CAPA report.",
        from_user="system",
        to_user=user.username,
        module_status="CAPA-Changes-Requested",
        background_tasks=background_tasks,
        prevention=None
    )




async def notify_capa_closed(
    db: Session,
    *,
    capa,
    background_tasks: BackgroundTasks
):

    print("🔒 CAPA CLOSED FULL FLOW TRIGGERED")

    user_ids = set()

    # =====================================================
    # 🔍 FETCH PREVENTION USING INCIDENT ID
    # =====================================================
    prevention = db.query(IncidentPrevention).filter(
        IncidentPrevention.incident_id == capa.incident_id
    ).first()

    if prevention:
        print("✅ Prevention ID:", prevention.ip_id)

        # creator
        if prevention.created_by:
            user_ids.add(prevention.created_by)

        # =================================================
        # TEAM MEMBERS
        # =================================================
        team_rows = db.execute(
            text("""
                SELECT DISTINCT user_id
                FROM incident_investigation_team
                WHERE prevention_id = :pid
                AND user_id IS NOT NULL
            """),
            {"pid": prevention.ip_id}
        ).fetchall()

        team_ids = {row[0] for row in team_rows}
        user_ids |= team_ids

        # =================================================
        # STATION INCHARGE
        # =================================================
        creator = db.query(User).filter(
            User.user_id == prevention.created_by
        ).first()

        if creator and creator.station_id:

            station_users = db.query(RolePermission).join(User).filter(
                RolePermission.role_id == 2,
                User.station_id == creator.station_id
            ).all()

            user_ids |= {u.user_id for u in station_users}

    # =====================================================
    # 🔍 ROLE BASED USERS
    # =====================================================
    role_map = [10, 12, 3]  # MD, HSE Head, HOP

    role_users = db.query(RolePermission).filter(
        RolePermission.role_id.in_(role_map),
        RolePermission.submenu_id == 3
    ).all()

    user_ids |= {u.user_id for u in role_users}

    # =====================================================
    # 🔍 CAPA USERS
    # =====================================================
    if capa.created_by:
        user_ids.add(int(capa.created_by))

    if capa.hse_head_id:
        user_ids.add(capa.hse_head_id)

    if not user_ids:
        print("❌ No recipients found")
        return

    print("👥 FINAL RECIPIENTS:", user_ids)

    # =====================================================
    # EMAIL BODY
    # =====================================================
    email_body = f"""
CAPA has been CLOSED.

Report No     : {capa.report_no}
Department    : {capa.department}
Problem       : {capa.problem_description}
Root Cause    : {capa.root_cause_analysis}
Corrective    : {capa.corrective_action}
Preventive    : {capa.preventive_action}
Status        : {capa.status}

The incident lifecycle is now fully completed.
"""

    # =====================================================
    # SEND TO ALL USERS
    # =====================================================
    for uid in user_ids:

        user = db.query(User).filter(User.user_id == uid).first()

        if not user:
            continue

        print("📢 Sending CAPA closed notification to:", user.username)

        await send_incident_notification(
            db=db,
            title="Incident Lifecycle Completed",
            description="CAPA has been closed. Incident lifecycle completed.",
            from_user="system",
            to_user=user.username,
            module_status="Closed",
            background_tasks=background_tasks,
            prevention=prevention
        )