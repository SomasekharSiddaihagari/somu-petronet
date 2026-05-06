from datetime import datetime
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.core.Websocket import manager
from app.utils.EmailUtils import send_email
from app.models.UserModel import User
from app.models.NotificationModel import Notification
from app.models.RolePermissionModel import RolePermission

# ============================================================
# ROLE FLOW CONFIG  (🔥 DO NOT CHANGE – OLD LOGIC)
# ============================================================

PREVIOUS_ROLE_MAP = {
    "HR": "Supervisor",
    "Finance": "HR",
}

UPSTREAM_ROLE_MAP = {
    "HR": ["Supervisor"],
    "Finance": ["Supervisor", "HR"],
}

ROLE_MAP = {
    "HR": 7,
    "Finance": 11,
}

# ============================================================
# MODULE CONFIG
# ============================================================

CLAIM_MODULES = {
    "asset": {
        "type": "Asset Claim",
        "module_name": "asset_claim",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Asset Claim Pending Approval",
            "approved": "Asset Claim Approved",
            "rejected": "Asset Claim Rejected",
            "disbursed": "Asset Claim Successfully Disbursed",
        },
    },
    "allowance": {
        "type": "Allowance Claim",
        "module_name": "allowance",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Allowance Claim Pending Approval",
            "approved": "Allowance Claim Approved",
            "rejected": "Allowance Claim Rejected",
        },
    },
    "encashment": {
        "type": "Leave Encashment",
        "module_name": "encashment",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Encashment Pending Approval",
            "approved": "Encashment Approved",
            "rejected": "Encashment Rejected",
        },
    },
    "mobile_reimbursement": {
        "type": "Mobile Bill Reimbursement",
        "module_name": "mobile_bill_reimbursement",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Mobile Bill Reimbursement Pending Approval",
            "approved": "Mobile Bill Reimbursement Approved",
            "rejected": "Mobile Bill Reimbursement Rejected",
        },
    },
    "data_card": {
        "type": "Data Card Reimbursement",
        "module_name": "data_card_reimbursement",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Data Card Reimbursement Pending Approval",
            "approved": "Data Card Reimbursement Approved",
            "rejected": "Data Card Reimbursement Rejected",
        },
    },
    "laptop": {
        "type": "Laptop Maintenance Reimbursement",
        "module_name": "laptop_maintenance_reimbursement",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Laptop Maintenance Pending Approval",
            "approved": "Laptop Maintenance Approved",
            "rejected": "Laptop Maintenance Rejected",
        },
    },
    "furniture": {
        "type": "Furniture R&M Reimbursement",
        "module_name": "furniture_rm_reimbursement",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Furniture R&M Pending Approval",
            "approved": "Furniture R&M Approved",
            "rejected": "Furniture R&M Rejected",
        },
    },
    "vehicle": {
        "type": "Vehicle C&M Reimbursement",
        "module_name": "vehicle_cm_reimbursement",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Vehicle C&M Pending Approval",
            "approved": "Vehicle C&M Approved",
            "rejected": "Vehicle C&M Rejected",
        },
    },
    "out_of_pocket": {
        "type": "Out of Pocket Claim",
        "module_name": "out_of_pocket_claim",
        "parent_module": "Claim Management",
        "submenu_id": 12,
        "titles": {
            "pending": "Out of Pocket Pending Approval",
            "approved": "Out of Pocket Approved",
            "rejected": "Out of Pocket Rejected",
        },
    },
}

# ============================================================
# HELPERS
# ============================================================

def get_full_name(user: User) -> str:
    return (
        f"{(user.first_name or '').strip()} {(user.last_name or '').strip()}".strip()
        or user.username
    )


def normalize_status(status: Optional[str]) -> Optional[str]:
    return status.strip() if status else None



def parse_claim_status(status: Optional[str]):
    """
    Parse claim status and return (action, role)
    Fixed to handle typos and variations in status strings
    """
    if not status:
        return None, None

    # Normalize status for comparison (handle typos)
    status_lower = status.lower()

    # ===================== PENDING STATUSES =====================
    if "pending supervisor" in status_lower:
        return "pending", "Supervisor"

    if "pending hr" in status_lower:
        return "pending", "HR"
    
    if "pending hop" in status_lower:
        return "pending", "HOP"

    if "pending finance" in status_lower:
        return "pending", "Finance"

    # ===================== APPROVED STATUSES =====================
    if status_lower.endswith("approved") or "approved" in status_lower:
        return "final_approve", "Finance"

    # ===================== REJECTION STATUSES =====================
    if "supervisor rejected" in status_lower or "supervisor rejection" in status_lower:
        return "reject", "Supervisor"
    
    if "hop rejected" in status_lower or "hop rejection" in status_lower:
        return "reject", "HOP"

    if "hr rejected" in status_lower or "hr rejection" in status_lower:
        return "reject", "HR"

    if "finance rejected" in status_lower or "finance rejection" in status_lower:
        return "reject", "Finance"

    # ===================== DISBURSED =====================
    if "disbursed" in status_lower:
        return "final_approve", "Finance"

    return None, None


def get_role_users(db: Session, *, role_name: str, submenu_id: int) -> List[User]:
    role_id = ROLE_MAP.get(role_name)
    if not role_id:
        return []

    return (
        db.query(User)
        .join(RolePermission, RolePermission.user_id == User.user_id)
        .filter(
            RolePermission.role_id == role_id,
            RolePermission.submenu_id == submenu_id,
        )
        .all()
    )


def add_upstream_users(db, employee, users, role, submenu_id):
    """
    🔥 RESTORES OLD WORKING BEHAVIOR
    HR → Supervisor
    Finance → HR + Supervisor
    """
    for r in UPSTREAM_ROLE_MAP.get(role, []):
        if r == "Supervisor" and employee.supervisor_id:
            sup = db.query(User).filter(
                User.user_id == employee.supervisor_id
            ).first()
            if sup:
                users.append(sup)

        elif r == "HR":
            users.extend(
                get_role_users(
                    db,
                    role_name="HR",
                    submenu_id=submenu_id
                )
            )

# ============================================================
# EMAIL BUILDERS (SAFE)
# ============================================================

def _role_comment(sheet, role):
    if role == "Supervisor" and getattr(sheet, "supervisor_comment", None):
        return (
            f"Supervisor : {getattr(sheet,'updated_by_supervisor_name','N/A')}\n"
            f"Date       : {getattr(sheet,'updated_by_supervisor','N/A')}\n"
            f"Comment:\n{sheet.supervisor_comment}\n"
        )

    if role == "HR" and getattr(sheet, "hr_comment", None):
        return (
            f"HR : {getattr(sheet,'updated_by_hr_name','N/A')}\n"
            f"Date : {getattr(sheet,'updated_by_hr','N/A')}\n"
            f"Comment:\n{sheet.hr_comment}\n"
        )

    if role == "Finance" and getattr(sheet, "finance_comment", None):
        return (
            f"Finance : {getattr(sheet,'updated_by_finance_name','N/A')}\n"
            f"Date    : {getattr(sheet,'updated_by_finance','N/A')}\n"
            f"Comment:\n{sheet.finance_comment}\n"
        )

    if role == "HOP" and getattr(sheet, "hop_comment", None):
        return (
            f"HOP : {getattr(sheet,'updated_by_hop_name','N/A')}\n"
            f"Date    : {getattr(sheet,'updated_by_hop','N/A')}\n"
            f"Comment:\n{sheet.hop_comment}\n"
        )
    return ""


def build_action_email_body(sheet, req_no, module_type, role):
    body = (
        f"{module_type} {req_no} status update.\n\n"
        f"Claim Amount : ₹{getattr(sheet,'claim_amount','N/A')}\n\n"
    )
    body += _role_comment(sheet, role)
    return body


def build_encashment_email_body(sheet, req_no, role):
    body = (
        f"Leave Encashment {req_no} status update.\n\n"
        f"Employee Name : {getattr(sheet,'employee_name','N/A')}\n"
        f"Leave Type    : {getattr(sheet,'leave_type','N/A')}\n"
        f"Encash EL     : {getattr(sheet,'encash_el','N/A')}\n\n"
    )
    body += _role_comment(sheet, role)
    return body


def build_allowance_email_body(sheet, req_no, role):
    body = (
        f"Allowance Claim {req_no} status update.\n\n"
        f"Employee Name : {getattr(sheet,'employee_name','N/A')}\n"
        f"Station       : {getattr(sheet,'station','N/A')}\n"
        f"Grand Total   : ₹{getattr(sheet,'grand_total','N/A')}\n\n"
    )
    body += _role_comment(sheet, role)
    return body


def build_mobile_reimbursement_email_body(sheet, req_no, role):
    body = (
        f"Mobile Bill Reimbursement {req_no} status update.\n\n"
        f"Bill Month : {getattr(sheet,'bill_month_year','N/A')}\n"
        f"Total Amount : ₹{getattr(sheet,'total_claimed_amount','N/A')}\n\n"
    )
    body += _role_comment(sheet, role)
    return body


def build_data_card_email_body(sheet, req_no, role):
    body = (
        f"Data Card Reimbursement {req_no} status update.\n\n"
        f"Data Card No : {getattr(sheet,'data_card_number','N/A')}\n"
        f"Amount       : ₹{getattr(sheet,'bill_amount_total','N/A')}\n\n"
    )
    body += _role_comment(sheet, role)
    return body


def build_laptop_email_body(sheet, req_no, role):
    body = (
        f"Laptop Maintenance Reimbursement {req_no} status update.\n\n"
        f"Amount Claimed : ₹{getattr(sheet,'amount_claimed','N/A')}\n"
        f"Annual Limit  : ₹{getattr(sheet,'annual_limit','N/A')}\n"
        f"Eligible Amt  : ₹{getattr(sheet,'eligible_amount','N/A')}\n\n"
    )

    # ✅ EMPLOYEE REMARKS
    if getattr(sheet, "remarks", None):
        body += (
            "Employee Remarks:\n"
            f"{sheet.remarks}\n\n"
        )

    # ✅ ROLE COMMENTS (Supervisor / HR / Finance)
    body += _role_comment(sheet, role)

    return body



def build_furniture_email_body(sheet, req_no, role):
    body = (
        f"Furniture R&M Reimbursement {req_no} status update.\n\n"
        f"Furniture : {getattr(sheet,'furniture_name','N/A')}\n"
        f"Amount    : ₹{getattr(sheet,'amount_claimed','N/A')}\n\n"
    )
    body += _role_comment(sheet, role)
    return body


def build_vehicle_email_body(sheet, req_no, role):
    body = (
        f"Vehicle C&M Reimbursement {req_no} status update.\n\n"
        f"Vehicle : {getattr(sheet,'vehicle_name','N/A')}\n"
        f"Amount  : ₹{getattr(sheet,'maintenance_claim_amount','N/A')}\n\n"
    )
    body += _role_comment(sheet, role)
    return body


def build_out_of_pocket_email_body(sheet, req_no, role):
    body = (
        f"Out of Pocket Claim {req_no} status update.\n\n"
        f"Total Claims : {getattr(sheet,'total_claims','N/A')}\n"
        f"Amount       : ₹{getattr(sheet,'total_amount','N/A')}\n\n"
    )
    body += _role_comment(sheet, role)
    return body


def build_email_body(module_key, sheet, req_no, role, cfg):
    return {
        "encashment": build_encashment_email_body,
        "allowance": build_allowance_email_body,
        "mobile_reimbursement": build_mobile_reimbursement_email_body,
        "data_card": build_data_card_email_body,
        "laptop": build_laptop_email_body,
        "furniture": build_furniture_email_body,
        "vehicle": build_vehicle_email_body,
        "out_of_pocket": build_out_of_pocket_email_body,
    }.get(
        module_key,
        lambda s, r, ro: build_action_email_body(s, r, cfg["type"], ro)
    )(sheet, req_no, role)

# ============================================================
# NOTIFICATION CORE
# ============================================================

def create_notification(db, *, cfg, title, description, from_user, to_user, status):
    notif = Notification(
        type=cfg["type"],
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        module_name=cfg["module_name"],
        module_status=status,
        date=datetime.now(),
        is_read=False,
    )
    db.add(notif)
    db.commit()
    return notif


async def send_notification(
    db, *, cfg, title, description, email_body,
    from_user, to_user, status, background_tasks
):
    create_notification(
        db=db,
        cfg=cfg,
        title=title,
        description=description,
        from_user=from_user,
        to_user=to_user,
        status=status,
    )

    await manager.send_personal_message(to_user, {
        "title": title,
        "description": description,
        "status": status,
    })

    user = db.query(User).filter(User.username == to_user).first()
    if user and user.email:
        background_tasks.add_task(
            send_email,
            user.email,
            title,
            f"Dear {get_full_name(user)},\n\n{email_body}\n\nRegards,\nPetronet Claim System",
            cfg["parent_module"],
        )

# ============================================================
# MASTER HANDLER (🔥 FIXED & SAFE)
# ============================================================

async def handle_claim_notification(db, *, module_key, sheet, background_tasks):
    print("\n" + "="*60)
    print("🔔 NOTIFICATION HANDLER STARTED")
    print("="*60)
    print(f"MODULE: {module_key}")
    print(f"STATUS: {getattr(sheet, 'status', None)}")
    print(f"USER_ID: {getattr(sheet, 'user_id', None)}")
    print(f"REQ_NO: {getattr(sheet, 'requisition_number', None)}")
    
    if module_key not in CLAIM_MODULES:
        print(f"❌ ERROR: Module '{module_key}' not in CLAIM_MODULES")
        print(f"Available modules: {list(CLAIM_MODULES.keys())}")
        return

    cfg = CLAIM_MODULES[module_key]
    print(f"✅ Config loaded for module: {module_key}")

    status = normalize_status(getattr(sheet, "status", None))
    user_id = getattr(sheet, "user_id", None)
    req_no = getattr(sheet, "requisition_number", None)

    print(f"After normalization - STATUS: '{status}'")

    if not status:
        print("❌ ERROR: Status is None or empty")
        return
    
    if not user_id:
        print("❌ ERROR: user_id is None")
        return
        
    if not req_no:
        print("❌ ERROR: requisition_number is None")
        return

    action, role = parse_claim_status(status)
    print(f"Parsed status - ACTION: {action}, ROLE: {role}")
    
    if not action:
        print(f"❌ ERROR: Could not parse action from status: '{status}'")
        return

    print(f"✅ Successfully parsed - action: {action}, role: {role}")

    employee = db.query(User).filter(User.user_id == user_id).first()
    if not employee:
        print(f"❌ ERROR: Employee not found for user_id: {user_id}")
        return

    print(f"✅ Employee found: {employee.username}")
    print(f"   - Email: {employee.email}")
    print(f"   - Supervisor ID: {employee.supervisor_id}")

    users = [employee]

    # ===================== PENDING =====================
    if action == "pending":
        print(f"\n📋 Processing PENDING action for role: {role}")
        
        if role == "Supervisor":
            if employee.supervisor_id:
                supervisor = db.query(User).filter(
                    User.user_id == employee.supervisor_id
                ).first()
                
                if supervisor:
                    users.append(supervisor)
                    print(f"✅ Added Supervisor: {supervisor.username} (ID: {supervisor.user_id})")
                    print(f"   - Email: {supervisor.email}")
                else:
                    print(f"❌ ERROR: Supervisor not found for ID: {employee.supervisor_id}")
            else:
                print(f"⚠️ WARNING: Employee has no supervisor_id")
        else:
            # For HR or Finance roles
            role_users = get_role_users(db, role_name=role, submenu_id=cfg["submenu_id"])
            print(f"Found {len(role_users)} {role} users")
            for ru in role_users:
                print(f"   - {ru.username} ({ru.email})")
            users.extend(role_users)

        title = cfg["titles"]["pending"]
        desc = f"{cfg['type']} {req_no} pending {role} approval."
        prev_role = PREVIOUS_ROLE_MAP.get(role)

    # ===================== REJECT =====================
    elif action == "reject":
        print(f"\n❌ Processing REJECT action for role: {role}")
        
        title = cfg["titles"]["rejected"]
        desc = f"{cfg['type']} {req_no} rejected by {role}."
        prev_role = role

        add_upstream_users(db, employee, users, role, cfg["submenu_id"])
        print(f"✅ Added upstream users for rejection")

    # ===================== FINAL APPROVE =====================
    else:
        print(f"\n✅ Processing APPROVE/DISBURSED action")
        
        if "Disbursed" in status or "disbursed" in status.lower():
            title = cfg["titles"].get("disbursed", cfg["titles"]["approved"])
            desc = f"{cfg['type']} {req_no} successfully disbursed."
            print("   Type: DISBURSED")
        else:
            title = cfg["titles"]["approved"]
            desc = f"{cfg['type']} {req_no} approved."
            print("   Type: APPROVED")

        prev_role = role

        add_upstream_users(db, employee, users, "Finance", cfg["submenu_id"])
        print(f"✅ Added upstream users for approval")

    email_body = build_email_body(module_key, sheet, req_no, prev_role, cfg)

    print(f"\n📧 SENDING NOTIFICATIONS")
    print(f"Title: {title}")
    print(f"Description: {desc}")
    print(f"Total users to notify: {len(users)}")

    sent = set()
    notification_count = 0
    
    for u in users:
        if not u:
            print(f"⏭️  Skipping None user")
            continue
            
        if u.username in sent:
            print(f"⏭️  Skipping duplicate: {u.username}")
            continue
            
        sent.add(u.username)

        print(f"\n📤 Sending notification #{notification_count + 1}")
        print(f"   To: {u.username}")
        print(f"   Email: {u.email}")
        
        try:
            await send_notification(
                db=db,
                cfg=cfg,
                title=title,
                description=desc,
                email_body=email_body,
                from_user="system",
                to_user=u.username,
                status=status,
                background_tasks=background_tasks,
            )
            notification_count += 1
            print(f"   ✅ SUCCESS")
            
        except Exception as e:
            print(f"   ❌ FAILED: {str(e)}")

    print(f"\n" + "="*60)
    print(f"✅ NOTIFICATION HANDLER COMPLETED")
    print(f"   Total notifications sent: {notification_count}")
    print("="*60 + "\n")