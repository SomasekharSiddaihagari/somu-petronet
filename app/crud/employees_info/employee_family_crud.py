from sqlalchemy.orm import Session
from sqlalchemy import text

def get_all_family_members(db: Session):
    rows = db.execute(text("SELECT * FROM get_all_family_members();")).fetchall()
    return [dict(r._mapping) for r in rows]


def get_family_member_by_id(db: Session, ef_id: int):
    row = db.execute(
        text("SELECT * FROM get_family_member_by_id(:fid);"),
        {"fid": ef_id}
    ).fetchone()

    return dict(row._mapping) if row else None


from sqlalchemy.orm import Session
from sqlalchemy import text

def get_family_members_by_user_id(db: Session, user_id: int):

    sql = text("""
        SELECT 
            ef_id,
            submission_id,
            relation,
            full_name,
            dob,
            document,
            user_id,
            gender,
            place_of_birth,
            date_of_marriage,
            status,
            document_details,
            comment,
            changed_fields
        FROM employee_family
        WHERE user_id = :uid
        ORDER BY ef_id;
    """)

    rows = db.execute(sql, {"uid": user_id}).fetchall()

    return [dict(r._mapping) for r in rows]

