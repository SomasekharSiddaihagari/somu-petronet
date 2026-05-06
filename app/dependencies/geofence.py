from fastapi import Header, HTTPException, status
from app.core.geofence import is_within_allowed_zone

def geo_fence_dependency(
    x_latitude: float = Header(..., description="Latitude in decimal degrees"),
    x_longitude: float = Header(..., description="Longitude in decimal degrees")
):
    if not is_within_allowed_zone(x_latitude, x_longitude):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: outside 3 KM geo-fence"
        )
