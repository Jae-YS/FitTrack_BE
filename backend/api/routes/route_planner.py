from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from datetime import date
from backend.db.session import get_db
from backend.schemas.route_schema import RouteRequest
from backend.db.models.planned_workout import PlannedWorkout
from backend.services.route_service import generate_route_geojson
import httpx


router = APIRouter(prefix="/route-planner", tags=["Route Planner"])


# Generate a route based on the user's location and today's workout distance
@router.post("/generate-route")
def generate_route(request: RouteRequest, db: Session = Depends(get_db)):
    # Get today's workout for the user
    today = date.today()
    workout = (
        db.query(PlannedWorkout)
        .filter(PlannedWorkout.user_id == request.user_id)
        .filter(PlannedWorkout.recommended_date == today)
        .first()
    )

    if not workout or not workout.distance_km:
        raise HTTPException(
            status_code=404, detail="No distance found for today's workout."
        )

    print(workout.distance_km)

    routes = generate_route_geojson(
        start_lat=request.start_lat,
        start_lon=request.start_lng,
        target_distance_km=workout.distance_per_workout,
    )

    return {
        "user_id": request.user_id,
        "routes": routes,
    }


#   # Geocode an address using Nominatim
@router.get("/geocode")
async def geocode_address(q: str = Query(..., description="Address to geocode")):
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "fittrack-ai-backend (youremail@example.com)"}
    params = {"format": "json", "q": q}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail="Failed to fetch from Nominatim"
            )

        results = response.json()
        if not results:
            raise HTTPException(status_code=404, detail="Location not found")

        return {
            "lat": float(results[0]["lat"]),
            "lon": float(results[0]["lon"]),
        }
