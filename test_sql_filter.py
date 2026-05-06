from sqlalchemy import text
from app.database import SessionLocal

def test_filter():
    db = SessionLocal()
    try:
        # We simulate what the user is doing
        login_user_id = 1  # User hits the endpoint with path ID 1
        filter_user_id = 1 # User sends user_id=1 in the body
        
        # This is the exact code from promotion_master_crud.py
        base_query = """
        SELECT * FROM (
            -- 1. HR Actions
            SELECT 
                u.user_id,
                u.employee_code,
                TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
                u.contact_phone AS mobile_no,
                s.station_name,
                u.designation,
                u.grade,
                TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')) AS supervisor,
                u.employment_type,
                a.created_at AS issue_date,
                a.action_type AS type,
                u.station_id
            FROM users u
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN station s ON u.station_id = s.station_id
            JOIN hr_action a ON a.user_id = u.user_id AND a.is_deleted = FALSE
            WHERE u.is_deleted = FALSE

            UNION ALL

            -- 2. Disciplinary
            SELECT 
                u.user_id,
                u.employee_code,
                TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
                u.contact_phone,
                s.station_name,
                u.designation,
                u.grade,
                TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')),
                u.employment_type,
                d.incident_date,
                'Disciplinary',
                u.station_id
            FROM users u
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN station s ON u.station_id = s.station_id
            JOIN disciplinary_incidents d ON d.user_id = u.user_id AND d.is_deleted = FALSE
            WHERE u.is_deleted = FALSE

            UNION ALL

            -- 3. Promotions
            SELECT 
                u.user_id,
                u.employee_code,
                TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
                u.contact_phone,
                s.station_name,
                p.new_designation,
                p.new_grade,
                TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')),
                u.employment_type,
                p.effective_date,
                'Promotion',
                u.station_id
            FROM users u
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN station s ON u.station_id = s.station_id
            JOIN promotions p ON p.user_id = u.user_id AND p.is_deleted = FALSE
            WHERE u.is_deleted = FALSE

            UNION ALL

            -- 4. Transfers
            SELECT 
                u.user_id,
                u.employee_code,
                TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')) AS name,
                u.contact_phone,
                s.station_name,
                u.designation,
                u.grade,
                TRIM(COALESCE(sup.first_name, '') || ' ' || COALESCE(sup.last_name, '')),
                u.employment_type,
                t.effective_date,
                'Transfer',
                u.station_id
            FROM users u
            LEFT JOIN users sup ON u.supervisor_id = sup.user_id
            LEFT JOIN station s ON u.station_id = s.station_id
            JOIN employee_transfers t ON t.user_id = u.user_id AND t.is_deleted = FALSE
            WHERE u.is_deleted = FALSE
        ) AS combined
        WHERE 1=1
        """
        
        params = {}
        # Apply filter from body
        base_query += " AND user_id = :employee_id"
        params["employee_id"] = filter_user_id
        
        # Apply visibility check
        # We assume the user is NOT HR for this test
        base_query += " AND (user_id IN (SELECT user_id FROM users WHERE supervisor_id = :login_user_id) OR user_id = :login_user_id)"
        params["login_user_id"] = login_user_id
        
        print("Executing Query...")
        result = db.execute(text(base_query), params).mappings().all()
        
        print(f"Results for User {filter_user_id}:")
        for row in result:
            print(f"ID: {row['user_id']}, Type: {row['type']}, Name: {row['name']}")
        
        if not result:
            print("No records found.")
            
    finally:
        db.close()

if __name__ == "__main__":
    test_filter()
