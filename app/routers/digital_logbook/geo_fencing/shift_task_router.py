
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
class ShiftHandoverTaskCreate(BaseModel):
    handover_id: Optional[int] = None
    used_handover_id: Optional[int] = None
    pending_task: Optional[str] = None
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None
    priority: Optional[str] = None  # High / Medium / Low
    is_acknowledged:Optional[bool]=False

class ShiftHandoverTaskUpdate(BaseModel):
    pending_task: Optional[str] = None
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None
    priority: Optional[str] = None
    is_acknowledged:Optional[bool]
    
class ShiftHandoverTaskResponse(BaseModel):
    task_id: int
    used_handover_id: Optional[int]
    pending_task: Optional[str]
    due_date: Optional[date]
    assigned_to: Optional[int]
    priority: Optional[str]
    created_at: Optional[datetime]
from sqlalchemy import text


def create_shift_handover_task(db, data: ShiftHandoverTaskCreate):
    query = text("""
        INSERT INTO shift_handover_task (
           
            used_handover_id,
            pending_task,
            due_date,
            assigned_to,
            priority
        )
        VALUES (
            :used_handover_id,
            :pending_task,
            :due_date,
            :assigned_to,
            :priority
        )
        RETURNING *
    """)

    result = db.execute(query, data.model_dump())
    db.commit()
    return result.mappings().first()




def update_shift_handover_task(db, task_id: int, data: ShiftHandoverTaskUpdate):
    fields = []
    params = {"task_id": task_id}

    for key, value in data.model_dump(exclude_unset=True).items():
        fields.append(f"{key} = :{key}")
        params[key] = value

    if not fields:
        return None

    query = text(f"""
        UPDATE shift_handover_task
        SET {", ".join(fields)}
        WHERE task_id = :task_id
        RETURNING *
    """)

    result = db.execute(query, params)
    db.commit()
    return result.mappings().first()
def get_tasks_by_used_handover_id(db, used_handover_id: int):
    query = text("""
        SELECT *
        FROM shift_handover_task
        WHERE used_handover_id = :used_handover_id
        ORDER BY created_at DESC
    """)

    result = db.execute(query, {"used_handover_id": used_handover_id})
    return result.mappings().all()
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from typing import List
router = APIRouter(
    prefix="/shift-handover-task",
    tags=["Shift Handover Task"]
)
@router.post(
    "",
    response_model=ShiftHandoverTaskResponse,
    summary="Create shift handover task"
)
def create_task(
    payload: ShiftHandoverTaskCreate,
    db=Depends(get_db)
):
    return create_shift_handover_task(db, payload)



@router.put(
    "/{task_id}",
    response_model=ShiftHandoverTaskResponse,
    summary="Update shift handover task"
)
def update_task(
    task_id: int,
    payload: ShiftHandoverTaskUpdate,
    db=Depends(get_db)
):
    task = update_shift_handover_task(db, task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get(
    "/by-used-handover/{used_handover_id}",
    response_model=List[ShiftHandoverTaskResponse],
    summary="Get tasks by used_handover_id"
)
def get_tasks(
    used_handover_id: int,
    db=Depends(get_db)
):
    return get_tasks_by_used_handover_id(db, used_handover_id)
