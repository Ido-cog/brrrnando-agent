
import sys
import os
import random
from datetime import date
# Ensure src module can be found
sys.path.append(os.getcwd())

from src.integrations.llm import generate_draft

def test_natural_messaging():
    print("Running Manual Variation Test (Natural Messaging)...")
    
    # Mock Data
    trip_name = "Test Resort"
    phase_name = "active"
    current_date = date(2026, 1, 24)
    
    # Scenario A: Mid-trip (Plenty of time) -> Should show future snow
    weather_data_mid = {
        "base_snow_depth": 50,
        "summit_snow_depth": 150,
        "temp_summit": -5,
        "forecast_confidence": "High",
        "snow_48h_forecast_cm": 10.0,
        "snow_future_forecast_cm": 25.0
    }
    insights = []
    seen_trivia = []
    seen_challenges = []
    recent_messages = []
    
    print("\n--- TEST CASE 1: Mid-Trip (5 days left) ---")
    print("Expected: Shows Future Outlook.")
    prompt_mid = generate_draft(
        trip_name, phase_name, weather_data_mid, insights, 
        seen_trivia, seen_challenges, recent_messages, ski_days_left=5, 
        current_date=current_date, return_prompt=True
    )
    
    if "Future Outlook (>48h): 25.0cm" in prompt_mid:
        print("[SUCCESS] Future snow included.")
    else:
        print("[FAILURE] Future snow missing but should be there.")
        
    if "TODAY'S DATE: January 24, 2026" in prompt_mid:
        print("[SUCCESS] Date correctly injected.")
    else:
        print("[FAILURE] Date missing from prompt.")

    # Scenario B: End-Trip (2 days left) -> Should SHOW future snow but instructing context
    # Note: main.py NO LONGER deletes the key. So we pass full data.
    weather_data_end = weather_data_mid.copy()
    
    print("\n--- TEST CASE 2: End-Trip (2 days left) ---")
    print("Expected: Future Outlook present, but specific instructions to frame it as 'next year'.")
    
    prompt_end = generate_draft(
        trip_name, phase_name, weather_data_end, insights, 
        seen_trivia, seen_challenges, recent_messages, ski_days_left=2,
        current_date=current_date, return_prompt=True
    )
    
    if "Future Outlook" in prompt_end:
        print("[SUCCESS] Future Outlook line is present (Bot has awareness).")
    else:
        print("[FAILURE] Future Outlook line is hidden (Bot is blind).")
        
    if "reason to come back" in prompt_end:
        print("[SUCCESS] Found instruction to frame future snow as 'reason to come back'.")
    else:
         print("[FAILURE] Contextual instruction missing.")

if __name__ == "__main__":
    test_natural_messaging()
