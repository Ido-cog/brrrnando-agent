from typing import Dict, Any, List
from ..models import WeatherSource, ConfidenceLevel
from .open_meteo import get_open_meteo_data
from .snow_forecast import get_snow_forecast_data

def get_weather_data(lat: float, lon: float, resort_name: str, elevation: int = None) -> Dict[str, Any]:
    """
    Fetch weather data from multiple sources and aggregate snow forecasts.
    
    Args:
        lat: Latitude
        lon: Longitude
        resort_name: Name of the resort (for scraping)
        elevation: Elevation in meters (optional)
        
    Returns:
        Dict containing:
        - temp_current
        - wind_current
        - snow_depth
        - weekly_snowfall_forecast_cm (Aggregated)
        - forecast_confidence
        - sources (List of strings)
    """
    # 1. Fetch Open-Meteo (Primary for current weather & backup for snow)
    om_data = get_open_meteo_data(lat, lon, elevation)
    
    # 2. Fetch Snow-Forecast (Primary for snow forecast)
    # Map elevation to 'mid'/'top'/'bot' loosely if needed, or just default to 'mid' 
    # as configured in scraper for now.
    # Future improvement: map elevation int to 'top'/'mid'/'bot' logic.
    sf_elevation = "mid" 
    sf_data = get_snow_forecast_data(resort_name, sf_elevation)
    
    # 3. Process Open-Meteo Data
    om_snow_cm = 0.0
    current_temp = None
    current_wind = None
    snow_depth = 0.0
    
    if om_data:
        current = om_data.get("current", {})
        current_temp = current.get("temperature_2m")
        current_wind = current.get("wind_speed_10m")
        snow_depth = current.get("snow_depth", 0)
        
        daily_snow_sum = om_data.get("daily", {}).get("snowfall_sum", [])
        # Sum next 6 days to match Snow-Forecast (approx)
        om_snow_cm = sum(daily_snow_sum[:6]) 
    
    # 4. Aggregation Logic
    aggregated_snow = 0.0
    confidence = ConfidenceLevel.LOW
    sources = []
    
    sf_snow_cm = sf_data.get("total_snow_cm")
    
    if om_data and sf_data:
        # Both sources available
        sources = [WeatherSource.OPEN_METEO, WeatherSource.SNOW_FORECAST]
        
        # Average
        aggregated_snow = (om_snow_cm + sf_snow_cm) / 2
        
        # Confidence Calculation
        diff = abs(om_snow_cm - sf_snow_cm)
        if diff <= 5: 
            confidence = ConfidenceLevel.HIGH
        elif diff <= 20: 
            confidence = ConfidenceLevel.MEDIUM
        else:
            confidence = ConfidenceLevel.LOW
            
    elif sf_data:
        # Only Snow-Forecast
        sources = [WeatherSource.SNOW_FORECAST]
        aggregated_snow = sf_snow_cm
        confidence = ConfidenceLevel.MEDIUM # Trusted source
        
    elif om_data:
        # Only Open-Meteo
        sources = [WeatherSource.OPEN_METEO]
        aggregated_snow = om_snow_cm
        confidence = ConfidenceLevel.MEDIUM # Single source
        
    else:
        # No data
        confidence = ConfidenceLevel.LOW
        
    return {
        "temp_current": current_temp,
        "wind_current": current_wind,
        "snow_depth": snow_depth,
        "weekly_snowfall_forecast_cm": round(aggregated_snow, 1),
        "forecast_confidence": confidence,
        "sources": [s.value for s in sources],
        "debug_om_snow": round(om_snow_cm, 1),
        "debug_sf_snow": sf_snow_cm
    }
