# Clarification Log: Natural Messaging

## Key Decisions

### 1. Handling Future Snowfall for Ending Trips
- **Initial Idea**: Show future snow (>48h) as "FOMO" or "Next Time" context.
- **User Feedback**: "If I'm leaving in two days, I don't need to know what happens next week it's not relevant."
- **Final Decision**: **Hide it completely.**
  - If `ski_days_left <= 2`, any snowfall forecast for `> 48h` out acts as noise.
  - The system must filter this data out *before* or *during* prompt construction so the LLM doesn't mention it.

### 2. "Natural" Messaging
- **Requirement**: No rigid headers like "--- TRIVIA ---". structure must be organic.
- **Implementation**: Ban specific header phrases in the prompt and instruct the LLM to weave content in naturally.
