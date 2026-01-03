```markdown
# Feature Specification: Brrrnando Agent — Ski trip monitoring agent

**Feature Branch**: `002-brrrnando-agent`  
**Created**: 2026-01-03  
**Status**: Draft  
**Input**: User description: "Build a serverless Python agent that runs on a GitHub Actions cron job to monitor ski trip conditions and notify a WhatsApp group. Runs twice daily (09:00 and 19:00 IST). Uses Open-Meteo (icon_eu), Brave/DuckDuckGo for road/video searches, Gemini 2.5 Flash for synthesis, and WhatsApp Business Cloud API for output. Config-driven; no UI."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Morning live report (Priority: P1)

When a trip is active (skiing) or the morning scheduled run occurs, the system delivers a concise, high-energy "Live" report to the configured WhatsApp group that focuses on current conditions (wind, fresh snowfall, lift status) and includes a short media link if available.

**Why this priority**: Morning live info directly affects on-mountain safety and decisions.

**Independent Test**: Run the morning workflow on a known trip in `trips.json` with mocked Open-Meteo and search results; verify a correctly formatted WhatsApp message is produced and that required fields (snowfall, windspeed_10m, lift status) appear.

**Acceptance Scenarios**:

1. **Given** a trip with status "skiing" and valid coordinates, **When** the 09:00 IST run executes, **Then** a WhatsApp message is sent containing current snowfall, wind speed, and lift status summary.
2. **Given** no recent snowfall, **When** the morning run executes, **Then** message includes a "No fresh snow" summary and omits media links.

---

### User Story 2 - Evening forecast summary (Priority: P1)

When the evening scheduled run executes, the system sends a forecast-focused message covering tomorrow's weather, road closures for planned transfers, and links to the latest social media snow-report clip.

**Why this priority**: Pre-trip planning and safety for next-day activities.

**Independent Test**: Run the evening workflow with mocked forecast and search results; assert the message includes next-day high-level forecast and at least one road-status or media search result (if found).

**Acceptance Scenarios**:

1. **Given** a trip within 14 days, **When** the 19:00 IST run executes, **Then** a forecast message containing the 24–48 hour outlook and any road warnings is sent.

---

### User Story 3 - Phase-driven notifications (Priority: P2)

The system uses `trips.json` to determine phase and cadence: ignore >90d, weekly for 90–14d (storms only), daily for 14–2d, logistics 1 day before and day before return, and full daily morning+evening while skiing.

**Why this priority**: Ensures the system only notifies at appropriate cadence and avoids spam.

**Independent Test**: Provide `trips.json` entries for each phase and simulate current dates; verify the correct runs produce or suppress messages per phase.

**Acceptance Scenarios**:

1. **Given** a trip 100 days away, **When** runs execute, **Then** no messages are generated for that trip.
2. **Given** a trip 10 days away, **When** a daily run executes, **Then** an evening forecast message is generated.

---

### Edge Cases

- Trip coordinates invalid: system logs and continues; an alert is sent to the ops contact only if all trips fail to resolve coordinates.
- API rate limits or failures: system retries with exponential backoff; if data unavailable, produce a best-effort summary and mark values as "unavailable" in the message.
- WhatsApp delivery failures: record failure and retry once; on persistent failure, create a diagnostic log and continue (do not block other trip reports).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST read `trips.json` and determine each trip's phase based on the current date.
- **FR-002**: The system MUST run on a GitHub Actions schedule twice daily (09:00 and 19:00 IST) and be triggerable on-demand.
- **FR-003**: The system MUST fetch current observations and forecast data from Open-Meteo (icon_eu) for each trip location and extract snowfall, freezing_level_height, and windspeed_10m.
- **FR-004**: The system MUST perform web searches (Brave Search or DuckDuckGo) for road status and latest snow-report media links related to the trip's resort/road_check.
- **FR-005**: The system MUST synthesize a human-friendly, high-energy summary using a text synthesis model (Gemini 2.5 Flash) given the raw data inputs.
- **FR-006**: The system MUST send messages to a configured WhatsApp group via the WhatsApp Business Cloud API, supporting markdown-style formatting, emojis, and media links.
- **FR-007**: The system MUST be fully config-driven; all credentials, phone/groups, schedules (if overridden), and trip data remain external to code (in `trips.json` and a config file).
- **FR-008**: The system MUST be stateless between runs and only rely on `trips.json` and ephemeral storage for processing.
- **FR-009**: The system MUST include diagnostic logging for data fetches, synthesis output, and delivery status.

### Key Entities *(include if feature involves data)*

- **Trip**: Represents a planned ski trip. Key attributes: `id`, `name`, `start_date`, `end_date`, `location` (lat/lon), `resort_name`, `road_check` (text used for road-status searches), `status` (planned, skiing, completed), `contact_group` (WhatsApp group id reference).
- **Report**: Generated message for a trip run. Attributes: `trip_id`, `phase`, `run_time_utc`, `payload_summary`, `media_links`, `delivery_status`.
- **Config**: System configuration (separate from code). Attributes: `open_meteo_base`, `search_providers`, `whatsapp_credentials_ref`, `notify_on_failure`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For a valid trip in `trips.json` and with live API responses available, the system sends the correctly formatted WhatsApp message for the scheduled run within 2 minutes of job start in 95% of runs.
- **SC-002**: When the trip is in a non-notify phase (>90 days), 100% of runs produce no message for that trip.
- **SC-003**: When APIs are reachable, 90% of generated summaries must include at least two of the expected data points (snowfall, windspeed_10m, freezing_level_height) when those data are available.
- **SC-004**: In simulated failure modes (Open-Meteo outage, search failure), the system produces a best-effort message marked with "data unavailable" and does not crash the run.

### Non-functional

- Message formatting must be readable on mobile (short paragraphs, bold headings, emojis). This is validated by a simple human check or automated rendering tests against a sample WhatsApp message.

## Assumptions

- `trips.json` is the single source of truth for trip timing and target locations.
- API credentials (Open-Meteo, Gemini, WhatsApp) are stored in GitHub Actions secrets and referenced from a config file; the spec does not mandate storage method.
- Road status and social media searches are best-effort; absence of results is acceptable and should be indicated in the message.
- Lift status may be scraped or inferred via search results; if unavailable, present as "unknown" rather than blocking delivery.

## Test Plan (high level)

- Unit tests for phase calculation logic given `trips.json` entries.
- Integration tests that mock Open-Meteo, search providers, Gemini synthesis, and WhatsApp endpoints to validate end-to-end message generation.
- End-to-end run in a feature branch using GitHub Actions with test credentials to confirm scheduling and delivery to a test WhatsApp group.

## Files created by script

- Spec path: /specs/002-brrrnando-agent/spec.md

