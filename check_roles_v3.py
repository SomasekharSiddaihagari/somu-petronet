import psycopg2
try:
    conn = psycopg2.connect("postgresql://postgres:pgadmin123@localhost/petronet")
    cur = conn.cursor()
    cur.execute("SELECT r.role_name FROM roles r JOIN role_permissions rp ON r.role_id = rp.role_id WHERE rp.user_id = 114")
    roles = cur.fetchall()
    print(f"Roles for 114: {roles}")
    cur.execute("SELECT r.role_name FROM roles r JOIN role_permissions rp ON r.role_id = rp.role_id WHERE rp.user_id = 1")
    roles1 = cur.fetchall()
    print(f"Roles for 1: {roles1}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
