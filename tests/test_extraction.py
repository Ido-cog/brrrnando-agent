import pytest
from src.extraction import extract_trivia, extract_challenge

def test_extract_trivia():
    message = """
    Great conditions today! ❄️
    
    --- 💡 SKI NERD TRIVIA ---
    Val Thorens is the highest ski resort in Europe at 2,300m! 🏔️
    
    Have fun!
    """
    
    trivia = extract_trivia(message)
    assert trivia is not None
    assert "Val Thorens" in trivia
    assert "highest" in trivia

def test_extract_challenge():
    message = """
    Morning update! ⛷️
    
    --- 🏆 BRRRNANDO'S DAILY CHALLENGE ---
    Find the hidden bar at 2500m and take a selfie! 🍻
    
    Enjoy!
    """
    
    challenge = extract_challenge(message)
    assert challenge is not None
    assert "hidden bar" in challenge
    assert "2500m" in challenge

def test_no_trivia():
    message = "Just a regular message with no trivia section"
    assert extract_trivia(message) is None

def test_no_challenge():
    message = "Just a regular message with no challenge section"
    assert extract_challenge(message) is None
