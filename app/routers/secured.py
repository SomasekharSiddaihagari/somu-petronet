from fastapi import APIRouter, Depends
from app.dependencies.geofence import geo_fence_dependency

router = APIRouter(
    prefix="/geo-api ",
    tags=["Secured APIs"],
    dependencies=[Depends(geo_fence_dependency)]
)

@router.get("/data")
def secured_data():
    return {
        "message": "You are inside the 3 KM geo-fence"
    }

@router.post("/action")
def secured_action():
    return {
        "status": "Action allowed within geo-fence"
    }
