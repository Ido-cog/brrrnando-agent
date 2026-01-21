# Feature Specification: Message Variation System

**Feature Branch**: `005-005-message-variation`  
**Created**: 2026-01-21  
**Status**: Draft  
**Input**: User description: "currently all agent messages look the same, with the same info and wording. Lets keep the last 3-4 messages the agent sent and use them when drafting new ones to make sure it's not just the same info all the time."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Message History Awareness (Priority: P1)

The agent tracks the last 3-4 messages it sent and uses that history when drafting new messages to avoid repetitive wording, topics, and phrasing.

**Why this priority**: Prevents message fatigue and makes the agent feel more dynamic and intelligent. Users will notice and appreciate the variety, making the daily updates feel fresh rather than robotic.

**Independent Test**: Run the agent 5 times consecutively with the same trip/phase and verify that each message has distinct wording and varies topics/emphasis based on previous messages.

**Acceptance Scenarios**:

1. **Given** the agent has sent 3 previous messages about Livigno with similar snow depth mentions, **When** drafting a new message, **Then** it prioritizes different aspects (e.g., lift status, local events) and uses different phrasing for snow depth if mentioned.
2. **Given** the last 2 messages opened with "Good morning, shredders!", **When** drafting a new message, **Then** it uses a different opening greeting.
3. **Given** previous messages heavily emphasized webcams and visual updates, **When** drafting a new message, **Then** it shifts focus to other aspects like restaurant recommendations or trivia.

---

### User Story 2 - Persistent Message Storage (Priority: P1)

The system persists the last 3-4 sent messages per resort in state.json so message history is maintained across agent runs.

**Why this priority**: Essential for the variation system to work in a stateless serverless environment. Without persistence, the agent would forget previous messages between runs.

**Independent Test**: Send 2 messages, restart the agent (reload state), send another message, and verify the agent references all 3 messages in its context.

**Acceptance Scenarios**:

1. **Given** the agent has sent 4 messages over 4 days, **When** the agent runs on day 5, **Then** it loads the last 3-4 messages from state.json into the LLM prompt.
2. **Given** state.json is empty for a new resort, **When** the agent runs for the first time, **Then** it proceeds normally without message history and stores the first message.

---

### User Story 3 - LLM-Driven Variation Guidance (Priority: P2)

The LLM receives explicit instructions to analyze recent messages and avoid repetition in structure, topics, and wording.

**Why this priority**: Leverages the LLM's natural language understanding to create genuinely varied content rather than just rotating templates.

**Independent Test**: Provide identical weather data and insights to the LLM with different message histories and verify it produces distinctly different messages based on those histories.

**Acceptance Scenarios**:

1. **Given** recent messages all started with weather data, **When** drafting a new message, **Then** it opens with a local insight or event instead.
2. **Given** recent messages used informal language ("crushing powder"), **When** drafting a new message, **Then** it balances with more data-focused language.

---

### Edge Cases

- What happens when there are fewer than 3 previous messages (e.g., first run, new resort)?
  - System gracefully handles null/empty history and proceeds without variation guidance
- How does the system handle message history when switching between morning and evening modes?
  - Stores all messages regardless of mode; LLM context notes the mode for each historical message
- What if state.json becomes corrupted or very large?
  - Implement MAX_STORED_MESSAGES limit (4 per resort) and validation on load

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST track and store the last 3-4 complete messages sent for each resort
- **FR-002**: System MUST include stored messages in the LLM prompt during draft generation with clear labeling (timestamp, phase, mode)
- **FR-003**: System MUST provide explicit variation instructions to the LLM referencing the message history
- **FR-004**: System MUST persist message history to state.json after each successful message send
- **FR-005**: System MUST handle cases where no message history exists (first run, new resort) gracefully
- **FR-006**: System MUST limit stored messages to a maximum of 4 per resort to prevent state bloat
- **FR-007**: System MUST trim oldest messages when the limit is exceeded (FIFO - First In First Out)
- **FR-008**: System MUST NOT send messages to messaging platforms if in dry-run mode but MUST still extract the message text for storage

### Key Entities

- **MessageHistory**: A stored message record containing the message text, timestamp, phase, and mode (morning/evening)
- **ResortState**: Extended to include a `recent_messages` list containing MessageHistory entries

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of messages after the first 3 include message history context in the LLM prompt
- **SC-002**: Manual review of 5 consecutive messages shows distinct variation in opening style, topic emphasis, and phrasing
- **SC-003**: State.json correctly persists and retrieves message history across agent runs
- **SC-004**: 0% of consecutive messages repeat the same opening greeting or sentence structure
