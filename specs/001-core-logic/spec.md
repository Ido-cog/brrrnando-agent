# Specification: Core Agent Logic (Brrrnando)

## User Stories

1. **Morning Briefing**
   As a group member, I want a morning update (09:00 IST) when a trip is active or approaching, showing live wind, snow, and lift status, so I can plan my ski day.

2. **Evening Hype/Forecast**
   As a group member, I want an evening update (19:00 IST), showing tomorrow's forecast and relevant social media clips, so I can get hyped or prepare for logistics.

3. **Smart Frequency & Phases**
    As a group member, I want the frequency and content of updates to adjust automatically based on the trip's phase.
    - `WAIT`: > 90 days before flight. Silent.
    - `PLANNING_WEEKLY`: 14-90 days before flight. Weekly update (Mondays @ 09:00 IST) with long-range trends.
    - `HYPE_DAILY`: 2-14 days before flight. Daily morning/evening updates.
    - `LOGISTICS_OUT`: 1 day before flight out. Focus on roads and airport status.
    - `TRAVEL`: On flight days or gap days not covered by other phases.
    - `ACTIVE`: During ski dates. High-frequency morning/evening updates.
    - `LOGISTICS_BACK`: 1 day before flight back. Focus on return logistics.
    - `POST`: After flight back. Season recap and next trip ideas.

4. **Configurable Trips**
   As the admin, I want to define trips in `trips.json` with flight dates, ski dates, resort names, coordinates, and elevation data (Summit/Base).

5. **Multi-Channel Delivery (WhatsApp & Telegram)**
   Reports are delivered to both WhatsApp (primary) and Telegram (fallback) to ensure reliability.

## Acceptance Criteria

### Core Logic
- [x] **Phase Determination**: Correctly maps current date to `Phase` enum (Wait, Planning, Hype, Logistics, Active, Travel, Post).
- [x] **Scheduling**: GitHub Action triggers at UTC times corresponding to 09:00 IST and 19:00 IST. `PLANNING_WEEKLY` only runs on Mondays.

### Data Gathering
- [x] **Weather**: Fetches current and forecast data from Open-Meteo for resort coordinates. Supports separate Summit and Base elevation queries for accurate snow depth and wind.
- [x] **Autonomous Discovery**: LLM evaluates initial findings and requests refined searches (webcams, menus) if needed.
- [x] **Search**: Integration with DuckDuckGo (via search tools) for live web and video data.

### Synthesis & Output
- [x] **Gemini Integration**: Uses `gemini-2.5-flash` for high-energy, data-grounded message synthesis.
- [x] **Review Loop**: A second LLM pass validates the draft for placeholders and quality before sending.
- [x] **Multi-Channel Delivery**: Sends to both configured WhatsApp and Telegram channels.

### Config & Deployment
- [x] **Config Schema**: `trips.json` supports full lifecycle dates and resort metadata.
- [x] **GitHub Action**: Managed via `.github/workflows/run_agent.yml` (or similar).
