from pydantic import BaseModel
from datetime import date
from typing import Optional

class Trip(BaseModel):
    resort_name: str
    flight_out_date: date
    ski_start_date: date
    ski_end_date: date
    flight_back_date: date
    lat: float
    lon: float
    road_check: str
    summit_elevation: Optional[int] = None
    base_elevation: Optional[int] = None
