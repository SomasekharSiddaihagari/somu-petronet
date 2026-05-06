from fastapi import APIRouter, Depends, HTTPException
from app.routers.leave.emolyee_weekoff_criud import create_employee_weekly_off, get_employee_weekly_offs_by_supervisor_id, update_employee_weekly_off
from app.schemas.leave.leave_week_off import EmployeeWeeklyOffCreate, EmployeeWeeklyOffCreateByEmail, EmployeeWeeklyOffResponse, EmployeeWeeklyOffUpdate
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List


from app.database import get_db


router = APIRouter(
    prefix="/api/employee-weekly-off",
    tags=["Employee Weekly Off"],
)


# =================================================
# CREATE
# =================================================
@router.post("", response_model=EmployeeWeeklyOffResponse)
def create_employee_weekly_off_api(
    data: EmployeeWeeklyOffCreate,
    db: Session = Depends(get_db),
):
    weekly_off_id = create_employee_weekly_off(db, data)

    return db.execute(
        text("SELECT * FROM employee_weekly_off WHERE id = :id"),
        {"id": weekly_off_id},
    ).mappings().first()



# =================================================
# GET BY ID
# =================================================
@router.get("/{weekly_off_id}", response_model=EmployeeWeeklyOffResponse)
def get_employee_weekly_off_by_id(
    weekly_off_id: int,
    db: Session = Depends(get_db),
):
    record = db.execute(
        text("SELECT * FROM employee_weekly_off WHERE id = :id"),
        {"id": weekly_off_id},
    ).mappings().first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return record



@router.get("/by-user/{user_id}")
def get_employee_weekly_offs_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    records = db.execute(
        text("""
            SELECT
                ewo.id,
                ewo.user_id,

                (
                    SELECT string_agg(
                        CASE day::int
                            WHEN 1 THEN 'Monday'
                            WHEN 2 THEN 'Tuesday'
                            WHEN 3 THEN 'Wednesday'
                            WHEN 4 THEN 'Thursday'
                            WHEN 5 THEN 'Friday'
                            WHEN 6 THEN 'Saturday'
                            WHEN 7 THEN 'Sunday'
                        END,
                        ', '
                    )
                    FROM unnest(string_to_array(ewo.week_off_day, ',')) AS day
                ) AS week_off_day,

                ewo.effective_from,
                ewo.effective_to,
                ewo.is_active,

                u.employee_code,
                CONCAT(
                    COALESCE(u.first_name, ''),
                    ' ',
                    COALESCE(u.last_name, '')
                ) AS employee_name,
                u.designation,
                s.station_name

            FROM employee_weekly_off ewo
            JOIN users u ON u.user_id = ewo.user_id
            LEFT JOIN station s
                ON s.station_id = u.station_id
               AND s.is_deleted = FALSE
            WHERE ewo.user_id = :user_id
              AND ewo.is_active = TRUE
            ORDER BY ewo.effective_from DESC
        """),
        {"user_id": user_id},
    ).mappings().all()

    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    return records




# =================================================
# GET ALL
# =================================================
@router.get("", response_model=List[EmployeeWeeklyOffResponse])
def get_all_employee_weekly_offs(
    db: Session = Depends(get_db),
):
    return db.execute(
        text("SELECT * FROM employee_weekly_off ORDER BY id DESC")
    ).mappings().all()


@router.delete("/{weekly_off_id}")
def delete_employee_weekly_off(
    weekly_off_id: int,
    db: Session = Depends(get_db),
):
    result = db.execute(
        text("""
            DELETE FROM employee_weekly_off
            WHERE id = :id
        """),
        {"id": weekly_off_id},
    )

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Weekly off record not found",
        )

    db.commit()

    return {
        "message": "Weekly off deleted successfully",
        "weekly_off_id": weekly_off_id,
    }

@router.get("/by-all/{supervisor_id}")
def get_weekly_offs_by_supervisor(
    supervisor_id: int,
    db: Session = Depends(get_db),
):
    records = get_employee_weekly_offs_by_supervisor_id(
        db,
        supervisor_id,
    )

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No weekly off records found",
        )

    return records

# =================================================
# UPDATE
# =================================================
@router.put("/{weekly_off_id}", response_model=EmployeeWeeklyOffResponse)
def update_employee_weekly_off_api(
    weekly_off_id: int,
    data: EmployeeWeeklyOffUpdate,
    db: Session = Depends(get_db),
):
    if not update_employee_weekly_off(db, weekly_off_id, data):
        raise HTTPException(status_code=404, detail="Record not found")

    return db.execute(
        text("SELECT * FROM employee_weekly_off WHERE id = :id"),
        {"id": weekly_off_id},
    ).mappings().first()


@router.post("/by-email")
def create_weekly_off_by_email(
    data: EmployeeWeeklyOffCreateByEmail,
    db: Session = Depends(get_db),
):
    weekly_off_id = create_employee_weekly_off_by_email(db, data)

    # Return inserted record
    return db.execute(
        text("""
            SELECT *
            FROM employee_weekly_off
            WHERE id = :id
        """),
        {"id": weekly_off_id},
    ).mappings().first()
def create_employee_weekly_off_by_email(
    db: Session,
    data: EmployeeWeeklyOffCreateByEmail,
):
    # 1️⃣ Fetch user_id using email (username OR work_email)
    user_query = text("""
        SELECT user_id
        FROM users
        WHERE is_deleted = FALSE
          AND (
                LOWER(username) = LOWER(:email)
             OR LOWER(email) = LOWER(:email)
          )
        LIMIT 1
    """)

    user = db.execute(
        user_query,
        {"email": data.email},
    ).mappings().first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found with given email"
        )

    user_id = user["user_id"]

    # 2️⃣ Insert weekly off
    insert_query = text("""
        INSERT INTO employee_weekly_off (
            user_id,
            week_off_day,
            effective_from,
            effective_to,
            is_active
        )
        VALUES (
            :user_id,
            :week_off_day,
            :effective_from,
            :effective_to,
            :is_active
        )
        RETURNING id
    """)

    result = db.execute(
        insert_query,
        {
            "user_id": user_id,
            "week_off_day": data.week_off_day,  # "1,2,3"
            "effective_from": data.effective_from,
            "effective_to": data.effective_to,
            "is_active": data.is_active,
        },
    )

    weekly_off_id = result.scalar()
    db.commit()

    return weekly_off_id
