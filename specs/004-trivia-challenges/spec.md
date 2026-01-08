# Specification: Group Engagement (Trivia & Challenges)

## Goal
Transform Brrrnando into a "Game Master" during the `ACTIVE` skiing phase. The agent will provide resort-specific trivia and daily challenges to encourage interaction and fun within the group.

## User Stories
- **Daily Challenge (P1)**: As a skier on the trip, I want to receive a fun daily challenge (e.g., finding a specific bar or lift) to make the day more interesting.
- **Resort Trivia (P2)**: As a group member, I want to learn interesting facts about the resort we are skiing in.
- **Competitive Spirit (P3)**: As a competitive skier, I want challenges that can be "won" to brag to my friends.

## Functional Requirements
1. **Contextual Generation**: Trivia and challenges must be relevant to the specific resort and the current phase (`ACTIVE`).
2. **LLM Integration**: Use Gemini to generate creative trivia/challenges based on resort knowledge or discovered insights.
3. **Daily Frequency**: One challenge or trivia nugget per day, integrated into the morning briefing during the `ACTIVE` phase.
4. **Variety**: The agent should alternate between types of engagement (Trivia vs. Challenge) to keep it fresh.

## Acceptance Criteria
- [ ] The morning briefing during `ACTIVE` phase includes a "Brrrnando's Daily Challenge" or "Ski Nerd Trivia" section.
- [ ] Content is specific to the resort (e.g., mentions the "Caron" lift in Val Thorens).
- [ ] Tone remains hyper-enthusiastic and encouraging.
- [ ] Does not disrupt the essential weather/logistics info.

## Success Metrics
- Increase in group chatter/replies to the agent's messages (manual observation).
- Positive feedback from the group on the "fun" factor.
