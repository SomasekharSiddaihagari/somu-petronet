from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from datetime import datetime

def fix_created_at(row: dict):
    if row.get("created_at") is None:
        row["created_at"] = datetime.now()
    return row



def clean_fields(data: dict):
    """Convert empty strings to None (DB NULL)."""
    for key, value in data.items():
        if isinstance(value, str) and value.strip() == "":
            data[key] = None
    return data


# -------------------------
# GET ALL
# -------------------------
def get_all_educations(db: Session):
    sql = text("SELECT * FROM user_education ORDER BY education_id ASC;")
    rows = db.execute(sql).fetchall()

    result = []

    for r in rows:
        row = dict(r._mapping)

        # 🔥 parse changed_fields
        if row.get("changed_fields"):
            try:
                row["changed_fields"] = json.loads(row["changed_fields"])
            except:
                row["changed_fields"] = []

        result.append(fix_created_at(row))

    return result



# -------------------------
# GET BY USER ID (ALL rows)
# -------------------------
def get_educations_by_user_id(db: Session, user_id: int):
    ##print("🔥 USER ID:", user_id)

    sql = text("""
        SELECT * FROM user_education
        WHERE user_id = :uid
        ORDER BY education_id ASC;
    """)

    rows = db.execute(sql, {"uid": user_id}).fetchall()

    ##print("🔥 ROWS:", rows)   # 👈 ADD THIS

    return [fix_created_at(dict(r._mapping)) for r in rows]


# -------------------------
# CREATE
# -------------------------
def create_education(db: Session, data: dict):
    data = clean_fields(data)

    sql = text("""
        INSERT INTO user_education
        (user_id, qualification, year_of_completion, education_document)
        VALUES (:user_id, :qualification, :year_of_completion, :education_document)
        RETURNING *;
    """)

    row = db.execute(sql, data).fetchone()
    db.commit()

    return fix_created_at(dict(row._mapping))



# -------------------------
# UPDATE
# -------------------------
def update_education(db: Session, education_id: int, data: dict):
    data = clean_fields(data)
    data["education_id"] = education_id

    set_clause = ", ".join([f"{k} = :{k}" for k in data if k != "education_id"])

    sql = text(f"""
        UPDATE user_education
        SET {set_clause}
        WHERE education_id = :education_id
        RETURNING *;
    """)

    row = db.execute(sql, data).fetchone()
    db.commit()

    return fix_created_at(dict(row._mapping)) if row else None

