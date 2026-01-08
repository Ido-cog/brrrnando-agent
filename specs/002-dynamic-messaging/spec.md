# Feature Specification: Dynamic Context-Aware Messaging

**Feature Branch**: `002-dynamic-messaging`  
**Created**: 2026-01-08  
**Status**: Draft  
**Input**: User description: "I'd like the agent to be smarter. I want it to draft the message dynamically, each time considering the specific resort and the trip status relative to the current time... the agent should have powerful web search and crawling capabilities... finally the agent will review the generated message and determine if it's good to send."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trip Phase Awareness (Priority: P1)

The agent automatically adjusts the tone and content of messages based on the time remaining until the trip or during the trip itself (e.g., Weekly Hype, Daily Prep, Logistics Day, Active Skiing).

**Why this priority**: Focuses the content on what matters most to the user at any given time, avoiding repetitive or irrelevant information.

**Independent Test**: Mock the "current date" in tests and verify the prompt/output changes for the same trip across different phases.

**Acceptance Scenarios**:
1. **Given** a trip is 30 days away, **When** the agent runs, **Then** it sends a weekly "Hype" message with long-range trends and a resort spotlight.
2. **Given** it is the morning of a ski day, **When** the agent runs, **Then** it sends a "Plan your Day" message with live lift status and a piste map link.

---

### User Story 2 - Local Insight Discovery (Priority: P1)

The agent uses web search and crawling to find "creative" and "relevant" info like local festivals, restaurant recommendations, lift closures, or social media clips from the previous day.

**Why this priority**: Delivers the "wow" factor and high value by providing information that isn't just weather or snow reports.

**Independent Test**: Supply a resort name and a date, and verify the agent successfully identifies an event or local tip via search.

**Acceptance Scenarios**:
1. **Given** a sale is happening at a local ski shop in Val Thorens, **When** the agent searches for "Val Thorens news/events", **Then** it includes the sale info in the message.
2. **Given** a major lift is scheduled for maintenance, **When** the agent crawls the resort status, **Then** it warns the group in the morning update.

---

### User Story 3 - Quality Review Loop (Priority: P1)

The agent reviews its own drafted message before sending. It checks for clarity, relevance, and ensures no placeholders (like "could not find info") are present.

**Why this priority**: Ensures a premium user experience and prevents "AI failures" from reaching the WhatsApp group.

**Independent Test**: Feed the reviewer a message containing "could not get info on lifts" and verify it triggers a revision or a more descriptive failure summary.

**Acceptance Scenarios**:
1. **Given** a drafted message is vague, **When** the review loop runs, **Then** it instructs the drafting agent to add specific details or search again.
2. **Given** the final message contains "???", **When** the review loop runs, **Then** it blocks the message and requires a fix.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST determine the "Trip Stage" relative to `trips.json` dates (Planning, Prep, Logistics, Active).
- **FR-002**: System MUST implement a "Discovery Engine" using web search (Brave/DDG) to find resort-specific events/news.
- **FR-003**: System MUST identify "Creative Content" (festivals, sales, videos, maps) based on the trip stage.
- **FR-004**: System MUST implement a two-stage LLM process: **Draft** -> **Review**.
- **FR-005**: System MUST forbid placeholders or "failure to find" messaging in the final output.
- **FR-006**: System MUST persist or "remember" what was sent recently to avoid duplicating "local gems" in subsequent messages (within a single run or across runs if state is managed). *Note: Per Constitution, state should be minimal, but we might need a way to track "seen" events.*

### Key Entities *(include if feature involves data)*

- **Trip Stage**: An ENUM representing the current relationship between the run date and trip dates.
- **Insight**: A piece of discovered information (Text, URL, Type) to be used in the message.
- **Draft**: The candidate message produced by the first LLM pass.
- **Review Report**: The critique and status (Go/No-Go) of the Draft.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of messages during the "Active" stage contain at least one resort-specific "Local Insight".
- **SC-002**: 0% of messages sent to WhatsApp contain placeholders like "???", "N/A", or "Could not find".
- **SC-003**: The "Review Loop" successfully identifies and triggers revisions for at least 90% of intentionally sabotaged drafts (tested via unit tests).
