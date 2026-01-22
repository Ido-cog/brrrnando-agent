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

## Feature: Multi-Source Weather (006-006)
- [ ] T001 Add `beautifulsoup4` to `requirements.txt`
- [ ] T002 Update `src/models.py` to support confidence and source attribution
- [ ] T003 Create `src/integrations/snow_forecast.py` (Empty shell with types)
- [ ] T004 Create `src/integrations/open_meteo.py` (Isolate existing logic)
- [ ] T005 [P] [US2] Create scraper logic in `src/integrations/snow_forecast.py`
- [ ] T006 [P] [US2] Implement parsing logic in `src/integrations/snow_forecast.py`
- [ ] T007 [US2] Handle elevation selection
- [ ] T008 [US2] Add unit tests for scraper
- [ ] T009 [P] [US1] Create aggregator logic in `src/integrations/weather.py`
- [ ] T010 [US1] Implement normalization and averaging logic
- [ ] T011 [US1] Implement fallback logic
- [ ] T012 [US1] Update `src/main.py`
- [ ] T013 [US3] Update `src/integrations/llm.py` prompts
- [ ] T014 [US3] Verify confidence language
- [ ] T015 Verify `trips.json` configuration
- [ ] T016 Run full integration test
