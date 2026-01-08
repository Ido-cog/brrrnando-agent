import json
import os
from datetime import datetime
from typing import Dict, List, Set

STATE_FILE = "state.json"
MAX_SEEN_URLS = 50

def load_state() -> Dict:
    """Load state from state.json, return empty dict if not found."""
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading state: {e}")
        return {}

def save_state(state: Dict):
    """Save state to state.json."""
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        print(f"Error saving state: {e}")

def get_resort_state(state: Dict, resort_name: str) -> Dict:
    """Get state for a specific resort, initialized if missing."""
    key = resort_name.lower().replace(" ", "_")
    if key not in state:
        state[key] = {
            "seen_urls": [],
            "seen_trivia": [],
            "seen_challenges": [],
            "last_run": None
        }
    # Ensure all keys exist for backwards compatibility
    if "seen_trivia" not in state[key]:
        state[key]["seen_trivia"] = []
    if "seen_challenges" not in state[key]:
        state[key]["seen_challenges"] = []
    return state[key]

def is_url_seen(resort_state: Dict, url: str) -> bool:
    """Check if a URL has been seen before for this resort."""
    return url in resort_state.get("seen_urls", [])

def mark_url_seen(resort_state: Dict, url: str):
    """Mark a URL as seen and trim the list if it exceeds MAX_SEEN_URLS."""
    seen = resort_state.get("seen_urls", [])
    if url not in seen:
        seen.append(url)
        # Keep only the last MAX_SEEN_URLS
        resort_state["seen_urls"] = seen[-MAX_SEEN_URLS:]

def update_last_run(resort_state: Dict):
    """Update the last run timestamp to now."""
    resort_state["last_run"] = datetime.now().isoformat()

def mark_trivia_seen(resort_state: Dict, trivia_text: str):
    """Mark a trivia fact as seen and trim the list if needed."""
    seen = resort_state.get("seen_trivia", [])
    if trivia_text and trivia_text not in seen:
        seen.append(trivia_text)
        resort_state["seen_trivia"] = seen[-MAX_SEEN_URLS:]

def mark_challenge_seen(resort_state: Dict, challenge_text: str):
    """Mark a challenge as seen and trim the list if needed."""
    seen = resort_state.get("seen_challenges", [])
    if challenge_text and challenge_text not in seen:
        seen.append(challenge_text)
        resort_state["seen_challenges"] = seen[-MAX_SEEN_URLS:]

def get_seen_trivia(resort_state: Dict) -> List[str]:
    """Get list of previously seen trivia."""
    return resort_state.get("seen_trivia", [])

def get_seen_challenges(resort_state: Dict) -> List[str]:
    """Get list of previously seen challenges."""
    return resort_state.get("seen_challenges", [])
