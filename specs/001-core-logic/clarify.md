# Clarification: Core Agent Logic

## 1. Weekly Updates in Stateless Mode
**Question**: Since the agent is stateless, how do we ensure "Weekly updates" (90-14 days out) don't fire every day?
**Assumption**: The agent will check if the current day is a specific day of the week (e.g., Monday) to trigger the weekly update.

## 2. Location Coordinates
**Question**: Does `trips.json` include latitude/longitude for Open-Meteo, or should the agent look them up?
**Assumption**: `trips.json` will include `lat` and `lon` to strictly avoid ambiguity and extra API calls.

## 3. Search Provider
**Question**: Brave Search requires an API key. DuckDuckGo is free but can be flaky.
**Assumption**: We will try DuckDuckGo (`duckduckgo-search` library) first for cost efficiency. If unstable, we'll allow switching to Brave via env var.

## 4. WhatsApp Credentials
**Question**: Do we have the Meta Developer App set up for WhatsApp Cloud API?
**Assumption**: Yes, user will provide `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, and `RECIPIENT_PHONE` (or Group ID) as secrets.
