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

- **FR-001**: System MUST determine the "Phase" relative to `trips.json` dates (Wait, Planning, Hype, Logistics, Active, Travel, Post).
- **FR-002**: System MUST implement a "Discovery Engine" using web and video search to find resort-specific events/news.
- **FR-003**: System MUST identify "Creative Content" (festivals, sales, videos, maps) and perform **Autonomous Discovery** where the LLM evaluates initial findings and requests 2-3 refined queries if more "flavor" is needed.
- **FR-004**: System MUST implement a two-stage LLM process: **Draft** -> **Review**. The review loop allows for up to 2 attempts, where a rejection triggers a new draft generation based on critique.
- **FR-005**: System MUST forbid placeholders ([Resort], ???) or generic dismissive phrases ("could not get info") in the final output.
- **FR-006**: System MUST persist previously shared URLs, trivia, and challenges to avoid duplication.
- **FR-007**: System MUST adhere to "Balanced Hype" tone: Professional, data-grounded, but energetic.
- **FR-008**: System MUST enforce specific "Banned Words" (Legends, Magic, Wooohooo, CHOO CHOO, EPIC, Woooooow) and WhatsApp formatting (bolding, short paragraphs).

### Key Entities
- **Phase**: An ENUM representing the current relationship between the run date and trip dates.
- **Insight**: A piece of discovered information (Text, URL, Type) to be used in the message.
- **Draft**: The candidate message produced by the first LLM pass.
- **Review Report**: The critique and status (APPROVED/REVISE) of the Draft.

## Success Criteria

### Measurable Outcomes
- [x] **SC-001**: 100% of messages during the "Active" stage contain at least one resort-specific "Local Insight".
- [x] **SC-002**: 0% of messages sent contain placeholders like "???", "[Resort]", or "Could not find info".
- [x] **SC-003**: The "Review Loop" successfully identifies and triggers revisions for drafts failing quality checks.
- [x] **SC-004**: Messages adhere to "Balanced Hype" style guide and avoid banned "cringe" words.
