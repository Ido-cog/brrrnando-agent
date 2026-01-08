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
            "last_run": None
        }
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
