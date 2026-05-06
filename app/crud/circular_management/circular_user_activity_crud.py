from sqlalchemy import text
from sqlalchemy.orm import Session

def mark_circular_as_read(db: Session, circular_id: int, user_id: int):
    # query = text("""
    #     INSERT INTO circular_user_activity (
    #         circular_id,
    #         user_id,
    #         is_read,
    #         read_at,
    #         created_at,
    #         updated_at
    #     )
    #     VALUES (
    #         :circular_id,
    #         :user_id,
    #         TRUE,
    #         now(),
    #         now(),
    #         now()
    #     )
    # """)

    # db.execute(query, {
    #     "circular_id": circular_id,
    #     "user_id": user_id
    # })
    # db.commit()

    # return True
    check_query = text("""
        SELECT 1
        FROM circular_user_activity
        WHERE circular_id = :circular_id
        AND user_id = :user_id
    """)

    result = db.execute(check_query, {
        "circular_id": circular_id,
        "user_id": user_id
    }).fetchone()

    if result:
        # 2️⃣ Update existing record
        update_query = text("""
            UPDATE circular_user_activity
            SET
                is_read = TRUE,
                read_at = NOW(),
                updated_at = NOW()
            WHERE circular_id = :circular_id
            AND user_id = :user_id
        """)

        db.execute(update_query, {
            "circular_id": circular_id,
            "user_id": user_id
        })

    else:
        # 3️⃣ Insert new record
        insert_query = text("""
            INSERT INTO circular_user_activity (
                circular_id,
                user_id,
                is_read,
                read_at,
                created_at,
                updated_at
            )
            VALUES (
                :circular_id,
                :user_id,
                TRUE,
                NOW(),
                NOW(),
                NOW()
            )
        """)

        db.execute(insert_query, {
            "circular_id": circular_id,
            "user_id": user_id
        })

    db.commit()

    return True

def acknowledge_circular(db: Session, circular_id: int, user_id: int):
    query = text("""
        UPDATE circular_user_activity
        SET
            is_acknowledged = TRUE,
            acknowledged_at = now(),
            updated_at = now()
        WHERE circular_id = :circular_id
          AND user_id = :user_id
    """)

    result = db.execute(query, {
        "circular_id": circular_id,
        "user_id": user_id
    })
    db.commit()

    return result.rowcount > 0


# def get_user_circular_activity(db: Session, circular_id: int, user_id: int):
#     query = text("""
#         SELECT
#             circular_id,
#             user_id,
#             is_read,
#             is_acknowledged,
#             read_at,
#             acknowledged_at
#         FROM circular_user_activity
#         WHERE circular_id = :circular_id
#           AND user_id = :user_id
#     """)

#     return db.execute(query, {
#         "circular_id": circular_id,
#         "user_id": user_id
#     }).mappings().first()

def get_circular_user_activity(db, circular_id: int):
    query = text("""
        WITH audience_users AS (

    SELECT DISTINCT u.user_id
    FROM circular_target_audience ca
    JOIN users u ON (
        /* 1️⃣ INDIVIDUAL */
        (
            ca.audience_type = 'INDIVIDUAL'
            AND u.user_id IN (
                SELECT ind.value::INT
                FROM jsonb_array_elements_text(ca.audience_ref_id) AS ind(value)
            )
        )

        OR

        /* 2️⃣ STATION */
        (
            ca.audience_type = 'STATION'
            AND u.station_id IN (
                SELECT st.value::INT
                FROM jsonb_array_elements_text(ca.audience_ref_id) AS st(value)
            )
        )

        OR

        /* 3️⃣ GROUP */
        (
            ca.audience_type = 'GROUP'
            AND u.user_id IN (
                SELECT emp.value::INT
                FROM group_master gm
                JOIN jsonb_array_elements_text(ca.audience_ref_id) AS gid(value)
                  ON gm.group_id = gid.value::INT
                JOIN jsonb_array_elements_text(gm.employee_ids) AS emp(value)
                  ON TRUE
            )
        )
    )
    WHERE ca.circular_id = :circular_id
      AND u.is_deleted = FALSE
)

SELECT DISTINCT
    u.user_id,
    u.username AS employee_name,
    u.first_name,
    u.last_name,
    u.station_id,
    s.station_name,

    CASE
        WHEN cua.is_acknowledged = TRUE THEN 'Acknowledged'
        WHEN cua.is_read = TRUE THEN 'Read'
        ELSE 'Unread'
    END AS status,

    cua.read_at,
    cua.acknowledged_at

FROM audience_users au
JOIN users u ON u.user_id = au.user_id
JOIN station s ON s.station_id = u.station_id
LEFT JOIN circular_user_activity cua
  ON cua.user_id = u.user_id
 AND cua.circular_id = :circular_id

ORDER BY u.username;

    """)

    return db.execute(query, {"circular_id": circular_id}).mappings().all()
    # return db.execute(query, {"circular_id": circular_id}).fetchall()