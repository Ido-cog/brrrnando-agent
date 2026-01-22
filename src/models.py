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

from enum import Enum
from typing import List, Dict, Any

class WeatherSource(str, Enum):
    OPEN_METEO = "Open-Meteo"
    SNOW_FORECAST = "Snow-Forecast.com"
    AGGREGATED = "Aggregated"

class ConfidenceLevel(str, Enum):
    HIGH = "High"         # Sources agree closely
    MEDIUM = "Medium"     # Sources diverge somewhat
    LOW = "Low"          # Significant disagreement or single source failure

class DailySnowForecast(BaseModel):
    date: date
    snowfall_cm: float
    source: WeatherSource

class AggregatedForecast(BaseModel):
    total_weekly_snow_cm: float
    confidence: ConfidenceLevel
    primary_source_data: Dict[str, Any] # e.g. Open-Meteo raw
    secondary_source_data: Dict[str, Any] # e.g. Snow-Forecast parsed
    sources_used: List[WeatherSource]
