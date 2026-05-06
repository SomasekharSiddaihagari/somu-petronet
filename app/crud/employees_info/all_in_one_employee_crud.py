from sqlalchemy import text
from sqlalchemy.orm import Session

from app.routers.UserAuthR2 import make_download_url


def get_user_basic_info(db: Session, user_id: int):
    row = db.execute(text("""
        SELECT employee_code, first_name, last_name
        FROM users WHERE user_id = :uid
    """), {"uid": user_id}).fetchone()

    return dict(row._mapping) if row else {
        "employee_code": None,
        "first_name": "",
        "last_name": ""
    }


def serialize_common(row, user, submission_type):
    
    def fix_file(path):
        if not path:
            return None
        return make_download_url(path)

    def fix_multiple(path_list):
        if not path_list:
            return None
        return [fix_file(p.strip()) for p in path_list.split(",")]

    return {
        **row,

        # USER DETAILS
        "employee_code": user.get("employee_code"),
        "employee_full_name": f"{user.get('first_name')} {user.get('last_name')}".strip(),

        # FIXED
        "submission_type": submission_type,

        # FILES
        "document": fix_multiple(row.get("document")) if row.get("document") else None,
        "upload_document": fix_multiple(row.get("upload_document")) if row.get("upload_document") else None,
        "signature": fix_file(row.get("signature")),
        "signature_name": fix_file(row.get("signature_name")),
    }





# -------------------------
# GET ALL
# -------------------------
def get_all_forms(db: Session):

    assets = db.execute(text("SELECT * FROM user_asset_declaration;")).fetchall()
    form12c = db.execute(text("SELECT * FROM employee_form_12c;")).fetchall()
    finance = db.execute(text("SELECT * FROM user_finance;")).fetchall()

    asset_list = []
    for r in assets:
        row = dict(r._mapping)
        user = get_user_basic_info(db, row["user_id"])
        asset_list.append(serialize_common(row, user, "Asset Declaration"))

    form12_list = []
    for r in form12c:
        row = dict(r._mapping)
        user = get_user_basic_info(db, row["user_id"])
        form12_list.append(serialize_common(row, user, "Form 12"))

    finance_list = []
    for r in finance:
        row = dict(r._mapping)
        user = get_user_basic_info(db, row["user_id"])
        finance_list.append(serialize_common(row, user, "Finance Declaration"))

    return {
        "form_type": "all_forms",
        "asset_declaration": asset_list,
        "employee_form_12c": form12_list,
        "user_finance": finance_list
    }


def get_forms_by_user_id(db: Session, user_id: int):

    assets = db.execute(
        text("SELECT * FROM user_asset_declaration WHERE user_id = :uid"),
        {"uid": user_id}
    ).fetchall()

    form12c = db.execute(
        text("SELECT * FROM employee_form_12c WHERE user_id = :uid"),
        {"uid": user_id}
    ).fetchall()

    finance = db.execute(
        text("SELECT * FROM user_finance WHERE user_id = :uid"),
        {"uid": user_id}
    ).fetchall()

    user = get_user_basic_info(db, user_id)

    return {
        "form_type": "all_forms",
        "asset_declaration": [
            serialize_common(dict(r._mapping), user, "Asset Declaration")
            for r in assets
        ],
        "employee_form_12c": [
            serialize_common(dict(r._mapping), user, "Form 12")
            for r in form12c
        ],
        "user_finance": [
            serialize_common(dict(r._mapping), user, "Finance Declaration")
            for r in finance
        ]
    }


def get_form_by_type_and_id(db: Session, form_type: str, item_id: int):

    if form_type == "asset_declaration":
        query = "SELECT * FROM user_asset_declaration WHERE asset_id = :id"
        submission_type = "Asset Declaration"

    elif form_type == "employee_form_12c":
        query = "SELECT * FROM employee_form_12c WHERE form_id = :id"
        submission_type = "Form 12"

    elif form_type == "user_finance":
        query = "SELECT * FROM user_finance WHERE user_finance_id = :id"
        submission_type = "Finance Declaration"

    else:
        return None

    row = db.execute(text(query), {"id": item_id}).fetchone()

    if not row:
        return None

    row = dict(row._mapping)
    user = get_user_basic_info(db, row["user_id"])

    return serialize_common(row, user, submission_type)
