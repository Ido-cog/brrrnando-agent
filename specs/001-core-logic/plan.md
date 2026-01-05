# Implementation Plan: Core Agent Logic (Brrrnando)

## Architecture

The application is a stateless Python CLI tool executed by GitHub Actions.

### Directory Structure
```
.
├── .github/
│   └── workflows/
│       └── schedule.yml    # Cron definition
├── src/
│   ├── __init__.py
│   ├── main.py             # Entry point
│   ├── logic.py            # Trip phase calculation
│   ├── models.py           # Pydantic models (Trip, Config)
│   └── integrations/
│       ├── weather.py      # Open-Meteo
│       ├── search.py       # DuckDuckGo
│       ├── llm.py          # Gemini Flash
│       └── whatsapp.py     # WhatsApp Cloud API
├── trips.json              # Config file
├── requirements.txt
└── tests/
    └── test_logic.py       # Unit tests
```

## Proposed Changes

### [NEW] `trips.json`
Define the schema for trips.
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

### [NEW] `src/models.py`
Pydantic models for validation.

### [NEW] `src/logic.py`
`determine_phase(trip, current_date)` -> Enum(WAIT, PLANNING_WEEKLY, HYPE_DAILY, LOGISTICS, ACTIVE, POST)

### [NEW] `src/integrations/*.py`
Wrappers for external APIs.

### [NEW] `src/main.py`
Orchestrator:
1. Load `trips.json`
2. Loop trips
3. Determine phase
4. If eligible for update:
   - Fetch data (Parallel/Sequential)
   - Call Gemini
   - Send WhatsApp

### [NEW] `.github/workflows/schedule.yml`
Cron configuration for 09:00 IST and 19:00 IST.

## Verification Plan

### Automated
- `pytest tests/` for date logic (Critical: Ensure correct phase for boundary dates).
- API mocks for integrations.

### Manual
- Run locally with `python src/main.py` (Dry Run mode).
- Verify WhatsApp delivery (User check).
