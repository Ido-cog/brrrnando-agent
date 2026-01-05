# Brrrnando Agent Constitution

## Core Principles

### I. Serverless & Stateless
The agent runs entirely on GitHub Actions ephemeral runners. It must not rely on local file persistence between runs. All state is derived from the repository content (`trips.json`) and the current date/time.

### II. Config-Driven
Trip data, preferences, and potentially prompt templates should be decoupled from code. `trips.json` is the source of truth for what is being monitored.

### III. No Frontend Logic
There is no web interface, dashboard, or database to maintain. The "UI" is the WhatsApp chat. All output is formatted for mobile readability (WhatsApp Markdown).

### IV. Free Tier Compatibility
The architecture must fit within GitHub Actions Free Tier limits (2000 minutes/month). Efficient execution and cron scheduling are critical.

### V. Privacy First
Personal data (phone numbers) and API keys are strictly managed via GitHub Secrets. No sensitive data hardcoded in the repo.

## Constraints

- **Language**: Python 3.x
- **Runtime**: GitHub Actions (Ubuntu latest)
- **Schedule**: Twice daily (09:00 IST, 19:00 IST)
- **APIs**: Open-Meteo (Weather), Brave/DDG (Search), Gemini (Synthesis), WhatsApp Business (Delivery)

## Governance
This constitution governs the development of the Brrrnando Agent. All features must align with the stateless, no-frontend, config-driven approach.
