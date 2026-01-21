# Specification: Group Engagement (Trivia & Challenges)

## Goal
Transform Brrrnando into a "Game Master" during the `ACTIVE` skiing phase. The agent will provide resort-specific trivia and daily challenges to encourage interaction and fun within the group.

## User Stories
- **Daily Challenge (P1)**: As a skier on the trip, I want to receive a fun daily challenge (e.g., finding a specific bar or lift) to make the day more interesting.
- **Resort Trivia (P2)**: As a group member, I want to learn interesting facts about the resort we are skiing in.
- **Competitive Spirit (P3)**: As a competitive skier, I want challenges that can be "won" to brag to my friends.

## Functional Requirements
1. **Contextual Generation**: Trivia and challenges are relevant to the resort and generated during the `ACTIVE` phase.
2. **LLM Integration**: Gemini generates one "Engagement Section" per day, alternating between '--- 🏆 BRRRNANDO'S DAILY CHALLENGE ---' and '--- 💡 SKI NERD TRIVIA ---'.
3. **Extraction & Persistence**: System uses regex markers (`extract_trivia`, `extract_challenge`) to pull the generated content from the finalized message and save it to `state.json`.
4. **Deduplication**: LLM is provided with the last 10 seen trivia/challenges to avoid repetition.

## Acceptance Criteria
- [x] Morning briefing during `ACTIVE` phase includes a specialized engagement section.
- [x] Content is specific to the resort.
- [x] Extraction logic correctly identifies and saves trivia/challenges.
- [x] Persistence layer prevents repetition within a 50-item window.

## Success Metrics
- Increase in group chatter/replies to the agent's messages (manual observation).
- Positive feedback from the group on the "fun" factor.
