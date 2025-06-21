from pydantic import BaseModel


class RouteRequest(BaseModel):
    user_id: int
    start_lat: float
    start_lng: float
