from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.UserModel import User
from app.models.digital_logbook.digital_shift_handover.shift_handover_task import ShiftHandoverTask

router = APIRouter(
    prefix="/shift-handover-task",
    tags=["Shift Handover Task"]
)

# =====================================================
# SCHEMAS (ALL FIELDS)
# =====================================================

class ShiftHandoverTaskCreate(BaseModel):
    pending_task: Optional[str] = None
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None
    priority: Optional[str] = None
    is_acknowledged: Optional[bool] = None


class ShiftHandoverTaskUpdatePayload(BaseModel):  # ← completely different name
    pending_task: Optional[str] = None
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None
    priority: Optional[str] = None
    is_acknowledged: Optional[bool] = None


# =====================================================
# POST — CREATE TASK
# =====================================================
@router.post("")
def create_shift_handover_task(
    payload: ShiftHandoverTaskCreate,
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO shift_handover_task (
            pending_task,
            due_date,
            assigned_to,
            is_acknowledged,
            priority
        )
        VALUES (
            :pending_task,
            :due_date,
            :assigned_to,
            :is_acknowledged,
            :priority
        )
        RETURNING task_id
    """)

    result = db.execute(query, payload.dict())
    db.commit()

    return {
        "message": "Shift handover task created successfully",
        "task_id": result.scalar()
    }



@router.get("/get_station_tasks")
def get_shift_handover_tasks(
    station_id: Optional[int] = Query(None, description="Filter tasks by station_id of the assigned user"),
    db: Session = Depends(get_db)
    ):
    """
    Get all ShiftHandoverTask records.
    If station_id is provided, returns only tasks where the assigned_to user
    belongs to the given station.
    Always returns assigned user's first_name and last_name.
    """
    try:
        if station_id is not None:
            sql = text("""
                SELECT 
                    sht.task_id,
                    sht.handover_id,
                    sht.used_handover_id,
                    sht.pending_task,
                    sht.due_date,
                    sht.assigned_to,
                    u.first_name      AS assigned_first_name,
                    u.last_name       AS assigned_last_name,
                    sht.priority,
                    sht.created_at,
                    sht.is_acknowledged,
                    sht.created_by,
                    sht.updated_at,
                    sht.updated_by
                FROM shift_handover_task sht
                JOIN users u ON sht.assigned_to = u.user_id
                WHERE u.station_id = :station_id
                AND u.is_deleted = false
            """)
            result = db.execute(sql, {"station_id": station_id})
        else:
            sql = text("""
                SELECT 
                    sht.task_id,
                    sht.handover_id,
                    sht.used_handover_id,
                    sht.pending_task,
                    sht.due_date,
                    sht.assigned_to,
                    u.first_name      AS assigned_first_name,
                    u.last_name       AS assigned_last_name,
                    sht.priority,
                    sht.created_at,
                    sht.is_acknowledged,
                    sht.created_by,
                    sht.updated_at,
                    sht.updated_by
                FROM shift_handover_task sht
                LEFT JOIN users u ON sht.assigned_to = u.user_id
            """)
            result = db.execute(sql)

        rows = result.fetchall()
        keys = result.keys()

        data = [dict(zip(keys, row)) for row in rows]

        return {
            "success": True,
            "total": len(data),
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cards")
async def get_unacknowledged_tasks_count(
    station_id: int,
    db: Session = Depends(get_db)
):
    count = db.query(ShiftHandoverTask).join(
        User, User.user_id == ShiftHandoverTask.assigned_to
    ).filter(
        ShiftHandoverTask.is_acknowledged == False,
        User.station_id == station_id
    ).count()
    
    return {
        "status": "success",
        "pending_task": count
    }

# =====================================================
# PUT — FULL UPDATE (ALL FIELDS)
# =====================================================



# PUT route — use the new name
@router.put("/{task_id}")
def update_shift_handover_task(
    task_id: int,
    payload: ShiftHandoverTaskUpdatePayload,  # ← updated here
    db: Session = Depends(get_db)
):
    params = payload.dict()
    params["id"] = task_id

    query = text("""
        UPDATE shift_handover_task
        SET
            pending_task     = :pending_task,
            due_date         = :due_date,
            assigned_to      = :assigned_to,
            is_acknowledged  = :is_acknowledged,
            priority         = :priority
        WHERE task_id = :id
    """)

    result = db.execute(query, params)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Shift handover task not found"
        )

    return {"message": "Shift handover task updated successfully"}


# =====================================================
# DELETE
# =====================================================

@router.delete("/{task_id}")
def delete_shift_handover_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            DELETE FROM shift_handover_task
            WHERE task_id = :id
        """),
        {"id": task_id}
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Shift handover task not found"
        )

    return {"message": "Shift handover task deleted successfully"}
