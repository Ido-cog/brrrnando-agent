import requests
from bs4 import BeautifulSoup

def inspect():
    url = "https://www.snow-forecast.com/resorts/Val-Thorens/6day/mid"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Look for the forecast table. Usually has class "forecast-table" or similar
        tables = soup.find_all("table")
        print(f"Found {len(tables)} tables.")
        
        for i, table in enumerate(tables):
            # Check if it looks like the forecast table (contains 'Snow')
            text = table.get_text()[:200]
            print(f"\n--- Table {i} ---")
            print(f"Classes: {table.get('class', [])}")
            print(f"Preview: {text}")
            
            # Print rows to see structure
            rows = table.find_all("tr")
            for j, row in enumerate(rows[:10]):
                print(f"  Row {j} class: {row.get('class', [])}")
                cells = row.find_all(["td", "th"])
                cell_texts = [c.get_text(strip=True) for c in cells]
                print(f"    Cells: {cell_texts}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
