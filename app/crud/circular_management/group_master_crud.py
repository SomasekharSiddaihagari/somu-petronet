import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from psycopg2.extras import Json
from app.schemas.circular_management.group_master_schema import GroupCreate, GroupUpdate

def create_group(db: Session, data: GroupCreate):
    payload = data.model_dump()
    payload["employee_ids"] = Json(payload["employee_ids"])
    query = text("""
        INSERT INTO group_master (
            group_name,
            description,
            employee_ids,
            is_deleted,
            created_by
        )
        VALUES (
            :group_name,
            :description,
            :employee_ids,
            FALSE,
            :created_by
        )
        RETURNING group_id
    """)

    result = db.execute(query, payload)
    group_id = result.scalar()
    db.commit()
    return group_id

def update_group(db: Session, group_id: int, data: GroupUpdate):
    payload = data.model_dump(exclude_unset=True)
    
    if "employee_ids" in payload:
        payload["employee_ids"] = json.dumps(payload["employee_ids"])

    if not payload:
        return False

    query = text("""
        UPDATE group_master
        SET
            group_name   = COALESCE(:group_name, group_name),
            description  = COALESCE(:description, description),
            employee_ids = COALESCE(CAST(:employee_ids AS jsonb), employee_ids),
            updated_by   = COALESCE(:updated_by, updated_by),
            updated_date = COALESCE(:updated_date, now())
        WHERE group_id = :group_id
          AND is_deleted = FALSE
    """)

    payload["group_id"] = group_id
    db.execute(query, payload)
    db.commit()
    return True

def get_group(db: Session, group_id: int):
    query = text("""
        SELECT
            gm.group_id,
            gm.group_name,
            gm.description,
            gm.employee_ids,
            gm.created_by,
            gm.created_date,
            gm.updated_by,
            gm.updated_date,
            COALESCE(
                json_agg(
                    jsonb_build_object(
                        'user_id', u.user_id,
                        'username', u.username,
                        'email', u.email
                    )
                ) FILTER (WHERE u.user_id IS NOT NULL),
                '[]'
            ) AS employee_ids
        FROM group_master gm
        LEFT JOIN users u
          ON u.user_id = ANY (
                SELECT jsonb_array_elements_text(gm.employee_ids)::int
          )
        WHERE gm.group_id = :group_id
          AND gm.is_deleted = FALSE
        GROUP BY gm.group_id
    """)

    return db.execute(query, {"group_id": group_id}).mappings().first()

def get_all_groups(db: Session):
    query = text("""
        SELECT
            gm.group_id,
            gm.group_name,
            gm.description,
            gm.employee_ids,
            gm.created_by,
            gm.created_date,
            gm.updated_by,
            gm.updated_date,
            COALESCE(
                json_agg(
                    jsonb_build_object(
                        'user_id', u.user_id,
                        'username', u.username,
                        'email', u.email
                    )
                ) FILTER (WHERE u.user_id IS NOT NULL),
                '[]'
            ) AS employee_ids
        FROM group_master gm
        LEFT JOIN users u
          ON u.user_id = ANY (
                SELECT jsonb_array_elements_text(gm.employee_ids)::int
          )
        WHERE gm.is_deleted = FALSE
        GROUP BY gm.group_id
        ORDER BY gm.group_id DESC
    """)

    return db.execute(query).mappings().all()

def delete_group(db: Session, group_id: int):
    query = text("""
        UPDATE group_master
        SET
            is_deleted = TRUE,
            updated_date = now()
        WHERE group_id = :group_id
          AND is_deleted = FALSE
    """)

    result = db.execute(query, {
        "group_id": group_id
    })

    db.commit()
    return result.rowcount > 0

def get_all_employee(db: Session):
    try:
        query = text("""
            SELECT DISTINCT
                u.user_id,
                u.username,
                u.email,
                u.first_name,
                u.last_name,
                s.station_name
            FROM users u
            INNER JOIN role_permissions rp 
                ON u.user_id = rp.user_id
            LEFT JOIN station s 
                ON u.station_id = s.station_id
            WHERE u.is_deleted = false and u.is_employee = true
        """)

        result = db.execute(query).fetchall()

        employees = []
        for row in result:
            employees.append({
                "user_id": row.user_id,
                "username": row.username,
                "email": row.email,
                "first_name":row.first_name,
                "last_name": row.last_name,
                "station_name": row.station_name
            })

        return {
            "status": "Success",
            "message": "Employees fetched successfully",
            "data": employees
        }

    except Exception as e:
        return {
            "status": False,
            "message": str(e),
            "data": []
        }


# def get_all_station_users(db: Session):
#     try:
#         query = text("""
#             SELECT
#                 s.station_id,
#                 s.station_name,
#                 COALESCE(
#                     json_agg(
#                         jsonb_build_object(
#                             'user_id', u.user_id,
#                             'username', u.username,
#                             'email', u.email
#                         )
#                     ) FILTER (WHERE u.user_id IS NOT NULL),
#                     '[]'
#                 ) AS users
#             FROM station s
#             INNER JOIN users u
#                 ON s.station_id = u.station_id
#             GROUP BY
#                 s.station_id,
#                 s.station_name
#             ORDER BY s.station_id
#         """)
 
#         result = db.execute(query).mappings().all()
 
#         return {
#             "status": "success",
#             "data": result
#         }
 
#     except Exception as e:
#         return {
#             "status": "fail",
#             "message": str(e),
#             "data": []
#         }
 
def get_all_station_users(db: Session):
    try:
        query = text("""
            SELECT
                s.station_id,
                s.station_name,
                COALESCE(
                    json_agg(
                        jsonb_build_object(
                            'user_id', u.user_id,
                            'username', u.username,
                            'first_name',u.first_name,
                            'last_name',u.last_name,
                            'email', u.email
                        )
                    ) FILTER (WHERE u.user_id IS NOT NULL and u.is_employee=true),
                    '[]'
                ) AS users
            FROM station s
            INNER JOIN users u
                ON s.station_id = u.station_id
            GROUP BY
                s.station_id,
                s.station_name
            ORDER BY s.station_id
        """)

        result = db.execute(query).mappings().all()

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "fail",
            "message": str(e),
            "data": []
        }