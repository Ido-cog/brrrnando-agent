# Implementation Plan: Multi-Source Weather Data

**Branch**: `006-006-multi-source` | **Date**: 2026-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/006-006-multi-source/spec.md`

## Summary

The goal is to improve snow forecast accuracy by aggregating data from multiple sources. We will add `Snow-Forecast.com` (via scraping) as a secondary source alongside the existing `Open-Meteo` API. The `get_weather_data` function will be refactored to query both sources, normalize the data (cm), and provide an aggregated forecast with confidence levels.

## Technical Context

**Language/Version**: Python 3.x
**Primary Dependencies**: `requests`, `beautifulsoup4` (NEW for scraping)
**Storage**: Stateless (in-memory aggregation during run)
**Testing**: `pytest` with mocked responses for both API and HTML scraping.
**Target Platform**: GitHub Actions Runner
**Project Type**: Single Script / CLI Agent

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Serverless & Stateless**: No local DB required. scraping is done on the fly.
- [x] **Config-Driven**: Resort URLs/identifiers will need to be added to `trips.json` or derived from resort name. **Decision**: Try to map resort name to snow-forecast URL format or add `snow_forecast_url` to `trips.json` (prefer derivation first, fallback to config if needed).
- [x] **No Frontend**: Output is text for WhatsApp.
- [x] **Free Tier Compatibility**: Scraping is lightweight.
- [x] **Privacy First**: No user data involved in weather fetching.

## Project Structure

### Documentation (this feature)

```text
specs/006-006-multi-source/
├── plan.md              # This file
├── spec.md              # Feature Specification
└── tasks.md             # Task Checklist
```

### Source Code (repository root)

```text
src/
├── integrations/
│   ├── weather.py          # [MODIFY] Refactor to become an aggregator/facade
│   ├── open_meteo.py       # [NEW] Extract existing Open-Meteo logic here (optional, or keep in weather.py and separate snow-forecast)
│   └── snow_forecast.py    # [NEW] Scraper for snow-forecast.com
├── main.py                 # [MODIFY] logic to handle aggregated weather object
└── models.py               # [MODIFY] Update Weather/Forecast models if needed
```

**Structure Decision**:
1.  Create `src/integrations/snow_forecast.py` to handle HTML parsing.
2.  Refactor `src/integrations/weather.py` to:
    - Call Open-Meteo (existing logic).
    - Call Snow-Forecast (new logic).
    - Aggregate results (averaging, confidence).
3.  Add `beautifulsoup4` to `requirements.txt`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New Dependency (`bs4`) | Required for parsing HTML from Snow-Forecast.com | Regex is brittle and error-prone for HTML. |
