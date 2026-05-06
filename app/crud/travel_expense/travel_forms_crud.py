from decimal import Decimal
from fastapi import logger
import os
import shutil
import json
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
 

from app.routers.UserAuthR2 import make_download_url

# -----------------------------------------
# GET SELF FORMS (USER ONLY)
# -----------------------------------------

# def get_self_travel_by_user_id(db: Session, user_id: int):

#     q1 = text("""
#         SELECT *
#         FROM travel_requisition
#         WHERE user_id = :uid
#         ORDER BY created_at DESC
#     """)

#     q2 = text("""
#         SELECT *
#         FROM daily_allowance_sheet
#         WHERE user_id = :uid
#         ORDER BY created_at DESC
#     """)

#     q3 = text("""
#         SELECT *
#         FROM meal_allowance_sheet
#         WHERE user_id = :uid
#         ORDER BY created_at DESC
#     """)

#     q4 = text("""
#         SELECT *
#         FROM travel_expense_sheet
#         WHERE user_id = :uid
#         ORDER BY created_at DESC
#     """)


#     forms = []

#     # travel requisition
#     for row in db.execute(q1, {"uid": user_id}).mappings():
#         data = dict(row)
#         data["form_type"] = "Travel Requisition"
#         sup_id, sup_name = fetch_supervisor(db, data["user_id"])
#         data["supervisor_id"] = sup_id
#         data["supervisor_name"] = sup_name
#         forms.append({"data": data})

#     # daily allowance
#     for row in db.execute(q2, {"uid": user_id}).mappings():
#         data = dict(row)
#         data["form_type"] = "Daily Allowance"
#         sup_id, sup_name = fetch_supervisor(db, data["user_id"])
#         data["supervisor_id"] = sup_id
#         data["supervisor_name"] = sup_name
#         forms.append({"data": data})

#     # meal allowance
#     for row in db.execute(q3, {"uid": user_id}).mappings():
#         data = dict(row)
#         data["form_type"] = "Meal Allowance"
#         sup_id, sup_name = fetch_supervisor(db, data["user_id"])
#         data["supervisor_id"] = sup_id
#         data["supervisor_name"] = sup_name
#         forms.append({"data": data})

# # travel expense
#     for row in db.execute(q4, {"uid": user_id}).mappings():
#         data = dict(row)
#         data["form_type"] = "Travel Expense"
#         data["form_id"] = data["tes_id"]  # 🔥 FIX
#         sup_id, sup_name = fetch_supervisor(db, data["user_id"])
#         data["supervisor_id"] = sup_id
#         data["supervisor_name"] = sup_name
#         forms.append({"data": data})

#     from datetime import datetime

#     forms.sort(
#         key=lambda x: (
#             x["created_at"] if x.get("created_at") is not None else datetime.min,
#             x.get("id", 0)
#         ),
#         reverse=True
#     ) 
#     return forms

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime


def get_self_travel_by_user_id(db: Session, user_id: int):

    q1 = text("""
        SELECT *
        FROM travel_requisition
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """)

    q2 = text("""
        SELECT *
        FROM daily_allowance_sheet
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """)

    q3 = text("""
        SELECT *
        FROM meal_allowance_sheet
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """)

    q4 = text("""
        SELECT *
        FROM travel_expense_sheet
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """)

    forms = []

    # travel requisition
    for row in db.execute(q1, {"uid": user_id}).mappings():
        data = dict(row)
        data["form_type"] = "Travel Requisition"
        sup_id, sup_name = fetch_supervisor(db, data["user_id"])
        data["supervisor_id"] = sup_id
        data["supervisor_name"] = sup_name
        forms.append({"data": data})

    # daily allowance
    for row in db.execute(q2, {"uid": user_id}).mappings():
        data = dict(row)
        data["form_type"] = "Daily Allowance"
        sup_id, sup_name = fetch_supervisor(db, data["user_id"])
        data["supervisor_id"] = sup_id
        data["supervisor_name"] = sup_name
        forms.append({"data": data})

    # meal allowance
    for row in db.execute(q3, {"uid": user_id}).mappings():
        data = dict(row)
        data["form_type"] = "Meal Allowance"
        sup_id, sup_name = fetch_supervisor(db, data["user_id"])
        data["supervisor_id"] = sup_id
        data["supervisor_name"] = sup_name
        forms.append({"data": data})

    # travel expense
    for row in db.execute(q4, {"uid": user_id}).mappings():
        data = dict(row)
        data["form_type"] = "Travel Expense"
        data["form_id"] = data["tes_id"]  # 🔥 FIX (unchanged)
        sup_id, sup_name = fetch_supervisor(db, data["user_id"])
        data["supervisor_id"] = sup_id
        data["supervisor_name"] = sup_name
        forms.append({"data": data})

    # =====================================================
    # ✅ GLOBAL SORT BY created_at (ONLY ADDITION)
    # =====================================================
    forms.sort(
        key=lambda x: x["data"].get("created_at") or datetime.min,
        reverse=True
    )

    return forms



from sqlalchemy import text
from sqlalchemy.orm import Session

def get_travel_for_supervisor(db: Session, supervisor_id: int):

    approvers = get_rolewise_users(db)

    # Get supervised users
    user_query = text("""
      SELECT user_id
    FROM users
    WHERE supervisor_id = :sid
    ORDER BY created_date DESC
    """)
    user_ids = [row[0] for row in db.execute(user_query, {"sid": supervisor_id})]

    if not user_ids:
        return {
            "forms": [],
            "form_ids": {}
        }

    forms = []
    form_ids = {
        "Travel Requisition": [],
        "Daily Allowance": [],
        "Meal Allowance": [],
        "Travel Expense": []
    }

    queries = [
    (
        "Travel Requisition",
        text("""
            SELECT *
            FROM travel_requisition
            WHERE user_id = ANY(:uids)
            ORDER BY created_at DESC
        """)
    ),
    (
        "Daily Allowance",
        text("""
            SELECT *
            FROM daily_allowance_sheet
            WHERE user_id = ANY(:uids)
            ORDER BY created_at DESC
        """)
    ),
    (
        "Meal Allowance",
        text("""
            SELECT *
            FROM meal_allowance_sheet
            WHERE user_id = ANY(:uids)
            ORDER BY created_at DESC
        """)
    ),
    (
        "Travel Expense",
        text("""
            SELECT *
            FROM travel_expense_sheet
            WHERE user_id = ANY(:uids)
            ORDER BY created_at DESC
        """)
    ),
]


    params = {"uids": user_ids}

    for form_type, query in queries:
        for row in db.execute(query, params).mappings():
            d = dict(row)
            d["form_type"] = form_type

            # Approvers
            d["hr"] = approvers["hr"]
            d["finance"] = approvers["finance"]
            d["md"] = approvers["md"]

            # Supervisor details
            sup_id, sup_name = fetch_supervisor(db, d["user_id"])
            d["supervisor_id"] = sup_id
            d["supervisor_name"] = sup_name

            # Collect IDs
            if "id" in d:
                form_ids[form_type].append(d["id"])

            forms.append(d)

    # Sort by created_at DESC
    from datetime import datetime

    forms.sort(
        key=lambda x: (
            x["created_at"] if x.get("created_at") is not None else datetime.min,
            x.get("id", 0)
        ),
        reverse=True
    ) 
    return {
        "forms": forms,
        "form_ids": form_ids
    }



# -------------------------------------------------------------------
# SUPERVISOR LOOKUP
# -------------------------------------------------------------------
def get_supervisor_id(db: Session, user_id: int):
    sql = text("SELECT supervisor_id FROM users WHERE user_id = :uid")
    row = db.execute(sql, {"uid": user_id}).mappings().first()
    return row["supervisor_id"] if row else None


# -------------------------------------------------------------------
# ROLEWISE USERS
# -------------------------------------------------------------------
def get_rolewise_users(db: Session):
    sql = text("""
        SELECT DISTINCT user_id, role_id
        FROM role_permissions
        WHERE submenu_id = :submenu_id
          AND role_id IN (7, 10, 11, 15)
          AND user_id IS NOT NULL
    """)

    rows = db.execute(sql, {"submenu_id": 11}).mappings().all()

    grouped = {
        "hr": [],
        "md": [],
        "finance": [],
        "head_tech": []
    }

    for row in rows:
        user_id = row["user_id"]
        role_id = row["role_id"]

        if role_id == 7:
            grouped["hr"].append(user_id)
        elif role_id == 10:
            grouped["md"].append(user_id)
        elif role_id == 11:
            grouped["finance"].append(user_id)
        elif role_id == 15:
            grouped["head_tech"].append(user_id)

    return grouped
# -------------------------------------------------------------------
# GET ALL TRAVEL FORMS WITH SUPERVISOR_ID + SORTED BY created_on
# -------------------------------------------------------------------
def get_all_travel_forms(db: Session):

    approvers = get_rolewise_users(db)

    forms = []
    q1 = text("""
        SELECT *
        FROM travel_requisition
        ORDER BY created_at DESC
    """)

    q2 = text("""
        SELECT *
        FROM daily_allowance_sheet
        ORDER BY created_at DESC
    """)

    q3 = text("""
        SELECT *
        FROM meal_allowance_sheet
        ORDER BY created_at DESC
    """)

    q4 = text("""
        SELECT *
        FROM travel_expense_sheet
        ORDER BY created_at DESC
    """)


    queries = [
        (q1, "Travel Requisition"),
        (q2, "Daily Allowance"),
        (q3, "Meal Allowance"),
        (q4, "Travel Expense")
    ]

    for query, form_type in queries:
        for row in db.execute(query).mappings():
            d = dict(row)
            d["form_type"] = form_type

            # Add approvers
            d["hr"] = approvers["hr"]
            d["finance"] = approvers["finance"]
            d["md"] = approvers["md"]
            d["head_tech"] = approvers["head_tech"]
            # Add supervisor_id
            user_id = d.get("user_id")
            d["supervisor_id"] = get_supervisor_id(db, user_id)
            sup_id, sup_name = fetch_supervisor(db, d["user_id"])
            d["supervisor_name"] = sup_name
            forms.append(d)

    # Sort all forms by created_on DESC (newest first)
    forms.sort(key=lambda x: x.get("created_at"), reverse=True)

    return {"forms": forms}



def get_global_dashboard_summary(db):
    tables = [
        "daily_allowance_sheet",
        "meal_allowance_sheet",
        "travel_expense_sheet",
    ]

    pending = 0
    approved = 0
    changes_requested = 0
    total_amount = Decimal("0.00")

    for table in tables:
        q = text(f"""
            SELECT status, total_incl_gst
            FROM {table}
        """)

        rows = db.execute(q).mappings()

        for row in rows:
            status = (row["status"] or "").lower()
            amount = row["total_incl_gst"] or 0

            if "pending" in status:
                pending += 1
                total_amount += Decimal(amount)


            elif "approved" in status or "completed" in status:
                approved += 1
                total_amount += Decimal(amount)

            elif "change" in status:
                changes_requested += 1
                total_amount += Decimal(amount)


    return {
        "pending_claims": pending,
        "approved_claims": approved,
        "changes_requested": changes_requested,
        "total_amount": float(total_amount),
    }




from sqlalchemy import text
from decimal import Decimal

from sqlalchemy import text

def get_global_dashboard_summary(db):
    # --------------------------------------------------
    # 1. STATUS COUNTS (unchanged, safe)
    # --------------------------------------------------
    tables = [
        "travel_requisition",
        "daily_allowance_sheet",
        "meal_allowance_sheet",
        "travel_expense_sheet",
    ]

    pending = 0
    approved = 0
    changes_requested = 0

    for table in tables:
        q = text(f"""
            SELECT status
            FROM {table}
            WHERE status IS NOT NULL
        """)
        rows = db.execute(q).mappings()

        for row in rows:
            status = row["status"].lower()

            if "approved" in status:
                approved += 1
            elif "changes request" in status:
                changes_requested += 1
            elif "pending" in status:
                pending += 1

    # --------------------------------------------------
    # 2. TOTAL AMOUNT (ALL RECORDS, NO FILTER)
    # --------------------------------------------------
    total_query = text("""
        SELECT COALESCE(SUM(total_incl_gst), 0) AS grand_total
        FROM (
            SELECT total_incl_gst FROM travel_expense_sheet
            UNION ALL
            SELECT total_incl_gst FROM daily_allowance_sheet
            UNION ALL
            SELECT total_incl_gst FROM meal_allowance_sheet
        ) t
    """)

    total_amount = db.execute(total_query).scalar() or 0

    return {
        "pending_claims": pending,
        "approved_claims": approved,
        "changes_requested": changes_requested,
        "total_amount": float(total_amount),
    }

# -------------------------------------------------------------------
# SQL CONFIG FOR SINGLE FORM VIEW
# -------------------------------------------------------------------
SQL_CONFIG = {
    "travel_requisition": {
        "main": """
            SELECT *
            FROM travel_requisition
            WHERE travel_id = :form_id
            ORDER BY created_at
        """,
        "children": {
            "travels": """
                SELECT *
                FROM travel_requisition_travel
                WHERE requisition_id = :form_id
                ORDER BY created_at
            """,
            "hotels": """
                SELECT *
                FROM travel_requisition_hotel
                WHERE requisition_id = :form_id
                ORDER BY created_at
            """,
            "cars": """
                SELECT *
                FROM travel_requisition_car
                WHERE requisition_id = :form_id
                ORDER BY created_at
            """
        }
    },

    "daily_allowance": {
        "main": """
            SELECT *
            FROM daily_allowance_sheet
            WHERE da_sheet_id = :form_id
            ORDER BY created_at
        """,
        "children": {
            "entries": """
                SELECT *
                FROM daily_allowance_sheet_detail
                WHERE da_sheet_id = :form_id
                ORDER BY created_at
            """
        }
    },

    "meal_allowance": {
        "main": """
            SELECT *
            FROM meal_allowance_sheet
            WHERE meal_sheet_id = :form_id
            ORDER BY created_at
        """,
        "children": {
            "entries": """
                SELECT *
                FROM meal_allowance_sheet_detail
                WHERE meal_sheet_id = :form_id
                ORDER BY created_at
            """
        }
    },

   "travel_expense": {
    "main": """
        SELECT
            tes.*,
            tes.travel_id
        FROM travel_expense_sheet tes
        WHERE tes.tes_id = :form_id
        ORDER BY tes.created_at
    """,

        "children": {
            "expense_details": """
                SELECT *
                FROM travel_expense_sheet_detail
                WHERE expense_sheet_id = :form_id
                ORDER BY created_at
            """
        }
    }
}

# All possible file fields across all modules
DOWNLOADABLE_FIELDS = {
    "da_proof",
    "meal_proof",
    "air_rail_bus_proof",
    "hotel_proof",
    "daily_allowance_proof",
    "local_conveyance_proof",
    "other_proof",
}
def convert_download_fields(record: dict) -> dict:
    """
    Converts all known proof fields into downloadable links.
    Handles:
      - None
      - Single file
      - Multiple comma-separated files
    """

    for key, value in record.items():
        if key not in DOWNLOADABLE_FIELDS:
            continue

        if not value or str(value).lower() in ("none", "null", ""):
            record[key] = None
            continue

        # Multiple files: a,b,c
        parts = [p.strip() for p in str(value).split(",") if p.strip()]
        urls = [make_download_url(p) for p in parts]

        # If only one file → return string
        # If multiple → return list
        record[key] = urls[0] if len(urls) == 1 else urls

    return record

def normalize_form_type(form_type: str) -> str:
    """
    Converts frontend form_type into backend canonical key.
    Handles typos & variations safely.
    """
    if not form_type:
        return ""

    ft = (
        form_type
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

    aliases = {
        "travel_requestion": "travel_requisition",
        "travel_reqiesion": "travel_requisition",
        "travel_requisition": "travel_requisition",

        "daily_allowance": "daily_allowance",
        "daily_allowance_sheet": "daily_allowance",

        "meal_allowance": "meal_allowance",
        "meal_allowance_sheet": "meal_allowance",

        "travel_expense": "travel_expense",
        "travel_expense_sheet": "travel_expense",
    }

    return aliases.get(ft, ft)
# -------------------------------------------------------------------
# GET SINGLE FORM DETAILS WITH CHILDREN + SUPERVISOR_ID
# -------------------------------------------------------------------
def get_form_details(db: Session, form_type: str, form_id: int):
    normalized_form_type = normalize_form_type(form_type)

    if normalized_form_type not in SQL_CONFIG:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid form_type: {form_type}"
        )

    config = SQL_CONFIG[normalized_form_type]
    
    # MAIN RECORD
    main_row = db.execute(
        text(config["main"]),
        {"form_id": form_id}
    ).mappings().first()

    if not main_row:
        return None

    main_data = convert_download_fields(dict(main_row))

    # CHILD RECORDS
    children = {}
    for key, sql in config["children"].items():
        rows = db.execute(
            text(sql),
            {"form_id": form_id}
        ).mappings().all()

        children[key] = [
            convert_download_fields(dict(r)) for r in rows
        ]

    return {
        "form_type": normalized_form_type,
        "form_id": form_id,
        "main": main_data,
        "children": children
    }
FORM_ID_COLUMN = {
    "travel_requisition": "travel_id",
    "daily_allowance": "da_sheet_id",
    "meal_allowance": "meal_sheet_id",
    "travel_expense": "tes_id",
}


def get_dashboard_summary(db, user_id: int):

    def fetch(sql):
        result = db.execute(text(sql), {"uid": user_id}).mappings().first()
        return result or {}

    # -------------------------
    # TRAVEL REQUISITION
    # -------------------------
    tr_sql = """
        SELECT
            SUM(CASE WHEN status LIKE '%Approved%' THEN 1 ELSE 0 END) AS approved,
            SUM(CASE WHEN status LIKE '%Changes Request%' THEN 1 ELSE 0 END) AS changes,
            SUM(CASE WHEN status LIKE '%Pending%' THEN 1 ELSE 0 END) AS pending
        FROM travel_requisition
        WHERE user_id = :uid
    """
    tr = fetch(tr_sql)

    # -------------------------
    # DAILY ALLOWANCE
    # -------------------------
    da_sql = """
        SELECT
            SUM(CASE WHEN status LIKE '%Approved%' THEN 1 ELSE 0 END) AS approved,
            SUM(CASE WHEN status LIKE '%Changes Request%' THEN 1 ELSE 0 END) AS changes,
            SUM(CASE WHEN status LIKE '%Approved%'
                     THEN total_incl_gst ELSE 0 END) AS changes_amount,
            SUM(CASE WHEN status LIKE '%Pending%' THEN 1 ELSE 0 END) AS pending
        FROM daily_allowance_sheet
        WHERE user_id = :uid
    """
    da = fetch(da_sql)

    # -------------------------
    # MEAL ALLOWANCE
    # -------------------------
    ma_sql = """
        SELECT
            SUM(CASE WHEN status LIKE '%Approved%' THEN 1 ELSE 0 END) AS approved,
            SUM(CASE WHEN status LIKE '%Changes Request%' THEN 1 ELSE 0 END) AS changes,
            SUM(CASE WHEN status LIKE '%Approved%'
                     THEN total_incl_gst ELSE 0 END) AS changes_amount,
            SUM(CASE WHEN status LIKE '%Pending%' THEN 1 ELSE 0 END) AS pending
        FROM meal_allowance_sheet
        WHERE user_id = :uid
    """
    ma = fetch(ma_sql)

    # -------------------------
    # TRAVEL EXPENSE
    # -------------------------
    te_sql = """
        SELECT
            SUM(CASE WHEN status LIKE '%Approved%' THEN 1 ELSE 0 END) AS approved,
            SUM(CASE WHEN status LIKE '%Changes Request%' THEN 1 ELSE 0 END) AS changes,
            SUM(CASE WHEN status LIKE '%Approved%'
                     THEN total_incl_gst ELSE 0 END) AS changes_amount,
            SUM(CASE WHEN status LIKE '%Pending%' THEN 1 ELSE 0 END) AS pending
        FROM travel_expense_sheet
        WHERE user_id = :uid
    """
    te = fetch(te_sql)

    # -------------------------
    # SAFE VALUE EXTRACTION
    # -------------------------
    def safe(val, key):
        return val.get(key) or 0

    # -------------------------
    # FINAL AGGREGATION
    # -------------------------
    final_response = {
        "total_pending": (
            safe(tr, "pending") +
            safe(da, "pending") +
            safe(ma, "pending") +
            safe(te, "pending")
        ),
        "total_approved": (
            safe(tr, "approved") +
            safe(da, "approved") +
            safe(ma, "approved") +
            safe(te, "approved")
        ),
        "total_changes_requested": (
            safe(tr, "changes") +
            safe(da, "changes") +
            safe(ma, "changes") +
            safe(te, "changes")
        ),
        "total_changes_requested_amount": (
            safe(da, "changes_amount") +
            safe(ma, "changes_amount") +
            safe(te, "changes_amount")
        )
    }

    return final_response




def fetch_supervisor(db: Session, user_id: int):
    sql = text("""
        SELECT 
            u2.user_id AS supervisor_id,
            u2.first_name AS supervisor_first_name,
            u2.last_name AS supervisor_last_name
        FROM users u1
        LEFT JOIN users u2 ON u1.supervisor_id = u2.user_id
        WHERE u1.user_id = :uid
    """)
    row = db.execute(sql, {"uid": user_id}).mappings().first()

    if not row or not row["supervisor_id"]:
        return None, None

    full = f"{row['supervisor_first_name']} {row['supervisor_last_name']}".strip()
    return row["supervisor_id"], full


