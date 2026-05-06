from fastapi import APIRouter, Depends, HTTPException, Request
from requests import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.digital_logbook.geo_fencing.common import AccessTokenResponse, AccessValidationSchema
from app.utils.access_service import issue_token, validate_ip_or_geo


router = APIRouter(prefix="/access", tags=["Access"])


@router.post("/validate", response_model=AccessTokenResponse)
def validate_access(
    payload: AccessValidationSchema,
    request: Request,
    db=Depends(get_db)
):
    ip = request.client.host
    print("ip",ip)

    result = validate_ip_or_geo(
        db,
        ip,
        payload.latitude,
        payload.longitude
    )

    if not result:
        raise HTTPException(
            status_code=403,
            detail="IP / Location not allowed"
        )

    token, expiry = issue_token(
        db,
        payload.user_id,
        ip,
        payload.latitude,
        payload.longitude,
        result   # IP or GEO
    )

    return {
        "token": token,
        "expires_at": expiry
    }








