import time
import re
import random
from typing import List, Dict, Tuple, Any, Optional
from datetime import date
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
                   seen_trivia: List[str] = None, seen_challenges: List[str] = None,
                   recent_messages: List[Dict] = None, ski_days_left: int = None, 
                   current_date: date = None, return_prompt: bool = False) -> str:
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
    
    # Format recent messages history for variation guidance
    recent_messages_str = ""
    if recent_messages and len(recent_messages) > 0:
        recent_messages_str = "\n\nRECENT MESSAGES HISTORY (FOR VARIATION REFERENCE):" 
        recent_messages_str += "\nYou MUST vary your new message from these recent ones. Use different:" 
        recent_messages_str += "\n- Opening greetings and sentence structures" 
        recent_messages_str += "\n- Topic emphasis (weather vs. local events vs. webcams vs. restaurants)" 
        recent_messages_str += "\n- Tone and energy levels" 
        recent_messages_str += "\n- Phrasing for similar data points\n"
        for i, msg in enumerate(recent_messages[-4:], 1):
            timestamp = msg.get('timestamp', 'unknown')
            phase = msg.get('phase', 'unknown')
            mode = msg.get('mode', 'unknown')
            message = msg.get('message', '')[:400]  # Limit to first 400 chars to save tokens
            recent_messages_str += f"\n--- MESSAGE {i} ({timestamp[:10]}, {phase}, {mode}) ---\n{message}\n"
    
    relevance_instruction = ""
    if ski_days_left is not None:
        if ski_days_left <= 2:
            relevance_instruction = f"CRITICAL: There are only {ski_days_left} days left. \n1. Focus heavily on immediate conditions (Next 48h).\n2. Frame 'Future Outlook' snow ONLY as a reason to come back next year, NOT as something they will ski this trip.\n3. Mention travel logistics/safe journey home if relevant."
        else:
            relevance_instruction = f"Trip Status: {ski_days_left} days of skiing remain."

    date_context = ""
    if current_date:
        date_context = f"TODAY'S DATE: {current_date.strftime('%B %d, %Y')}\n(Do NOT recommend events that happened before today!)"

    # Select a random persona for variation
    personas = [
        "The Hype Man (High energy, lots of emojis, focus on excitement)",
        "The Local Guide (Knowledgeable, authoritative, focus on specific spots)",
        "The Powder Hound (Focused purely on snow quality and conditions)",
        "The Chill Friend (Relaxed, conversational, less formatting)",
    ]
    persona = random.choice(personas)

    # Format weather specifically
    weather_lines = []
    weather_lines.append(f"- Snow Depth (Base): {weather_data.get('base_snow_depth', 'N/A')}cm")
    weather_lines.append(f"- Snow Depth (Summit): {weather_data.get('summit_snow_depth', 'N/A')}cm")
    
    if "snow_48h_forecast_cm" in weather_data:
         weather_lines.append(f"- Incoming Fresh Snow (Next 48h): {weather_data['snow_48h_forecast_cm']}cm")
         
    if "snow_future_forecast_cm" in weather_data:
         weather_lines.append(f"- Future Outlook (>48h): {weather_data['snow_future_forecast_cm']}cm")
         
    weather_lines.append(f"- Summit Temp: {weather_data.get('temp_summit', 'N/A')}")
    weather_lines.append(f"- Forecast Confidence: {weather_data.get('forecast_confidence', 'N/A')}")
    
    weather_display = "\n    ".join(weather_lines)

    prompt = f"""
    You are Brrrnando.
    CURRENT PERSONA: {persona} (Adopt this style heavily!)
    
    Your job is to draft a WhatsApp message for the group '{trip_name}'.
    
    CURRENT PHASE: {phase_name}
    {date_context}
    {relevance_instruction}
    
    WEATHER DATA:
    {weather_display}
    
    LOCAL INSIGHTS:
    {insights_str}
    {seen_trivia_str}
    {seen_challenges_str}
    {recent_messages_str}
    
    GUIDELINES:
    1. Tone: Match the CURRENT PERSONA. Be distinct from previous messages.
    2. Data Density: Use the 'Incoming Fresh Snow' data to hype immediate skiing.
    3. ANTI-REPETITION: CHECK 'RECENT MESSAGES'. Do not repeat static stats if they haven't changed.
    4. Venue & Insights: Mention one specific spot from insights naturally.
    5. Anti-Filler: Every sentence must add value.
    6. STRICTLY BANNED PHRASES: Do NOT use "--- 🏆 BRRRNANDO'S DAILY CHALLENGE ---", "--- 💡 SKI NERD TRIVIA ---", "Legends", "Magic", "Wooohooo", "CHOO CHOO".
    7. Structure:
       - Be organic. NO rigid headers.
       - If you include trivia/challenges, weave them into the flow conversationally (e.g. "By the way, did you guys know...").
    8. Link Formatting: [descriptive text](URL).
    9. Source Attribution: Mention weather sources naturally.
    """
    
    if return_prompt:
        return prompt

    response = _call_with_retry(model.generate_content, prompt)
    return response.text

def review_draft(draft: str, trip_name: str, phase_name: str, recent_messages: List[Dict] = None) -> Tuple[bool, str]:
    """
    Reviews the draft for quality, clarity, and presence of placeholders.
    Returns (is_approved, finalized_content_or_feedback).
    """
    model = _get_model()
    
    # Add recent messages context if available
    recent_context = ""
    if recent_messages and len(recent_messages) > 0:
        recent_context = "\n\nRECENT MESSAGES (check for excessive similarity):\n"
        for msg in recent_messages[-2:]:  # Only show last 2 for review
            message_preview = msg.get('message', '')[:200]
            recent_context += f"- {message_preview}...\n"
    
    prompt = f"""
    Review the following WhatsApp message draft for the trip '{trip_name}' in phase '{phase_name}'.
    
    DRAFT:
    ---
    {draft}
    ---{recent_context}
    
    TASKS:
    1. Ensure there are NO placeholders (e.g., [Resort], ???).
    2. Ensure the message doesn't say "could not get info" or similar dismissive phrases.
    3. Ensure the tone is high-energy and appropriate for the phase.
    4. If recent messages are provided, check that this draft has sufficient variation in opening, structure, and emphasis.
    
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

def evaluate_discovery(trip_name: str, insights: List[Any]) -> List[str]:
    """
    Evaluates the current insights and returns a list of specific follow-up queries
    if more information is needed (e.g., webcams, specific menus).
    """
    model = _get_model()
    insights_summary = "\n".join([f"- {i.title}: {i.content[:200]}" for i in insights])
    
    prompt = f"""
    You are Brrrnando's Discovery Brain. Analyze the current findings for the ski resort '{trip_name}'.
    
    CURRENT INSIGHTS:
    {insights_summary}
    
    TASK:
    Determine if we have enough "flavor" for a feature-packed report. We ideally want:
    1. At least one webcam link or recent visual update.
    2. Specific restaurant or après-ski venue details.
    3. Distinct local news or events (like Olympic updates).
    
    If we are missing these, provide 2-3 hyper-specific search queries to find them.
    If we have enough, respond with 'ENOUGH'.
    
    Format your response as a JSON list of strings if you need more, or just the word 'ENOUGH'.
    Example: ["Livigno Bivio Club menu", "Livigno mottolino webcam live"]
    """
    
    response = _call_with_retry(model.generate_content, prompt)
    text = response.text.strip()
    
    if "ENOUGH" in text.upper():
        return []
    
    # Try to extract JSON list
    try:
        import json
        match = re.search(r"(\[.*\])", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except:
        pass
    
    return []

def generate_summary(prompt: str) -> str:
    """
    Legacy summary function.
    """
    model = _get_model()
    response = _call_with_retry(model.generate_content, prompt)
    return response.text
