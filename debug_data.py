from sqlalchemy import text
from app.database import SessionLocal

def debug_user_data(user_id: int):
    db = SessionLocal()
    try:
        print(f"--- Debugging Data for User {user_id} ---")
        
        # 1. User Info
        user = db.execute(text("SELECT user_id, username, station_id FROM users WHERE user_id = :id"), {"id": user_id}).fetchone()
        if user:
            print(f"User found: {dict(user._mapping)}")
        else:
            print("User NOT found in 'users' table!")

        # 2. Check Promotion
        p = db.execute(text("SELECT count(*) FROM promotions WHERE user_id = :id"), {"id": user_id}).scalar()
        print(f"Promotions: {p}")

        # 3. Check Disciplinary
        d = db.execute(text("SELECT count(*) FROM disciplinary_incidents WHERE user_id = :id"), {"id": user_id}).scalar()
        print(f"Disciplinary: {d}")

        # 4. Check Transfers
        t = db.execute(text("SELECT count(*) FROM employee_transfers WHERE user_id = :id"), {"id": user_id}).scalar()
        print(f"Transfers: {t}")

        # 5. Check HR Actions
        a = db.execute(text("SELECT count(*) FROM hr_action WHERE user_id = :id"), {"id": user_id}).scalar()
        print(f"HR Actions: {a}")

        # 6. Check the exact query we are running
        # We need to see if the JOIN with users is failing or if the conditions are too strict.
        query = text("""
            SELECT count(*) 
            FROM hr_action a
            JOIN users u ON a.user_id = u.user_id
            WHERE u.user_id = :id
        """)
        join_count = db.execute(query, {"id": user_id}).scalar()
        print(f"HR Actions with User JOIN: {join_count}")

    finally:
        db.close()

if __name__ == "__main__":
    debug_user_data(428)
