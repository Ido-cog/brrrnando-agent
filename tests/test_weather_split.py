
import unittest
from unittest.mock import patch, MagicMock
from src.integrations.weather import get_weather_data
from src.models import WeatherSource, ConfidenceLevel

class TestWeatherSplitting(unittest.TestCase):

    @patch('src.integrations.weather.get_open_meteo_data')
    @patch('src.integrations.weather.get_snow_forecast_data')
    def test_split_snowfall_logic(self, mock_get_sf, mock_get_om):
        """Test that snowfall is correctly split into immediate (48h) and future components."""
        
        # MOCK INPUTS
        # Open-Meteo: 10cm total over 6 days
        # Days 0-1: 5cm (Immediate)
        # Days 2-5: 5cm (Future)
        mock_get_om.return_value = {
            "current": {"snow_depth": 100, "temperature_2m": -5, "wind_speed_10m": 10},
            "daily": {
                "snowfall_sum": [2.5, 2.5, 1.25, 1.25, 1.25, 1.25, 0.0] 
            }
        }
        
        # Snow-Forecast: 10cm total (Matches OM for simplicity)
        mock_get_sf.return_value = {
            "total_snow_cm": 10.0,
            "forecast_days": 6,
            "source": WeatherSource.SNOW_FORECAST
        }

        # EXECUTE
        result = get_weather_data(lat=0, lon=0, resort_name="Test")
        
        # VERIFY
        # Aggregated Total should be 10.0
        self.assertEqual(result["weekly_snowfall_forecast_cm"], 10.0)
        
        # Immediate (first 2 days of OM is 5.0) -> Ratio 0.5
        # Future (next 4 days of OM is 5.0) -> Ratio 0.5
        # Applied to Aggregate (10.0) -> 5.0 each
        self.assertEqual(result["snow_48h_forecast_cm"], 5.0)
        self.assertEqual(result["snow_future_forecast_cm"], 5.0)

    @patch('src.integrations.weather.get_open_meteo_data')
    @patch('src.integrations.weather.get_snow_forecast_data')
    def test_ratio_application(self, mock_get_sf, mock_get_om):
        """Test that the OM ratio is applied to the Aggregated total (even if totals differ)."""
        
        # MOCK INPUTS
        # Open-Meteo: 10cm total
        # Days 0-1: 8cm (80% Immediate)
        # Days 2-5: 2cm (20% Future)
        mock_get_om.return_value = {
            "current": {"snow_depth": 100},
            "daily": {
                "snowfall_sum": [4.0, 4.0, 0.5, 0.5, 0.5, 0.5, 0.0] 
            }
        }
        
        # Snow-Forecast: 20cm total (Higher forecast)
        mock_get_sf.return_value = {
            "total_snow_cm": 20.0
        }

        # EXECUTE
        result = get_weather_data(lat=0, lon=0, resort_name="Test")
        
        # VERIFY
        # Aggregated Total = (10 + 20) / 2 = 15.0
        self.assertEqual(result["weekly_snowfall_forecast_cm"], 15.0)
        
        # Ratio from OM: 80% immediate, 20% future
        # Expected Immediate: 15.0 * 0.8 = 12.0
        # Expected Future: 15.0 * 0.2 = 3.0
        self.assertAlmostEqual(result["snow_48h_forecast_cm"], 12.0, places=1)
        self.assertAlmostEqual(result["snow_future_forecast_cm"], 3.0, places=1)

if __name__ == '__main__':
    unittest.main()
