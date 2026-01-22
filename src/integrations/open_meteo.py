import requests
from typing import Dict, Any

def get_open_meteo_data(lat: float, lon: float, elevation: int = None) -> Dict[str, Any]:
    """
    Fetch current and forecast weather data from Open-Meteo.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,snowfall,snow_depth",
        "daily": "snowfall_sum,wind_speed_10m_max",
        "timezone": "auto",
        "forecast_days": 7
    }
    if elevation is not None:
        params["elevation"] = elevation
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching Open-Meteo weather: {e}")
        return {}
