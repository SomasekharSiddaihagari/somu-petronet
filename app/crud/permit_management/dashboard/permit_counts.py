from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException


def get_permit_dashboard_counts(db: Session):
    query = text("""
        SELECT
            /* TOTAL PERMITS */
            (
                (SELECT COUNT(*) FROM work_at_height_permit)
              + (SELECT COUNT(*) FROM composite_work_permit)
            ) AS total_permits,

            /* ONGOING PERMITS (COMBINED) */
            (
                (SELECT COUNT(*)
                 FROM work_at_height_permit
                 WHERE status IS NULL OR LOWER(status) != 'closed'
                )
              + (SELECT COUNT(*)
                 FROM composite_work_permit
                 WHERE status IS NULL OR LOWER(status) != 'closed'
                )
            ) AS ongoing_permits,

            /* COMPLETED PERMITS (COMBINED) */
            (
                (SELECT COUNT(*)
                 FROM work_at_height_permit
                 WHERE LOWER(COALESCE(status, '')) IN ('completed', 'closed')
                )
              + (SELECT COUNT(*)
                 FROM composite_work_permit
                 WHERE LOWER(COALESCE(status, '')) IN ('completed', 'closed')
                )
            ) AS completed_permits,

            /* COMPOSITE WORK (ONGOING) */
            (
                SELECT COUNT(*)
                FROM composite_work_permit
                WHERE status IS NULL OR LOWER(status) != 'closed'
            ) AS composite_work,

            /* HEIGHT WORK (ONGOING) */
            (
                SELECT COUNT(*)
                FROM work_at_height_permit
                WHERE status IS NULL OR LOWER(status) != 'closed'
            ) AS height_work,

            /* ELECTRICAL ISOLATION (TOTAL) */
            (
                (SELECT COUNT(*) FROM work_at_height_electrical_isolation_permit)
              + (SELECT COUNT(*) FROM composite_electrical_isolation_permit)
            ) AS electrical_isolation
    """)

    return db.execute(query).mappings().first()


def get_users_by_station_and_role(db: Session, station_id: int, role_id: int):
    # Validation: Check if station exists
    station_check = db.execute(text("SELECT 1 FROM station WHERE station_id = :sid AND is_deleted = FALSE"), {"sid": station_id}).first()
    if not station_check:
        raise HTTPException(status_code=404, detail=f"Station ID {station_id} not found or is deleted")
    
    # Validation: Check if role exists
    role_check = db.execute(text("SELECT 1 FROM roles WHERE role_id = :rid AND is_deleted = FALSE"), {"rid": role_id}).first()
    if not role_check:
        raise HTTPException(status_code=404, detail=f"Role ID {role_id} not found or is deleted")

    query = text("""
        SELECT 
            u.user_id, 
            CONCAT(u.first_name, ' ', u.last_name) AS user_name,
            r.role_name, 
            u.designation
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.station_id = :station_id
          AND u.role_id = :role_id
          AND u.is_deleted = FALSE
    """)
    
    return db.execute(query, {"station_id": station_id, "role_id": role_id}).mappings().all()
