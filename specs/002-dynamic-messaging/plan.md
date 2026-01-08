# Implementation Plan: Dynamic Context-Aware Messaging

**Branch**: `002-dynamic-messaging` | **Date**: 2026-01-08 | **Spec**: [spec.md](file:///Users/ifarhi/Library/CloudStorage/OneDrive-COGNYTE/Documents/vs_code_projects/brrrnardo/specs/002-dynamic-messaging/spec.md)
**Input**: Feature specification from `/specs/002-dynamic-messaging/spec.md`

## Summary

Enhance the Brrrnando agent to draft smarter, context-aware messages by integrating a discovery engine (web search/crawling) and a quality review loop. The agent will adapt its content based on the trip's current phase (e.g., Weekly Hype vs. Active Skiing).

## Technical Context

- **Language**: Python 3.11+
- **Primary Dependencies**: `google-generativeai`, `duckduckgo-search`
- **Testing**: `pytest`

## Proposed Changes

### Core Logic
- **[MODIFY] [logic.py](file:///Users/ifarhi/Library/CloudStorage/OneDrive-COGNYTE/Documents/vs_code_projects/brrrnardo/src/logic.py)**: Refine `Phase` logic and add search intent mapping.
- **[NEW] [discovery.py](file:///Users/ifarhi/Library/CloudStorage/OneDrive-COGNYTE/Documents/vs_code_projects/brrrnardo/src/discovery.py)**: Implement `DiscoveryEngine` to fetch resort-specific news, events, and logistics.

### LLM Integration
- **[MODIFY] [llm.py](file:///Users/ifarhi/Library/CloudStorage/OneDrive-COGNYTE/Documents/vs_code_projects/brrrnardo/src/integrations/llm.py)**: Add `review_draft` and enhance `generate_summary` prompts.

### Main Workflow
- **[MODIFY] [main.py](file:///Users/ifarhi/Library/CloudStorage/OneDrive-COGNYTE/Documents/vs_code_projects/brrrnardo/src/main.py)**: Integrate discovery and review loop into the main execution.

## Verification Plan

### Automated Tests
- Run `pytest tests/test_logic.py` to ensure phase determination still works.
- Create `tests/test_discovery.py` to test search query generation.
- Create `tests/test_reviewer.py` to verify the review logic with mock drafts.

### Manual Verification
- Run `python -m src.main --dry-run` and inspect the generated message.
