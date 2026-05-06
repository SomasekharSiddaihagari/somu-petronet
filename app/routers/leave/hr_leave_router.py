from decimal import Decimal
from typing import Optional
from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from app.crud.leave.hr_leave_crud import crud_all_leaves, crud_leave_by_id, crud_my_leaves, crud_subordinate_leaves
from app.database import get_db
from sqlalchemy.orm import Session

from app.models.leave.leave_balance import LeaveBalance
from app.models.leave.leave_type import LeaveType

 
router = APIRouter(prefix="/api/leave", tags=["Leave Management"])
 
@router.get("/my/{user_id}")
def get_my(user_id: int, db: Session = Depends(get_db)): # type: ignore
    return crud_my_leaves(db, user_id)
 
@router.get("/sub/{supervisor_id}")
def get_sub(supervisor_id: int, db: Session = Depends(get_db)): # type: ignore
    return crud_subordinate_leaves(db, supervisor_id)
 
@router.get("/all")
def get_all(db: Session = Depends(get_db)): # type: ignore
    return crud_all_leaves(db)
 
@router.get("/details/{leave_id}")
def get_leave_details(leave_id: int, db: Session = Depends(get_db)): # type: ignore
    return crud_leave_by_id(db, leave_id)



from fastapi import APIRouter, Depends, HTTPException, status

class LeaveBalanceUpdate(BaseModel):
    user_id: Optional[int] = None
    type_id: Optional[int] = None
    allocated: Optional[Decimal] = None
    used: Optional[Decimal] = None
    balance: Optional[Decimal] = None
    is_usable: Optional[bool] = None

from app.models import User   # make sure this import exists
from app.models import User

@router.get("/leave-balances/user/{user_id}", status_code=status.HTTP_200_OK)
def get_leave_balances_by_user_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            LeaveBalance,
            LeaveType.code.label("leave_code"),
            LeaveType.name.label("leave_name"),
            User.first_name,
            User.last_name,
            User.employee_code   # ✅ added
        )
        .join(
            LeaveType,
            LeaveBalance.type_id == LeaveType.type_id
        )
        .join(
            User,
            LeaveBalance.user_id == User.user_id
        )
        .filter(
            LeaveBalance.user_id == user_id
        )
        .order_by(LeaveBalance.created_date.desc())  # ✅ latest first
        .all()
    )

    if not results:
        return {
            "user_id": user_id,
            "user_name": None,
            "employee_code": None,
            "allocations": []
        }

    # take from first row (same user)
    _, _, _, first_name, last_name, employee_code = results[0]

    return {
        "user_id": user_id,
        "user_name": f"{first_name} {last_name}",
        "employee_code": employee_code,
        "allocations": [
            {
                "balance_id": lb.balance_id,
                "user_id": lb.user_id,
                "type_id": lb.type_id,
                "leave_code": leave_code,
                "leave_name": leave_name,
                "allocated": lb.allocated,
                "used": lb.used,
                "balance": lb.balance,
                "is_usable": lb.is_usable,
                "created_date": lb.created_date
            }
            for lb, leave_code, leave_name, _, _, _ in results
        ]
    }




@router.put("/leave-balances/{balance_id}", status_code=status.HTTP_200_OK)
def update_leave_balance(
    balance_id: int,
    payload: LeaveBalanceUpdate,
    db: Session = Depends(get_db)
):
    leave_balance = (
        db.query(LeaveBalance)
        .filter(LeaveBalance.balance_id == balance_id)
        .first()
    )

    if not leave_balance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave balance not found"
        )

    update_data = payload.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(leave_balance, field, value)

    db.commit()
    db.refresh(leave_balance)

    return {
        "message": "Leave balance updated successfully",
        "data": leave_balance
    }

