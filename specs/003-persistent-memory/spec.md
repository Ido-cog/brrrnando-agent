# Specification: Persistent Memory (Git-Commit Strategy)

## Goal
The agent should remember previously shared insights (URLs) to avoid repetition in successive runs. This state will be persisted across ephemeral GitHub Action runs by committing it back to the repository.

## User Stories
- **Anti-Repetition (P1)**: As a user, I want the agent to only share *new* content so the group doesn't get bored.
- **Run Tracking (P2)**: As a maintainer, I want to see when the last successful report was generated for each trip.

## Functional Requirements
1. **State Storage**: Store state in a `state.json` file.
2. **URL Deduplication**: `DiscoveryEngine` must filter out any URLs already present in the "seen" list for a specific resort.
3. **Trivia/Challenge Deduplication**: The LLM should be instructed to avoid repeating trivia facts or challenges that are in the "seen" lists.
4. **State Updates**: After a successful message is drafted (or sent):
   - URLs of insights used must be added to the resort's "seen_urls" list
   - Trivia/challenge content must be extracted and added to "seen_trivia" or "seen_challenges"
5. **Pruning**: To prevent the file from growing indefinitely, each "seen" list should only keep the last 50 entries per resort.
6. **Manual Run Safety**: If the agent is triggered manually (debug/test), the state should NOT be updated.

## Key Entities
### State Object
```json
{
  "val_thorens": {
    "seen_urls": ["url1", "url2"],
    "seen_trivia": ["The Caron cable car is the highest in Europe", "Val Thorens was founded in 1971"],
    "seen_challenges": ["Find the hidden bar at 2500m", "Take a photo at the summit sign"],
    "last_run": "2026-01-09T00:13:38"
  }
}
```

**Note**: `seen_trivia` and `seen_challenges` store the actual text content (or a hash) of previously shared trivia/challenges to prevent exact repetition.

## Acceptance Criteria
- [x] `state.json` is created automatically if it doesn't exist.
- [x] `DiscoveryEngine` filters out "seen" insights.
- [x] LLM prompt includes previously seen trivia/challenges to avoid repetition.
- [x] State is successfully extracted and updated at the end of a trip run.
- [x] `MAX_SEEN_URLS` (50) is enforced to prevent bloat.
