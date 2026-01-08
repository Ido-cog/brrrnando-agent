import re
from typing import Optional

def extract_trivia(message: str) -> Optional[str]:
    """
    Extract trivia content from a message containing the trivia section.
    Returns the trivia text without the header, or None if not found.
    """
    # Look for the trivia section marker
    trivia_pattern = r'---\s*💡\s*SKI NERD TRIVIA\s*---\s*\n(.+?)(?=\n---|$)'
    match = re.search(trivia_pattern, message, re.DOTALL | re.IGNORECASE)
    
    if match:
        trivia_text = match.group(1).strip()
        # Clean up and return just the core fact (first sentence or two)
        # Remove emojis and extra whitespace
        trivia_text = re.sub(r'[⛷️❄️🍻🏔️🎿]', '', trivia_text).strip()
        # Take first 200 chars to avoid storing too much
        return trivia_text[:200] if trivia_text else None
    
    return None

def extract_challenge(message: str) -> Optional[str]:
    """
    Extract challenge content from a message containing the challenge section.
    Returns the challenge text without the header, or None if not found.
    """
    # Look for the challenge section marker
    challenge_pattern = r'---\s*🏆\s*BRRRNANDO\'?S DAILY CHALLENGE\s*---\s*\n(.+?)(?=\n---|$)'
    match = re.search(challenge_pattern, message, re.DOTALL | re.IGNORECASE)
    
    if match:
        challenge_text = match.group(1).strip()
        # Clean up and return just the core challenge
        challenge_text = re.sub(r'[⛷️❄️🍻🏔️🎿🏆]', '', challenge_text).strip()
        # Take first 200 chars
        return challenge_text[:200] if challenge_text else None
    
    return None
