import math
from typing import List, Dict

# 3 KM GEOFENCE CENTER (Decimal Degrees)
ALLOWED_ZONES: List[Dict] = [
    {
        "name": "bangalore_zone",
        "center": (12.9930234, 77.7153992),
        "radius": 3000  # meters
    }
]

def haversine_distance(
    lat1: float, lon1: float,
    lat2: float, lon2: float
) -> float:
    """
    Calculate distance between two lat/lon points in meters
    """
    R = 6371000  # Earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(d_lambda / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def is_within_allowed_zone(lat: float, lon: float) -> bool:
    """
    Check if given coordinates fall within any allowed zone
    """
    for zone in ALLOWED_ZONES:
        distance = haversine_distance(
            lat,
            lon,
            zone["center"][0],
            zone["center"][1]
        )
        if distance <= zone["radius"]:
            return True

    return False
