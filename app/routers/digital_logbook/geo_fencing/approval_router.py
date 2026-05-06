from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy import text
from fastapi import HTTPException, Request
from app.schemas.digital_logbook.geo_fencing.geo_laa_schemas import ApproveRequestSchema, RejectRequestSchema

import uuid
from sqlalchemy import text
import secrets

# ---------- POST ----------
class AccessRequestSchema(BaseModel):
    requested_station_id: int
    requested_by_user_id: int
    approved_by_user_id: int
    reason: str | None
    approved_by_station_id: int


# ---------- PUT (Approve / Reject) ----------
class ApprovalUpdateSchema(BaseModel):
    status: str  # "APPROVED" or "REJECTED"


# ---------- RESPONSE ----------
class ApprovalResponseSchema(BaseModel):
    id: int
    requested_station_id: int
    requested_by_user_id: int
    approved_by_user_id: int
    approved_by_station_id: int
    reason: str | None
    status: str



# def create_access_request(db, payload: AccessRequestSchema):
#     query = text("""
#         INSERT INTO location_access_approval (
#             requested_station_id,
#             requested_by_user_id,
#             approved_by_user_id,
#             approved_by_station_id,
#             reason,
#             status,expires_at
#         )
#         VALUES (
#             :requested_station_id,
#             :requested_by_user_id,
#             :approved_by_user_id,
#             :approved_by_station_id,
#             :reason,
#             'PENDING',
#             NOW()
#         )
#         RETURNING
#             id,
#             requested_station_id,
#             requested_by_user_id,
#             approved_by_user_id,
#             approved_by_station_id,
#             reason,
#             status
#     """)

#     result = db.execute(query, payload.model_dump())
#     row = result.mappings().first()
#     db.commit()
#     return row

from fastapi import HTTPException
from sqlalchemy import text

def create_access_request(db, payload: AccessRequestSchema):
    # Step 1: Check AccessControlStation for this station
    check_query = text("""
        SELECT is_active, ip_from, ip_to, lat, lon, radius
        FROM access_control_station
        WHERE station_id = :station_id
        LIMIT 1
    """)

    result = db.execute(check_query, {"station_id": payload.requested_station_id})
    control = result.mappings().first()

    # Step 2: Not added by admin at all
    if not control:
    # Allow approval flow instead of blocking
        pass

    # Step 3: Added but turned off by admin
    if control and not control["is_active"]:
    # Still allow approval request
        pass

    insert_query = text("""
    INSERT INTO location_access_approval (
        requested_station_id,
        requested_by_user_id,
        approved_by_user_id,
        approved_by_station_id,
        reason,
        status,
        expires_at
    )
    VALUES (
        :requested_station_id,
        :requested_by_user_id,
        :approved_by_user_id,
        :approved_by_station_id,
        :reason,
        'PENDING',
        NOW() + INTERVAL '1 hour'    -- ✅ fixed
    )
    RETURNING
        id,
        requested_station_id,
        requested_by_user_id,
        approved_by_user_id,
        approved_by_station_id,
        reason,
        status
""")

    result = db.execute(insert_query, payload.model_dump())
    row = result.mappings().first()
    db.commit()
    return row

# def create_access_request(db, payload: AccessRequestSchema):
#     # Step 1: Check if station IP/Geo config exists at all
#     check_query = text("""
#         SELECT is_active
#         FROM access_control_station
#         WHERE station_id = :station_id
#         LIMIT 1
#     """)

#     result = db.execute(check_query, {"station_id": payload.requested_station_id})
#     control = result.mappings().first()

#     # Step 2: IP/Geo not added by admin at all
#     if not control:
#         raise HTTPException(
#             status_code=403,
#             detail="IP not present, please contact Admin to add it"
#         )

#     # Step 3: IP exists but admin has turned it off
#     if not control["is_active"]:
#         raise HTTPException(
#             status_code=403,
#             detail="Admin hasn't given access, please contact Admin"
#         )

#     # Step 4: All good — insert the request
#     insert_query = text("""
#         INSERT INTO location_access_approval (
#             requested_station_id,
#             requested_by_user_id,
#             approved_by_user_id,
#             approved_by_station_id,
#             reason,
#             status,
#             expires_at
#         )
#         VALUES (
#             :requested_station_id,
#             :requested_by_user_id,
#             :approved_by_user_id,
#             :approved_by_station_id,
#             :reason,
#             'PENDING',
#             NOW()
#         )
#         RETURNING
#             id,
#             requested_station_id,
#             requested_by_user_id,
#             approved_by_user_id,
#             approved_by_station_id,
#             reason,
#             status
#     """)

#     result = db.execute(insert_query, payload.model_dump())
#     row = result.mappings().first()
#     db.commit()
#     return row




def update_access_status(db, approval_id: int, status: str):
    if status not in ("APPROVED", "REJECTED"):
        raise HTTPException(400, "Invalid status")

    query = text("""
        UPDATE location_access_approval
        SET
            status = :status,
            approved_at = NOW()
        WHERE id = :id
          AND status = 'PENDING'
        RETURNING
            id,
            requested_station_id,
            requested_by_user_id,
            approved_by_user_id,
            approved_by_station_id,
            status
    """)

    result = db.execute(query, {
        "id": approval_id,
        "status": status
    })

    row = result.mappings().first()
    if not row:
        raise HTTPException(
            400,
            "Request not found or already processed"
        )

    db.commit()
    return row


router = APIRouter(
    prefix="/approval",
    tags=["Location Access Approval"]
)


# @router.post(
#     "/request",
#     response_model=ApprovalResponseSchema,
#     summary="Request cross-station access"
# )
# def request_access(
#     payload: AccessRequestSchema,
#     db=Depends(get_db)
# ):
#     return create_access_request(db, payload)


@router.post(
    "/request",
    response_model=ApprovalResponseSchema,
    summary="Request cross-station access"
)
def request_access(
    payload: AccessRequestSchema,
    db=Depends(get_db)
):
    return create_access_request(db, payload)





def generate_secure_token(length: int = 32) -> str:
    """
    Cryptographically secure, URL-safe token
    """
    return secrets.token_urlsafe(length)

def issue_location_token(
    db,
    user_id,
    station_id,
    ip,
    lat,
    lon,
    approver_user_id,
    access_type

):
    token = generate_secure_token()
    expiry = datetime.utcnow() + timedelta(hours=8)

    db.execute(
        text("""
            INSERT INTO location_access_token (
                user_id,
                station_id,
                token,
             access_type,
                ip_address,
                 latitude,
                longitude,
                expires_at,
                is_active,
                approved_by_user_id
            )
            VALUES (
                :user_id,
                :station_id,
                :token,
             :access_type,
                :ip,
                :lat,
                :lon,
                :expires_at,
                TRUE,
                :approver_user_id
            )
        """),
        {
            "user_id": user_id,
            "station_id": station_id,
            "token": token,
            "ip": ip,
            "lat": lat,
            "lon": lon,
            "expires_at": expiry,
            "approver_user_id": approver_user_id,
            "access_type":access_type
        }
    )

    db.commit()
    return token, expiry
def issue_location_token_approval(
    db,
    user_id: int,
    station_id: int,
    ip: str,
    lat: float,
    lon: float,
    approver_user_id: int
):
    token = str(uuid.uuid4())

    query = text("""
        INSERT INTO location_access_token (
            user_id,
            station_id,
            token,
            access_type,
            ip_address,
            latitude,
            longitude,
            approved_by_user_id,
            expires_at,
            is_active
        )
        VALUES (
            :user_id,
            :station_id,
            :token,
            'APPROVAL',
            :ip,
            :lat,
            :lon,
            :approved_by_user_id,
            NOW() + INTERVAL '1 hour',
            TRUE
        )
        RETURNING token, expires_at
    """)

    row = db.execute(query, {
        "user_id": user_id,
        "station_id": station_id,
        "token": token,
        "ip": ip,
        "lat": lat,
        "lon": lon,
        "approved_by_user_id": approver_user_id
    }).mappings().first()

    db.commit()
    return row["token"], row["expires_at"]



@router.put("/approval/approve/{approval_id}")
def approve_access_api(
    approval_id: int,
    payload: ApproveRequestSchema,
    request: Request,
    db=Depends(get_db)
):
    token, expiry = approve_access_crud(
        db=db,
        approval_id=approval_id,
        approver_user_id=payload.approver_user_id,
        ip=request.client.host,
        lat=payload.latitude,
        lon=payload.longitude,
        reason=payload.reason
    )

    return {
        "status": "APPROVED",
        "token": token,
        "expires_at": expiry
    }


@router.put("/approval/reject/{approval_id}")
def reject_access_api(
    approval_id: int,
    payload: RejectRequestSchema,
    db=Depends(get_db)
):
    reject_access_crud(
        db=db,
        approval_id=approval_id,
        approver_user_id=payload.approver_user_id,
        reason=payload.reason
    )

    return {
        "status": "REJECTED",
        "message": "Access request rejected"
    }

def reject_access_crud(
    db,
    approval_id: int,
    approver_user_id: int,
    reason: str | None
):
    approval = db.execute(text("""
        SELECT id
        FROM location_access_approval
        WHERE id = :id
          AND status = 'PENDING'
        FOR UPDATE
    """), {"id": approval_id}).first()

    if not approval:
        raise HTTPException(400, "Invalid or already processed approval")

    db.execute(text("""
        UPDATE location_access_approval
        SET status = 'REJECTED',
            approved_at = NOW(),
            reason = :reason,
            approved_by_user_id = :approver_user_id
        WHERE id = :id
    """), {
        "id": approval_id,
        "approver_user_id": approver_user_id,
        "reason": reason
    })

    db.commit()

from fastapi import HTTPException

def approve_access_crud(
    db,
    approval_id: int,
    approver_user_id: int,
    ip: str,
    lat: float,
    lon: float,
    reason: str | None
):
    approval = db.execute(text("""
        SELECT *
        FROM location_access_approval
        WHERE id = :id
          AND status = 'PENDING'
        FOR UPDATE
    """), {"id": approval_id}).mappings().first()

    if not approval:
        raise HTTPException(400, "Invalid or already processed approval")

    db.execute(text("""
        UPDATE location_access_approval
        SET status = 'APPROVED',
            approved_at = NOW(),
            approved_by_user_id = :approver_user_id,
            reason = :reason
        WHERE id = :id
    """), {
        "id": approval_id,
        "approver_user_id": approver_user_id,
        "reason": reason
    })

    token, expiry = issue_location_token_approval(
        db=db,
        user_id=approval["requested_by_user_id"],
        station_id=approval["requested_station_id"],
        ip=ip,
        lat=lat,
        lon=lon,
        approver_user_id=approver_user_id
    )

    return token, expiry
