import psycopg2
import os
from datetime import datetime

# Direct connection to the database
conn = psycopg2.connect("postgresql://postgres:pgadmin123@localhost/petronet")
cur = conn.cursor()

try:
    print("--- Diagnostic Report ---")
    
    # 1. Check User 1 Roles
    cur.execute("""
        SELECT r.role_name
        FROM roles r
        JOIN role_permissions rp ON r.role_id = rp.role_id
        WHERE rp.user_id = 1
    """)
    roles = [row[0] for row in cur.fetchall()]
    print(f"User 1 Roles: {roles}")
    is_hr = any(r.lower() == "hr" for r in roles)
    print(f"Is User 1 HR? {is_hr}")

    # 2. Check if 605 is a subordinate of 1
    cur.execute("SELECT user_id, supervisor_id FROM users WHERE user_id = 605")
    user_data = cur.fetchone()
    print(f"User 605 Data (ID, Supervisor): {user_data}")
    is_sub = user_data and user_data[1] == 1
    print(f"Is 605 a direct subordinate of 1? {is_sub}")

    # 3. Check the record itself
    cur.execute("SELECT user_id, created_at, action_type, is_deleted FROM hr_action WHERE id = 3")
    record = cur.fetchone()
    print(f"HR Action Record 3: {record}")

    # 4. Check Visibility Query Simulation
    if not is_hr:
        cur.execute("""
            SELECT user_id 
            FROM (
                SELECT user_id FROM hr_action WHERE id = 3
            ) as sub
            WHERE user_id IN (SELECT user_id FROM users WHERE supervisor_id = 1) 
               OR user_id = 1
        """)
        visible = cur.fetchone()
        print(f"Is Record 3 visible to User 1 in current logic? {visible is not None}")

finally:
    cur.close()
    conn.close()
