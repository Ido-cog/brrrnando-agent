# Feature Specification: Natural, Context-Aware Messaging

**Feature Branch**: `007-natural-messaging`  
**Created**: 2026-01-24  
**Status**: Draft  
**Input**: User request for "Natural message, different than previous ones" and to "hide future snowfall" if trip is ending (irrelevant).

## User Scenarios & Testing

### User Story 1 - Organic & Varied Messaging (Priority: P1)

As a skier on a trip, I want the bot's daily messages to feel like they come from a human friend who talks naturally, so that I don't get bored by repetitive structures or robotic headers.

**Why this priority**: The user explicitly stated the current messages are "very repetitive" and "boring". This is critical for engagement.

**Independent Test**: Generate 3 consecutive messages for the same trip state. They should all have distinct structures (e.g., one starts with weather, one with a joke, one with a venue tip) and NO rigid headers like "--- SKI NERD TRIVIA ---".

**Acceptance Scenarios**:

1. **Given** 3 previous messages in history, **When** generating a new draft, **Then** the new message must not share the same opening sentence structure or "hook" as the previous ones.
2. **Given** any phase, **When** generating a draft, **Then** the output MUST NOT contain "--- [SECTION NAME] ---" headers.

---

### User Story 2 - Smart Snowfall Resolution (Priority: P1)

As a skier near the end of my trip, I want to know about snowfall hitting *tomorrow* versus snowfall hitting *next week* distinctively. If I am leaving, I do not care about next week's snow.

**Why this priority**: The user rejected the "hide data" approach. They want awareness, just better resolution.

**Independent Test**: Mock a scenario with heavy snow in 5 days (after trip ends). The bot should **NOT** report it.

**Acceptance Scenarios**:

1. **Given** snow is forecast for tomorrow (and user is there), **When** generating message, **Then** bot explicitly hypes it as "incoming freshies for tomorrow".
2. **Given** snow is forecast for 5 days away (and user leaves in 2), **When** generating message, **Then** bot **DOES NOT MENTION IT**. It is irrelevant.

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST NOT enforce any rigid messaging structure (headers, specific section ordering) in the LLM prompt.
- **FR-002**: System MUST inject a "Style/Persona" directive that encourages variation (e.g., "Casual Hype", "Tech/Data Focus", "Local Guide") to prevent monotony.
- **FR-003**: System MUST separate `snowfall_forecast` into `immediate_snow` (next 48h) and `future_snow` (>48h) in the prompt context.
- **FR-004**: If `ski_days_left <= 2`, System MUST **REMOVE** `future_snow` data from the prompt context entirely.
- **FR-005**: System MUST maintain the "Anti-Repetition" check for static data points (Base Depth) defined in previous iteration.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 10/10 generated test messages contain NO rigid headers (e.g. "--- TRIVIA ---").
- **SC-002**: In "End of Trip" scenarios with future snow (>48h away), the generated message **should not mention** the future snow at all.
