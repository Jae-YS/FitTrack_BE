import requests
import random
import math
from backend.core.config import settings
from typing import List

ORS_BASE_URL = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"


def _offset_point(
    lat: float, lon: float, distance_km: float, angle_deg: float
) -> List[float]:
    """Generate a point offset from the origin by a distance and angle (approximate)."""
    dx = distance_km * math.cos(math.radians(angle_deg))
    dy = distance_km * math.sin(math.radians(angle_deg))
    return [lon + dx / 111, lat + dy / 111]


# Generate a route GeoJSON with a random mid-point offset from the start point
def generate_route_geojson(
    start_lat: float, start_lon: float, target_distance_km: float, count: int = 3
) -> List[dict]:
    """Return full GeoJSON LineString geometry for each route."""
    routes = []

    for _ in range(count):
        angle = random.randint(0, 360)
        mid_point = _offset_point(start_lat, start_lon, target_distance_km / 2.5, angle)
        coordinates = [[start_lon, start_lat], mid_point, [start_lon, start_lat]]

        res = requests.post(
            ORS_BASE_URL,
            headers={
                "Authorization": settings.ORS_API_KEY,
                "Content-Type": "application/json",
            },
            json={"coordinates": coordinates, "instructions": False},
        )

        if not res.ok:
            print(f"ORS error {res.status_code}: {res.text}")
            continue

        data = res.json()
        print("ORS response:", data)

        if "features" not in data or not data["features"]:
            print("No features in ORS response")
            continue

        feature = data["features"][0]
        geometry = feature["geometry"]
        summary = feature.get("properties", {}).get("summary", {})

        actual_distance_km = summary.get("distance", 0) / 1000
        duration_min = summary.get("duration", 0) / 60

        print(f"Generated route: {actual_distance_km:.2f} km, {duration_min:.1f} min")

        if target_distance_km * 0.7 < actual_distance_km < target_distance_km * 1.3:
            routes.append(
                {
                    "type": "Feature",
                    "geometry": geometry,
                    "properties": {
                        "distance_km": round(actual_distance_km, 2),
                        "duration_min": round(duration_min, 1),
                    },
                }
            )
        else:
            print("Rejected route due to distance mismatch")

    return {"type": "FeatureCollection", "features": routes}
