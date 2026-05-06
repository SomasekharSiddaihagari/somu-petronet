# from app.utils.access_service import issue_token
# from app.utils.sql_utils import fetch_one


# def approve_access(conn, approval_id, approver_user, approver_station, ip, lat, lon):
#     approval = fetch_one(
#         conn,
#         """
#         SELECT *
#         FROM location_access_approval
#         WHERE id = :id
#           AND approved_by_station_id = :station
#         """,
#         {"id": approval_id, "station": approver_station}
#     )

#     if not approval:
#         raise Exception("Invalid approval")

#     return issue_token(
#         conn,
#         approval["requested_by_user_id"],
#         approval["requested_station_id"],
#         ip,
#         lat,
#         lon,
#         "APPROVAL",
#         approved_by=approver_user
#     )



from fastapi import HTTPException, status
from sqlalchemy import text

from app.utils.access_service import issue_token
from app.utils.sql_utils import fetch_one, now_utc


# ─────────────────────────────────────────────
# APPROVE ACCESS REQUEST
#
# Validates the approval record belongs to the
# approver's station, marks it APPROVED, then
# issues a token for the requester.
# ─────────────────────────────────────────────
def approve_access(
    conn,
    approval_id: int,
    approver_user: int,
    approver_station: int,
    ip: str,
    lat: float | None,
    lon: float | None,
) -> tuple[str, object]:

    # ── 1. Fetch and lock the pending approval ──
    approval = fetch_one(
        conn,
        """
        SELECT *
        FROM location_access_approval
        WHERE id                    = :id
          AND approved_by_station_id = :station
          AND status                 = 'PENDING'
        """,
        {"id": approval_id, "station": approver_station}
    )

    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found, already processed, or station mismatch"
        )

    # ── 2. Mark approval as APPROVED ──
    conn.execute(
        text("""
            UPDATE location_access_approval
            SET status              = 'APPROVED',
                approved_at         = NOW(),
                approved_by_user_id = :approver_user
            WHERE id = :id
        """),
        {"approver_user": approver_user, "id": approval_id}
    )

    # ── 3. Issue access token for the requester ──
    token, expiry = issue_token(
        db=conn,
        user_id=approval["requested_by_user_id"],
        station_id=approval["requested_station_id"],
        ip=ip,
        lat=lat,
        lon=lon,
        access_type="APPROVAL",
        approved_by=approver_user,
    )

    conn.commit()

    return token, expiry


# ─────────────────────────────────────────────
# REJECT ACCESS REQUEST
# ─────────────────────────────────────────────
def reject_access(
    conn,
    approval_id: int,
    approver_user: int,
    approver_station: int,
    reason: str | None = None,
) -> None:

    approval = fetch_one(
        conn,
        """
        SELECT id
        FROM location_access_approval
        WHERE id                    = :id
          AND approved_by_station_id = :station
          AND status                 = 'PENDING'
        """,
        {"id": approval_id, "station": approver_station}
    )

    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found, already processed, or station mismatch"
        )

    conn.execute(
        text("""
            UPDATE location_access_approval
            SET status              = 'REJECTED',
                approved_at         = NOW(),
                approved_by_user_id = :approver_user,
                reason              = :reason
            WHERE id = :id
        """),
        {"approver_user": approver_user, "reason": reason, "id": approval_id}
    )

    conn.commit()