from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.crud.permit_management.dashboard.permit_counts import (
    get_permit_dashboard_counts,
    get_users_by_station_and_role
)
from app.database import get_db
from app.crud.permit_management.composit_permit.composite_electrical_isolation_permit import (
    get_all_composite_electrical_isolation_permits
)
from app.crud.permit_management.work_height_permit.work_at_height_electrical_isolation_permit import (
    get_all_work_at_height_electrical_isolation_permits
)
from app.crud.permit_management.composit_permit.composite_electrical_energization_permit import (
    get_all_composite_electrical_energization_permits
)
from app.crud.permit_management.work_height_permit.work_at_height_electrical_energization_permit import (
    get_all_work_at_height_electrical_energization_permits
)
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/permit-counts")
def get_dashboard_permit_counts(
    db: Session = Depends(get_db)
):
    """
    Dashboard permit counts
    """
    return get_permit_dashboard_counts(db)


@router.get("/electrical-isolation-permits")
def get_all_electrical_isolation_permits(
    db: Session = Depends(get_db)
):
    composite = get_all_composite_electrical_isolation_permits(db)
    wah = get_all_work_at_height_electrical_isolation_permits(db)

    return {
        "composite_electrical_isolation": composite,
        "work_at_height_electrical_isolation": wah
    }


@router.get("/electrical-energization-permits")
def get_all_electrical_energization_permits(
    db: Session = Depends(get_db)
):
    composite = get_all_composite_electrical_energization_permits(db)
    wah = get_all_work_at_height_electrical_energization_permits(db)

    return {
        "composite_electrical_energization": composite,
        "work_at_height_electrical_energization": wah
    }

@router.get("/users-dropdown")
def get_users_dropdown(
    role_id: int,
    station_id: int,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT DISTINCT
            u.user_id,

            CONCAT(
                COALESCE(u.first_name, ''),
                CASE
                    WHEN u.last_name IS NOT NULL
                         AND u.last_name <> ''
                    THEN ' ' || u.last_name
                    ELSE ''
                END
            ) AS full_name,

            u.designation,
            r.role_name,
            s.station_name

        FROM role_permissions rp

        JOIN users u
            ON u.user_id = rp.user_id

        JOIN roles r
            ON r.role_id = rp.role_id

        LEFT JOIN station s
            ON s.station_id = u.station_id

        WHERE rp.role_id = :role_id
          AND u.station_id = :station_id
          AND COALESCE(u.is_deleted, false) = false

        ORDER BY full_name
    """)

    result = db.execute(query, {
        "role_id": role_id,
        "station_id": station_id
    }).mappings().all()

    return {
        "status": True,
        "data": [dict(row) for row in result]
    }