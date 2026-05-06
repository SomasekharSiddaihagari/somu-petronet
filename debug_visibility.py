from sqlalchemy import text
from app.core.database import SessionLocal

def check_visibility():
    db = SessionLocal()
    try:
        # 1. Check User 1 Roles
        role_query = text("""
            SELECT r.role_name
            FROM roles r
            JOIN role_permissions rp ON r.role_id = rp.role_id
            WHERE rp.user_id = 1
        """)
        roles = db.execute(role_query).scalars().all()
        print(f"User 1 Roles: {roles}")
        is_hr = any(r.lower() == "hr" for r in roles)
        print(f"Is User 1 HR? {is_hr}")

        # 2. Check if 605 is a subordinate of 1
        sub_query = text("SELECT user_id FROM users WHERE supervisor_id = 1 AND user_id = 605")
        is_sub = db.execute(sub_query).fetchone()
        print(f"Is 605 a subordinate of 1? {is_sub is not None}")

        # 3. Check the record itself
        record_query = text("SELECT user_id, created_at FROM hr_action WHERE id = 3")
        record = db.execute(record_query).fetchone()
        print(f"Record 3 Data: {record}")

    finally:
        db.close()

if __name__ == "__main__":
    check_visibility()
