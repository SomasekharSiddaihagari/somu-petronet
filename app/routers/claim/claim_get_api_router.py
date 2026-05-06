from datetime import date, datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import bindparam, text
from sqlalchemy.orm import Session
from app.crud.claim.get_all_asset_claim_details_crud import get_asset_entitlement
from app.crud.claim.get_apis import get_approved_asset_claims_by_user_id_sql, get_asset_claims_by_user_id_sql
from app.database import get_db
from app.routers.UserAuthR2 import make_download_url
from sqlalchemy.sql import text as sql_text
router = APIRouter(prefix="/get", tags=["Claims Get API's"])
from sqlalchemy import text


def attach_submissions_to_claims(db, claims):

    if not claims:
        return []

    claims_dict = [dict(c) for c in claims]
    claim_ids = [c["asset_claim_id"] for c in claims_dict]

    submissions = db.execute(
        text("""
            SELECT *
            FROM asset_claim_submission
            WHERE asset_claim_id = ANY(:claim_ids)
        """),
        {"claim_ids": claim_ids}
    ).mappings().all()

    submissions_map = {}

    for s in submissions:
        sub = dict(s)

        # ✅ MAKE DOCUMENTS DOWNLOADABLE
        if sub.get("document_names"):
            sub["document_names"] = [
                make_download_url(p.strip())
                for p in sub["document_names"].split(",")
                if p.strip()
            ]
        else:
            sub["document_names"] = []

        submissions_map.setdefault(
            sub["asset_claim_id"], []
        ).append(sub)

    for claim in claims_dict:
        claim["submissions"] = submissions_map.get(
            claim["asset_claim_id"], []
        )

    return claims_dict

def serialize_common(row):

    def fix_file(path):
        if not path:
            return None
        return make_download_url(path)

    def fix_multiple(path_list):
        if not path_list:
            return None
        return [fix_file(p.strip()) for p in path_list.split(",") if p.strip()]

    return {
        **row,


        # ✅ DOWNLOADABLE LINKS
        "document_names": fix_multiple(row.get("document_names")),
    }


@router.get("/asset-claims/user_id")
def get_asset_claims(


    user_id: str = Query(...),
    db: Session = Depends(get_db)
    ):
    claims = get_asset_claims_by_user_id_sql(db, user_id)

    if not claims:
        raise HTTPException(
            status_code=404,
            detail="No asset claims found for this user"
        )

    claims = attach_submissions_to_claims(db, claims)

    return {
        "success": True,
        "user_id": user_id,
        "data": claims
    }


@router.get("/approved-asset-claims/user_id")
def get_asset_claims(


    user_id: str = Query(...),
    db: Session = Depends(get_db)
    ):
    claims = get_approved_asset_claims_by_user_id_sql(db, user_id)

    if not claims:
        raise HTTPException(
            status_code=200,
            detail="No asset claims found for this user"
        )

    return {
        "success": True,
        "user_id": user_id,
        "data": claims
    }


# @router.get("/asset-claims/all")
# def get_asset_claims(

#     user_id: str = Query(...),

#     db: Session = Depends(get_db)

# ):

#     PENDING_STATUSES = {

#         "Pending Supervisor Approval",

#         "Pending HR Approval",

#         "Pending Finance Approval",

#     }
 
#     # Step 1: fetch requester

#     requester = db.execute(

#         text("""

#             SELECT user_id

#             FROM users

#             WHERE user_id = :user_id

#         """),

#         {"user_id": user_id}

#     ).fetchone()
 
#     if not requester:

#         raise HTTPException(status_code=404, detail="User not found")
 
#     requester_id = requester.user_id
 
#     # Step 2: detect ALL roles

#     is_supervisor = db.execute(

#         text("""

#             SELECT 1 FROM users

#             WHERE supervisor_id = :user_id

#               AND user_id != :user_id

#             LIMIT 1

#         """),

#         {"user_id": requester_id}

#     ).fetchone()
 
#     is_hr = db.execute(

#         text("""

#             SELECT 1 FROM role_permissions

#             WHERE user_id = :user_id

#               AND submenu_id = 12

#               AND role_id = 7

#             LIMIT 1

#         """),

#         {"user_id": requester_id}

#     ).fetchone()
 
#     is_finance = db.execute(

#         text("""

#             SELECT 1 FROM role_permissions

#             WHERE user_id = :user_id

#               AND submenu_id = 12

#               AND role_id = 11

#             LIMIT 1

#         """),

#         {"user_id": requester_id}

#     ).fetchone()
 
#     is_md = db.execute(

#         text("""

#             SELECT 1 FROM role_permissions

#             WHERE user_id = :user_id

#               AND submenu_id = 12

#               AND role_id = 10

#             LIMIT 1

#         """),

#         {"user_id": requester_id}

#     ).fetchone()
 
#     # Step 3: fetch claims based on role

#     # ⚠️ Supervisor ALWAYS takes highest priority

#     # even if user is also MD/HR/Finance

#     if is_supervisor:

#         claim_ids = set()
 
#         # Always add subordinates' Pending Supervisor Approval

#         rows = db.execute(

#             text("""

#                 SELECT DISTINCT ac.asset_claim_id

#                 FROM asset_claim ac

#                 JOIN users u ON u.user_id = ac.created_by

#                 WHERE u.supervisor_id = :user_id

#                   AND u.user_id != :user_id

#                   AND ac.asset_claim_id IN (

#                     SELECT DISTINCT asset_claim_id

#                     FROM asset_claim_submission

#                     WHERE status = 'Pending Supervisor Approval'

#                   )

#             """),

#             {"user_id": requester_id}

#         ).scalars().all()

#         claim_ids.update(rows)
 
#         # If also HR — add Pending HR Approval

#         if is_hr:

#             rows = db.execute(

#                 text("""

#                     SELECT DISTINCT asset_claim_id

#                     FROM asset_claim_submission

#                     WHERE status = 'Pending HR Approval'

#                 """)

#             ).scalars().all()

#             claim_ids.update(rows)
 
#         # If also Finance — add Pending Finance Approval

#         if is_finance:

#             rows = db.execute(

#                 text("""

#                     SELECT DISTINCT asset_claim_id

#                     FROM asset_claim_submission

#                     WHERE status IN ('Pending Finance Approval', 'Asset Claim Approved')
 
#                     UNION
 
#                     SELECT DISTINCT acs.asset_claim_id

#                     FROM asset_claim_submission acs

#                     JOIN asset_claim ac ON ac.asset_claim_id = acs.asset_claim_id

#                     WHERE ac.bought_back = TRUE

#                       AND acs.status = 'Asset Claim Disbursed'

#                 """)

#             ).scalars().all()

#             claim_ids.update(rows)
 
#         # NOTE: MD role is ignored here intentionally

#         # MD full history is available in /asset-claims/history API
 
#         if claim_ids:

#             claims = db.execute(

#                 text("""

#                     SELECT *

#                     FROM asset_claim

#                     WHERE asset_claim_id IN :ids

#                     ORDER BY COALESCE(updated_at, created_at) DESC

#                 """),

#                 {"ids": tuple(claim_ids)}

#             ).mappings().all()

#         else:

#             claims = []
 
#     elif is_md:

#         # Pure MD (not a supervisor) → sees all claims

#         claims = db.execute(

#             text("""

#                 SELECT *

#                 FROM asset_claim

#                 ORDER BY COALESCE(updated_at, created_at) DESC

#             """)

#         ).mappings().all()
 
#     else:

#         # HR / Finance / Employee

#         claim_ids = set()
 
#         if is_hr:

#             rows = db.execute(

#                 text("""

#                     SELECT DISTINCT asset_claim_id

#                     FROM asset_claim_submission

#                     WHERE status = 'Pending HR Approval'

#                 """)

#             ).scalars().all()

#             claim_ids.update(rows)
 
#         if is_finance:

#             rows = db.execute(

#                 text("""

#                     SELECT DISTINCT asset_claim_id

#                     FROM asset_claim_submission

#                     WHERE status IN ('Pending Finance Approval', 'Asset Claim Approved')
 
#                     UNION
 
#                     SELECT DISTINCT acs.asset_claim_id

#                     FROM asset_claim_submission acs

#                     JOIN asset_claim ac ON ac.asset_claim_id = acs.asset_claim_id

#                     WHERE ac.bought_back = TRUE

#                       AND acs.status = 'Asset Claim Disbursed'

#                 """)

#             ).scalars().all()

#             claim_ids.update(rows)
 
#         if claim_ids:

#             claims = db.execute(

#                 text("""

#                     SELECT *

#                     FROM asset_claim

#                     WHERE asset_claim_id IN :ids

#                     ORDER BY COALESCE(updated_at, created_at) DESC

#                 """),

#                 {"ids": tuple(claim_ids)}

#             ).mappings().all()
 
#         elif is_hr or is_finance:

#             # ✅ FIX: HR or Finance with no pending items in queue

#             # should get empty list — NOT fall through to their own personal claims

#             claims = []
 
#         else:

#             # Pure employee → only their own claims

#             claims = db.execute(

#                 text("""

#                     SELECT *

#                     FROM asset_claim

#                     WHERE created_by = :user_id

#                     ORDER BY COALESCE(updated_at, created_at) DESC

#                 """),

#                 {"user_id": requester_id}

#             ).mappings().all()
 
#     # Step 4: attach submissions

#     claims = attach_submissions_to_claims(db, claims)
 
#     # Step 5: role-based arrays from role_permissions

#     hr_ids = db.execute(

#         text("""

#             SELECT DISTINCT user_id

#             FROM role_permissions

#             WHERE submenu_id = 12

#               AND role_id = 7

#         """)

#     ).scalars().all()
 
#     finance_ids = db.execute(

#         text("""

#             SELECT DISTINCT user_id

#             FROM role_permissions

#             WHERE submenu_id = 12

#               AND role_id = 11

#         """)

#     ).scalars().all()
 
#     md_ids = db.execute(

#         text("""

#             SELECT DISTINCT user_id

#             FROM role_permissions

#             WHERE submenu_id = 12

#               AND role_id = 10

#         """)

#     ).scalars().all()
 
#     # Step 6: build data list

#     data = []

#     for claim in claims:

#         record = dict(claim)
 
#         supervisor_row = db.execute(

#             text("""

#                 SELECT supervisor_id

#                 FROM users

#                 WHERE user_id = :emp_id

#             """),

#             {"emp_id": claim["created_by"]}

#         ).fetchone()
 
#         record["supervisor_ids"] = (

#             [supervisor_row.supervisor_id]

#             if supervisor_row and supervisor_row.supervisor_id

#             else []

#         )

#         record["hr_ids"] = list(hr_ids)

#         record["finance_ids"] = list(finance_ids)

#         record["md_ids"] = list(md_ids)
 
#         data.append(record)
 
#     # Step 7: sort — pending first, then by latest submission created_at DESC

#     def latest_submission_date(record):

#         submission_dates = [

#             s["created_at"]

#             for s in record.get("submissions", [])

#             if s.get("created_at")

#         ]

#         return max(submission_dates) if submission_dates else (record.get("created_at") or "")
 
#     pending = [r for r in data if r.get("status") in PENDING_STATUSES]

#     others  = [r for r in data if r.get("status") not in PENDING_STATUSES]
 
#     pending.sort(key=latest_submission_date, reverse=True)

#     others.sort(key=latest_submission_date, reverse=True)
 
#     data = pending + others
 
#     return {

#         "success": True,

#         "data": data

#     }
 
@router.get("/asset-claims/all")
def get_asset_claims(
    user_id: str = Query(...),
    db: Session = Depends(get_db)
):
    # Check if user exists
    requester = db.execute(
        text("SELECT user_id FROM users WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchone()
    
    if not requester:
        raise HTTPException(status_code=404, detail="User not found")
    
    requester_id = requester.user_id
    
    # Get user's roles and supervisor status
    user_info = db.execute(
        text("""
            WITH user_roles AS (
                SELECT 
                    u.user_id,
                    MAX(CASE WHEN rp.role_id = 10 THEN 1 ELSE 0 END) AS is_md,
                    MAX(CASE WHEN rp.role_id = 7 THEN 1 ELSE 0 END) AS is_hr,
                    MAX(CASE WHEN rp.role_id = 11 THEN 1 ELSE 0 END) AS is_finance,
                    EXISTS(
                        SELECT 1 FROM users u2 
                        WHERE u2.supervisor_id = u.user_id 
                        AND u2.user_id != u.user_id
                        LIMIT 1
                    ) AS is_supervisor
                FROM users u
                LEFT JOIN role_permissions rp ON rp.user_id = u.user_id AND rp.submenu_id = 12
                WHERE u.user_id = :user_id
                GROUP BY u.user_id
            )
            SELECT * FROM user_roles
        """),
        {"user_id": requester_id}
    ).mappings().first()
    
    # PENDING_STATUSES constant
    PENDING_STATUSES = {
        "Pending Supervisor Approval",
        "Pending HR Approval",
        "Pending Finance Approval",
    }
    
    # Fetch claims based on roles
    claim_ids = set()
    
    # IMPORTANT FIX: MD users should be treated as supervisors
    # So they see subordinates' pending approvals + their role-based approvals
    is_acting_as_supervisor = user_info['is_supervisor'] or user_info['is_md']
    
    # Case 1: User acts as supervisor (either is_supervisor OR has MD role)
    if is_acting_as_supervisor:
        # 1. Add subordinates' claims with 'Pending Supervisor Approval'
        #    (only if user has subordinates)
        rows = db.execute(
            text("""
                SELECT DISTINCT ac.asset_claim_id
                FROM asset_claim ac
                JOIN users u ON u.user_id = ac.created_by
                WHERE u.supervisor_id = :user_id
                  AND u.user_id != :user_id
                  AND ac.asset_claim_id IN (
                      SELECT DISTINCT asset_claim_id
                      FROM asset_claim_submission
                      WHERE status = 'Pending Supervisor Approval'
                  )
            """),
            {"user_id": requester_id}
        ).scalars().all()
        claim_ids.update(rows)
        
        # 2. If also HR — add Pending HR Approval
        if user_info['is_hr']:
            rows = db.execute(
                text("""
                    SELECT DISTINCT asset_claim_id
                    FROM asset_claim_submission
                    WHERE status = 'Pending HR Approval'
                """)
            ).scalars().all()
            claim_ids.update(rows)
        
        # 3. If also Finance — add Pending Finance Approval
        if user_info['is_finance']:
            rows = db.execute(
                text("""
                    SELECT DISTINCT asset_claim_id
                    FROM asset_claim_submission
                    WHERE status IN ('Pending Finance Approval', 'Asset Claim Approved')
                    
                    UNION
                    
                    SELECT DISTINCT acs.asset_claim_id
                    FROM asset_claim_submission acs
                    JOIN asset_claim ac ON ac.asset_claim_id = acs.asset_claim_id
                    WHERE ac.bought_back = TRUE
                      AND acs.status = 'Asset Claim Disbursed'
                """)
            ).scalars().all()
            claim_ids.update(rows)
    
    # Case 2: Pure HR (not supervisor, not MD)
    elif user_info['is_hr'] and not is_acting_as_supervisor:
        rows = db.execute(
            text("""
                SELECT DISTINCT asset_claim_id
                FROM asset_claim_submission
                WHERE status = 'Pending HR Approval'
            """)
        ).scalars().all()
        claim_ids.update(rows)
    
    # Case 3: Pure Finance (not supervisor, not MD)
    elif user_info['is_finance'] and not is_acting_as_supervisor:
        rows = db.execute(
            text("""
                SELECT DISTINCT asset_claim_id
                FROM asset_claim_submission
                WHERE status IN ('Pending Finance Approval', 'Asset Claim Approved')
                
                UNION
                
                SELECT DISTINCT acs.asset_claim_id
                FROM asset_claim_submission acs
                JOIN asset_claim ac ON ac.asset_claim_id = acs.asset_claim_id
                WHERE ac.bought_back = TRUE
                  AND acs.status IN ('Asset Claim Disbursed','Asset Buyback Rejected') 
            """)
        ).scalars().all()
        claim_ids.update(rows)
    
    # Fetch claims based on collected IDs or employee's own claims
    if claim_ids:
        # Has role-based claims to fetch
        claims = db.execute(
            text("""
                SELECT *
                FROM asset_claim
                WHERE asset_claim_id IN :ids
                ORDER BY COALESCE(updated_at, created_at) DESC
            """),
            {"ids": tuple(claim_ids)}
        ).mappings().all()
    elif is_acting_as_supervisor or user_info['is_hr'] or user_info['is_finance']:
        # Has roles but no pending claims in queue
        claims = []
    else:
        # Pure employee → only their own claims
        claims = db.execute(
            text("""
                SELECT *
                FROM asset_claim
                WHERE created_by = :user_id
                ORDER BY COALESCE(updated_at, created_at) DESC
            """),
            {"user_id": requester_id}
        ).mappings().all()
    
    # Attach submissions
    claims = attach_submissions_to_claims(db, claims)
    
    # Get role-based user IDs for frontend
    hr_ids = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM role_permissions
            WHERE submenu_id = 12 AND role_id = 7
        """)
    ).scalars().all()
    
    finance_ids = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM role_permissions
            WHERE submenu_id = 12 AND role_id = 11
        """)
    ).scalars().all()
    
    md_ids = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM role_permissions
            WHERE submenu_id = 12 AND role_id = 10
        """)
    ).scalars().all()
    
    hop_ids = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM role_permissions
            WHERE submenu_id = 12 AND role_id = 3
        """)
    ).scalars().all()
    
    # Build data list
    data = []
    for claim in claims:
        record = dict(claim)
        
        # Get actual status from submissions (most recent)
        if record.get("submissions"):
            # Get the latest submission status
            latest_submission = max(record["submissions"], key=lambda x: x.get("created_at", ""))
            record["status"] = latest_submission.get("status", record.get("status"))
        
        supervisor_row = db.execute(
            text("SELECT supervisor_id FROM users WHERE user_id = :emp_id"),
            {"emp_id": claim["created_by"]}
        ).fetchone()
        
        record["supervisor_ids"] = (
            [supervisor_row.supervisor_id]
            if supervisor_row and supervisor_row.supervisor_id
            else []
        )
        
        # Set role arrays based on claim type
        if record.get("category") == "Out of Pocket Claim":
            record["hr_ids"] = []
            record["hop_ids"] = list(hop_ids)
        else:
            record["hr_ids"] = list(hr_ids)
            record["hop_ids"] = []
        
        record["finance_ids"] = list(finance_ids)
        record["md_ids"] = list(md_ids)
        
        data.append(record)
    
    # Sort: pending first, then by latest submission created_at DESC
    def latest_submission_date(record):
        submission_dates = [
            s["created_at"]
            for s in record.get("submissions", [])
            if s.get("created_at")
        ]
        return max(submission_dates) if submission_dates else (record.get("created_at") or "")
    
    pending = [r for r in data if r.get("status") in PENDING_STATUSES]
    others = [r for r in data if r.get("status") not in PENDING_STATUSES]
    
    pending.sort(key=latest_submission_date, reverse=True)
    others.sort(key=latest_submission_date, reverse=True)
    
    data = pending + others
    
    return {
        "success": True,
        "data": data
    }
 
 
@router.get("/asset-claims/history")
def get_asset_claims_history(
    user_id: str = Query(...),
    db: Session = Depends(get_db)
    ):
    # Step 1: Fetch requester
    requester = db.execute(
        text("SELECT user_id, username FROM users WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchone()

    if not requester:
        raise HTTPException(status_code=404, detail="User not found")

    requester_id = requester.user_id
    requester_username = requester.username

    # Step 2: Detect roles
    is_admin = db.execute(
        text("SELECT 1 FROM role_permissions WHERE user_id = :uid AND submenu_id = 12 AND role_id = 4 LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    is_hr = db.execute(
        text("SELECT 1 FROM role_permissions WHERE user_id = :uid AND submenu_id = 12 AND role_id = 7 LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    is_finance = db.execute(
        text("SELECT 1 FROM role_permissions WHERE user_id = :uid AND submenu_id = 12 AND role_id = 11 LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    is_supervisor = db.execute(
        text("SELECT 1 FROM users WHERE supervisor_id = :uid AND user_id != :uid LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    is_md = db.execute(
        text("SELECT 1 FROM role_permissions WHERE user_id = :uid AND submenu_id = 12 AND role_id = 10 LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    # Step 3: Fetch claims
    if is_admin or is_hr or is_finance:
        # Admin, HR, Finance → See ALL claims
        claims = db.execute(
            text("SELECT * FROM asset_claim ORDER BY COALESCE(updated_at, created_at) DESC")
        ).mappings().all()

    else:
        claim_ids = set()

        # Supervisor → ONLY subordinates' claims (NOT his own)
        if is_supervisor:
            rows = db.execute(
                text("""
                    SELECT DISTINCT ac.asset_claim_id
                    FROM asset_claim ac
                    JOIN users u ON u.user_id = ac.created_by
                    WHERE u.supervisor_id = :supervisor_id
                """),
                {"supervisor_id": requester_id}
            ).scalars().all()
            claim_ids.update(rows)

        # MD → Actioned claims
        if is_md:
            rows = db.execute(
                text("""
                    SELECT DISTINCT ac.asset_claim_id
                    FROM asset_claim ac
                    JOIN asset_claim_submission acs ON acs.asset_claim_id = ac.asset_claim_id
                    WHERE acs.updated_by = :md_id
                """),
                {"md_id": requester_id}
            ).scalars().all()
            claim_ids.update(rows)

        if claim_ids:
            claims = db.execute(
                text("""
                    SELECT *
                    FROM asset_claim
                    WHERE asset_claim_id IN :ids
                    ORDER BY COALESCE(updated_at, created_at) DESC
                """),
                {"ids": tuple(claim_ids)}
            ).mappings().all()
        else:
            claims = []

    # Step 4: Attach submissions
    claims = attach_submissions_to_claims(db, claims)

    # Step 5: Get role user lists
    def role_users(role_id):
        return db.execute(
            text("SELECT DISTINCT user_id FROM role_permissions WHERE submenu_id = 12 AND role_id = :rid"),
            {"rid": role_id}
        ).scalars().all()

    hr_ids = role_users(7)
    finance_ids = role_users(11)
    md_ids = role_users(10)
    admin_ids = role_users(4)

    # Step 6: Build response
    data = []
    for claim in claims:
        record = dict(claim)

        # Get supervisor of the employee
        sup_row = db.execute(
            text("SELECT supervisor_id FROM users WHERE user_id = :emp_id"),
            {"emp_id": claim["created_by"]}
        ).fetchone()

        record["supervisor_ids"] = [sup_row.supervisor_id] if sup_row and sup_row.supervisor_id else []
        record["hr_ids"] = list(hr_ids)
        record["finance_ids"] = list(finance_ids)
        record["md_ids"] = list(md_ids)
        record["admin_ids"] = list(admin_ids)

        data.append(record)

    return {
        "success": True,
        "data": data
    }


@router.get("/asset-claims/audit-trail")
def get_asset_claims_audit_trail(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
    ):
    # Step 1: check user exists
    exists = db.execute(
        text("SELECT 1 FROM users WHERE user_id = :id"),
        {"id": user_id}
    ).fetchone()

    if not exists:
        raise HTTPException(404, "User not found")

    # Step 2: detect roles
    is_md = db.execute(
        text("""
            SELECT 1 FROM role_permissions
            WHERE user_id = :user_id
              AND submenu_id = 12
              AND role_id = 10
            LIMIT 1
        """),
        {"user_id": user_id}
    ).fetchone()

    is_hr = db.execute(
        text("""
            SELECT 1 FROM role_permissions
            WHERE user_id = :user_id
              AND submenu_id = 12
              AND role_id = 7
            LIMIT 1
        """),
        {"user_id": user_id}
    ).fetchone()

    is_finance = db.execute(
        text("""
            SELECT 1 FROM role_permissions
            WHERE user_id = :user_id
              AND submenu_id = 12
              AND role_id = 11
            LIMIT 1
        """),
        {"user_id": user_id}
    ).fetchone()

    is_supervisor = db.execute(
        text("""
            SELECT 1 FROM users
            WHERE supervisor_id = :user_id
              AND user_id != :user_id
            LIMIT 1
        """),
        {"user_id": user_id}
    ).fetchone()

    # Step 3: base query — reused across all roles
    BASE_QUERY = """
        SELECT
            ac.asset_claim_id,
            ac.employee_name,
            ac.employee_id,
            ac.department,
            ac.designation,
            ac.station,
            ac.grade,
            ac.claim_module,
            ac.category,
            ac.sub_category,
            ac.item_type,
            ac.total_entitlement_limit,
            ac.amount_utilized,
            ac.balance_available,
            ac.status,
            ac.claim_ref_id,
            ac.claim_date,
            ac.created_at,
            ac.updated_at               AS last_updated_at,
            ac.bought_back,
            ac.buy_back_date,
            ac.updated_by_supervisor,
            ac.updated_by_supervisor_name,
            ac.updated_by_hr,
            ac.updated_by_hr_name,
            ac.updated_by_finance,
            ac.updated_by_finance_name,
            acs.claim_amount,
            acs.residual_value_percent,
            acs.residual_value_amount,
            acs.amount_to_be_disbursed,
            acs.owned_by,
            acs.sap_assets_no,
            acs.supervisor_comment,
            acs.hr_comment,
            acs.finance_comment,
            acs.status                  AS submission_status
        FROM asset_claim ac
        LEFT JOIN asset_claim_submission acs
            ON acs.asset_claim_id = ac.asset_claim_id
    """

    # Step 4: role-based filtering
    # Audit trail logic:
    # MD          → all claims in system
    # Supervisor  → own claims + subordinates' claims
    # HR/Finance  → own claims + claims they actioned
    # Employee    → only own claims

    if is_md:
        rows = db.execute(
            text(BASE_QUERY + " ORDER BY ac.created_at DESC")
        ).mappings().all()

    elif is_supervisor:
        # Own claims + subordinates' claims
        rows = db.execute(
            text(BASE_QUERY + """
                WHERE ac.created_by = :user_id
                   OR (
                        EXISTS (
                            SELECT 1 FROM users u
                            WHERE u.user_id = ac.created_by
                              AND u.supervisor_id = :user_id
                              AND u.user_id != :user_id
                        )
                      )
                ORDER BY ac.created_at DESC
            """),
            {"user_id": user_id}
        ).mappings().all()

    elif is_hr or is_finance:
        # Own claims + claims they personally actioned
        rows = db.execute(
            text(BASE_QUERY + """
                WHERE ac.created_by = :user_id
                   OR acs.updated_by = :user_id
                ORDER BY ac.created_at DESC
            """),
            {"user_id": user_id}
        ).mappings().all()

    else:
        # Regular employee → only their own claims
        rows = db.execute(
            text(BASE_QUERY + """
                WHERE ac.created_by = :user_id
                ORDER BY ac.created_at DESC
            """),
            {"user_id": user_id}
        ).mappings().all()

    # Step 5: build response
    data = []
    for row in rows:
        data.append({
            "asset_claim_id":               row["asset_claim_id"],
            "employee_name":                row["employee_name"],
            "employee_id":                  row["employee_id"],
            "department":                   row["department"],
            "designation":                  row["designation"],
            "station":                      row["station"],
            "grade":                        row["grade"],
            "claim_module":                 row["claim_module"],
            "category":                     row["category"],
            "sub_category":                 row["sub_category"],
            "item_type":                    row["item_type"],
            "total_entitlement_limit":      row["total_entitlement_limit"],
            "amount_utilized":              row["amount_utilized"],
            "balance_available":            row["balance_available"],
            "claim_amount":                 row["claim_amount"],
            "residual_value_percent":       row["residual_value_percent"],
            "residual_value_amount":        row["residual_value_amount"],
            "amount_to_be_disbursed":       row["amount_to_be_disbursed"],
            "status":                       row["status"],
            "submission_status":            row["submission_status"],
            "claim_ref_id":                 row["claim_ref_id"],
            "claim_date":                   row["claim_date"],
            "created_at":                   row["created_at"],
            "last_updated_at":              row["last_updated_at"],
            "bought_back":                  row["bought_back"],
            "buy_back_date":                row["buy_back_date"],
            "updated_by_supervisor":        row["updated_by_supervisor"],
            "updated_by_supervisor_name":   row["updated_by_supervisor_name"],
            "updated_by_hr":                row["updated_by_hr"],
            "updated_by_hr_name":           row["updated_by_hr_name"],
            "updated_by_finance":           row["updated_by_finance"],
            "updated_by_finance_name":      row["updated_by_finance_name"],
            "supervisor_comment":           row["supervisor_comment"],
            "hr_comment":                   row["hr_comment"],
            "finance_comment":              row["finance_comment"],
            "owned_by":                     row["owned_by"],
            "sap_assets_no":                row["sap_assets_no"],
        })

    return {
        "success": True,
        "total": len(data),
        "data": data
    }


@router.get("/asset-claims/by-id")
def get_asset_claim_by_id(
    asset_claim_id: int = Query(...),
    db: Session = Depends(get_db)
    ):
    asset_claim = db.execute(
        text("""
            SELECT *
            FROM asset_claim
            WHERE asset_claim_id = :asset_claim_id
        """),
        {"asset_claim_id": asset_claim_id}
    ).mappings().first()

    if not asset_claim:
        raise HTTPException(status_code=404, detail="Asset claim not found")

    submissions = db.execute(
        text("""
            SELECT *
            FROM asset_claim_submission
            WHERE asset_claim_id = :asset_claim_id
        """),
        {"asset_claim_id": asset_claim_id}
    ).mappings().all()

    serialized_submissions = [
        serialize_common(row=s)
        for s in submissions
    ]

    # 👇 Convert to mutable dict
    asset_claim_dict = dict(asset_claim)

    # 👇 Dynamically recalculate entitlement
    try:
        entitlement_data = get_asset_entitlement(
            db=db,
            user_id=asset_claim_dict["created_by"],
            category=asset_claim_dict["category"],
            item_type=asset_claim_dict["item_type"],
            sub_category=asset_claim_dict.get("sub_category"),
        )

        # 👇 Override stale snapshot values with live calculated values
        asset_claim_dict["total_entitlement_limit"] = entitlement_data["total_entitlement_limit"]
        asset_claim_dict["amount_utilized"] = entitlement_data["amount_utilized"]
        asset_claim_dict["balance_available"] = entitlement_data["balance_available"]

    except Exception:
        # fallback to stored values if entitlement calc fails
        pass

    return {
        "success": True,
        "asset_claim": asset_claim_dict,
        "asset_claim_submissions": serialized_submissions
    }


@router.get("/encashment-claims/by-id")
def get_encashment_by_id(
    encashment_main_id: int = Query(...),
    db: Session = Depends(get_db)
    ):
    # Encashment Main
    encashment_main = db.execute(
        text("""
            SELECT *
            FROM encashment_main
            WHERE encashment_main_id = :encashment_main_id
        """),
        {"encashment_main_id": encashment_main_id}
    ).mappings().first()

    if not encashment_main:
        raise HTTPException(status_code=404, detail="Encashment not found")

    # Leave Encashment (child table)
    leave_encashments = db.execute(
        text("""
            SELECT *
            FROM leave_encashment
            WHERE encashment_main_id = :encashment_main_id
        """),
        {"encashment_main_id": encashment_main_id}
    ).mappings().all()

    return {
        "success": True,
        "encashment_main": encashment_main,
        "leave_encashment": leave_encashments
    }



@router.get("/encashment-claims/by-user_id")
def get_encashment_by_employee(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
    ):
    encashments = db.execute(
        text("""
            SELECT *
            FROM encashment_main
            WHERE created_by = :user_id
            ORDER BY updated_at DESC NULLS LAST
        """),
        {"user_id": user_id}
    ).mappings().all()

    if not encashments:
        return {"success": True, "data": []}

    result = []

    for enc in encashments:
        leaves = db.execute(
            text("""
                SELECT *
                FROM leave_encashment
                WHERE encashment_main_id = :encashment_main_id
            """),
            {"encashment_main_id": enc["encashment_main_id"]}
        ).mappings().all()

        enc_dict = dict(enc)
        enc_dict["leave_encashment"] = leaves
        result.append(enc_dict)

    return {
        "success": True,
        "data": result
    }



@router.get("/encashment-claims/all")
def get_all_encashments(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    # Step 1: check user exists
    exists = db.execute(
        text("SELECT 1 FROM users WHERE user_id = :id"),
        {"id": user_id}
    ).fetchone()

    if not exists:
        raise HTTPException(404, "User not found")

    # Step 2: get user's roles and supervisor status in one query
    user_info = db.execute(
        text("""
            WITH user_roles AS (
                SELECT 
                    u.user_id,
                    MAX(CASE WHEN rp.role_id = 10 THEN 1 ELSE 0 END) AS is_md,
                    MAX(CASE WHEN rp.role_id = 7 THEN 1 ELSE 0 END) AS is_hr,
                    MAX(CASE WHEN rp.role_id = 11 THEN 1 ELSE 0 END) AS is_finance,
                    MAX(CASE WHEN rp.role_id = 3 THEN 1 ELSE 0 END) AS is_hop,
                    EXISTS(
                        SELECT 1 FROM users u2 
                        WHERE u2.supervisor_id = u.user_id 
                        AND u2.user_id != u.user_id
                        LIMIT 1
                    ) AS is_supervisor
                FROM users u
                LEFT JOIN role_permissions rp ON rp.user_id = u.user_id AND rp.submenu_id = 12
                WHERE u.user_id = :user_id
                GROUP BY u.user_id
            )
            SELECT * FROM user_roles
        """),
        {"user_id": user_id}
    ).mappings().first()

    # IMPORTANT FIX: MD users should be treated as supervisors
    # So they see subordinates' pending approvals + their role-based approvals
    is_acting_as_supervisor = user_info['is_supervisor'] or user_info['is_md']

    # Step 3: fetch encashments based on role
    claim_ids = set()

    # Case 1: User acts as supervisor (either is_supervisor OR has MD role)
    if is_acting_as_supervisor:
        # 1. Add subordinates' claims with 'Pending Supervisor Approval'
        rows = db.execute(
            text("""
                SELECT DISTINCT em.encashment_main_id
                FROM encashment_main em
                JOIN users u ON u.user_id = em.created_by
                WHERE u.supervisor_id = :user_id
                  AND u.user_id != :user_id
                  AND em.encashment_main_id IN (
                      SELECT DISTINCT encashment_main_id
                      FROM leave_encashment
                      WHERE status = 'Pending Supervisor Approval'
                  )
            """),
            {"user_id": user_id}
        ).scalars().all()
        claim_ids.update(rows)

        # 2. If also HR → add Pending HR Approval
        if user_info['is_hr']:
            rows = db.execute(
                text("""
                    SELECT DISTINCT encashment_main_id
                    FROM leave_encashment
                    WHERE status = 'Pending HR Approval'
                """)
            ).scalars().all()
            claim_ids.update(rows)

        # 3. If also Finance → add Pending Finance Approval
        if user_info['is_finance']:
            rows = db.execute(
                text("""
                    SELECT DISTINCT encashment_main_id
                    FROM leave_encashment
                    WHERE status = 'Pending Finance Approval'
                """)
            ).scalars().all()
            claim_ids.update(rows)
        
        # 4. If also HOP → add Pending HOP Approval
        if user_info['is_hop']:
            rows = db.execute(
                text("""
                    SELECT DISTINCT encashment_main_id
                    FROM leave_encashment
                    WHERE status = 'Pending HOP Approval'
                """)
            ).scalars().all()
            claim_ids.update(rows)

        # Fetch claims
        if claim_ids:
            encashments = db.execute(
                text("""
                    SELECT *
                    FROM encashment_main
                    WHERE encashment_main_id IN :ids
                    ORDER BY updated_at DESC NULLS LAST
                """),
                {"ids": tuple(claim_ids)}
            ).mappings().all()
        else:
            encashments = []

    # Case 2: Pure HR, Finance, or HOP (not supervisor, not MD)
    elif any([user_info['is_hr'], user_info['is_finance'], user_info['is_hop']]):
        # Add HR pending approvals
        if user_info['is_hr']:
            rows = db.execute(
                text("""
                    SELECT DISTINCT encashment_main_id
                    FROM leave_encashment
                    WHERE status = 'Pending HR Approval'
                """)
            ).scalars().all()
            claim_ids.update(rows)

        # Add Finance pending approvals
        if user_info['is_finance']:
            rows = db.execute(
                text("""
                    SELECT DISTINCT encashment_main_id
                    FROM leave_encashment
                    WHERE status = 'Pending Finance Approval'
                """)
            ).scalars().all()
            claim_ids.update(rows)

        # Add HOP pending approvals
        if user_info['is_hop']:
            rows = db.execute(
                text("""
                    SELECT DISTINCT encashment_main_id
                    FROM leave_encashment
                    WHERE status = 'Pending HOP Approval'
                """)
            ).scalars().all()
            claim_ids.update(rows)

        # Fetch based on collected IDs
        if claim_ids:
            encashments = db.execute(
                text("""
                    SELECT *
                    FROM encashment_main
                    WHERE encashment_main_id IN :ids
                    ORDER BY updated_at DESC NULLS LAST
                """),
                {"ids": tuple(claim_ids)}
            ).mappings().all()
        else:
            # Has roles but no pending claims
            encashments = []

    # Case 3: Regular employee (no roles, not supervisor, not MD)
    else:
        # Pure employee → only their own claims
        encashments = db.execute(
            text("""
                SELECT *
                FROM encashment_main
                WHERE created_by = :user_id
                ORDER BY updated_at DESC NULLS LAST
            """),
            {"user_id": user_id}
        ).mappings().all()

    # Step 4: get role-based arrays from role_permissions
    hr_ids = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM role_permissions
            WHERE submenu_id = 12 AND role_id = 7
        """)
    ).scalars().all()

    finance_ids = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM role_permissions
            WHERE submenu_id = 12 AND role_id = 11
        """)
    ).scalars().all()

    md_ids = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM role_permissions
            WHERE submenu_id = 12 AND role_id = 10
        """)
    ).scalars().all()

    hop_ids = db.execute(
        text("""
            SELECT DISTINCT user_id
            FROM role_permissions
            WHERE submenu_id = 12 AND role_id = 3
        """)
    ).scalars().all()

    # Step 5: build response
    result = []
    for enc in encashments:
        leaves = db.execute(
            text("""
                SELECT *
                FROM leave_encashment
                WHERE encashment_main_id = :encashment_main_id
                ORDER BY created_at DESC
            """),
            {"encashment_main_id": enc["encashment_main_id"]}
        ).mappings().all()

        enc_dict = dict(enc)
        enc_dict["leave_encashment"] = leaves
        
        # Get the latest status from leave_encashment if available
        if leaves:
            # Get the status from the first leave (they should all have same status for a main record)
            enc_dict["status"] = leaves[0].get("status", enc_dict.get("status"))

        supervisor_row = db.execute(
            text("SELECT supervisor_id FROM users WHERE user_id = :emp_id"),
            {"emp_id": enc["created_by"]}
        ).fetchone()

        enc_dict["supervisor_ids"] = (
            [supervisor_row.supervisor_id]
            if supervisor_row and supervisor_row.supervisor_id
            else []
        )

        # Set role arrays
        enc_dict["hr_ids"] = list(hr_ids)
        enc_dict["finance_ids"] = list(finance_ids)
        enc_dict["md_ids"] = list(md_ids)
        enc_dict["hop_ids"] = list(hop_ids)

        result.append(enc_dict)

    # Step 6: sort - pending first, then by updated_at
    PENDING_STATUSES = {
        "Pending Supervisor Approval",
        "Pending HR Approval",
        "Pending Finance Approval",
        "Pending HOP Approval"
    }
    
    pending = [r for r in result if r.get("status") in PENDING_STATUSES]
    others = [r for r in result if r.get("status") not in PENDING_STATUSES]
    
    pending.sort(key=lambda x: x.get("updated_at") or x.get("created_at") or "", reverse=True)
    others.sort(key=lambda x: x.get("updated_at") or x.get("created_at") or "", reverse=True)
    
    result = pending + others

    return {
        "success": True,
        "data": result
    }




@router.get("/encashment-claims/history")
def get_encashment_claims_history(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
    ):
    # 1️⃣ Get requester
    user = db.execute(
        text("SELECT user_id, username FROM users WHERE user_id = :uid"),
        {"uid": user_id}
    ).fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    requester_id = user.user_id
    username = user.username.lower()

    # 2️⃣ Detect roles
    is_admin = db.execute(
        text("SELECT 1 FROM role_permissions WHERE user_id = :uid AND submenu_id = 12 AND role_id = 4 LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    is_hr = db.execute(
        text("SELECT 1 FROM role_permissions WHERE user_id = :uid AND submenu_id = 12 AND role_id = 7 LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    is_finance = db.execute(
        text("SELECT 1 FROM role_permissions WHERE user_id = :uid AND submenu_id = 12 AND role_id = 11 LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    is_supervisor = db.execute(
        text("SELECT 1 FROM users WHERE supervisor_id = :uid LIMIT 1"),
        {"uid": requester_id}
    ).fetchone() is not None

    # 3️⃣ Fetch claims
    if is_admin or is_hr or is_finance:
        encashments = db.execute(
            text("SELECT * FROM encashment_main ORDER BY encashment_main_id DESC")
        ).mappings().all()

    else:
        enc_ids = set()

        # Supervisor → ONLY subordinates' claims
        if is_supervisor:
            rows = db.execute(
                text("""
                    SELECT DISTINCT le.encashment_main_id
                    FROM leave_encashment le
                    JOIN users u ON u.user_id = le.created_by
                    WHERE u.supervisor_id = :supervisor_id
                """),
                {"supervisor_id": requester_id}
            ).scalars().all()
            enc_ids.update(rows)

        if not enc_ids:
            return {"success": True, "data": []}

        encashments = db.execute(
            text("SELECT * FROM encashment_main WHERE encashment_main_id IN :ids ORDER BY encashment_main_id DESC")
            .bindparams(bindparam("ids", expanding=True)),
            {"ids": list(enc_ids)}
        ).mappings().all()

    # 4️⃣ Attach leave details
    result = []
    for enc in encashments:
        leaves = db.execute(
            text("SELECT * FROM leave_encashment WHERE encashment_main_id = :id"),
            {"id": enc["encashment_main_id"]}
        ).mappings().all()

        enc_dict = dict(enc)
        enc_dict["leave_encashment"] = leaves
        result.append(enc_dict)

    return {
        "success": True,
        "data": result
    }

def serialize_documents(rows):
    data = []
    for r in rows:
        r = dict(r)
        r = make_document_fields_downloadable(
            r,
            ["document_names", "bill_path", "attachment_path"]
        )
        data.append(r)
    return data

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.routers.UserAuthR2 import make_download_url
import os

import os
import json

BASE_STORAGE_DIR = "files"
import os
import json

def make_downloadable(value) -> list[str]:
    """
    Always returns a list of downloadable URLs.
    Handles:
    - comma-separated paths
    - JSON string arrays
    - absolute Windows paths
    """
    if not value:
        return []

    # ----------------------------
    # Normalize input to list
    # ----------------------------
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("["):
            try:
                paths = json.loads(value)
            except Exception:
                paths = [value]
        else:
            paths = value.split(",")
    elif isinstance(value, list):
        paths = value
    else:
        return []

    urls = []

    for p in paths:
        if not p:
            continue

        # normalize slashes
        p = p.strip().replace("\\", "/")

        # ----------------------------
        # Convert absolute → relative
        # ----------------------------
        if "/files/" in p:
            p = "files/" + p.split("/files/", 1)[1]

        # safety: remove accidental quotes
        p = p.strip('"').strip("'")

        urls.append(make_download_url(p))

    return urls

def make_document_fields_downloadable(row: dict, fields: list[str]) -> dict:
    for field in fields:
        row[field] = make_downloadable(row.get(field))
    return row




@router.get("/asset-claims/cards")
def get_asset_claim_cards(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
    ):
    # --------------------------------------------------
    # 1️⃣ USER CHECK
    # --------------------------------------------------
    user_exists = db.execute(
        text("SELECT 1 FROM users WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchone()

    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    # --------------------------------------------------
    # 2️⃣ ADMIN CHECK (FIXED ❗)
    # --------------------------------------------------
    is_admin = db.execute(
        text("""
            SELECT 1
            FROM users
            WHERE user_id = :user_id
              AND role_id IN (10, 11)
            LIMIT 1
        """),
        {"user_id": user_id}
    ).fetchone()

    # --------------------------------------------------
    # 3️⃣ WHERE CLAUSE (LOCKED)
    # --------------------------------------------------
    if is_admin:
        where_clause = ""
        params = {}
    else:
        where_clause = """
            WHERE ac.created_by = :user_id
        """
        params = {"user_id": user_id}

    # --------------------------------------------------
    # 4️⃣ DASHBOARD QUERY
    # --------------------------------------------------
    cards = db.execute(
        text(f"""
            SELECT
                COUNT(DISTINCT acs.asset_claim_submission_id) AS total_claims,

                COUNT(*) FILTER (
                    WHERE acs.status ILIKE '%pending%'
                ) AS pending,

                COUNT(*) FILTER (
                    WHERE acs.status ILIKE '%approved%'
                       OR acs.status ILIKE '%disbursed%'
                ) AS approved,

                COALESCE(
                    SUM(acs.amount_to_be_disbursed) FILTER (
                        WHERE acs.status ILIKE '%approved%'
                           OR acs.status ILIKE '%disbursed%'
                    ),
                    0
                ) AS total_claimed
            FROM asset_claim_submission acs
            JOIN asset_claim ac
              ON ac.asset_claim_id = acs.asset_claim_id
            {where_clause}
        """),
        params
    ).mappings().one()

    # --------------------------------------------------
    # 5️⃣ RESPONSE
    # --------------------------------------------------
    return {
        "success": True,
        "data": {
            "total_claims": cards["total_claims"],
            "approved": cards["approved"],
            "pending": cards["pending"],
            "total_claimed": float(cards["total_claimed"])
        }
    }




# =====================================================
# Main Fetch Function
# =====================================================
def fetch_ra_entries(db: Session, ra_claim: dict):
    """
    ra_claim expected structure:
    {
        "ra_claim_id": int,
        "claim_module": "Reimbursement" | "Allowance",
        "category": str | None
    }
    """

    ra_id = ra_claim.get("ra_claim_id")
    module = ra_claim.get("claim_module")
    # if module != "Reimbursement":
        
        # print("aman  bau yaha hub yaha",ra_id)
    category = ra_claim.get("category")
    # print("module hai malik",module)

    # print("ra_id hai malik",ra_id)
    # print("category hai malik",category)

    if not ra_id or not module:
        return []

    # ==================================================
    # REIMBURSEMENT (RA)
    # ==================================================
    # print(module,"= module")
    if module == "Reimbursement":
        table_map = {
            "VEHICLE C&M Reimbursement": "vehicle_cm_reimbursement",
            "Mobile Bill Reimbursement": "mobile_bill_reimbursement",
            "LAPTOP Maintenance": "laptop_maintenance_reimbursement",
            "FURNITURE R&M Reimbursement": "furniture_rm_reimbursement",
            "Data Card Charges Reimbursement": "data_card_reimbursement",
            "Out of Pocket Claim": "out_of_pocket_claim",
        }

        table_name = table_map.get(category)
        if not table_name:
            return []

        parents = db.execute(
            text(f"""
                SELECT *
                FROM {table_name}
                WHERE ra_claim_id = :ra_id
                ORDER BY created_at
            """),
            {"ra_id": ra_id}
        ).mappings().all()

        results = []

        for p in parents:
            parent = dict(p)

            # 📎 Parent documents
            parent = make_document_fields_downloadable(
                parent,
                fields=["document_names"]
            )

            # ==================================================
            # 🔥 OUT OF POCKET → FETCH CHILD ENTRIES
            # ==================================================
            if category == "Out of Pocket Claim":
                entries = db.execute(
                    text("""
                        SELECT *
                        FROM out_of_pocket_claim_entry
                        WHERE out_of_pocket_claim_id = :pid
                        ORDER BY created_at
                    """),
                    {
                        "pid": parent["out_of_pocket_claim_id"]
                    }
                ).mappings().all()

                parent["entries"] = [dict(e) for e in entries]

            results.append(parent)

        return results

    # ==================================================
    # ALLOWANCE (Admission Children)
    # ==================================================

    else:
        # print("➡️ Entered ALLOWANCE block")

        parents = db.execute(
            text("""
                SELECT *
                FROM allowance_claim
                WHERE ra_claim_id = :ra_id
                ORDER BY created_at
            """),
            {"ra_id": ra_id}
        ).mappings().all()

        if not parents:
            # print("❌ No allowance_claim found")
            return []

        results = []

        for p in parents:
            parent = dict(p)
            allowance_claim_id = parent.get("allowance_claim_id")

            # print("🧾 Processing allowance_claim_id:", allowance_claim_id)

            # 📎 Parent documents
            parent = make_document_fields_downloadable(
                parent,
                fields=["document_names"]
            )

            # 👶 Fetch child entries
            # 👶 Fetch child entries
            children = db.execute(
                text("""
                    SELECT *
                    FROM allowance_admission_child
                    WHERE allowance_claim_id = :id
                """),
                {"id": allowance_claim_id}
            ).mappings().all()

            # ✅ FIX: serialize children properly
            child_list = []
            for c in children:
                c_dict = dict(c)
                c_dict = make_document_fields_downloadable(
                    c_dict,
                    fields=["document_names"]
                )
                child_list.append(c_dict)

            parent["children"] = child_list


            # parent["children"] = [dict(c) for c in children]

            results.append(parent)

        return results

    return []


def build_ra_payload(data: dict):
    
    return {
        "ra_claim_id": data.get("ra_claim_id"),
        "claim_module": data.get("claim_module"),  # Reimbursement | Allowance
        "category": data.get("category")
    }

# =================================================
# GET CLAIM BY ID
# =================================================
@router.get("/ra-claims/by-id")
def get_claim_by_id(
    module: str = Query(..., regex="^(RA|ALLOWANCE)$"),
    claim_id: int = Query(...),
    db: Session = Depends(get_db)
    ):
    # print("========== GET CLAIM BY ID API HIT ==========")
    # print(f"Incoming params -> module: {module}, claim_id: {claim_id}")

    if module == "RA":
        # print("Module is RA → Fetching from ra_claim table")

        main = db.execute(
            text("""
                SELECT *
                FROM ra_claim
                WHERE ra_claim_id = :id
            """),
            {"id": claim_id}
        ).mappings().first()

        claim_module = "Reimbursement"
        document_fields = ["bill_path", "invoice_path", "supporting_documents"]

    else:
        # print("Module is ALLOWANCE → Joining ra_claim & allowance_claim")

        main = db.execute(
            text("""
               SELECT *
                FROM ra_claim
                WHERE ra_claim_id = :id
            """),
            {"id": claim_id}
        ).mappings().first()

        claim_module = "Allowance"
        document_fields = ["bill_path", "invoice_path", "supporting_documents"]

    if not main:
        # print("❌ No claim found for given ID")
        raise HTTPException(404, "Claim not found")

    # print("✅ Main claim fetched successfully")
    # print("Main claim raw data:", dict(main))

    main = make_document_fields_downloadable(dict(main), document_fields)
    # print("📎 Document fields processed for download")

    payload_data = {
        **main,
        "claim_module": claim_module
    }

    # print("📦 Payload before build_ra_payload:", payload_data)

    payload = build_ra_payload(payload_data)
    # print("🛠️ Payload after build_ra_payload:", payload)

    # print("🔍 Fetching RA entries using payload")
    entries = fetch_ra_entries(db, payload)

    # print(f"📄 Entries fetched count: {len(entries) if entries else 0}")
    # print("========== API END ==========")

    return {
        "success": True,
        "module": module,
        "claim": main,
        "entries": entries
    }




@router.get("/ra-claims/user-id")
def get_claims_by_user_id(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
    ):
    ra_claims = db.execute(
     text("""
    SELECT *,
        CASE
            WHEN claim_module = 'Allowance' THEN 'ALLOWANCE'
            ELSE 'RA'
        END AS module
    FROM ra_claim
    WHERE created_by = :uid
   ORDER BY created_at DESC NULLS LAST
    """),  {"uid": user_id}
    ).mappings().all()

  
    all_claims = ra_claims 

    if not all_claims:
        raise HTTPException(404, "No claims found")

    data = []
    for c in all_claims:
        record = dict(c)

        payload = build_ra_payload({
            **record,
           "claim_module":c.claim_module
        })
        # print("payload",payload)
        record["entries"] = fetch_ra_entries(db, payload)
        data.append(record)

    return {
        "success": True,
        "user_id": user_id,
        "data": data
    }

# @router.get("/ra-claims/all")
# def get_all_claims(
#     user_id: int = Query(...),
#     db: Session = Depends(get_db)
# ):
#     exists = db.execute(
#         text("SELECT 1 FROM users WHERE user_id = :id"),
#         {"id": user_id}
#     ).fetchone()

#     if not exists:
#         raise HTTPException(404, "User not found")

#     is_supervisor = db.execute(
#         text("""
#             SELECT 1 FROM users
#             WHERE supervisor_id = :user_id
#               AND user_id != :user_id
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).fetchone()

#     is_md = db.execute(
#         text("""
#             SELECT 1 FROM role_permissions
#             WHERE user_id = :user_id
#               AND submenu_id = 12
#               AND role_id = 10
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).fetchone()

#     is_hr = db.execute(
#         text("""
#             SELECT 1 FROM role_permissions
#             WHERE user_id = :user_id
#               AND submenu_id = 12
#               AND role_id = 7
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).fetchone()

#     is_finance = db.execute(
#         text("""
#             SELECT 1 FROM role_permissions
#             WHERE user_id = :user_id
#               AND submenu_id = 12
#               AND role_id = 11
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).fetchone()

#     is_hop = db.execute(
#         text("""
#             SELECT 1 FROM role_permissions
#             WHERE user_id = :user_id
#               AND submenu_id = 12
#               AND role_id = 3
#             LIMIT 1
#         """),
#         {"user_id": user_id}
#     ).fetchone()

#     # ─── DEBUG: print all distinct statuses in ra_claim for subordinates ───
#     distinct_statuses = db.execute(
#         text("""
#             SELECT DISTINCT rc.status
#             FROM ra_claim rc
#             JOIN users u ON u.user_id = rc.created_by
#             WHERE u.supervisor_id = :user_id
#               AND u.user_id != :user_id
#         """),
#         {"user_id": user_id}
#     ).fetchall()

#     print(f"""
#     ========== DEBUG user_id={user_id} ==========
#     is_supervisor : {bool(is_supervisor)}
#     is_md         : {bool(is_md)}
#     is_hr         : {bool(is_hr)}
#     is_finance    : {bool(is_finance)}
#     is_hop        : {bool(is_hop)}
#     distinct subordinate claim statuses: {[r[0] for r in distinct_statuses]}
#     =============================================
#     """)
#     # ─────────────────────────────────────────────────────────────────────────

#     if is_supervisor:
#         claim_ids = set()

#         # Fetch subordinates' claims with EXACT status match
#         # (status values must match exactly what's stored in DB)
#         subordinate_claim_ids = db.execute(
#             text("""
#                 SELECT DISTINCT rc.ra_claim_id
#                 FROM ra_claim rc
#                 JOIN users u ON u.user_id = rc.created_by
#                 WHERE u.supervisor_id = :user_id
#                   AND u.user_id != :user_id
#                   AND rc.status = 'Pending Supervisor Approval'
#             """),
#             {"user_id": user_id}
#         ).scalars().all()

#         claim_ids.update(subordinate_claim_ids)

#         print(f"Supervisor {user_id}: found {len(subordinate_claim_ids)} pending supervisor approval claims")

#         # If also HR → add Pending HR Approval
#         if is_hr:
#             rows = db.execute(
#                 text("""
#                     SELECT DISTINCT ra_claim_id
#                     FROM ra_claim
#                     WHERE status = 'Pending HR Approval'
#                 """)
#             ).scalars().all()
#             claim_ids.update(rows)

#         # If also HOP → add Pending HOP Approval
#         if is_hop:
#             rows = db.execute(
#                 text("""
#                     SELECT DISTINCT ra_claim_id
#                     FROM ra_claim
#                     WHERE status = 'Pending HOP Approval'
#                 """)
#             ).scalars().all()
#             claim_ids.update(rows)

#         # If also Finance → add Pending Finance Approval
#         if is_finance:
#             rows = db.execute(
#                 text("""
#                     SELECT DISTINCT ra_claim_id
#                     FROM ra_claim
#                     WHERE status = 'Pending Finance Approval'
#                 """)
#             ).scalars().all()
#             claim_ids.update(rows)

#         # MD role intentionally ignored for supervisors

#         if claim_ids:
#             ra_claims = db.execute(
#                 text("""
#                     SELECT *, CASE
#                         WHEN claim_module = 'Allowance' THEN 'ALLOWANCE'
#                         ELSE 'RA'
#                     END AS module
#                     FROM ra_claim
#                     WHERE ra_claim_id IN :ids
#                     ORDER BY updated_at DESC NULLS LAST
#                 """),
#                 {"ids": tuple(claim_ids)}
#             ).mappings().all()
#         else:
#             ra_claims = []

#     elif is_md:
#         ra_claims = db.execute(
#             text("""
#                 SELECT *, CASE
#                     WHEN claim_module = 'Allowance' THEN 'ALLOWANCE'
#                     ELSE 'RA'
#                 END AS module
#                 FROM ra_claim
#                 ORDER BY updated_at DESC NULLS LAST
#             """)
#         ).mappings().all()

#     else:
#         claim_ids = set()

#         if is_hr:
#             rows = db.execute(
#                 text("""
#                     SELECT DISTINCT ra_claim_id
#                     FROM ra_claim
#                     WHERE status = 'Pending HR Approval'
#                 """)
#             ).scalars().all()
#             claim_ids.update(rows)

#         if is_hop:
#             rows = db.execute(
#                 text("""
#                     SELECT DISTINCT ra_claim_id
#                     FROM ra_claim
#                     WHERE status = 'Pending HOP Approval'
#                 """)
#             ).scalars().all()
#             claim_ids.update(rows)

#         if is_finance:
#             rows = db.execute(
#                 text("""
#                     SELECT DISTINCT ra_claim_id
#                     FROM ra_claim
#                     WHERE status = 'Pending Finance Approval'
#                 """)
#             ).scalars().all()
#             claim_ids.update(rows)

#         if claim_ids:
#             ra_claims = db.execute(
#                 text("""
#                     SELECT *, CASE
#                         WHEN claim_module = 'Allowance' THEN 'ALLOWANCE'
#                         ELSE 'RA'
#                     END AS module
#                     FROM ra_claim
#                     WHERE ra_claim_id IN :ids
#                     ORDER BY updated_at DESC NULLS LAST
#                 """),
#                 {"ids": tuple(claim_ids)}
#             ).mappings().all()

#         elif is_hr or is_hop or is_finance:
#             ra_claims = []

#         else:
#             # Pure employee → only their own claims
#             ra_claims = db.execute(
#                 text("""
#                     SELECT rc.*, CASE
#                         WHEN claim_module = 'Allowance' THEN 'ALLOWANCE'
#                         ELSE 'RA'
#                     END AS module
#                     FROM ra_claim rc
#                     WHERE rc.created_by = :user_id
#                     ORDER BY updated_at DESC NULLS LAST
#                 """),
#                 {"user_id": user_id}
#             ).mappings().all()

#     # Step 3: role-based user id arrays
#     def role_users(role_id):
#         return db.execute(
#             text("""
#                 SELECT DISTINCT user_id
#                 FROM role_permissions
#                 WHERE submenu_id = 12
#                   AND role_id = :rid
#             """),
#             {"rid": role_id}
#         ).scalars().all()

#     hr_ids = role_users(7)
#     finance_ids = role_users(11)
#     md_ids = role_users(10)
#     hop_ids = role_users(3)

#     data = []
#     for c in ra_claims:
#         record = dict(c)
#         payload = build_ra_payload({
#             **record,
#             "claim_module": c.claim_module
#         })
#         record["entries"] = fetch_ra_entries(db, payload)

#         sup = db.execute(
#             text("SELECT supervisor_id FROM users WHERE user_id = :id"),
#             {"id": record["created_by"]}
#         ).fetchone()

#         record["supervisor_ids"] = (
#             [sup.supervisor_id] if sup and sup.supervisor_id else []
#         )

#         if record.get("category") == "Out of Pocket Claim":
#             record["hr_ids"] = []
#             record["hop_ids"] = list(hop_ids)
#         else:
#             record["hr_ids"] = list(hr_ids)
#             record["hop_ids"] = []

#         record["finance_ids"] = list(finance_ids)
#         record["md_ids"] = list(md_ids)

#         data.append(record)

#     return {
#         "success": True,
#         "data": data
#     }


@router.get("/ra-claims/all")
def get_all_claims(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    # Check if user exists
    exists = db.execute(
        text("SELECT 1 FROM users WHERE user_id = :id"),
        {"id": user_id}
    ).fetchone()
    
    if not exists:
        raise HTTPException(404, "User not found")
    
    # Get user's roles and supervisor status
    user_info = db.execute(
        text("""
            WITH user_roles AS (
                SELECT 
                    u.user_id,
                    MAX(CASE WHEN rp.role_id = 10 THEN 1 ELSE 0 END) AS is_md,
                    MAX(CASE WHEN rp.role_id = 7 THEN 1 ELSE 0 END) AS is_hr,
                    MAX(CASE WHEN rp.role_id = 11 THEN 1 ELSE 0 END) AS is_finance,
                    MAX(CASE WHEN rp.role_id = 3 THEN 1 ELSE 0 END) AS is_hop,
                    EXISTS(
                        SELECT 1 FROM users u2 
                        WHERE u2.supervisor_id = u.user_id 
                        AND u2.user_id != u.user_id
                        LIMIT 1
                    ) AS is_supervisor
                FROM users u
                LEFT JOIN role_permissions rp ON rp.user_id = u.user_id AND rp.submenu_id = 12
                WHERE u.user_id = :user_id
                GROUP BY u.user_id
            )
            SELECT * FROM user_roles
        """),
        {"user_id": user_id}
    ).mappings().first()
    
    params = {"user_id": user_id}
    
    # IMPORTANT FIX: MD users should be treated as supervisors
    # So they see subordinates' pending approvals + their role-based approvals
    is_acting_as_supervisor = user_info['is_supervisor'] or user_info['is_md']
    
    # Case 1: User acts as supervisor (either is_supervisor OR has MD role)
    if is_acting_as_supervisor:
        union_parts = []
        
        # 1. Subordinates' claims with 'Pending Supervisor Approval'
        #    (if user has subordinates)
        if user_info['is_supervisor'] or user_info['is_md']:
            union_parts.append(f"""
                SELECT DISTINCT rc.ra_claim_id
                FROM ra_claim rc
                INNER JOIN users u ON u.user_id = rc.created_by
                WHERE u.supervisor_id = :user_id
                  AND u.user_id != :user_id
                  AND EXISTS (
                      SELECT 1 FROM allowance_claim ac WHERE ac.ra_claim_id = rc.ra_claim_id AND ac.status = 'Pending Supervisor Approval'
                      UNION
                      SELECT 1 FROM data_card_reimbursement dcr WHERE dcr.ra_claim_id = rc.ra_claim_id AND dcr.status = 'Pending Supervisor Approval'
                      UNION
                      SELECT 1 FROM furniture_rm_reimbursement frmr WHERE frmr.ra_claim_id = rc.ra_claim_id AND frmr.status = 'Pending Supervisor Approval'
                      UNION
                      SELECT 1 FROM laptop_maintenance_reimbursement lmr WHERE lmr.ra_claim_id = rc.ra_claim_id AND lmr.status = 'Pending Supervisor Approval'
                      UNION
                      SELECT 1 FROM mobile_bill_reimbursement mbr WHERE mbr.ra_claim_id = rc.ra_claim_id AND mbr.status = 'Pending Supervisor Approval'
                      UNION
                      SELECT 1 FROM out_of_pocket_claim oop WHERE oop.ra_claim_id = rc.ra_claim_id AND oop.status = 'Pending Supervisor Approval'
                      UNION
                      SELECT 1 FROM vehicle_cm_reimbursement vcmr WHERE vcmr.ra_claim_id = rc.ra_claim_id AND vcmr.status = 'Pending Supervisor Approval'
                  )
            """)
        
        # 2. If HR role - add Pending HR Approval claims
        if user_info['is_hr']:
            union_parts.append(f"""
                SELECT DISTINCT rc.ra_claim_id
                FROM ra_claim rc
                WHERE EXISTS (
                    SELECT 1 FROM allowance_claim ac WHERE ac.ra_claim_id = rc.ra_claim_id AND ac.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM data_card_reimbursement dcr WHERE dcr.ra_claim_id = rc.ra_claim_id AND dcr.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM furniture_rm_reimbursement frmr WHERE frmr.ra_claim_id = rc.ra_claim_id AND frmr.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM laptop_maintenance_reimbursement lmr WHERE lmr.ra_claim_id = rc.ra_claim_id AND lmr.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM mobile_bill_reimbursement mbr WHERE mbr.ra_claim_id = rc.ra_claim_id AND mbr.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM out_of_pocket_claim oop WHERE oop.ra_claim_id = rc.ra_claim_id AND oop.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM vehicle_cm_reimbursement vcmr WHERE vcmr.ra_claim_id = rc.ra_claim_id AND vcmr.status = 'Pending HR Approval'
                )
            """)
        
        # 3. If HOP role - add Pending HOP Approval claims
        if user_info['is_hop']:
            union_parts.append(f"""
                SELECT DISTINCT rc.ra_claim_id
                FROM ra_claim rc
                WHERE EXISTS (
                    SELECT 1 FROM allowance_claim ac WHERE ac.ra_claim_id = rc.ra_claim_id AND ac.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM data_card_reimbursement dcr WHERE dcr.ra_claim_id = rc.ra_claim_id AND dcr.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM furniture_rm_reimbursement frmr WHERE frmr.ra_claim_id = rc.ra_claim_id AND frmr.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM laptop_maintenance_reimbursement lmr WHERE lmr.ra_claim_id = rc.ra_claim_id AND lmr.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM mobile_bill_reimbursement mbr WHERE mbr.ra_claim_id = rc.ra_claim_id AND mbr.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM out_of_pocket_claim oop WHERE oop.ra_claim_id = rc.ra_claim_id AND oop.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM vehicle_cm_reimbursement vcmr WHERE vcmr.ra_claim_id = rc.ra_claim_id AND vcmr.status = 'Pending HOP Approval'
                )
            """)
        
        # 4. If Finance role - add Pending Finance Approval claims
        if user_info['is_finance']:
            union_parts.append(f"""
                SELECT DISTINCT rc.ra_claim_id
                FROM ra_claim rc
                WHERE EXISTS (
                    SELECT 1 FROM allowance_claim ac WHERE ac.ra_claim_id = rc.ra_claim_id AND ac.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM data_card_reimbursement dcr WHERE dcr.ra_claim_id = rc.ra_claim_id AND dcr.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM furniture_rm_reimbursement frmr WHERE frmr.ra_claim_id = rc.ra_claim_id AND frmr.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM laptop_maintenance_reimbursement lmr WHERE lmr.ra_claim_id = rc.ra_claim_id AND lmr.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM mobile_bill_reimbursement mbr WHERE mbr.ra_claim_id = rc.ra_claim_id AND mbr.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM out_of_pocket_claim oop WHERE oop.ra_claim_id = rc.ra_claim_id AND oop.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM vehicle_cm_reimbursement vcmr WHERE vcmr.ra_claim_id = rc.ra_claim_id AND vcmr.status = 'Pending Finance Approval'
                )
            """)
        
        if union_parts:
            union_query = " UNION ".join(union_parts)
            final_query = f"""
                SELECT DISTINCT
                    rc.*,
                    CASE
                        WHEN rc.claim_module = 'Allowance' THEN 'ALLOWANCE'
                        ELSE 'RA'
                    END AS module
                FROM ra_claim rc
                WHERE rc.ra_claim_id IN ({union_query})
                ORDER BY rc.updated_at DESC NULLS LAST
            """
            ra_claims = db.execute(text(final_query), params).mappings().all()
        else:
            ra_claims = []
    
    # Case 2: Pure role users (HR, HOP, Finance only - not supervisor, not MD)
    elif any([user_info['is_hr'], user_info['is_hop'], user_info['is_finance']]):
        union_parts = []
        
        # Add role-specific pending approvals
        if user_info['is_hr']:
            union_parts.append(f"""
                SELECT DISTINCT rc.ra_claim_id
                FROM ra_claim rc
                WHERE EXISTS (
                    SELECT 1 FROM allowance_claim ac WHERE ac.ra_claim_id = rc.ra_claim_id AND ac.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM data_card_reimbursement dcr WHERE dcr.ra_claim_id = rc.ra_claim_id AND dcr.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM furniture_rm_reimbursement frmr WHERE frmr.ra_claim_id = rc.ra_claim_id AND frmr.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM laptop_maintenance_reimbursement lmr WHERE lmr.ra_claim_id = rc.ra_claim_id AND lmr.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM mobile_bill_reimbursement mbr WHERE mbr.ra_claim_id = rc.ra_claim_id AND mbr.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM out_of_pocket_claim oop WHERE oop.ra_claim_id = rc.ra_claim_id AND oop.status = 'Pending HR Approval'
                    UNION
                    SELECT 1 FROM vehicle_cm_reimbursement vcmr WHERE vcmr.ra_claim_id = rc.ra_claim_id AND vcmr.status = 'Pending HR Approval'
                )
            """)
        
        if user_info['is_hop']:
            union_parts.append(f"""
                SELECT DISTINCT rc.ra_claim_id
                FROM ra_claim rc
                WHERE EXISTS (
                    SELECT 1 FROM allowance_claim ac WHERE ac.ra_claim_id = rc.ra_claim_id AND ac.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM data_card_reimbursement dcr WHERE dcr.ra_claim_id = rc.ra_claim_id AND dcr.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM furniture_rm_reimbursement frmr WHERE frmr.ra_claim_id = rc.ra_claim_id AND frmr.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM laptop_maintenance_reimbursement lmr WHERE lmr.ra_claim_id = rc.ra_claim_id AND lmr.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM mobile_bill_reimbursement mbr WHERE mbr.ra_claim_id = rc.ra_claim_id AND mbr.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM out_of_pocket_claim oop WHERE oop.ra_claim_id = rc.ra_claim_id AND oop.status = 'Pending HOP Approval'
                    UNION
                    SELECT 1 FROM vehicle_cm_reimbursement vcmr WHERE vcmr.ra_claim_id = rc.ra_claim_id AND vcmr.status = 'Pending HOP Approval'
                )
            """)
        
        if user_info['is_finance']:
            union_parts.append(f"""
                SELECT DISTINCT rc.ra_claim_id
                FROM ra_claim rc
                WHERE EXISTS (
                    SELECT 1 FROM allowance_claim ac WHERE ac.ra_claim_id = rc.ra_claim_id AND ac.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM data_card_reimbursement dcr WHERE dcr.ra_claim_id = rc.ra_claim_id AND dcr.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM furniture_rm_reimbursement frmr WHERE frmr.ra_claim_id = rc.ra_claim_id AND frmr.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM laptop_maintenance_reimbursement lmr WHERE lmr.ra_claim_id = rc.ra_claim_id AND lmr.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM mobile_bill_reimbursement mbr WHERE mbr.ra_claim_id = rc.ra_claim_id AND mbr.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM out_of_pocket_claim oop WHERE oop.ra_claim_id = rc.ra_claim_id AND oop.status = 'Pending Finance Approval'
                    UNION
                    SELECT 1 FROM vehicle_cm_reimbursement vcmr WHERE vcmr.ra_claim_id = rc.ra_claim_id AND vcmr.status = 'Pending Finance Approval'
                )
            """)
        
        if union_parts:
            union_query = " UNION ".join(union_parts)
            final_query = f"""
                SELECT DISTINCT
                    rc.*,
                    CASE
                        WHEN rc.claim_module = 'Allowance' THEN 'ALLOWANCE'
                        ELSE 'RA'
                    END AS module
                FROM ra_claim rc
                WHERE rc.ra_claim_id IN ({union_query})
                ORDER BY rc.updated_at DESC NULLS LAST
            """
            ra_claims = db.execute(text(final_query), params).mappings().all()
        else:
            ra_claims = []
    
    # Case 3: Regular employee - only their own claims (any status)
    else:
        ra_claims = db.execute(
            text("""
                SELECT DISTINCT
                    rc.*,
                    CASE
                        WHEN rc.claim_module = 'Allowance' THEN 'ALLOWANCE'
                        ELSE 'RA'
                    END AS module
                FROM ra_claim rc
                WHERE rc.created_by = :user_id
                ORDER BY rc.updated_at DESC NULLS LAST
            """),
            {"user_id": user_id}
        ).mappings().all()
    
    # Get role-based user IDs for frontend
    def role_users(role_id):
        return db.execute(
            text("""
                SELECT DISTINCT user_id
                FROM role_permissions
                WHERE submenu_id = 12 AND role_id = :rid
            """),
            {"rid": role_id}
        ).scalars().all()
    
    hr_ids = role_users(7)
    finance_ids = role_users(11)
    md_ids = role_users(10)
    hop_ids = role_users(3)
    
    # Build response
    data = []
    for c in ra_claims:
        record = dict(c)
        
        # Get the actual status from child tables for the response
        status_result = db.execute(
            text("""
                SELECT COALESCE(
                    (SELECT status FROM allowance_claim WHERE ra_claim_id = :claim_id LIMIT 1),
                    (SELECT status FROM data_card_reimbursement WHERE ra_claim_id = :claim_id LIMIT 1),
                    (SELECT status FROM furniture_rm_reimbursement WHERE ra_claim_id = :claim_id LIMIT 1),
                    (SELECT status FROM laptop_maintenance_reimbursement WHERE ra_claim_id = :claim_id LIMIT 1),
                    (SELECT status FROM mobile_bill_reimbursement WHERE ra_claim_id = :claim_id LIMIT 1),
                    (SELECT status FROM out_of_pocket_claim WHERE ra_claim_id = :claim_id LIMIT 1),
                    (SELECT status FROM vehicle_cm_reimbursement WHERE ra_claim_id = :claim_id LIMIT 1)
                ) as status
            """),
            {"claim_id": record["ra_claim_id"]}
        ).fetchone()
        
        if status_result and status_result.status:
            record["claim_status"] = status_result.status
        
        payload = build_ra_payload({
            **record,
            "claim_module": c.claim_module
        })
        record["entries"] = fetch_ra_entries(db, payload)
        
        sup = db.execute(
            text("SELECT supervisor_id FROM users WHERE user_id = :id"),
            {"id": record["created_by"]}
        ).fetchone()
        
        record["supervisor_ids"] = [sup.supervisor_id] if sup and sup.supervisor_id else []
        
        if record.get("category") == "Out of Pocket Claim":
            record["hr_ids"] = []
            record["hop_ids"] = list(hop_ids)
        else:
            record["hr_ids"] = list(hr_ids)
            record["hop_ids"] = []
        
        record["finance_ids"] = list(finance_ids)
        record["md_ids"] = list(md_ids)
        
        data.append(record)
    
    return {
        "success": True,
        "data": data
    }

@router.get("/ra-claims/history")
def get_ra_claims_history(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    # Step 1: Fetch requester
    requester = db.execute(
        text("SELECT user_id, username FROM users WHERE user_id = :id"),
        {"id": user_id}
    ).fetchone()

    if not requester:
        raise HTTPException(status_code=404, detail="User not found")

    requester_id = requester.user_id
    requester_username = requester.username

    # Step 2: Detect roles (Priority order is important)
    is_admin = db.execute(
        text("""
            SELECT 1 FROM role_permissions 
            WHERE user_id = :uid AND submenu_id = 12 AND role_id = 4 LIMIT 1
        """),
        {"uid": requester_id}
    ).fetchone() is not None

    is_hr = db.execute(
        text("""
            SELECT 1 FROM role_permissions 
            WHERE user_id = :uid AND submenu_id = 12 AND role_id = 7 LIMIT 1
        """),
        {"uid": requester_id}
    ).fetchone() is not None

    is_finance = db.execute(
        text("""
            SELECT 1 FROM role_permissions 
            WHERE user_id = :uid AND submenu_id = 12 AND role_id = 11 LIMIT 1
        """),
        {"uid": requester_id}
    ).fetchone() is not None

    is_supervisor = db.execute(
        text("""
            SELECT 1 FROM users 
            WHERE supervisor_id = :uid AND user_id != :uid LIMIT 1
        """),
        {"uid": requester_id}
    ).fetchone() is not None

    is_md = db.execute(
        text("""
            SELECT 1 FROM role_permissions 
            WHERE user_id = :uid AND submenu_id = 12 AND role_id = 10 LIMIT 1
        """),
        {"uid": requester_id}
    ).fetchone() is not None

    is_hop = db.execute(
        text("""
            SELECT 1 FROM role_permissions 
            WHERE user_id = :uid AND submenu_id = 12 AND role_id = 3 LIMIT 1
        """),
        {"uid": requester_id}
    ).fetchone() is not None

    # Step 3: Fetch claims with proper priority
    if is_admin or is_hr or is_finance:
        # 🔥 These roles see EVERYTHING (including their own)
        ra_claims = db.execute(
            text("""
                SELECT *, 
                       CASE WHEN claim_module = 'Allowance' THEN 'ALLOWANCE' ELSE 'RA' END AS module
                FROM ra_claim 
                ORDER BY updated_at DESC NULLS LAST
            """)
        ).mappings().all()

    else:
        # Restricted users
        claim_ids = set()

        # Supervisor → ONLY subordinates' claims (NO own claims)
        if is_supervisor:
            rows = db.execute(
                text("""
                    SELECT DISTINCT rc.ra_claim_id
                    FROM ra_claim rc
                    JOIN users u ON u.user_id = rc.created_by
                    WHERE u.supervisor_id = :supervisor_id
                """),
                {"supervisor_id": requester_id}
            ).scalars().all()
            claim_ids.update(rows)

        # HOP logic
        if is_hop:
            rows = db.execute(
                text("""
                    SELECT DISTINCT rc.ra_claim_id
                    FROM ra_claim rc
                    JOIN out_of_pocket_claim opc ON opc.ra_claim_id = rc.ra_claim_id
                    WHERE opc.updated_by_hop_name = :username
                """),
                {"username": requester_username}
            ).scalars().all()
            claim_ids.update(rows)

        # MD logic
        if is_md:
            rows = db.execute(
                text("""
                    SELECT DISTINCT ra_claim_id 
                    FROM ra_claim 
                    WHERE updated_by = :md_id
                """),
                {"md_id": requester_id}
            ).scalars().all()
            claim_ids.update(rows)

        if claim_ids:
            ra_claims = db.execute(
                text("""
                    SELECT *, 
                           CASE WHEN claim_module = 'Allowance' THEN 'ALLOWANCE' ELSE 'RA' END AS module
                    FROM ra_claim 
                    WHERE ra_claim_id IN :ids
                    ORDER BY updated_at DESC NULLS LAST
                """),
                {"ids": tuple(claim_ids)}
            ).mappings().all()
        else:
            ra_claims = []

    # ====================== Rest of the function (unchanged) ======================
    def role_users(role_id: int):
        return db.execute(
            text("""
                SELECT DISTINCT user_id 
                FROM role_permissions 
                WHERE submenu_id = 12 AND role_id = :rid
            """),
            {"rid": role_id}
        ).scalars().all()

    hr_ids = role_users(7)
    finance_ids = role_users(11)
    md_ids = role_users(10)
    hop_ids = role_users(3)

    data = []
    for c in ra_claims:
        record = dict(c)
        payload = build_ra_payload({
            **record,
            "claim_module": c.claim_module
        })
        record["entries"] = fetch_ra_entries(db, payload)

        # Supervisor of the employee who created the claim
        sup = db.execute(
            text("SELECT supervisor_id FROM users WHERE user_id = :id"),
            {"id": record["created_by"]}
        ).fetchone()

        record["supervisor_ids"] = [sup.supervisor_id] if sup and sup.supervisor_id else []

        if record.get("category") == "Out of Pocket Claim":
            record["hr_ids"] = []
            record["hop_ids"] = list(hop_ids)
        else:
            record["hr_ids"] = list(hr_ids)
            record["hop_ids"] = []

        record["finance_ids"] = list(finance_ids)
        record["md_ids"] = list(md_ids)

        data.append(record)

    return {
        "success": True,
        "data": data
    }


@router.get("/ra-claims/cards")
def get_ra_claim_cards(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    # -------------------------------------------------
    # 1️⃣ USER VALIDATION
    # -------------------------------------------------
    exists = db.execute(
        sql_text("SELECT 1 FROM users WHERE user_id = :id"),
        {"id": user_id}
    ).fetchone()

    if not exists:
        raise HTTPException(status_code=404, detail="User not found")

    # -------------------------------------------------
    # 2️⃣ TOTAL CLAIM COUNT (RA + ALLOWANCE)
    # -------------------------------------------------
    total_claims = db.execute(
        sql_text("""
            SELECT
                (
                    SELECT COUNT(*)
                    FROM ra_claim
                    WHERE created_by = :id
                )
                +
                (
                    SELECT COUNT(*)
                    FROM allowance_claim
                    WHERE created_by = :id
                ) AS total_claims
        """),
        {"id": user_id}
    ).scalar()

    # -------------------------------------------------
    # 3️⃣ APPROVED & PENDING (RA + ALLOWANCE STATUS)
    # -------------------------------------------------
    status_counts = db.execute(
        sql_text("""
            SELECT
                COUNT(*) FILTER (
                    WHERE status ILIKE '%approved%'
                ) AS approved,

                COUNT(*) FILTER (
                    WHERE status ILIKE '%pending%'
                ) AS pending
            FROM (
                SELECT status
                FROM ra_claim
                WHERE created_by = :id

                UNION ALL

                SELECT status
                FROM allowance_claim
                WHERE created_by = :id
            ) t
        """),
        {"id": user_id}
    ).mappings().one()

    # -------------------------------------------------
    # 4️⃣ TOTAL CLAIMED AMOUNT (ALL MODULES)
    # -------------------------------------------------
    total_claimed = db.execute(
        sql_text("""
            SELECT COALESCE(SUM(amount), 0)
            FROM (
                SELECT total_claimed_amount AS amount
                FROM mobile_bill_reimbursement
                WHERE created_by = :id

                UNION ALL
                SELECT amount_claimed
                FROM laptop_maintenance_reimbursement
                WHERE created_by = :id

                UNION ALL
                SELECT bill_amount
                FROM data_card_reimbursement
                WHERE created_by = :id

                UNION ALL
                SELECT amount_claimed
                FROM furniture_rm_reimbursement
                WHERE created_by = :id

                UNION ALL
                SELECT fuel_claim_amount + maintenance_claim_amount
                FROM vehicle_cm_reimbursement
                WHERE created_by = :id

                UNION ALL
                SELECT total_amount
                FROM out_of_pocket_claim
                WHERE created_by = :id

                UNION ALL
                SELECT grand_total
                FROM allowance_claim
                WHERE created_by = :id
            ) t
        """),
        {"id": user_id}
    ).scalar()

    # -------------------------------------------------
    # 5️⃣ RESPONSE
    # -------------------------------------------------
    return {
        "success": True,
        "data": {
            "total_claims": total_claims,
            "approved": status_counts["approved"],
            "pending": status_counts["pending"],
            "total_claimed": float(total_claimed)
        }
    }



@router.get("/encashment-cards")
def get_el_balance(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    # -------------------------------------------------
    # 1. Fetch EL leave type IDs
    # -------------------------------------------------
    leave_types = {
        r.code.lower(): r.type_id
        for r in db.execute(text("SELECT type_id, code FROM leave_types"))
    }

    if "el_e" not in leave_types or "el_ne" not in leave_types:
        raise HTTPException(
            status_code=500,
            detail="EL_E / EL_NE leave types not configured"
        )

    EL_E = leave_types["el_e"]
    EL_NE = leave_types["el_ne"]

    # -------------------------------------------------
    # 2. Allocated EL (Decimal)
    # -------------------------------------------------
    alloc = db.execute(text("""
        SELECT
            COALESCE(SUM(CASE WHEN type_id = :enc THEN allocated ELSE 0 END), 0) AS enc,
            COALESCE(SUM(CASE WHEN type_id = :non THEN allocated ELSE 0 END), 0) AS non
        FROM leave_balances
        WHERE user_id = :uid
    """), {
        "uid": user_id,
        "enc": EL_E,
        "non": EL_NE
    }).mappings().first()

    alloc_enc = Decimal(alloc["enc"] or 0)
    alloc_non = Decimal(alloc["non"] or 0)

    # -------------------------------------------------
    # 3. Used EL (Decimal)
    # -------------------------------------------------
    used = Decimal(db.execute(text("""
        SELECT COALESCE(SUM(number_of_days), 0)
        FROM hr_leave_application
        WHERE user_id = :uid
          AND leave_type = 'EL'
          AND LOWER(status) IN (
              'approved',
              'reversal approved',
              'withdraw rejected'
          )
    """), {"uid": user_id}).scalar() or 0)

    # -------------------------------------------------
    # 4. Encashed EL (Decimal)
    # -------------------------------------------------
    encashed = Decimal(db.execute(text("""
    SELECT COALESCE(SUM(le.encash_el), 0)
    FROM leave_encashment le
    JOIN encashment_main em
      ON em.encashment_main_id = le.encashment_main_id
    WHERE em.created_by = :uid
      AND NOT (
            le.status ILIKE '%rejected%'
         OR le.status ILIKE '%cancelled%'
      )
"""), {"uid": user_id}).scalar() or 0)



    # -------------------------------------------------
    # 4.1 Total Amount Claimed (Decimal)
    # -------------------------------------------------
    total_amount_claimed = Decimal(db.execute(text("""
    SELECT COALESCE(SUM(le.amount_claimed), 0)
    FROM leave_encashment le
    JOIN encashment_main em
      ON em.encashment_main_id = le.encashment_main_id
    WHERE em.created_by = :uid
      AND NOT (
            le.status ILIKE '%rejected%'
         OR le.status ILIKE '%cancelled%'
      )
"""), {"uid": user_id}).scalar() or 0)



    # -------------------------------------------------
    # 5. Final EL Calculation (Decimal-safe)
    # -------------------------------------------------
    total_alloc = alloc_enc + alloc_non
    total_deduct = used + encashed

    remaining = total_alloc - total_deduct
    if remaining < 0:
        remaining = Decimal("0")

    # Proportional split
    if total_alloc > 0:
        enc_ratio = alloc_enc / total_alloc
    else:
        enc_ratio = Decimal("0")

    el_enc = (remaining * enc_ratio).quantize(Decimal("1"))
    el_non = remaining - el_enc

    # Auto-adjust negatives
    if el_enc < 0:
        el_non += el_enc
        el_enc = Decimal("0")

    if el_non < 0:
        el_enc += el_non
        el_non = Decimal("0")

    # -------------------------------------------------
    # 6. Response
    # -------------------------------------------------
    return {
        "user_id": user_id,
        "el_encashable": int(el_enc),
        "el_non_encashable": int(el_non),
        "total_el": int(el_enc + el_non),
         "total_amount_claimed": float(total_amount_claimed)
    }


from datetime import datetime, date, timedelta



@router.get("/furniture-claim-sum")
def get_furniture_claim_sum(
    month_year: str,
    user_id: int,
    db: Session = Depends(get_db)
    ):
    try:
        parsed_date = datetime.strptime(month_year, "%Y-%m")

        # Detect current FY start
        if parsed_date.month >= 4:
            current_fy_start = date(parsed_date.year, 4, 1)
        else:
            current_fy_start = date(parsed_date.year - 1, 4, 1)

        # All previous FYs = anything before current FY start
        # No lower bound — include everything historically
        all_previous_fy_end = current_fy_start - timedelta(days=1)  # last day of previous FY

        result = db.execute(
            text("""
                SELECT 
                    COALESCE(SUM(acs.claim_amount), 0) AS total_furniture_claim
                FROM asset_claim_submission acs
                JOIN asset_claim ac
                    ON ac.asset_claim_id = acs.asset_claim_id
                WHERE 
                    ac.category = 'Furniture'
                    AND acs.status IN ( 
                        'Asset Claim Disbursed'
                    )
                    AND acs.created_by = :user_id
                    AND acs.created_at::date < :current_fy_start
            """),
            {
                "user_id": user_id,
                "current_fy_start": current_fy_start,
            }
        ).fetchone()

        total_claim = float(result.total_furniture_claim)
        eligible_amount = round(total_claim * 0.15, 2)

        return {
            "user_id": user_id,
            "all_previous_financial_years_up_to": all_previous_fy_end,
            "current_financial_year_start": current_fy_start,
            "total_furniture_claim": total_claim,
            "eligible_amount": eligible_amount
        }

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid month_year format. Use YYYY-MM"
        )
