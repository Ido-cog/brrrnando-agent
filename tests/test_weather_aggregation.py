import pytest
from unittest.mock import patch
from src.integrations.weather import get_weather_data
from src.models import WeatherSource, ConfidenceLevel

# Mock Data
MOCK_OM_DATA = {
    "current": {
        "temperature_2m": -5,
        "wind_speed_10m": 12,
        "snow_depth": 0.8
    },
    "daily": {
        "snowfall_sum": [5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0] # 10cm total over 6 days
    }
}

MOCK_SF_DATA = {
    "total_snow_cm": 12.0, # 12cm
    "forecast_days": 6,
    "source": WeatherSource.SNOW_FORECAST
}

@patch("src.integrations.weather.get_snow_forecast_data")
@patch("src.integrations.weather.get_open_meteo_data")
def test_aggregation_high_confidence(mock_om, mock_sf):
    """Test aggregation when sources agree closely (10cm vs 12cm)."""
    mock_om.return_value = MOCK_OM_DATA
    mock_sf.return_value = MOCK_SF_DATA
    
    result = get_weather_data(lat=0, lon=0, resort_name="Test")
    
    assert result["weekly_snowfall_forecast_cm"] == 11.0 # (10 + 12) / 2
    assert result["forecast_confidence"] == ConfidenceLevel.HIGH
    assert len(result["sources"]) == 2
    assert "Open-Meteo" in result["sources"]

@patch("src.integrations.weather.get_snow_forecast_data")
@patch("src.integrations.weather.get_open_meteo_data")
def test_aggregation_medium_confidence(mock_om, mock_sf):
    """Test aggregation when sources diverge somewhat (10cm vs 25cm)."""
    mock_om.return_value = MOCK_OM_DATA
    
    sf_data = MOCK_SF_DATA.copy()
    sf_data["total_snow_cm"] = 25.0
    mock_sf.return_value = sf_data
    
    result = get_weather_data(lat=0, lon=0, resort_name="Test")
    
    # Average: (10 + 25) / 2 = 17.5
    assert result["weekly_snowfall_forecast_cm"] == 17.5
    # Diff: 15cm (<= 20cm is Medium)
    assert result["forecast_confidence"] == ConfidenceLevel.MEDIUM

@patch("src.integrations.weather.get_snow_forecast_data")
@patch("src.integrations.weather.get_open_meteo_data")
def test_aggregation_low_confidence(mock_om, mock_sf):
    """Test aggregation when sources diverge significantly (10cm vs 50cm)."""
    mock_om.return_value = MOCK_OM_DATA
    
    sf_data = MOCK_SF_DATA.copy()
    sf_data["total_snow_cm"] = 50.0
    mock_sf.return_value = sf_data
    
    result = get_weather_data(lat=0, lon=0, resort_name="Test")
    
    assert result["forecast_confidence"] == ConfidenceLevel.LOW

@patch("src.integrations.weather.get_snow_forecast_data")
@patch("src.integrations.weather.get_open_meteo_data")
def test_fallback_sf_only(mock_om, mock_sf):
    """Test behavior when Open-Meteo fails."""
    mock_om.return_value = {} # Failed
    mock_sf.return_value = MOCK_SF_DATA
    
    result = get_weather_data(lat=0, lon=0, resort_name="Test")
    
    assert result["weekly_snowfall_forecast_cm"] == 12.0
    assert result["forecast_confidence"] == ConfidenceLevel.MEDIUM # Trusted source but single
    assert result["sources"] == [WeatherSource.SNOW_FORECAST]

@patch("src.integrations.weather.get_snow_forecast_data")
@patch("src.integrations.weather.get_open_meteo_data")
def test_fallback_om_only(mock_om, mock_sf):
    """Test behavior when Snow-Forecast fails."""
    mock_om.return_value = MOCK_OM_DATA
    mock_sf.return_value = {} # Failed
    
    result = get_weather_data(lat=0, lon=0, resort_name="Test")
    
    assert result["weekly_snowfall_forecast_cm"] == 10.0
    assert result["forecast_confidence"] == ConfidenceLevel.MEDIUM # Trusted source but single
    assert result["sources"] == [WeatherSource.OPEN_METEO]
