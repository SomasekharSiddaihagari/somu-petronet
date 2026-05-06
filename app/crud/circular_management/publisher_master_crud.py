from sqlalchemy.orm import Session
from sqlalchemy.sql import text,bindparam
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import JSONB

from app.schemas.circular_management.publisher_master_schema import (
    PublisherCreate,
    PublisherUpdate
)

# -------------------------------------------------
# CREATE (MASTER + HISTORY)
# -------------------------------------------------
def create_publisher(db: Session, data: PublisherCreate):
    payload = data.model_dump()

    insert_master = text("""
        INSERT INTO publisher_master (
            user_id,
            category_id,
            status,
            role_id,
            role_name
        )
        VALUES (
            :user_id,
            :category_id,
            :status,
            14,
            'PUBLISHER'           
        )
        RETURNING publisher_id
    """).bindparams(
        bindparam("category_id", type_=JSONB)
    )

    insert_history = text("""
        INSERT INTO publisher_master_history (
            publisher_id,
            user_id,
            category_id,
            status,
            role_id,
            role_name            
        )
        VALUES (
            :publisher_id,
            :user_id,
            :category_id,
            :status,
            14,
            'PUBLISHER'             
        )
    """).bindparams(
        bindparam("category_id", type_=JSONB)
    )

    try:
        publisher_id = db.execute(insert_master, payload).scalar()

        db.execute(
            insert_history,
            {
                "publisher_id": publisher_id,
                "user_id": payload.get("user_id"),
                "category_id": payload.get("category_id"),
                "status": payload.get("status"),
                "role_id":payload.get(14),
                "role_name":payload.get("PUBLISHER")
            }
        )

        db.commit()
        return publisher_id

    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create publisher: {str(e)}")


# -------------------------------------------------
# UPDATE (MASTER + HISTORY)
# -------------------------------------------------
def update_publisher(db: Session, publisher_id: int, data: PublisherUpdate):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return 0

    payload["publisher_id"] = publisher_id

    update_query = text("""
        UPDATE publisher_master
        SET
            user_id = COALESCE(:user_id, user_id),
            category_id = COALESCE(:category_id, category_id),
            status = COALESCE(:status, status)
        WHERE publisher_id = :publisher_id
    """).bindparams(
        bindparam("category_id", type_=JSONB)
    )

    history_query = text("""
        INSERT INTO publisher_master_history (
            publisher_id,
            user_id,
            category_id,
            status
        )
        SELECT
            publisher_id,
            user_id,
            category_id,
            status
        FROM publisher_master
        WHERE publisher_id = :publisher_id
    """)

    try:
        result = db.execute(update_query, payload)

        if result.rowcount > 0:
            db.execute(history_query, {"publisher_id": publisher_id})

        db.commit()
        return result.rowcount

    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update publisher: {str(e)}")


# -------------------------------------------------
# GET BY ID
# -------------------------------------------------
# def get_publisher(db: Session, publisher_id: int):
#     query = text("""
#         SELECT
#             pm.publisher_id,
#             pm.user_id,
#             u.username,
#             u.email,
#             pm.category_id,
#             string_agg(c.category_name, ', ') AS category_names,
#             pm.status
#         FROM publisher_master pm
#         JOIN users u
#             ON pm.user_id = u.user_id
#         JOIN LATERAL jsonb_array_elements_text(pm.category_id) AS cat_id(value)
#             ON TRUE
#         JOIN category_master c
#             ON c.category_id = cat_id.value::int
#         WHERE pm.publisher_id = :publisher_id
#         GROUP BY
#             pm.publisher_id,
#             pm.user_id,
#             u.username,
#             pm.category_id,
#             pm.status
#     """)

#     result = db.execute(
#         query,
#         {"publisher_id": publisher_id}
#     ).mappings().first()

#     return result
# def get_publisher(db: Session, publisher_id: int):
#     query = text("""
#         SELECT
#             pm.publisher_id,
#             pm.user_id,
#             u.username,
#             u.email,
#             u.first_name,
#             u.last_name,
#             pm.status,
#             COALESCE(
#                 json_agg(
#                     jsonb_build_object(
#                         'is_deleted', c.is_deleted,
#                         'category_id', c.category_id,
#                         'description', c.description,
#                         'category_name', c.category_name
#                     )
#                 ) FILTER (WHERE c.category_id IS NOT NULL),
#                 '[]'
#             ) AS category
#         FROM publisher_master pm
#         JOIN users u
#             ON pm.user_id = u.user_id
#         LEFT JOIN LATERAL jsonb_array_elements_text(
#             COALESCE(pm.category_id, '[]'::jsonb)
#         ) AS cat_id(value) ON TRUE
#         LEFT JOIN category_master c
#             ON c.category_id = cat_id.value::int
#         WHERE pm.publisher_id = :publisher_id
#         GROUP BY
#             pm.publisher_id,
#             pm.user_id,
#             u.username,
#             u.email,
#             pm.status,
#             u.first_name,
#             u.last_name
#     """)

#     result = db.execute(
#         query,
#         {"publisher_id": publisher_id}
#     ).mappings().first()

#     return result
def get_publisher(db: Session, publisher_id: int):
    query = text("""
        SELECT
            pm.publisher_id,
            pm.user_id,
            u.username,
            u.email,
            u.first_name,
            u.last_name,
            pm.status,
            pm.role_id,
            pm.role_name,
            COALESCE(
                json_agg(
                    jsonb_build_object(
                        'is_deleted', c.is_deleted,
                        'category_id', c.category_id,
                        'description', c.description,
                        'category_name', c.category_name
                    )
                ) FILTER (WHERE c.category_id IS NOT NULL),
                '[]'
            ) AS category
        FROM publisher_master pm
        JOIN users u
            ON pm.user_id = u.user_id
        LEFT JOIN LATERAL jsonb_array_elements_text(
            COALESCE(pm.category_id, '[]'::jsonb)
        ) AS cat_id(value) ON TRUE
        LEFT JOIN category_master c
            ON c.category_id = cat_id.value::int
        WHERE pm.publisher_id = :publisher_id
        GROUP BY
            pm.publisher_id,
            pm.user_id,
            u.username,
            u.email,
            pm.status,
            u.first_name,
            u.last_name,
            pm.role_id,
            pm.role_name
    """)

    result = db.execute(
        query,
        {"publisher_id": publisher_id}
    ).mappings().first()

    return result

# -------------------------------------------------
# GET ALL
# -------------------------------------------------
# def get_all_publishers(db: Session):
#     query = text("""
#         SELECT
#             MAX(t.publisher_id) AS publisher_id,
#             t.user_id,
#             t.username,
#             t.email,
#             t.first_name,
#             t.last_name,
#             JSONB_AGG(
#                 JSONB_BUILD_OBJECT(
#                     'category_id', t.category_id,
#                     'category_name', t.category_name,
#                     'description', t.description,
#                     'is_deleted', t.is_deleted
#                 )
#                 ORDER BY t.category_id
#             ) AS category,

#             COUNT(t.category_id) AS category_count,

#             CASE
#                 WHEN BOOL_OR(t.status = 'ACTIVE') THEN 'ACTIVE'
#                 ELSE 'INACTIVE'
#             END AS status

#         FROM (
#             SELECT
#                 pm.publisher_id,
#                 pm.user_id,
#                 u.username,
#                 u.email,
#                 u.first_name,
#                 u.last_name,
#                 pm.status,
#                 c.category_id,
#                 c.category_name,
#                 c.description,
#                 c.is_deleted

#             FROM publisher_master pm

#             LEFT JOIN users u
#                 ON pm.user_id = u.user_id

#             -- 🔥 Expand JSONB array
#             LEFT JOIN LATERAL
#                 jsonb_array_elements_text(pm.category_id) AS cat_id(value)
#                 ON TRUE

#             -- 🔥 Join category using extracted value
#             LEFT JOIN category_master c
#                 ON c.category_id = cat_id.value::int

#             WHERE pm.status != 'DELETED'
#         ) t

#         GROUP BY
#             t.user_id,
#             t.username,
#             t.email,
#             t.first_name,
#             t.last_name

#         ORDER BY
#             publisher_id DESC
#     """)

#     result = db.execute(query).mappings().all()
#     return result
def get_all_publishers(db: Session):
    query = text("""
        SELECT
            MAX(t.publisher_id) AS publisher_id,
            t.user_id,
            t.username,
            t.email,
            t.first_name,
            t.last_name,
            JSONB_AGG(
                JSONB_BUILD_OBJECT(
                    'category_id', t.category_id,
                    'category_name', t.category_name,
                    'description', t.description,
                    'is_deleted', t.is_deleted
                )
                ORDER BY t.category_id
            ) AS category,

            COUNT(t.category_id) AS category_count,

            CASE
                WHEN BOOL_OR(t.status = 'ACTIVE') THEN 'ACTIVE'
                ELSE 'INACTIVE'
            END AS status,
            t.role_id,
            t.role_name
        FROM (
            SELECT
                pm.publisher_id,
                pm.user_id,
                u.username,
                u.email,
                u.first_name,
                u.last_name,
                pm.status,
                c.category_id,
                c.category_name,
                c.description,
                c.is_deleted,
                pm.role_id,
                pm.role_name
            FROM publisher_master pm

            LEFT JOIN users u
                ON pm.user_id = u.user_id

            -- 🔥 Expand JSONB array
            LEFT JOIN LATERAL
                jsonb_array_elements_text(pm.category_id) AS cat_id(value)
                ON TRUE

            -- 🔥 Join category using extracted value
            LEFT JOIN category_master c
                ON c.category_id = cat_id.value::int

            WHERE pm.status != 'DELETED'
        ) t

        GROUP BY
            t.user_id,
            t.username,
            t.email,
            t.first_name,
            t.last_name,
            t.role_id,
            t.role_name

        ORDER BY
            publisher_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result

# -------------------------------------------------
# GET ALL BY USER
# -------------------------------------------------
def get_all_publishers_by_user(db: Session, user_id: int):
    query = text("""
        SELECT
            MAX(t.publisher_id) AS publisher_id,
            t.user_id,
            t.username,

            JSONB_AGG(
                JSONB_BUILD_OBJECT(
                    'category_id', t.category_id,
                    'category_name', t.category_name,
                    'description', t.description,
                    'is_deleted', t.is_deleted
                )
                ORDER BY t.category_id
            ) AS category,

            COUNT(t.category_id) AS category_count,

            CASE
                WHEN BOOL_OR(t.status = 'ACTIVE') THEN 'ACTIVE'
                ELSE 'INACTIVE'
            END AS status

        FROM (
            SELECT
                pm.publisher_id,
                pm.user_id,
                u.username,
                pm.status,
                c.category_id,
                c.category_name,
                c.description,
                c.is_deleted

            FROM publisher_master pm

            LEFT JOIN users u
                ON pm.user_id = u.user_id

            LEFT JOIN LATERAL
                jsonb_array_elements_text(pm.category_id) AS cat_id(value)
                ON TRUE

            LEFT JOIN category_master c
                ON c.category_id = cat_id.value::int

            WHERE pm.status != 'DELETED'
            AND pm.user_id = :user_id
        ) t

        GROUP BY
            t.user_id,
            t.username

        ORDER BY
            publisher_id DESC
    """)

    result = db.execute(query, {"user_id": user_id}).mappings().all()
    return result


# -------------------------------------------------
# STATUS ACTIVE / INACTIVE + HISTORY
# -------------------------------------------------
def update_publisher_status(
    db: Session,
    publisher_id: int,
    status: str
):
    # update_query = text("""
    #     UPDATE publisher_master
    #     SET
    #         status = :status
    #     WHERE publisher_id = :publisher_id
    # """)
    update_query = text("""
    UPDATE publisher_master
    SET
        status = :status,
        role_id = CASE
                    WHEN :status = 'INACTIVE' THEN 0
                    ELSE role_id
                 END
    WHERE publisher_id = :publisher_id
    """)

    history_query = text("""
        INSERT INTO publisher_master_history (
            publisher_id,
            user_id,
            category_id,
            status
        )
        SELECT
            publisher_id,
            user_id,
            category_id,
            status
        FROM publisher_master
        WHERE publisher_id = :publisher_id

    """)

    try:
        result = db.execute(
            update_query,
            {
                "publisher_id": publisher_id,
                "status": status
            }
        )
        if result.rowcount == 0:
            raise Exception("Publisher not found or already deleted")
        # 🔹 Snapshot after update
        db.execute(history_query, {"publisher_id": publisher_id})

        db.commit()

        return {
            "publisher_id": publisher_id,
            "status": status
        }

    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update publisher status: {str(e)}")
