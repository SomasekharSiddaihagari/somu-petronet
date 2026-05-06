from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List
from collections import defaultdict

from app.crud.permit_management.work_height_permit.work_at_height_electrical_energization_permit import get_all_work_at_height_electrical_energization_permits, get_work_at_height_electrical_energization_permit_by_id
from app.database import get_db
from app.schemas.permit_management.work_height_permit.work_at_height_electrical_energization_permit import WorkAtHeightElectricalEnergizationPermitSchema

router = APIRouter(
    prefix="/work-at-height-electrical-energization-permit",
    tags=["Work At Height Electrical Energization Permit"]
)


def get_role_users_directory(db: Session) -> dict:
    """Fetches users mapped to Permit Management (Submenu 4) grouped by role."""
    users_data = (
        db.execute(
            text(
                """
            SELECT rp.user_id, r.role_name
            FROM role_permissions rp
            JOIN roles r ON r.role_id = rp.role_id
            WHERE rp.submenu_id = 4
              AND rp.user_id IS NOT NULL
        """
            )
        )
        .mappings()
        .all()
    )

    users_by_role = defaultdict(list)
    for u in users_data:
        users_by_role[u["role_name"]].append(u["user_id"])

    return {
        "Engineer": users_by_role.get("Engineer", []),
        "EAP": users_by_role.get("EAP", []),
        "SIC": users_by_role.get("SIC", []),
        "ASIC": users_by_role.get("ASIC", []),
        "Admin": users_by_role.get("Admin", []),
    }


@router.get(
    ""
)
def read_all_work_at_height_electrical_energization_permits(
    db: Session = Depends(get_db)
):
    data = get_all_work_at_height_electrical_energization_permits(db)
    role_users = get_role_users_directory(db)

    results = []
    for item in data:
        item_dict = dict(item)
        item_dict["role_users"] = role_users
        results.append(item_dict)

    return results


@router.get(
    "/{whpep_id}"
)
def read_work_at_height_electrical_energization_permit_by_id(
    whpep_id: int,
    db: Session = Depends(get_db)
):
    data = get_work_at_height_electrical_energization_permit_by_id(db, whpep_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Work At Height Electrical Energization Permit not found"
        )

    role_users = get_role_users_directory(db)
    result = dict(data)
    result["role_users"] = role_users

    return result

