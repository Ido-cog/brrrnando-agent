# Specification: Persistent Memory (Git-Commit Strategy)

## Goal
The agent should remember previously shared insights (URLs) to avoid repetition in successive runs. This state will be persisted across ephemeral GitHub Action runs by committing it back to the repository.

## User Stories
- **Anti-Repetition (P1)**: As a user, I want the agent to only share *new* content so the group doesn't get bored.
- **Run Tracking (P2)**: As a maintainer, I want to see when the last successful report was generated for each trip.

## Functional Requirements
1. **State Storage**: Store state in a `state.json` file.
2. **Deduplication**: `DiscoveryEngine` must filter out any URLs already present in the "seen" list for a specific resort.
3. **State Updates**: After a successful message is drafted (or sent), the URLs of the insights used must be added to the resort's "seen" list.
4. **Pruning**: To prevent the file from growing indefinitely, the "seen" list should only keep the last 50 entries per resort.
5. **Manual Run Safety**: If the agent is triggered manually (debug/test), the state should NOT be updated.

## Key Entities
### State Object
```json
{
  "val_thorens": {
    "seen_urls": ["url1", "url2"],
    "last_run": "2026-01-09T00:13:38"
  }
}
```

## Acceptance Criteria
- [ ] `state.json` is created automatically if it doesn't exist.
- [ ] `DiscoveryEngine` returns 0 "seen" insights when filtering.
- [ ] `main.py` successfully saves the updated state at the end of a run.
- [ ] A clear instruction is provided for the GitHub Action to commit this file back to `main`.
