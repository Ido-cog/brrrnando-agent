
import sys
import os
import random
# Ensure src module can be found
sys.path.append(os.getcwd())

from src.integrations.llm import generate_draft

def test_natural_messaging():
    print("Running Manual Variation Test (Natural Messaging)...")
    
    # Mock Data
    trip_name = "Test Resort"
    phase_name = "active"
    
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
        seen_trivia, seen_challenges, recent_messages, ski_days_left=5, return_prompt=True
    )
    
    if "Future Outlook (>48h): 25.0cm" in prompt_mid:
        print("[SUCCESS] Future snow included.")
    else:
        print("[FAILURE] Future snow missing but should be there.")
        
    if "CURRENT PERSONA:" in prompt_mid:
        print(f"[SUCCESS] Persona injected: {prompt_mid.split('CURRENT PERSONA:')[1].splitlines()[0]}")
    else:
        print("[FAILURE] Persona missing.")

    # Scenario B: End-trip (2 days left) -> Should HIDE future snow
    # Note: In main.py, the key is deleted BEFORE calling generate_draft. 
    # Here we mock that deletions by removing the key from input.
    weather_data_end = weather_data_mid.copy()
    del weather_data_end["snow_future_forecast_cm"]
    
    print("\n--- TEST CASE 2: End-Trip (2 days left) ---")
    print("Expected: Future Outlook line is GONE.")
    
    prompt_end = generate_draft(
        trip_name, phase_name, weather_data_end, insights, 
        seen_trivia, seen_challenges, recent_messages, ski_days_left=2, return_prompt=True
    )
    
    if "Future Outlook" in prompt_end:
        print("[FAILURE] Future Outlook line is present (should be hidden).")
        print(prompt_end) # Debug
    else:
        print("[SUCCESS] Future Outlook line is hidden.")
        
    if "IGNORE any long-range" in prompt_end:
        print("[SUCCESS] Found critical instruction to ignore long-range.")
    else:
         print("[FAILURE] Critical instruction missing.")

if __name__ == "__main__":
    test_natural_messaging()
