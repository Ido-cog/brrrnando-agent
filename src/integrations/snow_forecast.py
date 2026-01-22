import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, List
from ..models import WeatherSource

def clean_resort_name(name: str) -> str:
    """
    Converts 'Val Thorens' to 'Val-Thorens', 'St. Anton' to 'St-Anton', etc.
    """
    # Replace spaces with hyphens
    clean = name.replace(" ", "-")
    # Remove dots (St. Anton -> St-Anton)
    clean = clean.replace(".", "")
    return clean

def get_snow_forecast_data(resort_name: str, elevation: str = "mid") -> Dict[str, Any]:
    """
    Scrapes snow-forecast.com for the given resort.
    Returns parsed snowfall data or empty dict if failure.
    
    Returns:
        {
            "total_snow_cm": float,
            "forecast_days": int,
            "source": "Snow-Forecast.com",
            "daily_snow": [ ... ] # Optional detailed breakdown
        }
    """
    formatted_name = clean_resort_name(resort_name)
    url = f"https://www.snow-forecast.com/resorts/{formatted_name}/6day/{elevation}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the forecast table
        table = soup.find("table", class_="forecast-table__table")
        if not table:
            print(f"Snow-Forecast: Could not find forecast table for {resort_name}")
            return {}
            
        # Find the row with snow in cm
        # The structure is headers in row 0, data in rows. 
        # We look for a row where the first cell is 'cm'
        rows = table.find_all("tr")
        snow_row = None
        for row in rows:
            cells = row.find_all(["td", "th"])
            if cells and cells[0].get_text(strip=True) == "cm":
                snow_row = row
                break
        
        if not snow_row:
            print(f"Snow-Forecast: Could not find 'cm' row for {resort_name}")
            return {}
            
        # Parse snow values
        cells = snow_row.find_all("td")[1:] # Skip the first 'cm' cell
        total_snow = 0.0
        
        for cell in cells:
            text = cell.get_text(strip=True)
            if text and text != "—" and text != "-":
                try:
                    val = float(text)
                    total_snow += val
                except ValueError:
                    pass
                    
        return {
            "total_snow_cm": round(total_snow, 1),
            "forecast_days": 6, # Usually 6 days
            "source": WeatherSource.SNOW_FORECAST
        }

    except Exception as e:
        print(f"Error scraping Snow-Forecast for {resort_name}: {e}")
        return {}
