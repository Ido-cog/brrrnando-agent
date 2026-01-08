import time
import re
from typing import List, Dict, Tuple, Any
import google.generativeai as genai
from google.api_core import exceptions
import os
from dotenv import load_dotenv

load_dotenv()

def _get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

def _call_with_retry(model_method, *args, **kwargs):
    """
    Helper to call Gemini with a single retry if rate limited (429) 
    and the delay is <= 2 minutes.
    """
    try:
        return model_method(*args, **kwargs)
    except exceptions.ResourceExhausted as e:
        message = str(e)
        # Extract delay from "Please retry in 53.527820394s." or similar
        match = re.search(r"retry in (\d+\.?\d*)s", message)
        
        delay = 65 # Default to slightly over 1 minute if not found
        if match:
            delay = float(match.group(1))
        
        if delay <= 120:
            print(f"Rate limited (429). Waiting {delay:.1f} seconds to retry...")
            time.sleep(delay + 2) # Buffer
            try:
                return model_method(*args, **kwargs)
            except Exception as e2:
                # If it fails again, we return the error string as before to 'proceed'
                return type('obj', (object,), {'text': f"Error after retry: {str(e2)}"})
        else:
            print(f"Rate limit delay too long ({delay:.1f}s). Proceeding without retry.")
            return type('obj', (object,), {'text': f"Rate limit exceeded (delay {delay:.1f}s)."})
    except Exception as e:
        return type('obj', (object,), {'text': f"Error: {str(e)}"})

def generate_draft(trip_name: str, phase_name: str, weather_data: Dict, insights: List[Any], 
                   seen_trivia: List[str] = None, seen_challenges: List[str] = None) -> str:
    """
    Drafts a high-energy WhatsApp message based on context.
    """
    model = _get_model()
    
    insights_str = "\n".join([f"- {i.title}: {i.content} ({i.url})" for i in insights])
    
    seen_trivia_str = ""
    if seen_trivia and len(seen_trivia) > 0:
        seen_trivia_str = "\n\nPREVIOUSLY SHARED TRIVIA (DO NOT REPEAT):\n" + "\n".join([f"- {t}" for t in seen_trivia[-10:]])
    
    seen_challenges_str = ""
    if seen_challenges and len(seen_challenges) > 0:
        seen_challenges_str = "\n\nPREVIOUSLY SHARED CHALLENGES (DO NOT REPEAT):\n" + "\n".join([f"- {c}" for c in seen_challenges[-10:]])
    
    prompt = f"""
    You are Brrrnando, a hyper-enthusiastic ski trip assistant.
    Your job is to draft a WhatsApp message for the group '{trip_name}'.
    
    CURRENT PHASE: {phase_name}
    WEATHER DATA: {weather_data}
    LOCAL INSIGHTS:
    {insights_str}
    {seen_trivia_str}
    {seen_challenges_str}
    
    If CURRENT PHASE is 'active', you MUST include a special engagement section at the end:
    EITHER '--- 🏆 BRRRNANDO'S DAILY CHALLENGE ---' (a fun, safe physical or social task)
    OR '--- 💡 SKI NERD TRIVIA ---' (an interesting fact about the resort geography, history, or quirks).
    Use the LOCAL INSIGHTS and your own training data about {trip_name} to make it hyper-specific.
    IMPORTANT: Do NOT repeat any trivia or challenges from the "PREVIOUSLY SHARED" lists above.
    
    GUIDELINES:
    1. Be creative and hyper-enthusiastic. Use emojis (⛷️, ❄️, 🍻).
    2. Context is key: If we're there, focus on lifts and après-ski. If we're weeks out, focus on hype and long-range trends.
    3. Be specific! Mention the resort name and the insights found.
    4. Format for WhatsApp (bolding, short paragraphs).
    5. DO NOT use placeholders like [Resort Name] or "could not find info".
    6. Ensure challenges are fun and safe.
    """
    
    response = _call_with_retry(model.generate_content, prompt)
    return response.text

def review_draft(draft: str, trip_name: str, phase_name: str) -> Tuple[bool, str]:
    """
    Reviews the draft for quality, clarity, and presence of placeholders.
    Returns (is_approved, finalized_content_or_feedback).
    """
    model = _get_model()
    
    prompt = f"""
    Review the following WhatsApp message draft for the trip '{trip_name}' in phase '{phase_name}'.
    
    DRAFT:
    ---
    {draft}
    ---
    
    TASKS:
    1. Ensure there are NO placeholders (e.g., [Resort], ???).
    2. Ensure the message doesn't say "could not get info" or similar dismissive phrases.
    3. Ensure the tone is high-energy and appropriate for the phase.
    
    If it's good, respond with 'APPROVED' followed by the EXACT message on the next line.
    If it needs fixes, respond with 'REVISE' followed by specific instructions for the drafter.
    """
    
    response = _call_with_retry(model.generate_content, prompt)
    result = response.text.strip()
    
    if result.startswith("APPROVED"):
        # Extract the message part
        lines = result.split("\n")
        if len(lines) > 1:
            return True, "\n".join(lines[1:]).strip()
        return True, draft # Fallback to original draft if no separate line
    
    return False, result

def generate_summary(prompt: str) -> str:
    """
    Legacy summary function.
    """
    model = _get_model()
    response = _call_with_retry(model.generate_content, prompt)
    return response.text
