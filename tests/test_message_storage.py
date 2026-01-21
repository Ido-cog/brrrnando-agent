import pytest
from src.state import (
    get_resort_state, 
    get_recent_messages, 
    store_message,
    MAX_STORED_MESSAGES
)


def test_empty_message_history():
    """Test getting messages when history is empty."""
    state = {}
    resort_state = get_resort_state(state, "Test Resort")
    messages = get_recent_messages(resort_state)
    
    assert messages == []


def test_store_first_message():
    """Test storing the first message."""
    state = {}
    resort_state = get_resort_state(state, "Test Resort")
    
    store_message(resort_state, "Hello world!", "active", "morning")
    messages = get_recent_messages(resort_state)
    
    assert len(messages) == 1
    assert messages[0]["message"] == "Hello world!"
    assert messages[0]["phase"] == "active"
    assert messages[0]["mode"] == "morning"
    assert "timestamp" in messages[0]


def test_store_multiple_messages():
    """Test storing multiple messages."""
    state = {}
    resort_state = get_resort_state(state, "Test Resort")
    
    for i in range(3):
        store_message(resort_state, f"Message {i}", "active", "morning")
    
    messages = get_recent_messages(resort_state)
    assert len(messages) == 3
    assert messages[2]["message"] == "Message 2"
    assert messages[0]["message"] == "Message 0"


def test_fifo_trimming_at_limit():
    """Test that messages are trimmed when exceeding MAX_STORED_MESSAGES."""
    state = {}
    resort_state = get_resort_state(state, "Test Resort")
    
    # Store MAX_STORED_MESSAGES + 1 messages
    for i in range(MAX_STORED_MESSAGES + 1):
        store_message(resort_state, f"Message {i}", "active", "morning")
    
    messages = get_recent_messages(resort_state)
    
    # Should only have MAX_STORED_MESSAGES messages
    assert len(messages) == MAX_STORED_MESSAGES
    
    # First message should be removed (Message 0)
    # Last message should be Message 4 (if MAX is 4)
    assert messages[0]["message"] == "Message 1"
    assert messages[-1]["message"] == f"Message {MAX_STORED_MESSAGES}"


def test_backward_compatibility():
    """Test that old state without recent_messages still works."""
    # Simulate old state format
    state = {
        "test_resort": {
            "seen_urls": ["http://example.com"],
            "seen_trivia": ["Some trivia"],
            "seen_challenges": ["Some challenge"],
            "last_run": "2026-01-20T10:00:00"
        }
    }
    
    resort_state = get_resort_state(state, "Test Resort")
    
    # Should have recent_messages initialized
    assert "recent_messages" in resort_state
    assert resort_state["recent_messages"] == []
    
    # Should still have old data
    assert resort_state["seen_urls"] == ["http://example.com"]


def test_message_metadata_format():
    """Test that message metadata is properly formatted."""
    state = {}
    resort_state = get_resort_state(state, "Livigno")
    
    store_message(resort_state, "Test message", "hype_daily", "evening")
    messages = get_recent_messages(resort_state)
    
    msg = messages[0]
    assert "message" in msg
    assert "timestamp" in msg
    assert "phase" in msg
    assert "mode" in msg
    
    # Timestamp should be in ISO format
    assert "T" in msg["timestamp"]
    assert msg["phase"] == "hype_daily"
    assert msg["mode"] == "evening"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
