# Task List: Core Agent Logic

## Initialization
- [x] Create `requirements.txt` (pydantic, requests, google-generativeai, duckduckgo-search, python-dotenv).
- [x] Create `trips.json` with sample data.

## Core Logic
- [x] Create `src/models.py` (Trip, Config models).
- [x] Create `src/logic.py` (Phase determination logic).
- [x] Create `tests/test_logic.py` and verify phase calculation (including flight logistics boundaries).

## Integrations
- [x] Create `src/integrations/weather.py` (Open-Meteo).
- [x] Create `src/integrations/search.py` (DuckDuckGo).
- [x] Create `src/integrations/llm.py` (Gemini).
- [x] Create `src/integrations/whatsapp.py` (WhatsApp API).

## Orchestration
- [x] Create `src/main.py` (Main flow).
- [x] Add dry-run support to `main.py`.

## Deployment
- [x] Create `.github/workflows/schedule.yml`.
- [x] Document Secrets in `README.md` (for User action).
