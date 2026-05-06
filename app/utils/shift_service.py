
from app.utils.sql_utils import execute, fetch_one, now_utc

from fastapi import HTTPException, status

def get_current_incharge(conn, station_id):
    return fetch_one(
        conn,
        """
        SELECT *
        FROM station_shift_incharge
        WHERE station_id = :station
          AND responsibility_to IS NULL
        LIMIT 1
        """,
        {"station": station_id}
    )
from fastapi import HTTPException, status
from app.utils.sql_utils import execute, fetch_one, now_utc

def request_handover(
    conn,
    comment_for_next_incharge: str,
    station_id: int,
    shift_id: int,
    from_user: int,
    to_user: int
):
    now = now_utc()

    # 🔎 fetch correct active shift incharge
    current = get_current_incharge(conn, station_id)

    if not current or current["user_id"] != from_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not the active shift in-charge"
        )

    # ✅ UPDATE station_shift_incharge
    execute(
        conn,
        """
        UPDATE station_shift_incharge
        SET
            handover_requested_at = :now,
            handover_to_user_id = :to_user,
            comment_for_next_incharge = :comment
        WHERE id = :id
        """,
        {
            "now": now,
            "to_user": to_user,
            "comment": comment_for_next_incharge,
            "id": current["id"]
        }
    )

    # ✅ INSERT audit log
    execute(
        conn,
        """
        INSERT INTO shift_handover_log (
            station_id,
            shift_id,
            from_user_id,
            to_user_id,
            comment_for_next_incharge,
            event_type,
            event_time
        )
        VALUES (
            :station,
            :shift,
            :from_u,
            :to_u,
            :comment,
            'HANDOVER_REQUESTED',
            :now
        )
        """,
        {
            "station": station_id,
            "shift": shift_id,
            "from_u": from_user,
            "to_u": to_user,
            "comment": comment_for_next_incharge,
            "now": now
        }
    )

    # 🔥 THIS WAS MISSING
    conn.commit()

def accept_handover(conn, station_id, shift_id, accepting_user):
    now = now_utc()

    # 🔒 lock current responsibility
    current = fetch_one(
        conn,
        """
        SELECT *
        FROM station_shift_incharge
        WHERE station_id = :station
          AND responsibility_to IS NULL
          AND handover_to_user_id = :user
        FOR UPDATE
        """,
        {"station": station_id, "user": accepting_user}
    )
    if not current:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Handover already accepted or invalid"
        )

    # close old responsibility
    execute(
        conn,
        """
        UPDATE station_shift_incharge
        SET responsibility_to = :now,
            handover_accepted_at = :now
        WHERE id = :id
        """,
        {"now": now, "id": current["id"]}
    )

    # create new responsibility
    execute(
        conn,
        """
        INSERT INTO station_shift_incharge
        (station_id, shift_id, user_id, responsibility_from)
        VALUES (:station, :shift, :user, :from_t)
        """,
        {
            "station": station_id,
            "shift": shift_id,
            "user": accepting_user,
            "from_t": now
        }
    )

    # audit
    execute(
        conn,
        """
        INSERT INTO shift_handover_log
        (station_id, shift_id, from_user_id, to_user_id, event_type, event_time)
        VALUES (:station, :shift, :from_u, :to_u, 'HANDOVER_ACCEPTED', :now)
        """,
        {
            "station": station_id,
            "shift": shift_id,
            "from_u": current["user_id"],
            "to_u": accepting_user,
            "now": now
        }
    )   
    conn.commit()


