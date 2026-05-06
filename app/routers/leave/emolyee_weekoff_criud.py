from app.models.leave.employe_weekly_off import EmployeeWeeklyOff
from app.schemas.leave.leave_week_off import EmployeeWeeklyOffCreate, EmployeeWeeklyOffUpdate
from sqlalchemy.orm import Session
from sqlalchemy.sql import text



# =================================================
# CREATE
# =================================================

def create_employee_weekly_off(db: Session, data: EmployeeWeeklyOffCreate):

    # 1️⃣ Deactivate all previous weekly-offs for this user
    db.execute(
        text("""
            UPDATE employee_weekly_off
            SET is_active = FALSE
            WHERE user_id = :user_id
        """),
        {"user_id": data.user_id},
    )

    # 2️⃣ Insert new weekly-off record
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
            TRUE
        )
        RETURNING id
    """)

    result = db.execute(
        insert_query,
        {
            "user_id": data.user_id,
            "week_off_day": data.week_off_day,  # "1,2,3"
            "effective_from": data.effective_from,
            "effective_to": data.effective_to,
        },
    )

    weekly_off_id = result.scalar()
    db.commit()

    return weekly_off_id
# =================================================
# UPDATE
# =================================================
def update_employee_weekly_off(
    db: Session,
    weekly_off_id: int,
    data: EmployeeWeeklyOffUpdate,
):
    update_fields = data.model_dump(exclude_unset=True)

    if not update_fields:
        return False

    set_clause = ", ".join(f"{k} = :{k}" for k in update_fields)

    query = text(f"""
        UPDATE employee_weekly_off
        SET {set_clause}
        WHERE id = :id
    """)

    update_fields["id"] = weekly_off_id
    result = db.execute(query, update_fields)

    if result.rowcount == 0:
        return False

    db.commit()
    return True

from sqlalchemy import text
from sqlalchemy.orm import Session

# def get_employee_weekly_offs_by_supervisor_id(
#     db: Session,
#     supervisor_id: int,
# ):
#     # print("===================================")
#     # print("START FETCH WEEKLY OFF DATA")
#     # print(f"Supervisor ID received: {supervisor_id}")

#     is_admin = has_admin_role(db, supervisor_id)

#     if is_admin:
#         # print("ROLE DECISION: ADMIN / HR")
#         # print("Fetching ALL weekly-off records")

#         query = text("""
#             SELECT
#                 ewo.id,
#                 ewo.user_id,

#                 array_to_string(
#                     ARRAY(
#                         SELECT
#                             CASE day::INT
#                                 WHEN 1 THEN 'Monday'
#                                 WHEN 2 THEN 'Tuesday'
#                                 WHEN 3 THEN 'Wednesday'
#                                 WHEN 4 THEN 'Thursday'
#                                 WHEN 5 THEN 'Friday'
#                                 WHEN 6 THEN 'Saturday'
#                                 WHEN 7 THEN 'Sunday'
#                             END
#                         FROM unnest(
#                             string_to_array(ewo.week_off_day, ',')
#                         ) AS day
#                     ),
#                     ', '
#                 ) AS week_off_day,

#                 ewo.effective_from,
#                 ewo.effective_to,
#                 ewo.is_active,

#                 u.employee_code,
#                 CONCAT(
#                     COALESCE(u.first_name, ''),
#                     ' ',
#                     COALESCE(u.last_name, '')
#                 ) AS employee_name,
#                 u.designation,
#                 s.station_name

#             FROM employee_weekly_off ewo
#             JOIN users u ON u.user_id = ewo.user_id
#             LEFT JOIN station s
#                 ON s.station_id = u.station_id
#                AND s.is_deleted = FALSE

#             WHERE  u.is_deleted = FALSE

#             ORDER BY ewo.effective_from DESC
#         """)

#         params = {}

#     else:
#         print("ROLE DECISION: NORMAL SUPERVISOR")
#         print(f"Fetching records where supervisor_id = {supervisor_id}")

#         query = text("""
#             SELECT
#                 ewo.id,
#                 ewo.user_id,

#                 array_to_string(
#                     ARRAY(
#                         SELECT
#                             CASE day::INT
#                                 WHEN 1 THEN 'Monday'
#                                 WHEN 2 THEN 'Tuesday'
#                                 WHEN 3 THEN 'Wednesday'
#                                 WHEN 4 THEN 'Thursday'
#                                 WHEN 5 THEN 'Friday'
#                                 WHEN 6 THEN 'Saturday'
#                                 WHEN 7 THEN 'Sunday'
#                             END
#                         FROM unnest(
#                             string_to_array(ewo.week_off_day, ',')
#                         ) AS day
#                     ),
#                     ', '
#                 ) AS week_off_day,

#                 ewo.effective_from,
#                 ewo.effective_to,
#                 ewo.is_active,

#                 u.employee_code,
#                 CONCAT(
#                     COALESCE(u.first_name, ''),
#                     ' ',
#                     COALESCE(u.last_name, '')
#                 ) AS employee_name,
#                 u.designation,
#                 s.station_name

#             FROM employee_weekly_off ewo
#             JOIN users u ON u.user_id = ewo.user_id
#             LEFT JOIN station s
#                 ON s.station_id = u.station_id
#                AND s.is_deleted = FALSE

#             WHERE  u.is_deleted = FALSE
#               AND u.supervisor_id = :supervisor_id

#             ORDER BY ewo.effective_from DESC
#         """)

#         params = {"supervisor_id": supervisor_id}

#     # print("Executing SQL query...")
#     # print("SQL Params:", params)

#     result = db.execute(query, params).mappings().all()

#     # print(f"Total records fetched: {len(result)}")
#     # print("END FETCH WEEKLY OFF DATA")
#     # print("===================================\n")

#     return result

def get_employee_weekly_offs_by_supervisor_id(
    db: Session,
    supervisor_id: int,
):
    is_admin = has_admin_role(db, supervisor_id)

    day_sort_order = """
        ORDER BY (
            SELECT MIN(
                CASE day::INT
                    WHEN 7 THEN 0   -- Sunday → 0 (first)
                    ELSE day::INT   -- Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6
                END
            )
            FROM unnest(string_to_array(ewo.week_off_day, ',')) AS day
        )
    """

    base_select = """
        SELECT
            ewo.id,
            ewo.user_id,

            array_to_string(
                ARRAY(
                    SELECT
                        CASE day::INT
                            WHEN 1 THEN 'Monday'
                            WHEN 2 THEN 'Tuesday'
                            WHEN 3 THEN 'Wednesday'
                            WHEN 4 THEN 'Thursday'
                            WHEN 5 THEN 'Friday'
                            WHEN 6 THEN 'Saturday'
                            WHEN 7 THEN 'Sunday'
                        END
                    FROM unnest(
                        string_to_array(ewo.week_off_day, ',')
                    ) AS day
                ),
                ', '
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
    """

    if is_admin:
        query = text(f"""
            {base_select}
            WHERE u.is_deleted = FALSE
            {day_sort_order}
        """)
        params = {}

    else:
        query = text(f"""
            {base_select}
            WHERE u.is_deleted = FALSE
              AND u.supervisor_id = :supervisor_id
            {day_sort_order}
        """)
        params = {"supervisor_id": supervisor_id}

    result = db.execute(query, params).mappings().all()
    return result




def has_admin_role(db: Session, user_id: int) -> bool:
    # print("---- ROLE CHECK START ----")
    # print(f"Checking role for user_id = {user_id}")

    query = text("""
        SELECT rp.role_id
        FROM users u
        JOIN role_permissions rp
            ON rp.user_id = u.user_id
        WHERE u.user_id = :user_id
          AND rp.submenu_id = 9
          AND rp.role_id IN (10, 7, 4)
        LIMIT 1
    """)

    result = db.execute(
        query,
        {"user_id": user_id},
    ).first()

    # print("Role query result:", result)

    is_admin = result is not None
    # print("Is admin / HR:", is_admin)
    # print("---- ROLE CHECK END ----\n")

    return is_admin