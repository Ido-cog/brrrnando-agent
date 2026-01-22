import pytest
from unittest.mock import patch, MagicMock
from src.integrations.snow_forecast import get_snow_forecast_data

# Sample HTML for mocking
MOCK_HTML_SUCCESS = """
<html>
<body>
    <table class="forecast-table__table">
        <tbody>
            <tr class="forecast-table__row">
                <td>cm</td>
                <td>5</td>
                <td>—</td>
                <td>10</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
"""

MOCK_HTML_FAILURE = """
<html>
<body>
    <div class="no-table"></div>
</body>
</html>
"""

@patch("src.integrations.snow_forecast.requests.get")
def test_scraper_success(mock_get):
    """Test successful parsing of snowfall data."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = MOCK_HTML_SUCCESS.encode("utf-8")
    mock_get.return_value = mock_response

    data = get_snow_forecast_data("Test Resort")
    
    assert data["total_snow_cm"] == 15.0  # 5 + 10
    assert data["source"] == "Snow-Forecast.com"
    assert "forecast_days" in data

@patch("src.integrations.snow_forecast.requests.get")
def test_scraper_no_table(mock_get):
    """Test handling when forecast table is missing."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = MOCK_HTML_FAILURE.encode("utf-8")
    mock_get.return_value = mock_response

    data = get_snow_forecast_data("Test Resort")
    assert data == {}

@patch("src.integrations.snow_forecast.requests.get")
def test_scraper_network_error(mock_get):
    """Test handling of network errors."""
    mock_get.side_effect = Exception("Network Timeout")
    
    data = get_snow_forecast_data("Test Resort")
    assert data == {}
