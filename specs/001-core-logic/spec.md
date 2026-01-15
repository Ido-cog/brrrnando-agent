# Specification: Core Agent Logic (Brrrnando)

## User Stories

1. **Morning Briefing**
   As a group member, I want a morning update (09:00 IST) when a trip is active or approaching, showing live wind, snow, and lift status, so I can plan my ski day.

2. **Evening Hype/Forecast**
   As a group member, I want an evening update (19:00 IST), showing tomorrow's forecast and relevant social media clips, so I can get hyped or prepare for logistics.

3. **Smart Frequency**
   As a group member, I want the frequency of updates to increase as the trip gets closer (Weekly -> Daily -> Active), so I stay informed without being spammed months in advance.
    - > 90 days: Silent.
    - 90-14 days: Weekly (major storms).
    - 14-2 days before Flight Out: Daily (Forecast + Hype).
    - 1 day before Flight Out: Logistics focus (Roads to airport, Airport weather).
    - During Ski Days: Daily Morning/Evening (Snow, Wind, Lifts).
    - 1 day before Flight Back: Logistics focus (Roads to airport, Airport Weather).

4. **Configurable Trips**
   As the admin, I want to define trips in a `trips.json` file with flight dates, ski dates, resort names, and specific queries, so I can manage multiple trips easily.

5. **WhatsApp Delivery**
   As a user, I want to receive these agents in my WhatsApp group, formatted with emojis and bold text for quick scanning.

## Acceptance Criteria

### Core Logic
- [ ] **State Determination**: The agent correctly identifies the current phase for each trip in `trips.json` relative to the current date.
- [ ] **Scheduling**: The GitHub Action triggers at the correct UTC times to map to 09:00 IST and 19:00 IST.

### Data Gathering
- [ ] **Weather**: Successfully fetches Snowfall, Freezing Level, and Windsuped from Open-Meteo API.
- [ ] **Search**: Successfully retrieves search results for "Road status" and "Snow report video" using DuckDuckGo (primary) or Tavily (fallback on rate limit).

### Synthesis & Output
- [ ] **Gemini Integration**: Prompts Gemini 2.5 Flash with raw data and receives a "high-energy" natural language summary.
- [ ] **WhatsApp Integration**: Successfully sends the generated message to the configured WhatsApp number/Group (via API).

### Config & Deployment
- [ ] **Config Schema**: `trips.json` supports `flight_out_date`, `ski_start_date`, `ski_end_date`, `flight_back_date`.
- [ ] **Secrets**: API keys (Gemini, WhatsApp, Search) are read from Environment Variables.
- [ ] **GitHub Action**: Workflow file exists and passes the static check (linting) and runs successfully in the repo.
