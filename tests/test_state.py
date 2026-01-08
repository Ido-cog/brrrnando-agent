import os
import json
import pytest
from src.state import load_state, save_state, get_resort_state, is_url_seen, mark_url_seen

@pytest.fixture
def temp_state_file(tmp_path):
    # Change dynamic path for testing
    import src.state
    original_file = src.state.STATE_FILE
    new_file = str(tmp_path / "test_state.json")
    src.state.STATE_FILE = new_file
    yield new_file
    src.state.STATE_FILE = original_file

def test_load_save_state(temp_state_file):
    state = load_state()
    assert state == {}
    
    state["test"] = {"seen_urls": ["url1"]}
    save_state(state)
    
    loaded = load_state()
    assert loaded["test"]["seen_urls"] == ["url1"]

def test_resort_state_initialization():
    state = {}
    resort_state = get_resort_state(state, "Val Thorens")
    assert "val_thorens" in state
    assert resort_state["seen_urls"] == []

def test_mark_url_seen():
    resort_state = {"seen_urls": []}
    mark_url_seen(resort_state, "url1")
    assert is_url_seen(resort_state, "url1")
    
    # Check deduplication
    mark_url_seen(resort_state, "url1")
    assert len(resort_state["seen_urls"]) == 1

def test_trimming():
    resort_state = {"seen_urls": [f"url{i}" for i in range(50)]}
    mark_url_seen(resort_state, "new_url")
    assert len(resort_state["seen_urls"]) == 50
    assert "url0" not in resort_state["seen_urls"]
    assert "new_url" in resort_state["seen_urls"]
