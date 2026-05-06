from fastapi import APIRouter, Depends, Request
from requests import Session
from app.crud.digital_logbook.geo_fencing.verification_logic import get_active_token_for_user, validate_ip_geo_and_issue_token, verify_location_token
from app.database import get_db
from app.schemas.digital_logbook.geo_fencing.geo_laa_schemas import AccessTokenGetResponse
from fastapi import APIRouter, Depends, Request, Query

router = APIRouter(prefix="/access", tags=["Location Access"])

@router.get(
    "/token",
    response_model=AccessTokenGetResponse,
    summary="Get or generate location access token"
)
def get_or_generate_token(
    user_id: int = Query(..., description="User ID"),
    lat: float | None = Query(None, description="Latitude"),
    lon: float | None = Query(None, description="Longitude"),
    request: Request = None,
    db: Session = Depends(get_db)
):
    ip = request.client.host
    header_token = request.headers.get("X-Location-Token")

    print("\n==============================")
    print("DEBUG: get_or_generate_token")
    print("User ID:", user_id)
    print("IP:", ip)
    print("Header Token:", header_token)
    print("Query Lat:", lat)
    print("Query Lon:", lon)
    print("==============================")

    # ---------------- STEP 1: HEADER TOKEN ----------------
    if header_token:
        row = verify_location_token(db, header_token)
        if row:
            return {
                "status": "SUCCESS",
                "token": row["token"],
                "expires_at": row["expires_at"]
            }

    # ---------------- STEP 2: ACTIVE DB TOKEN ----------------
    row = get_active_token_for_user(db, user_id)
    if row:
        return {
            "status": "SUCCESS",
            "token": row["token"],
            "expires_at": row["expires_at"]
        }

    # ---------------- STEP 3: IP / GEO ----------------
    if lat is not None and lon is not None:
        result = validate_ip_geo_and_issue_token(
            db=db,
            user_id=user_id,
            ip=ip,
            lat=lat,
            lon=lon
        )

        if result:
            token, expiry = result
            return {
                "status": "SUCCESS",
                "token": token,
                "expires_at": expiry
            }

    # ---------------- STEP 4: APPROVAL ----------------
    return {
        "status": "DENIED",
        "next_action": "REQUEST_SHIFT_INCHARGE_APPROVAL"
    }