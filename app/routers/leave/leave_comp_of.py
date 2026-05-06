from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date

from app.database import get_db

router = APIRouter(
    prefix="/hr-leave-compoff",
    tags=["HR Leave Comp Off"]
)
from datetime import date
from pydantic import BaseModel


class HRLeaveCompOffCreate(BaseModel):
    leave_application_id: int
    leave_date: date


class HRLeaveCompOffUpdate(BaseModel):
    leave_date: date

@router.post("/create")
def create_compoff_day(
    leave_application_id: int,
    leave_date: date,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO hr_leave_compof_day (
            leave_application_id,
            leave_date
        )
        VALUES (
            :leave_application_id,
            :leave_date
        )
        RETURNING
            leave_compof_id,
            leave_application_id,
            leave_date,
            created_at
    """)

    result = db.execute(
        query,
        {
            "leave_application_id": leave_application_id,
            "leave_date": leave_date
        }
    ).mappings().first()

    db.commit()

    return {
        "success": True,
        "message": "Comp-off day created successfully",
        "data": result
    }

@router.put("/update/{leave_compof_id}")
def update_compoff_day(
    leave_compof_id: int,
    leave_date: date,
    db: Session = Depends(get_db)
):
    # Check existence
    exists = db.execute(
        text("""
            SELECT leave_compof_id
            FROM hr_leave_compof_day
            WHERE leave_compof_id = :leave_compof_id
        """),
        {"leave_compof_id": leave_compof_id}
    ).first()

    if not exists:
        raise HTTPException(
            status_code=404,
            detail="Comp-off day record not found"
        )

    # Update
    result = db.execute(
        text("""
            UPDATE hr_leave_compof_day
            SET leave_date = :leave_date
            WHERE leave_compof_id = :leave_compof_id
            RETURNING
                leave_compof_id,
                leave_application_id,
                leave_date,
                created_at
        """),
        {
            "leave_compof_id": leave_compof_id,
            "leave_date": leave_date
        }
    ).mappings().first()

    db.commit()

    return {
        "success": True,
        "message": "Comp-off day updated successfully",
        "data": result
    }
