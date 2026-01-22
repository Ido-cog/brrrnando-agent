# Tasks: Multi-Source Weather Data

**Input**: Design documents from `/specs/006-006-multi-source/`
**Prerequisites**: plan.md (required), spec.md (required)

## Phase 1: Setup

- [ ] T001 Add `beautifulsoup4` to `requirements.txt`
- [ ] T002 Update `src/models.py` to support confidence and source attribution (if needed) or define new internal types in `weather.py`.

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T003 Create `src/integrations/snow_forecast.py` (Empty shell with types)
- [ ] T004 Create `src/integrations/open_meteo.py` (Isolate existing logic from `weather.py` or just prepare `weather.py` for refactor)

## Phase 3: User Story 2 - Snow-Forecast.com Integration (Priority: P1)

**Goal**: Successfully scrape and parse snow data from Snow-Forecast.com

- [ ] T005 [P] [US2] Create scraper logic in `src/integrations/snow_forecast.py` to fetch HTML
- [ ] T006 [P] [US2] Implement parsing logic in `src/integrations/snow_forecast.py` to extract snow amounts (cm)
- [ ] T007 [US2] Handle elevation selection (mid-mountain vs base) in scraper
- [ ] T008 [US2] Add unit tests for scraper in `tests/test_snow_forecast.py` with mocked HTML

## Phase 4: User Story 1 - Multi-Source Snow Forecast (Priority: P1)

**Goal**: Aggregate data from Open-Meteo and Snow-Forecast

- [ ] T009 [P] [US1] Create aggregator logic in `src/integrations/weather.py` to call both sources
- [ ] T010 [US1] Implement normalization (all to cm) and averaging logic
- [ ] T011 [US1] Implement fallback logic (if one source fails)
- [ ] T012 [US1] Update `src/main.py` to use the new aggregated `get_weather_data` response structure (confidence, sources)

## Phase 5: User Story 3 - Source Attribution & Confidence (Priority: P2)

**Goal**: Indicate source and confidence in the final message

- [ ] T013 [US3] Update `src/integrations/llm.py` prompts to include source/confidence info in draft generation
- [ ] T014 [US3] Verify confidence language in generated messages (manual verification or updated E2E test)

## Phase 6: Polish

- [ ] T015 Verify `trips.json` configuration for resorts (ensure mapping to Snow-Forecast URLs works)
- [ ] T016 Run full integration test with `--dry-run` to verify no crashes
