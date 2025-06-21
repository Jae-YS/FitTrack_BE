from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from datetime import date
from backend.db.session import get_db
from backend.models.schemas.route_schema import RouteRequest
from backend.models.sql_models import SuggestedWorkout
from backend.services.route_service import generate_route_geojson

router = APIRouter()


@router.post("/generate-route")
def generate_route(request: RouteRequest, db: Session = Depends(get_db)):
    # Get today's workout for the user
    today = date.today()
    workout = (
        db.query(SuggestedWorkout)
        .filter(SuggestedWorkout.user_id == request.user_id)
        .filter(SuggestedWorkout.recommended_date == today)
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
