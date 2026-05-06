import os
from sqlalchemy.orm import Session
from sqlalchemy import text


base_url = os.getenv("BackEndPath")

import json

def parse_document_field(record):
    rec = dict(record._mapping) if hasattr(record, "_mapping") else dict(record)

    if rec.get("document_name"):
        try:
            rec["document_name"] = json.loads(rec["document_name"])
        except:
            rec["document_name"] = []
    else:
        rec["document_name"] = []

    # changed_fields ✅ ADD THIS
    if rec.get("changed_fields"):
        try:
            rec["changed_fields"] = json.loads(rec["changed_fields"])
        except:
            rec["changed_fields"] = []
    else:
        rec["changed_fields"] = []


    return rec





# -------------------------
# GET ALL
# -------------------------
def get_all_employee_banks(db: Session):
    sql = text("SELECT * FROM employee_bank ORDER BY id ASC;")
    rows = db.execute(sql).fetchall()

    records = []
    for r in rows:
        rec = dict(r._mapping)
        rec = parse_document_field(rec)
        records.append(rec)

    return records



def get_employee_bank_by_user_id(db: Session, user_id: int):
    sql = text("""
        SELECT * FROM employee_bank
        WHERE user_id = :uid
        ORDER BY id DESC;
    """)
    rows = db.execute(sql, {"uid": user_id}).fetchall()

    records = []
    for r in rows:
        rec = dict(r._mapping)
        rec = parse_document_field(rec)
        records.append(rec)

    return records

# -------------------------
# CREATE
# -------------------------
def create_employee_bank(db: Session, data: dict):
    sql = text("""
        INSERT INTO employee_bank
        (user_id, bank_name, branch_name, account_number,
         ifsc_code, account_holder_name, account_type,
         cancelled_cheque, document_name, is_active, status, remarks)
        VALUES
        (:user_id, :bank_name, :branch_name, :account_number,
         :ifsc_code, :account_holder_name, :account_type,
         :cancelled_cheque, :document_name, :is_active, :status, :remarks)
        RETURNING *;
    """)
    row = db.execute(sql, data).fetchone()
    db.commit()

    rec = dict(row._mapping)
    return parse_document_field(rec)




# -------------------------
# UPDATE
# -------------------------
def update_employee_bank(db: Session, bank_id: int, data: dict):
    data["id"] = bank_id

    set_clause = ", ".join(
        [f"{k} = :{k}" for k in data if k != "id"]
    )

    sql = text(f"""
        UPDATE employee_bank
        SET {set_clause}
        WHERE id = :id
        RETURNING *;
    """)

    row = db.execute(sql, data).fetchone()
    db.commit()

    if not row:
        return None

    rec = dict(row._mapping)
    return parse_document_field(rec)

# -------------------------
# DELETE
# -------------------------
def delete_employee_bank(db: Session, bank_id: int):
    sql = text("DELETE FROM employee_bank WHERE id = :id;")
    db.execute(sql, {"id": bank_id})
    db.commit()
