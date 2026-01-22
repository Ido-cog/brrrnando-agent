from src.integrations.snow_forecast import get_snow_forecast_data

def test():
    resort = "Val Thorens"
    print(f"Testing scraper for {resort}...")
    data = get_snow_forecast_data(resort)
    print("Result:", data)

if __name__ == "__main__":
    test()
