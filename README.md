# Brrrnando Agent ⛷️🤖

A serverless Python agent that runs on GitHub Actions to monitor ski trip conditions and notify a WhatsApp group.

## Features

- **Morning Briefing** (09:00 IST): Live conditions (Wind, Snow, Lifts).
- **Evening Hype** (19:00 IST): Tomorrow's forecast + Social media hype videos.
- **Smart Logistics**:
  - Weekly updates 90-14 days out.
  - Daily updates 14 days out.
  - **Flight Logistics**: Road status and Airport weather 1 day before flights.

## Configuration

### 1. `trips.json`
Configure your trips here.
```json
[
  {
    "resort_name": "Val Thorens",
    "flight_out_date": "2026-02-14",
    "ski_start_date": "2026-02-15",
    "ski_end_date": "2026-02-21",
    "flight_back_date": "2026-02-22",
    "lat": 45.2983,
    "lon": 6.5824,
    "road_check": "Moûtiers to Val Thorens"
  }
]
```

### 2. Secrets
Set the following secrets in your GitHub Repository (Settings -> Secrets and variables -> Actions):

- `GEMINI_API_KEY`: Google Gemini API Key.
- `WHATSAPP_TOKEN`: Meta/Facebook Developer Access Token (System User).
- `WHATSAPP_PHONE_ID`: WhatsApp Phone Number ID.
- `RECIPIENT_PHONE`: Phone number or Group ID to receive messages (e.g. `972501234567`).

## Local Development

```bash
pip install -r requirements.txt
python -m src.main --mode morning --dry-run
```
