from typing import List, Dict, Tuple, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def _get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def generate_draft(trip_name: str, phase_name: str, weather_data: Dict, insights: List[Any]) -> str:
    """
    Drafts a high-energy WhatsApp message based on context.
    """
    model = _get_model()
    
    insights_str = "\n".join([f"- {i.title}: {i.content} ({i.url})" for i in insights])
    
    prompt = f"""
    You are Brrrnando, a hyper-enthusiastic ski trip assistant.
    Your job is to draft a WhatsApp message for the group '{trip_name}'.
    
    CURRENT PHASE: {phase_name}
    WEATHER DATA: {weather_data}
    LOCAL INSIGHTS:
    {insights_str}
    
    GUIDELINES:
    1. Be creative and hyper-enthusiastic. Use emojis (⛷️, ❄️, 🍻).
    2. Context is key: If we're there, focus on lifts and après-ski. If we're weeks out, focus on hype and long-range trends.
    3. Be specific! Mention the resort name and the insights found.
    4. Format for WhatsApp (bolding, short paragraphs).
    5. DO NOT use placeholders like [Resort Name] or "could not find info".
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error drafting message: {str(e)}"

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
    
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        if result.startswith("APPROVED"):
            # Extract the message part
            lines = result.split("\n")
            if len(lines) > 1:
                return True, "\n".join(lines[1:]).strip()
            return True, draft # Fallback to original draft if no separate line
        
        return False, result
    except Exception as e:
        return False, f"Error reviewing draft: {str(e)}"

# Keeping the old function for backward compatibility if needed, but pointing to generate_draft logic
def generate_summary(prompt: str) -> str:
    """
    Legacy summary function.
    """
    try:
        model = _get_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
